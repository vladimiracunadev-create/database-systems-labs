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

ROOT = Path(__file__).resolve().parents[1]

ARCHIVOS_OBLIGATORIOS = [
    "README.md", "LICENSE", "PROMPT_MAESTRO.md", "curriculum.yaml",
    "catalog/databases.json", "catalog/sources.json",
    "classes/README.md",
    "docs/ARCHITECTURE.md", "docs/LEARNING-MODEL.md", "docs/SOURCES.md",
    "labs/01-sql-foundations/run_lab.py", "labs/06-vector-search/run_vector_lab.py",
    "reference-data/school/schema.sqlite.sql", "reference-data/school/seed.sqlite.sql",
    "assessments/rubric.md",
    "scripts/build_classes.py", "scripts/generate_site.py",
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


def validar_curriculo(curriculo: dict, fuentes: dict, motores: dict) -> None:
    ids_fuente = {f["id"] for f in fuentes["sources"]}
    ids_motor = {m["id"] for m in motores["systems"]}
    ids_clase: list[str] = []
    slugs_parte: set[str] = set()
    citadas: set[str] = set()

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
        fallo(f"fuentes registradas y no citadas por ninguna clase: {huerfanas}")


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
    validar_curriculo(curriculo, fuentes, motores)
    validar_clases(curriculo)
    validar_datos_referencia()
    validar_enlaces_relativos()
    validar_codificacion()

    if fallos:
        _informe(args.verbose)
        return 1

    total = sum(len(p["classes"]) for p in curriculo["parts"])
    horas = sum(c["hours"] for p in curriculo["parts"] for c in p["classes"])
    print(f"REPOSITORY_OK  {len(curriculo['parts'])} partes · {total} clases · "
          f"{horas} horas · {len(fuentes['sources'])} fuentes · "
          f"{len(motores['systems'])} motores")
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
