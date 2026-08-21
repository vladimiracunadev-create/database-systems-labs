"""Ejecuta la implementacion de cada motor y compara su salida con el contrato.

Este es el verificador que sostiene la afirmacion central del repositorio:

    EL MISMO PROBLEMA, RESUELTO EN VARIOS MOTORES, DA LA MISMA RESPUESTA
    -- Y ESO LO COMPRUEBA UNA MAQUINA, NO UNA PROMESA DEL TEXTO.

Cada clase declara en `motores.yaml` un caso con su salida esperada. Cada
implementacion de `implementaciones/<motor>/` se ejecuta contra el motor real
y su resultado se normaliza a filas de texto para poder compararse entre
motores que devuelven tipos distintos.

Tres niveles, y el informe distingue siempre cual es cual:

    nucleo      SQLite y DuckDB. Sin servicios, en cualquier maquina y en
                todos los trabajos de CI. Es el sello fuerte.
    servicio    PostgreSQL, MySQL, MongoDB, Redis y Neo4j contra el contenedor
                real, con su propio cliente oficial. Solo con `--con-servicios`
                y el stack levantado.
    declarado   El codigo se muestra y se revisa a mano. La maquina no lo
                ejecuta, y el informe lo dice con esas palabras.

Formato de una implementacion: dos secciones separadas por un marcador.

    -- motor: postgresql
    -- doc: https://www.postgresql.org/docs/current/tutorial-agg.html

    -- === preparacion ===
    CREATE TABLE ...;
    INSERT INTO ...;

    -- === consulta ===
    SELECT ...;

La seccion de consulta debe producir exactamente las filas del contrato, en
orden. En los motores que no devuelven tablas (MongoDB, Redis, Neo4j) la
consulta imprime las filas con las columnas separadas por `|`: la comparacion
entre modelos distintos solo es posible sobre una forma comun.

Uso:
    python scripts/verificar_equivalencia.py
    python scripts/verificar_equivalencia.py --clase 016 --verbose
    python scripts/verificar_equivalencia.py --con-servicios
"""

from __future__ import annotations

import argparse
import re
import shutil
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import motores_lib as ml  # noqa: E402

ROOT = ml.ROOT

MARCADOR = re.compile(r"^\s*(?:--|//|#)\s*=+\s*(preparacion|consulta)\s*=+\s*$", re.IGNORECASE)

# Como se habla con cada motor de la capa `servicio`: su propio cliente oficial,
# dentro del contenedor que levanta `docker-compose.yml`. Nada de drivers
# intermedios, para que lo que se ejecute sea exactamente lo que la clase
# muestra.
SERVICIOS: dict[str, dict] = {
    "postgresql": {
        "servicio": ["postgres"],
        # Cada clase corre en su propio esquema: sin aislamiento, las tablas de
        # una clase impiden borrar las de otra por sus claves foraneas, y el
        # verificador acabaria midiendo la basura que dejo la clase anterior.
        "aislar": ["psql", "-U", "learner", "-d", "learning", "-v", "ON_ERROR_STOP=1", "-q",
                   "-c", "DROP SCHEMA IF EXISTS {ns} CASCADE; CREATE SCHEMA {ns};"],
        # El esquema se fija en la conexion, no con un SET dentro del guion:
        # psql imprimiria «SET» como una fila mas del resultado.
        "entorno": ["PGOPTIONS=--search_path={ns}"],
        "preparacion": ["psql", "-U", "learner", "-d", "learning",
                        "-v", "ON_ERROR_STOP=1", "-q", "-f", "-"],
        # `-q` calla los mensajes de estado («SET», «INSERT 0 1») sin tocar el
        # resultado: sin el, una sentencia SET dentro de la consulta apareceria
        # como una fila mas.
        "consulta": ["psql", "-U", "learner", "-d", "learning", "-v", "ON_ERROR_STOP=1",
                     "-q", "-At", "-F", "|", "-f", "-"],
        "separador": "|",
    },
    "mysql": {
        "servicio": ["mysql"],
        # MySQL no tiene esquemas dentro de una base: el aislamiento por clase
        # es una base de datos por clase, y crearla exige privilegios de root.
        "aislar": ["mysql", "-uroot", "-plocal_root_only", "-e",
                   "DROP DATABASE IF EXISTS {ns}; CREATE DATABASE {ns};"],
        "preparacion": ["mysql", "-uroot", "-plocal_root_only", "{ns}"],
        "consulta": ["mysql", "-uroot", "-plocal_root_only", "-N", "-B", "{ns}"],
        "separador": "\t",
    },
    "mongodb": {
        "servicio": ["mongodb"],
        # mongosh leido desde la entrada estandar se comporta como una consola
        # interactiva y parte las expresiones de varias lineas. El guion se
        # deposita en un archivo dentro del contenedor y se ejecuta con --file.
        "preparacion": ["sh", "-c", "cat > /tmp/paso.js; mongosh --quiet "
                        "-u learner -p local_mongo_only --authenticationDatabase admin "
                        "{ns} --file /tmp/paso.js"],
        "consulta": ["sh", "-c", "cat > /tmp/paso.js; mongosh --quiet "
                     "-u learner -p local_mongo_only --authenticationDatabase admin "
                     "{ns} --file /tmp/paso.js"],
        "separador": "|",
    },
    "redis": {
        "servicio": ["redis"],
        # Redis tiene 16 bases numeradas; la clase entra en una de ellas y el
        # propio guion la vacia con FLUSHDB antes de escribir.
        "preparacion": ["redis-cli", "-a", "local_redis_only", "--no-auth-warning"],
        "consulta": ["redis-cli", "-a", "local_redis_only", "--no-auth-warning"],
        "separador": "|",
    },
    "neo4j": {
        "servicio": ["neo4j"],
        # La edicion Community solo tiene una base de datos de usuario, asi que
        # el aislamiento lo hace el propio guion con un borrado inicial.
        "preparacion": ["cypher-shell", "-u", "neo4j", "-p", "local_neo4j_only",
                        "--format", "plain"],
        "consulta": ["cypher-shell", "-u", "neo4j", "-p", "local_neo4j_only",
                     "--format", "plain"],
        # El formato `plain` separa las columnas por coma y espacio, imprime
        # una primera linea con los nombres y entrecomilla las cadenas: nada de
        # eso forma parte del resultado.
        "separador": ", ",
        "cabecera": True,
        "comillas": True,
    },
}


