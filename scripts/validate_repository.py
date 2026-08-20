"""Validacion estructural del repositorio.

La regla que este script existe para hacer cumplir es una sola:

    NINGUNA CLASE SE PUBLICA SIN FUENTES, Y NINGUNA CITA APUNTA AL VACIO.

Alrededor de ella se comprueba todo lo que puede desincronizarse en silencio:
el curriculo frente a las carpetas, las lecciones frente a su estructura
minima, los motores citados frente al catalogo, los enlaces relativos y la
integridad del conjunto de datos de referencia.

Se ejecuta en cada `push` y es lo que decide si `main` esta en verde.

Uso:
    python scripts/validate_repository.py
    python scripts/validate_repository.py --verbose
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import motores_lib as ml  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

ARCHIVOS_OBLIGATORIOS = [
    "README.md", "LICENSE", "PROMPT_MAESTRO.md", "curriculum.yaml",
    "catalog/databases.json", "catalog/sources.json",
    "classes/README.md",
    "docs/ARCHITECTURE.md", "docs/LEARNING-MODEL.md", "docs/SOURCES.md",
    "labs/01-sql-foundations/run_lab.py",
    "labs/03-transactions/run_transactions_lab.py",
    "labs/04-indexing/run_indexing_lab.py",
    "labs/05-nosql-workloads/run_nosql_lab.py",
    "labs/06-vector-search/run_vector_lab.py",
    "labs/07-replication/run_replication_lab.py",
    "labs/08-recovery/run_recovery_lab.py",
    "reference-data/school/schema.sqlite.sql", "reference-data/school/seed.sqlite.sql",
    "assessments/README.md",
    "assessments/rubric.md",
    "assessments/diagnostic.md",
    "assessments/evidencias.md",
    "assessments/examen-por-rol.md",
    "projects/README.md",
    "projects/capstone.md",
    "projects/portafolio.md",
    "rutas/README.md",
    "certificaciones/README.md",
    "certificaciones/_mapeo.json",
    "scripts/build_classes.py", "scripts/generate_site.py",
    "scripts/motores_lib.py", "scripts/verificar_equivalencia.py",
    "site/index.html",
]

# Secciones que toda leccion debe traer. Sin ellas, el material no es una clase:
# es una nota. El orden no se exige; la presencia, si.
SECCIONES_LECCION = [
    "## Propósito",
    "## Resultados de aprendizaje",
    "## Fundamentos",
    "## Ejemplo trabajado",
    "## Errores frecuentes",
    "## Reto de transferencia",
    "## Preguntas de evaluación",
]

MINIMO_FUENTES_POR_CLASE = 2
MINIMO_CARACTERES_LECCION = 2500
# Una guia de rol corta no orienta a nadie: repite el titulo del cargo y ya.
MINIMO_CARACTERES_GUIA = 6000

# Lo que toda guia de rol debe responder. Sin esto es una lista de partes con
# un nombre de cargo encima.
SECCIONES_GUIA = [
    "## 🧭 Qué es y por qué importa",
    "## 🗓️ Un día en el puesto",
    "## 🧠 Qué necesitas saber",
    "## 📚 Tu ruta en el programa",
    "## 🧪 Qué tienes que poder demostrar",
    "## 🎓 Credenciales",
    "## 📈 Progresión y mercado",
    "## ⚠️ Mitos y errores comunes",
    "## 🚀 Siguientes pasos",
    "## 📖 De dónde sale esto",
]
ENLACE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SLUG_VALIDO = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

fallos: list[str] = []


def fallo(mensaje: str) -> None:
    fallos.append(mensaje)


# --------------------------------------------------------------------------- #

def cargar():
    curriculo = yaml.safe_load((ROOT / "curriculum.yaml").read_text(encoding="utf-8"))
    fuentes = json.loads((ROOT / "catalog" / "sources.json").read_text(encoding="utf-8"))
    motores = json.loads((ROOT / "catalog" / "databases.json").read_text(encoding="utf-8"))
    return curriculo, fuentes, motores


def validar_archivos() -> None:
    for item in ARCHIVOS_OBLIGATORIOS:
        if not (ROOT / item).exists():
            fallo(f"falta el archivo obligatorio: {item}")


def validar_curriculo(curriculo: dict, fuentes: dict, motores: dict,
                      citadas_por_laboratorios: set[str]) -> None:
    ids_fuente = {f["id"] for f in fuentes["sources"]}
    ids_motor = {m["id"] for m in motores["systems"]}
    ids_clase: list[str] = []
    slugs_parte: set[str] = set()
    citadas: set[str] = set(citadas_por_laboratorios)

    for parte in curriculo["parts"]:
        if not SLUG_VALIDO.match(parte["slug"]):
            fallo(f"parte {parte['id']}: slug no ASCII-kebab: {parte['slug']!r}")
        if parte["slug"] in slugs_parte:
            fallo(f"slug de parte duplicado: {parte['slug']}")
        slugs_parte.add(parte["slug"])

        for clase in parte["classes"]:
            cid = clase["id"]
            ids_clase.append(cid)

            if not SLUG_VALIDO.match(clase["slug"]):
                fallo(f"clase {cid}: slug no ASCII-kebab: {clase['slug']!r}")

            # --- la regla principal ---
            if len(clase["sources"]) < MINIMO_FUENTES_POR_CLASE:
                fallo(f"clase {cid}: {len(clase['sources'])} fuentes; el minimo es "
                      f"{MINIMO_FUENTES_POR_CLASE}")
            for sid in clase["sources"]:
                citadas.add(sid)
                if sid not in ids_fuente:
                    fallo(f"clase {cid}: cita la fuente inexistente {sid!r}")

            for motor in clase["engines"]:
                if motor not in ids_motor:
                    fallo(f"clase {cid}: motor {motor!r} ausente de catalog/databases.json")

            if clase["level"] not in {"fundamentos", "intermedio", "avanzado"}:
                fallo(f"clase {cid}: nivel desconocido {clase['level']!r}")
            if not isinstance(clase["hours"], int) or not 1 <= clase["hours"] <= 12:
                fallo(f"clase {cid}: horas fuera de rango: {clase['hours']!r}")
            if not clase["concepts"]:
                fallo(f"clase {cid}: sin conceptos declarados")

            lab = ROOT / clase["lab"]
            if not lab.is_dir():
                fallo(f"clase {cid}: laboratorio inexistente {clase['lab']}")

    esperado = [f"{n:03d}" for n in range(1, len(ids_clase) + 1)]
    if ids_clase != esperado:
        fallo("los identificadores de clase no forman la secuencia 001..N sin huecos")

    # Una fuente que nadie cita es peso muerto en el registro y envejece sin
    # que nadie la revise: se trata como error, no como aviso.
    huerfanas = sorted(ids_fuente - citadas)
    if huerfanas:
        fallo("fuentes registradas y no citadas por ninguna clase, laboratorio, ruta ni "
              f"certificacion: {huerfanas}")


def validar_laboratorios(curriculo: dict, fuentes: dict) -> set[str]:
    """Comprueba los laboratorios declarados y devuelve las fuentes que citan.

    Un laboratorio que dice ser ejecutable y no lo es seria la peor mentira del
    repositorio: aqui se comprueba que el guion existe y que la marca que dice
    imprimir esta de verdad en su codigo.
    """
    ids_fuente = {f["id"] for f in fuentes["sources"]}
    citadas: set[str] = set()
    vistos: set[str] = set()
    rutas: set[str] = set()

    for lab in curriculo.get("laboratorios", []):
        lid = lab["id"]
        if lid in vistos:
            fallo(f"laboratorio duplicado: {lid}")
        vistos.add(lid)
        rutas.add(lab["ruta"])

        if not (ROOT / lab["ruta"]).is_dir():
            fallo(f"laboratorio {lid}: la ruta {lab['ruta']} no existe")
        if not (ROOT / lab["ruta"] / "README.md").exists():
            fallo(f"laboratorio {lid}: sin README.md")
        if not lab.get("mide"):
            fallo(f"laboratorio {lid}: no declara que mide")

        comando = lab.get("comando", "")
        if comando:
            guion = comando.split()[-1]
            ruta_guion = ROOT / guion
            if not ruta_guion.exists():
                fallo(f"laboratorio {lid}: el comando apunta a {guion}, que no existe")
            elif not lab.get("marca"):
                fallo(f"laboratorio {lid}: es ejecutable y no declara marca de exito")
            elif lab["marca"] not in ruta_guion.read_text(encoding="utf-8"):
                fallo(f"laboratorio {lid}: el guion no imprime la marca {lab['marca']!r}")
        elif lab.get("marca"):
            fallo(f"laboratorio {lid}: declara marca sin comando que la produzca")

        if len(lab["fuentes"]) < MINIMO_FUENTES_POR_CLASE:
            fallo(f"laboratorio {lid}: {len(lab['fuentes'])} fuentes; el minimo es "
                  f"{MINIMO_FUENTES_POR_CLASE}")
        for sid in lab["fuentes"]:
            citadas.add(sid)
            if sid not in ids_fuente:
                fallo(f"laboratorio {lid}: cita la fuente inexistente {sid!r}")

    # Un laboratorio al que apunta una clase pero que nadie declara queda fuera
    # del sitio y del control: se trata como error.
    for parte in curriculo["parts"]:
        for clase in parte["classes"]:
            if clase["lab"] not in rutas:
                fallo(f"clase {clase['id']}: el laboratorio {clase['lab']} no esta "
                      f"declarado en la seccion `laboratorios`")
    return citadas


def validar_rutas(curriculo: dict, fuentes: dict) -> set[str]:
    """Comprueba las rutas por rol y devuelve las fuentes que citan.

    Una ruta es una promesa de recorrido: si apunta a una parte que no existe,
    a una clase que se renombro o a una guia que nadie escribio, deja de serlo.
    """
    ids_fuente = {f["id"] for f in fuentes["sources"]}
    ids_parte = {p["id"] for p in curriculo["parts"]}
    ids_clase = {c["id"] for p in curriculo["parts"] for c in p["classes"]}
    ids_lab = {lab["id"] for lab in curriculo.get("laboratorios", [])}
    horas_por_parte = {p["id"]: sum(c["hours"] for c in p["classes"]) for p in curriculo["parts"]}
    citadas: set[str] = set()

    for clave, ruta in curriculo["rutas"].items():
        if not SLUG_VALIDO.match(clave):
            fallo(f"ruta {clave!r}: clave no ASCII-kebab")

        for pid in ruta["partes"]:
            if pid not in ids_parte:
                fallo(f"ruta {clave}: la parte {pid} no existe")
        if len(set(ruta["partes"])) != len(ruta["partes"]):
            fallo(f"ruta {clave}: partes repetidas")

        for cid in ruta["clases_clave"]:
            if cid not in ids_clase:
                fallo(f"ruta {clave}: la clase clave {cid} no existe")
        for lid in ruta["laboratorios"]:
            if lid not in ids_lab:
                fallo(f"ruta {clave}: el laboratorio {lid} no esta declarado")

        if ruta["nivel"] not in {"entrada", "intermedio", "avanzado"}:
            fallo(f"ruta {clave}: nivel desconocido {ruta['nivel']!r}")
        if not ruta.get("cargos"):
            fallo(f"ruta {clave}: no declara a que cargos apunta")

        guia = ROOT / ruta["guia"]
        if not guia.exists():
            fallo(f"ruta {clave}: falta la guia {ruta['guia']}")
        else:
            texto = guia.read_text(encoding="utf-8")
            if len(texto) < MINIMO_CARACTERES_GUIA:
                fallo(f"ruta {clave}: guia de {len(texto)} caracteres; el minimo es "
                      f"{MINIMO_CARACTERES_GUIA}")
            for seccion in SECCIONES_GUIA:
                if seccion not in texto:
                    fallo(f"ruta {clave}: la guia no tiene la seccion {seccion!r}")
            # Las horas de la guia salen de sus partes: escritas a mano se
            # desincronizan en cuanto una parte cambia de duracion.
            horas = sum(horas_por_parte.get(pid, 0) for pid in ruta["partes"])
            if f"{horas} horas" not in texto:
                fallo(f"ruta {clave}: la guia no declara las {horas} horas que suman sus partes")

        if len(ruta["fuentes"]) < MINIMO_FUENTES_POR_CLASE:
            fallo(f"ruta {clave}: {len(ruta['fuentes'])} fuentes; el minimo es "
                  f"{MINIMO_FUENTES_POR_CLASE}")
        for sid in ruta["fuentes"]:
            citadas.add(sid)
            if sid not in ids_fuente:
                fallo(f"ruta {clave}: cita la fuente inexistente {sid!r}")

    if not (ROOT / "rutas" / "README.md").exists():
        fallo("falta el indice de rutas rutas/README.md")
    return citadas


def validar_certificaciones(curriculo: dict, fuentes: dict) -> set[str]:
    """Comprueba el mapeo de certificaciones y devuelve las fuentes que cita.

    Un porcentaje de cobertura es una afirmacion como cualquier otra: si el
    peso no es el oficial, si la clase que dice cubrir un dominio no existe o
    si la suma de los pesos no da 100, el numero publicado miente.
    """
    ruta = ROOT / "certificaciones" / "_mapeo.json"
    if not ruta.exists():
        fallo("falta certificaciones/_mapeo.json")
        return set()

    mapeo = json.loads(ruta.read_text(encoding="utf-8"))
    ids_fuente = {f["id"] for f in fuentes["sources"]}
    ids_clase = {c["id"] for p in curriculo["parts"] for c in p["classes"]}
    ids_lab = {lab["id"] for lab in curriculo.get("laboratorios", [])}
    citadas: set[str] = set()
    vistos: set[str] = set()

    for cert in mapeo["certificaciones"]:
        cid = cert["id"]
        if cid in vistos:
            fallo(f"certificacion duplicada: {cid}")
        vistos.add(cid)

        if cert["metodo"] not in mapeo["metodos"]:
            fallo(f"certificacion {cid}: metodo desconocido {cert['metodo']!r}")
        if cert["nivel"] not in {"entrada", "intermedio", "avanzado"}:
            fallo(f"certificacion {cid}: nivel desconocido {cert['nivel']!r}")
        for campo in ("url", "temario"):
            if not cert[campo].startswith("https://"):
                fallo(f"certificacion {cid}: {campo} no es una URL segura")
        if cert["ruta"] not in curriculo["rutas"]:
            fallo(f"certificacion {cid}: la ruta {cert['ruta']!r} no existe")
        for lid in cert["laboratorios"]:
            if lid not in ids_lab:
                fallo(f"certificacion {cid}: el laboratorio {lid} no esta declarado")

        # Los pesos son los oficiales del temario. Cuando el proveedor los
        # publica como rangos ("15-20 %"), el punto medio no suma exactamente
        # 100 y el generador normaliza; aqui solo se comprueba que la desviacion
        # sea la de un redondeo y no la de un dominio olvidado.
        suma = sum(d["peso"] for d in cert["dominios"])
        if abs(suma - 100) > 10:
            fallo(f"certificacion {cid}: los pesos suman {suma}; falta o sobra un dominio")

        for dominio in cert["dominios"]:
            if cert["metodo"] == "subareas":
                if not dominio.get("subareas"):
                    fallo(f"certificacion {cid}: el dominio {dominio['nombre']!r} no lista subareas")
                for sub in dominio.get("subareas", []):
                    if sub["cubierto"] and not sub["clases"]:
                        fallo(f"certificacion {cid}: {sub['nombre']!r} se declara cubierta "
                              f"sin decir por que clases")
                    if not sub["cubierto"] and sub["clases"]:
                        fallo(f"certificacion {cid}: {sub['nombre']!r} no esta cubierta "
                              f"pero cita clases")
                    for clase in sub["clases"]:
                        if clase not in ids_clase:
                            fallo(f"certificacion {cid}: la clase {clase} no existe")
            else:
                cobertura = dominio.get("cobertura")
                if not isinstance(cobertura, (int, float)) or not 0 <= cobertura <= 100:
                    fallo(f"certificacion {cid}: cobertura fuera de rango en "
                          f"{dominio['nombre']!r}")
                if not dominio.get("clases"):
                    fallo(f"certificacion {cid}: el dominio {dominio['nombre']!r} estima "
                          f"cobertura sin citar clases")
                for clase in dominio.get("clases", []):
                    if clase not in ids_clase:
                        fallo(f"certificacion {cid}: la clase {clase} no existe")

        if len(cert["fuentes"]) < MINIMO_FUENTES_POR_CLASE:
            fallo(f"certificacion {cid}: {len(cert['fuentes'])} fuentes; el minimo es "
                  f"{MINIMO_FUENTES_POR_CLASE}")
        for sid in cert["fuentes"]:
            citadas.add(sid)
            if sid not in ids_fuente:
                fallo(f"certificacion {cid}: cita la fuente inexistente {sid!r}")

        if not (ROOT / "certificaciones" / f"{cid}.md").exists():
            fallo(f"certificacion {cid}: falta la ficha; ejecuta "
                  f"scripts/generar_certificaciones.py")

    for item in mapeo["sin_mapeo"]:
        if not item.get("motivo"):
            fallo(f"certificacion sin mapear {item['nombre']!r}: sin motivo declarado")

    return citadas


def validar_evaluacion(curriculo: dict) -> None:
    """Comprueba la rubrica y el examen por rol.

    Una rubrica es una promesa de trato igual: si los pesos no suman, si a una
    dimension le falta un nivel o si exige un minimo que su escala no tiene,
    dos correctores no llegaran al mismo numero por mucho que lo intenten.
    """
    evaluacion = curriculo["evaluacion"]
    escala = evaluacion["escala"]
    ids_clase = {c["id"] for p in curriculo["parts"] for c in p["classes"]}
    ids_lab = {lab["id"] for lab in curriculo.get("laboratorios", [])}

    if set(escala) != {1, 2, 3, 4}:
        fallo(f"la escala de la rubrica deberia tener cuatro niveles, tiene {sorted(escala)}")

    peso = 0
    vistos: set[str] = set()
    for dimension in evaluacion["dimensiones"]:
        did = dimension["id"]
        if did in vistos:
            fallo(f"dimension duplicada en la rubrica: {did}")
        vistos.add(did)
        peso += dimension["peso"]

        if set(dimension["niveles"]) != set(escala):
            fallo(f"dimension {did}: no describe los cuatro niveles de la escala")
        for nivel, texto in dimension["niveles"].items():
            if not str(texto).strip():
                fallo(f"dimension {did}: el nivel {nivel} no describe nada")
        if dimension["minimo"] not in escala:
            fallo(f"dimension {did}: minimo {dimension['minimo']} fuera de la escala")
        if not dimension.get("evidencia"):
            fallo(f"dimension {did}: no dice que evidencia hay que ver")
        if not dimension.get("pregunta"):
            fallo(f"dimension {did}: no dice que pregunta responde")
        for cid in dimension.get("clases", []):
            if cid not in ids_clase:
                fallo(f"dimension {did}: la clase {cid} no existe")
        for lid in dimension.get("laboratorios", []):
            if lid not in ids_lab:
                fallo(f"dimension {did}: el laboratorio {lid} no esta declarado")

    if peso != 100:
        fallo(f"los pesos de la rubrica suman {peso}, no 100")
    if not 0 < evaluacion["aprobacion"] <= 100:
        fallo(f"umbral de aprobacion fuera de rango: {evaluacion['aprobacion']}")
    faltas = evaluacion.get("faltas_criticas", [])
    if len(faltas) < 3:
        fallo("la rubrica declara menos de tres faltas criticas")
    for falta in faltas:
        # Una frase con dos puntos sin comillas la lee YAML como diccionario y
        # deja de ser texto sin que nadie lo note hasta que se publica.
        if not isinstance(falta, str):
            fallo(f"falta critica que no es texto (¿faltan comillas en el YAML?): {falta!r}")

    # Los cinco componentes de la nota tambien tienen que sumar el total.
    componentes = ["diagnostico", "evidencias_de_laboratorio", "retos_de_transferencia",
                   "decisiones_de_arquitectura", "proyecto_final"]
    total = sum(evaluacion[c] for c in componentes)
    if total != 100:
        fallo(f"los componentes de la nota suman {total}, no 100")

    examen = evaluacion["examen"]
    puntos = sum(b["puntos"] for b in examen["bloques"])
    if puntos != 100:
        fallo(f"los bloques del examen suman {puntos} puntos, no 100")
    for bloque in examen["bloques"]:
        if not bloque.get("formato", "").strip():
            fallo(f"bloque {bloque['id']}: sin formato declarado")
        if bloque.get("minimo") and bloque["minimo"] > bloque["puntos"]:
            fallo(f"bloque {bloque['id']}: el minimo supera sus puntos")
    if examen["aprobacion"] > puntos:
        fallo("el examen exige mas puntos de los que reparte")


def validar_fuentes(fuentes: dict) -> None:
    vistos: set[str] = set()
    for f in fuentes["sources"]:
        fid = f["id"]
        if fid in vistos:
            fallo(f"fuente duplicada en el registro: {fid}")
        vistos.add(fid)

        if not f.get("url", "").startswith(("http://", "https://")):
            fallo(f"fuente {fid}: sin URL utilizable")
        if not f.get("note"):
            fallo(f"fuente {fid}: sin nota que explique para que sirve")
        if f["kind"] not in fuentes["kinds"]:
            fallo(f"fuente {fid}: tipo desconocido {f['kind']!r}")
        # Un libro sin ISBN o un articulo sin sede ni DOI no es localizable con
        # certeza: es justo el tipo de cita vaga que este repositorio prohibe.
        if f["kind"] == "book" and not f.get("isbn"):
            fallo(f"fuente {fid}: libro sin ISBN")
        if f["kind"] == "paper" and not (f.get("doi") or f.get("venue")):
            fallo(f"fuente {fid}: articulo sin DOI ni sede de publicacion")
        if not f.get("authors"):
            fallo(f"fuente {fid}: sin autoria")


def validar_clases(curriculo: dict) -> None:
    for parte in curriculo["parts"]:
        base = ROOT / "classes" / f"part-{parte['id']}-{parte['slug']}"
        if not (base / "README.md").exists():
            fallo(f"parte {parte['id']}: falta el indice classes/.../README.md")

        for clase in parte["classes"]:
            carpeta = base / f"{clase['id']}-{clase['slug']}"
            leccion = carpeta / "lesson.md"
            readme = carpeta / "README.md"

            if not leccion.exists():
                fallo(f"clase {clase['id']}: falta lesson.md")
                continue
            if not readme.exists():
                fallo(f"clase {clase['id']}: falta README.md (ejecuta build_classes.py)")

            texto = leccion.read_text(encoding="utf-8")
            for seccion in SECCIONES_LECCION:
                if seccion not in texto:
                    fallo(f"clase {clase['id']}: la leccion no tiene la seccion {seccion!r}")
            if len(texto) < MINIMO_CARACTERES_LECCION:
                fallo(f"clase {clase['id']}: leccion de {len(texto)} caracteres; "
                      f"el minimo es {MINIMO_CARACTERES_LECCION}")
            # Un ejemplo trabajado sin ningun bloque de codigo o traza no es un
            # ejemplo trabajado.
            if "```" not in texto:
                fallo(f"clase {clase['id']}: la leccion no incluye ningun bloque de codigo")


def validar_catalogo_motores(motores: dict) -> None:
    sistemas = motores["systems"]
    ids = [s["id"] for s in sistemas]
    if len(sistemas) < 20:
        fallo(f"el catalogo tiene {len(sistemas)} motores; el minimo es 20")
    if len(ids) != len(set(ids)):
        fallo("hay identificadores de motor duplicados")
    for s in sistemas:
        if not s["official_docs"].startswith("https://"):
            fallo(f"motor {s['id']}: documentacion oficial ausente o no segura")
        if not s["families"] or not s["query"]:
            fallo(f"motor {s['id']}: sin familias o sin lenguaje de consulta")


def validar_datos_referencia() -> None:
    datos = ROOT / "reference-data" / "school"
    conexion = sqlite3.connect(":memory:")
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.executescript((datos / "schema.sqlite.sql").read_text(encoding="utf-8"))
    conexion.executescript((datos / "seed.sqlite.sql").read_text(encoding="utf-8"))
    estudiantes = conexion.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    colgantes = conexion.execute("PRAGMA foreign_key_check").fetchall()
    if estudiantes < 1:
        fallo("el conjunto de datos de referencia esta vacio")
    if colgantes:
        fallo(f"el conjunto de datos de referencia tiene referencias colgantes: {colgantes}")
    conexion.close()


def validar_enlaces_relativos() -> None:
    for archivo in ROOT.rglob("*.md"):
        if any(p in archivo.parts for p in (".git", "site", "node_modules")):
            continue
        for destino in ENLACE.findall(archivo.read_text(encoding="utf-8")):
            limpio = destino.split("#", 1)[0].strip()
            if not limpio or limpio.startswith(("http://", "https://", "mailto:")):
                continue
            if not (archivo.parent / limpio).resolve().exists():
                fallo(f"enlace roto: {archivo.relative_to(ROOT)} -> {destino}")


def validar_codificacion() -> None:
    """Detecta el mojibake tipico de un archivo leido como latin-1 y guardado como UTF-8."""
    # Los patrones se derivan en vez de escribirse: el mojibake es exactamente
    # lo que sale de codificar en UTF-8 y leer como latin-1. Escribirlos
    # literales haria que este archivo diera positivo en su propia comprobacion.
    sospechosos = tuple(
        caracter.encode("utf-8").decode("latin-1")
        for caracter in "áéíóúñ¿¡—"
    ) + (chr(0xFFFD),)
    for archivo in ROOT.rglob("*"):
        if archivo.suffix not in {".md", ".yaml", ".yml", ".json", ".py", ".html", ".css", ".js"}:
            continue
        if any(p in archivo.parts for p in (".git", "node_modules", "__pycache__")):
            continue
        try:
            texto = archivo.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fallo(f"archivo que no es UTF-8 valido: {archivo.relative_to(ROOT)}")
            continue
        for patron in sospechosos:
            if patron in texto:
                fallo(f"codificacion corrupta ({patron!r}) en {archivo.relative_to(ROOT)}")
                break


def validar_comparaciones(curriculo: dict) -> int:
    """Comprueba el eje comparado: un caso por clase, resuelto en varios motores.

    Lo que se hace cumplir aqui es el contrato del repositorio a partir de la
    version 3: si una clase declara una comparacion, esa comparacion tiene que
    estar completa. Cada motor con su `por que si` y su `por que no`, cada
    afirmacion con su pagina oficial, y cada implementacion declarada existiendo
    de verdad en el disco.

    Devuelve cuantas clases traen comparacion, para el informe final.
    """
    comparaciones = ml.todas(ROOT)
    for comparacion in comparaciones:
        for error in comparacion.errores:
            fallo(f"comparacion de motores: {error}")

    ids_clase = {c["id"] for p in curriculo["parts"] for c in p["classes"]}
    for comparacion in comparaciones:
        if comparacion.clase not in ids_clase:
            fallo(f"comparacion de motores: la clase {comparacion.clase} no esta "
                  f"en curriculum.yaml")
    return len(comparaciones)


# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    validar_archivos()
    if fallos:
        _informe(args.verbose)
        return 1

    curriculo, fuentes, motores = cargar()
    validar_fuentes(fuentes)
    validar_catalogo_motores(motores)
    citadas_labs = validar_laboratorios(curriculo, fuentes)
    citadas_rutas = validar_rutas(curriculo, fuentes)
    citadas_certs = validar_certificaciones(curriculo, fuentes)
    validar_evaluacion(curriculo)
    validar_curriculo(curriculo, fuentes, motores,
                      citadas_labs | citadas_rutas | citadas_certs)
    validar_clases(curriculo)
    comparadas = validar_comparaciones(curriculo)
    validar_datos_referencia()
    validar_enlaces_relativos()
    validar_codificacion()

    if fallos:
        _informe(args.verbose)
        return 1

    total = sum(len(p["classes"]) for p in curriculo["parts"])
    horas = sum(c["hours"] for p in curriculo["parts"] for c in p["classes"])
    implementaciones = sum(len(c.aplicables) for c in ml.todas(ROOT))
    print(f"REPOSITORY_OK  {len(curriculo['parts'])} partes · {total} clases · "
          f"{horas} horas · {len(fuentes['sources'])} fuentes · "
          f"{len(motores['systems'])} motores · {comparadas} clases comparadas "
          f"con {implementaciones} implementaciones")
    return 0


def _informe(verbose: bool) -> None:
    print(f"VALIDATION_FAILED: {len(fallos)} problemas", file=sys.stderr)
    limite = len(fallos) if verbose else 40
    for mensaje in fallos[:limite]:
        print(f"  - {mensaje}", file=sys.stderr)
    if len(fallos) > limite:
        print(f"  ... y {len(fallos) - limite} mas (usa --verbose)", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
