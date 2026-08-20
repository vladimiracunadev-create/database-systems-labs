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
    filas = re.findall(r"\| \[(\d{2})\]\([^)]+\) \| [^|]+ \| (\d+) \| (\d+) \|", README)
    assert len(filas) == len(real), "la tabla del programa no lista todas las partes"
    for pid, clases, horas in filas:
        assert (int(clases), int(horas)) == real[pid], (
            f"parte {pid}: el README dice {clases} clases y {horas} h; "
            f"el currículo suma {real[pid][0]} y {real[pid][1]}")


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
    assert total == 210, f"el programa suma {total} horas; el material publicado dice 210"
    datos = yaml.safe_load((RAIZ / "curriculum.yaml").read_text(encoding="utf-8"))
    assert datos["programa"]["idioma"] == "es"
