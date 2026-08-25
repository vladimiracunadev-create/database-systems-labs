"""Lo que el README afirma frente a lo que el repositorio contiene.

Las cifras de una portada envejecen solas: se añade una clase, se registra una
fuente, se escribe una prueba, y el README sigue diciendo lo de ayer. Aquí se
comprueba contra la fuente de verdad, que es `curriculum.yaml` y el propio
repositorio.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from conftest import leer_curriculo

RAIZ = Path(__file__).resolve().parents[1]
README = (RAIZ / "README.md").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def curriculo() -> dict:
    return leer_curriculo(RAIZ)


def test_la_tabla_del_programa_cuadra_con_el_curriculo(curriculo: dict) -> None:
    real = {p["id"]: (len(p["classes"]), sum(c["hours"] for c in p["classes"]))
            for p in curriculo["parts"]}
    rangos = {p["id"]: (p["classes"][0]["id"], p["classes"][-1]["id"])
              for p in curriculo["parts"]}
    # | 🪜 | [**00**](…) | Tema | Qué sabrás hacer | **001–010** (10) | 20 | 🟢… | — |
    filas = re.findall(
        r"\| [^|]* \| \[\*\*(\d{2})\*\*\]\([^)]+\) \| [^|]+ \| [^|]+ "
        r"\| \*\*(\d{3})–(\d{3})\*\* \((\d+)\) \| (\d+) \|",
        README)
    assert len(filas) == len(real), "la tabla del programa no lista todas las partes"
    for pid, primera, ultima, clases, horas in filas:
        assert (int(clases), int(horas)) == real[pid], (
            f"parte {pid}: el README dice {clases} clases y {horas} h; "
            f"el currículo suma {real[pid][0]} y {real[pid][1]}")
        assert (primera, ultima) == rangos[pid], (
            f"parte {pid}: el README dice que va de la clase {primera} a la {ultima}; "
            f"el currículo dice {rangos[pid][0]}–{rangos[pid][1]}")


def test_la_tabla_de_tramos_suma_lo_que_suman_sus_partes(curriculo: dict) -> None:
    """Un resumen por tramos que no suma es peor que no tenerlo.

    Es el error 3 del manual de coherencia: corregir el total de una tabla y
    dejar las filas, o al reves. Aqui se comprueba fila a fila contra la lista
    de partes que la propia fila declara.
    """
    clases = {p["id"]: len(p["classes"]) for p in curriculo["parts"]}
    horas = {p["id"]: sum(c["hours"] for c in p["classes"]) for p in curriculo["parts"]}
    ids_clase = {p["id"]: [c["id"] for c in p["classes"]] for p in curriculo["parts"]}
    filas = re.findall(
        r"\| \*\*[^*]+\*\* \| ([0-9 ·]+) \| \*\*(\d{3})–(\d{3})\*\* \((\d+)\) \| (\d+) \|",
        README)
    assert filas, "el README no trae la tabla de tramos"

    vistas: list[str] = []
    for ids_texto, primera, ultima, n_clases, n_horas in filas:
        ids = ids_texto.replace("·", " ").split()
        vistas += ids
        assert sum(clases[p] for p in ids) == int(n_clases), (
            f"tramo {ids_texto.strip()}: dice {n_clases} clases y sus partes suman "
            f"{sum(clases[p] for p in ids)}")
        assert sum(horas[p] for p in ids) == int(n_horas), (
            f"tramo {ids_texto.strip()}: dice {n_horas} horas y sus partes suman "
            f"{sum(horas[p] for p in ids)}")
        del_tramo = [c for p in ids for c in ids_clase[p]]
        assert (primera, ultima) == (del_tramo[0], del_tramo[-1]), (
            f"tramo {ids_texto.strip()}: dice que va de la clase {primera} a la {ultima}; "
            f"sus partes van de la {del_tramo[0]} a la {del_tramo[-1]}")

    assert sorted(vistas) == sorted(clases), (
        "los tramos no cubren todas las partes exactamente una vez: "
        f"{sorted(vistas)}")


def test_la_tabla_de_rutas_cuadra_con_el_curriculo(curriculo: dict) -> None:
    horas_parte = {p["id"]: sum(c["hours"] for c in p["classes"]) for p in curriculo["parts"]}
    filas = re.findall(r"\| ([^|]+) \| ([0-9 ·]+|todas) \| (entrada|intermedio|avanzado) \| "
                       r"(\d+) \| \[guía\]\(rutas/([a-z0-9-]+)\.md\) \|", README)
    assert len(filas) == len(curriculo["rutas"]), "faltan rutas en la tabla del README"
    for titulo, _partes, nivel, horas, clave in filas:
        ruta = curriculo["rutas"][clave]
        assert titulo.strip() == ruta["titulo"]
        assert nivel == ruta["nivel"]
        esperado = sum(horas_parte[pid] for pid in ruta["partes"])
        assert int(horas) == esperado, f"ruta {clave}: {horas} h en el README, {esperado} reales"


def test_las_cifras_de_la_portada_son_las_del_repositorio(curriculo: dict) -> None:
    fuentes = json.loads((RAIZ / "catalog" / "sources.json").read_text(encoding="utf-8"))
    clases = sum(len(p["classes"]) for p in curriculo["parts"])
    horas = sum(c["hours"] for p in curriculo["parts"] for c in p["classes"])
    ejecutables = sum(1 for lab in curriculo["laboratorios"] if lab["comando"])

    encabezado = README.split("</div>", 1)[0]
    assert f"{len(curriculo['parts'])} partes" in encabezado
    assert f"{clases} clases" in encabezado
    assert f"{horas} horas" in encabezado
    assert f"{len(fuentes['sources'])} fuentes" in encabezado, (
        f"el encabezado no declara las {len(fuentes['sources'])} fuentes del registro")
    assert f"fuentes-{len(fuentes['sources'])}" in encabezado, "la insignia de fuentes está stale"
    assert f"laboratorios-{ejecutables}%20ejecutables" in encabezado

    glosario = json.loads((RAIZ / "catalog" / "glosario.json").read_text(encoding="utf-8"))
    terminos = len(glosario["terms"])
    assert f"glosario-{terminos}" in encabezado, "la insignia del glosario está stale"
    assert f"{terminos} términos" in encabezado, (
        f"el encabezado no declara los {terminos} términos del glosario")


def test_el_about_de_github_no_se_comprueba_aqui() -> None:
    """Recordatorio deliberado, no una prueba de verdad.

    El «About» del repositorio no vive en el árbol de ficheros, así que ningún
    grep local lo alcanza y ninguna revisión de PR lo mira — y es lo primero que
    lee quien llega. Se quedó anunciando 64 clases y 109 fuentes mucho después
    de que el README dijera lo correcto. Se comprueba a mano:

        gh api repos/<owner>/<repo> --jq '{description, homepage, topics}'

    y se corrige con `--method PATCH --input payload.json`, nunca pasando el
    texto por el shell: los emoji y las tildes se corrompen en tránsito y se
    acaba publicando mojibake justo al arreglar la coherencia.
    """
    assert (RAIZ / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8").count(
        "About") >= 1, "docs/ARCHITECTURE.md debe recordar que el About también deriva"


def test_la_insignia_de_pruebas_dice_cuantas_hay() -> None:
    """La insignia declara un número de pruebas: que sea el que pytest recolecta."""
    recuento = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=RAIZ)
    por_archivo = re.findall(r"^tests/\S+: (\d+)$", recuento.stdout, re.M)
    assert por_archivo, recuento.stdout[-500:]
    total = sum(int(n) for n in por_archivo)
    declaradas = re.search(r"pruebas-(\d+)%20pytest", README)
    assert declaradas, "la insignia de pruebas no está en el README"
    assert int(declaradas.group(1)) == total, (
        f"el README declara {declaradas.group(1)} pruebas y hay {total}")


def test_el_indice_de_rutas_lista_todas_las_guias(curriculo: dict) -> None:
    indice = (RAIZ / "rutas" / "README.md").read_text(encoding="utf-8")
    for clave, ruta in curriculo["rutas"].items():
        assert f"({clave}.md)" in indice, f"la ruta {clave} no aparece en rutas/README.md"
        assert ruta["titulo"].split(" / ")[0] in indice


def test_el_curriculo_no_tiene_horas_sueltas(curriculo: dict) -> None:
    """La suma de las partes es la del programa: sin esto, toda cifra publicada miente."""
    total = sum(c["hours"] for p in curriculo["parts"] for c in p["classes"])
    assert f"{total} horas" in README, (
        f"el programa suma {total} horas y la portada no lo dice")
    datos = yaml.safe_load((RAIZ / "curriculum.yaml").read_text(encoding="utf-8"))
    assert datos["programa"]["idioma"] == "es"