@dataclass
class Resultado:
    clase: str
    motor: str
    estado: str          # ok | fallo | omitido | declarado
    detalle: str = ""

    @property
    def simbolo(self) -> str:
        return {"ok": "OK", "fallo": "FALLO", "omitido": "--", "declarado": "decl"}[self.estado]


def secciones(codigo: str) -> tuple[str, str]:
    """Parte una implementacion en (preparacion, consulta) por sus marcadores."""
    actual = "preparacion"
    bloques: dict[str, list[str]] = {"preparacion": [], "consulta": []}
    for linea in codigo.splitlines():
        marca = MARCADOR.match(linea)
        if marca:
            actual = marca.group(1).lower()
            continue
        bloques[actual].append(linea)
    return "\n".join(bloques["preparacion"]).strip(), "\n".join(bloques["consulta"]).strip()


def normalizar(valor: object) -> str:
    """Toda salida se compara como texto: es lo unico comun a todos los motores."""
    if valor is None:
        return "NULL"
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, float):
        return str(int(valor)) if valor.is_integer() else f"{valor:g}"
    return str(valor).strip()


def filas_de_texto(salida: str, separador: str, cabecera: bool = False,
                   comillas: bool = False) -> list[list[str]]:
    lineas = [linea for linea in salida.splitlines() if linea.strip()]
    if cabecera and lineas:
        lineas = lineas[1:]
    filas = [[c.strip() for c in linea.split(separador)] for linea in lineas]
    if comillas:
        filas = [[c[1:-1] if len(c) >= 2 and c[0] == c[-1] == '"' else c for c in fila]
                 for fila in filas]
    return filas


# --------------------------------------------------------------------------- #
# Motores de nucleo: en proceso, sin servicios, en cualquier maquina.

def correr_sqlite(codigo: str) -> list[list[str]]:
    preparacion, consulta = secciones(codigo)
    conexion = sqlite3.connect(":memory:")
    try:
        conexion.execute("PRAGMA foreign_keys = ON")
        if preparacion:
            conexion.executescript(preparacion)
        cursor = conexion.execute(consulta)
        return [[normalizar(v) for v in fila] for fila in cursor.fetchall()]
    finally:
        conexion.close()


def correr_duckdb(codigo: str) -> list[list[str]]:
    import duckdb  # se importa aqui: sin DuckDB instalado el resto sigue verificandose

    preparacion, consulta = secciones(codigo)
    conexion = duckdb.connect()
    try:
        if preparacion:
            conexion.execute(preparacion)
        return [[normalizar(v) for v in fila] for fila in conexion.execute(consulta).fetchall()]
    finally:
        conexion.close()


NUCLEO = {"sqlite": correr_sqlite, "duckdb": correr_duckdb}


# --------------------------------------------------------------------------- #
# Motores de servicio: el cliente oficial dentro del contenedor.

def compose(argumentos: list[str], entrada: str,
            entorno: list[str] | None = None) -> subprocess.CompletedProcess:
    variables = [x for variable in (entorno or []) for x in ("-e", variable)]
    return subprocess.run(
        ["docker", "compose", "exec", "-T", *variables, *argumentos],
        input=entrada, capture_output=True, text=True, encoding="utf-8",
        errors="replace", cwd=ROOT, timeout=120,
    )


