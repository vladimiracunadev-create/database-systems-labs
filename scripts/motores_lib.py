"""Carga y validacion del eje comparado: el mismo problema en cada motor.

Este modulo es el corazon del cambio de modelo del repositorio. Hasta la
version 2 cada clase explicaba un concepto y citaba motores de pasada. A
partir de la version 3 cada clase declara **un caso**, lo resuelve en varios
motores, y dice para cada motor **por que si** conviene resolverlo ahi y **por
que no**.

    classes/<parte>/<clase>/motores.yaml        el contrato y la matriz
    classes/<parte>/<clase>/implementaciones/   el codigo real, uno por motor

El formato de `motores.yaml`:

    caso:
      titulo: Contar inscritos activos por curso
      contrato: |
        Con el dataset de la clase, devolver una fila por curso con su
        codigo y el numero de inscritos activos, ordenado por codigo.
      esperado:
        - ["DB-101", "3"]
        - ["SE-201", "2"]
      columnas: [codigo, activos]

    motores:
      - id: sqlite
        aplica: si
        ejecucion: nucleo            # nucleo | servicio | declarado
        archivo: implementaciones/sqlite/consulta.sql
        porque_si: ...
        porque_no: ...
        doc: https://sqlite.org/lang_select.html
      - id: redis
        aplica: no
        porque_no: ...
        alternativa: ...
        doc: https://redis.io/docs/latest/develop/data-types/

Reglas que se hacen cumplir (y por que):

- Todo motor declara `porque_si` **y** `porque_no`. Un motor que solo tiene
  ventajas no se entendio: se copio del folleto del fabricante.
- Todo motor declara `doc`, y `doc` tiene que colgar del dominio oficial que
  el catalogo `catalog/databases.json` registra para ese motor. Una
  afirmacion sobre un motor sin su pagina oficial al lado es una opinion.
- Si `aplica: si`, hay archivo y el archivo existe.
- Si `ejecucion` no es `declarado`, la implementacion se ejecuta de verdad en
  `scripts/verificar_equivalencia.py`: no se afirma que algo corre sin correrlo.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]

# Los tres niveles de prueba, del mas fuerte al mas honesto.
#
#   nucleo     se ejecuta en cualquier maquina y en todos los trabajos de CI,
#              sin servicios: SQLite (biblioteca estandar) y DuckDB (un pip).
#   servicio   se ejecuta contra el motor real levantado con `docker compose`,
#              usando su propio cliente oficial. Fuera de ese entorno, la
#              implementacion se muestra pero no se sella.
#   declarado  se muestra y se revisa a mano; la maquina no la ejecuta. Se
#              dice asi, con esas palabras, en la clase y en el sitio.
EJECUCION = ("nucleo", "servicio", "declarado")

MOTORES_NUCLEO = ("sqlite", "duckdb")

# Extensiones por motor, para que el generador sepa con que resaltar el bloque.
LENGUAJE_BLOQUE = {
    ".sql": "sql",
    ".cql": "sql",
    ".cypher": "cypher",
    ".js": "javascript",
    ".json": "json",
    ".txt": "text",
    ".sh": "bash",
    ".py": "python",
}


@dataclass
class Motor:
    """Una fila de la matriz: un motor frente al caso de la clase."""

    id: str
    aplica: bool
    porque_si: str
    porque_no: str
    doc: str
    ejecucion: str = "declarado"
    archivo: str | None = None
    alternativa: str | None = None
    como: str | None = None

    @property
    def ejecutable(self) -> bool:
        return self.aplica and self.ejecucion != "declarado"


@dataclass
class Caso:
    """El contrato de la clase: mismo enunciado, misma salida, en todo motor.

    `modo` distingue las dos formas de comparar:

        comparado    hay un caso ejecutable y una salida esperada; la maquina
                     comprueba que todos los motores devuelven lo mismo.
        conceptual   la decision no se puede reducir a una consulta con
                     resultado (consenso, CAP, gobierno del dato). Se compara
                     lo que cada motor OFRECE, no lo que devuelve, y se dice
                     abiertamente que aqui no hay sello de maquina.
    """

    titulo: str
    contrato: str
    columnas: list[str]
    esperado: list[list[str]]
    dataset: str = ""
    modo: str = "comparado"

    @property
    def conceptual(self) -> bool:
        return self.modo == "conceptual"


@dataclass
class Comparacion:
    """`motores.yaml` de una clase, ya cargado y comprobado."""

    clase: str
    caso: Caso
    motores: list[Motor]
    ruta: Path
    errores: list[str] = field(default_factory=list)

    @property
    def aplicables(self) -> list[Motor]:
        return [m for m in self.motores if m.aplica]

    @property
    def descartados(self) -> list[Motor]:
        return [m for m in self.motores if not m.aplica]

    @property
    def ejecutables(self) -> list[Motor]:
        return [m for m in self.motores if m.ejecutable]

    def codigo(self, motor: Motor) -> str:
        return (self.ruta.parent / motor.archivo).read_text(encoding="utf-8")


def dominio(url: str) -> str:
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def cargar_catalogo() -> dict[str, dict]:
    datos = json.loads((ROOT / "catalog" / "databases.json").read_text(encoding="utf-8"))
    return {s["id"]: s for s in datos["systems"]}


def cargar(ruta: Path, catalogo: dict[str, dict] | None = None) -> Comparacion:
    """Lee un `motores.yaml` y devuelve la comparacion con sus errores dentro.

    No lanza excepciones: acumula. El validador quiere el informe completo de
    lo que esta mal, no el primer fallo.
    """
    catalogo = catalogo if catalogo is not None else cargar_catalogo()
    errores: list[str] = []
    clase = ruta.parent.name.split("-", 1)[0]
    try:
        datos = yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as error:
        detalle = str(error).splitlines()[0]
        return Comparacion(clase=clase, caso=Caso("", "", [], []), motores=[], ruta=ruta,
                           errores=[f"{clase}: motores.yaml ilegible ({detalle})"])

    bruto_caso = datos.get("caso") or {}
    esperado = [[str(v) for v in fila] for fila in bruto_caso.get("esperado", [])]
    caso = Caso(
        titulo=bruto_caso.get("titulo", ""),
        contrato=(bruto_caso.get("contrato") or "").strip(),
        columnas=[str(c) for c in bruto_caso.get("columnas", [])],
        esperado=esperado,
        dataset=(bruto_caso.get("dataset") or "").strip(),
        modo=(bruto_caso.get("modo") or "comparado").strip(),
    )
    if caso.modo not in ("comparado", "conceptual"):
        errores.append(f"{clase}: modo de caso desconocido {caso.modo!r}")
    if not caso.titulo:
        errores.append(f"{clase}: el caso no tiene titulo")
    if not caso.contrato:
        errores.append(f"{clase}: el caso no declara contrato")
    if not caso.esperado and not caso.conceptual:
        errores.append(f"{clase}: el caso no declara salida esperada")
    if caso.columnas and any(len(f) != len(caso.columnas) for f in caso.esperado):
        errores.append(f"{clase}: filas esperadas con distinto numero de columnas")

    motores: list[Motor] = []
    vistos: set[str] = set()
    for bruto in datos.get("motores", []):
        mid = bruto.get("id", "")
        if mid in vistos:
            errores.append(f"{clase}: motor duplicado {mid!r}")
        vistos.add(mid)
        if mid not in catalogo:
            errores.append(f"{clase}: motor {mid!r} ausente de catalog/databases.json")

        aplica = bool(bruto.get("aplica", False))
        ejecucion = bruto.get("ejecucion", "declarado")
        if ejecucion not in EJECUCION:
            errores.append(f"{clase}/{mid}: ejecucion desconocida {ejecucion!r}")
        if ejecucion == "nucleo" and mid not in MOTORES_NUCLEO:
            errores.append(f"{clase}/{mid}: solo {MOTORES_NUCLEO} pueden ser de nucleo")

        porque_si = (bruto.get("porque_si") or "").strip()
        porque_no = (bruto.get("porque_no") or "").strip()
        if aplica and not porque_si:
            errores.append(f"{clase}/{mid}: aplica y no dice por que si")
        if caso.conceptual and aplica and not (bruto.get("como") or "").strip():
            errores.append(f"{clase}/{mid}: comparacion conceptual sin decir COMO se hace "
                           f"en este motor")
        if not porque_no:
            errores.append(f"{clase}/{mid}: no dice por que no; ningun motor sale gratis")

        doc = (bruto.get("doc") or "").strip()
        if not doc:
            errores.append(f"{clase}/{mid}: sin enlace a documentacion oficial")
        elif mid in catalogo and dominio(doc) != dominio(catalogo[mid]["official_docs"]):
            errores.append(
                f"{clase}/{mid}: la doc citada ({dominio(doc)}) no es el dominio oficial "
                f"({dominio(catalogo[mid]['official_docs'])})")

        archivo = bruto.get("archivo")
        if aplica and not caso.conceptual:
            if not archivo:
                errores.append(f"{clase}/{mid}: aplica y no declara archivo")
            elif not (ruta.parent / archivo).exists():
                errores.append(f"{clase}/{mid}: el archivo {archivo} no existe")
        elif archivo and not (ruta.parent / archivo).exists():
            errores.append(f"{clase}/{mid}: el archivo {archivo} no existe")
        elif archivo and not aplica:
            errores.append(f"{clase}/{mid}: no aplica pero declara archivo")
        if not aplica and not (bruto.get("alternativa") or "").strip():
            errores.append(f"{clase}/{mid}: descartado sin decir con que se resuelve entonces")

        motores.append(Motor(
            id=mid, aplica=aplica, porque_si=porque_si, porque_no=porque_no, doc=doc,
            ejecucion=ejecucion if aplica else "declarado", archivo=archivo,
            alternativa=(bruto.get("alternativa") or "").strip() or None,
            como=(bruto.get("como") or "").strip() or None,
        ))

    if not motores:
        errores.append(f"{clase}: la comparacion no tiene motores")
    if not caso.conceptual and not any(m.ejecucion == "nucleo" for m in motores):
        errores.append(f"{clase}: ninguna implementacion es de nucleo; nada se podria "
                       f"verificar sin servicios")

    return Comparacion(clase=clase, caso=caso, motores=motores, ruta=ruta, errores=errores)


def todas(raiz: Path | None = None) -> list[Comparacion]:
    """Todas las comparaciones del repositorio, en orden de clase."""
    base = (raiz or ROOT) / "classes"
    catalogo = cargar_catalogo()
    return [cargar(p, catalogo) for p in sorted(base.glob("part-*/*/motores.yaml"))]


CABECERA = re.compile(r"^\s*(?:--|//|#)\s*(?P<clave>motor|doc|nota)\s*:\s*(?P<valor>.+?)\s*$",
                      re.IGNORECASE)


def cabecera(codigo: str) -> dict[str, str]:
    """Lee las lineas `-- motor:` / `-- doc:` con las que abre cada implementacion."""
    campos: dict[str, str] = {}
    for linea in codigo.splitlines():
        if not linea.strip():
            continue
        encontrado = CABECERA.match(linea)
        if not encontrado:
            break
        campos[encontrado.group("clave").lower()] = encontrado.group("valor")
    return campos