def correr_servicio(motor: str, codigo: str, clase: str) -> list[list[str]]:
    plan = SERVICIOS[motor]
    espacio = f"clase_{clase}"
    preparacion, consulta = secciones(codigo)

    def argumentos(clave: str) -> list[str]:
        return [a.format(ns=espacio) for a in plan[clave]]

    entorno = [v.format(ns=espacio) for v in plan.get("entorno", [])]
    if "aislar" in plan:
        limpio = compose(plan["servicio"] + argumentos("aislar"), "")
        if limpio.returncode != 0:
            raise RuntimeError(f"aislamiento: {limpio.stderr.strip()[:300]}")
    if preparacion:
        previo = compose(plan["servicio"] + argumentos("preparacion"), preparacion, entorno)
        if previo.returncode != 0:
            raise RuntimeError(f"preparacion: {previo.stderr.strip()[:300]}")
    hecho = compose(plan["servicio"] + argumentos("consulta"), consulta, entorno)
    if hecho.returncode != 0:
        raise RuntimeError(f"consulta: {hecho.stderr.strip()[:300]}")
    return filas_de_texto(hecho.stdout, plan["separador"],
                          cabecera=bool(plan.get("cabecera")),
                          comillas=bool(plan.get("comillas")))


def servicios_disponibles() -> set[str]:
    """Que contenedores estan realmente arriba. Si no hay ninguno, no se miente."""
    if shutil.which("docker") is None:
        return set()
    try:
        hecho = subprocess.run(["docker", "compose", "ps", "--services", "--status", "running"],
                               capture_output=True, text=True, cwd=ROOT, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return set()
    return {s.strip() for s in hecho.stdout.splitlines() if s.strip()}


# --------------------------------------------------------------------------- #

def verificar(comparacion: ml.Comparacion, con_servicios: bool,
              arriba: set[str]) -> list[Resultado]:
    resultados: list[Resultado] = []
    for motor in comparacion.motores:
        if not motor.aplica:
            continue
        if motor.ejecucion == "declarado":
            resultados.append(Resultado(comparacion.clase, motor.id, "declarado"))
            continue

        codigo = comparacion.codigo(motor)
        try:
            if motor.ejecucion == "nucleo":
                filas = NUCLEO[motor.id](codigo)
            else:
                plan = SERVICIOS.get(motor.id)
                if plan is None:
                    resultados.append(Resultado(comparacion.clase, motor.id, "omitido",
                                                "sin adaptador de servicio"))
                    continue
                if not con_servicios or not set(plan["servicio"]) <= arriba:
                    resultados.append(Resultado(comparacion.clase, motor.id, "omitido",
                                                "servicio no levantado"))
                    continue
                filas = correr_servicio(motor.id, codigo, comparacion.clase)
        except ImportError as error:
            resultados.append(Resultado(comparacion.clase, motor.id, "omitido", str(error)))
            continue
        except Exception as error:  # noqa: BLE001 - cualquier fallo del motor es un fallo
            resultados.append(Resultado(comparacion.clase, motor.id, "fallo",
                                        f"{type(error).__name__}: {error}"))
            continue

        if filas == comparacion.caso.esperado:
            resultados.append(Resultado(comparacion.clase, motor.id, "ok"))
        else:
            resultados.append(Resultado(
                comparacion.clase, motor.id, "fallo",
                f"esperado {comparacion.caso.esperado} y devolvio {filas}"))
    return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--clase", help="verificar solo esta clase (por ejemplo 016)")
    parser.add_argument("--motor", help="verificar solo este motor")
    parser.add_argument("--con-servicios", action="store_true",
                        help="ejecutar tambien contra los contenedores de docker compose")
    parser.add_argument("--verbose", action="store_true", help="una linea por implementacion")
    args = parser.parse_args()

    comparaciones = ml.todas()
    if args.clase:
        comparaciones = [c for c in comparaciones if c.clase == args.clase]
    if not comparaciones:
        print("No hay comparaciones que verificar.", file=sys.stderr)
        return 1

    estructurales = [e for c in comparaciones for e in c.errores]
    if estructurales:
        print("Comparaciones mal declaradas:", file=sys.stderr)
        for error in estructurales:
            print(f"  {error}", file=sys.stderr)
        return 1

    arriba = servicios_disponibles() if args.con_servicios else set()
    resultados: list[Resultado] = []
    for comparacion in comparaciones:
        resultados.extend(verificar(comparacion, args.con_servicios, arriba))
    if args.motor:
        resultados = [r for r in resultados if r.motor == args.motor]

    if args.verbose:
        for resultado in resultados:
            linea = f"  [{resultado.simbolo:>5}] {resultado.clase} {resultado.motor}"
            print(linea if not resultado.detalle else f"{linea} - {resultado.detalle}")

    fallos = [r for r in resultados if r.estado == "fallo"]
    if fallos and not args.verbose:
        for resultado in fallos:
            print(f"  [FALLO] {resultado.clase} {resultado.motor} - {resultado.detalle}",
                  file=sys.stderr)

    conteo = {estado: sum(1 for r in resultados if r.estado == estado)
              for estado in ("ok", "fallo", "omitido", "declarado")}
    print(f"EQUIVALENCIA_{'FALLIDA' if fallos else 'OK'} "
          f"{conteo['ok']} verificadas, {conteo['fallo']} fallidas, "
          f"{conteo['omitido']} omitidas, {conteo['declarado']} declaradas "
          f"en {len(comparaciones)} clases")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
