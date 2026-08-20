"""Los laboratorios del nucleo, ejecutados de verdad.

Un laboratorio que no se ejecuta es una guia de lectura. Estas pruebas exigen
tres cosas de cada uno: que termine con exito, que imprima su marca de
resultado, y que no necesite dependencias fuera de la biblioteca estandar.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

from conftest import ejecutar

RAIZ = Path(__file__).resolve().parents[1]

LABORATORIOS = [
    ("labs/01-sql-foundations/run_lab.py", "LAB_OK"),
    ("labs/03-transactions/run_transactions_lab.py", "TRANSACTIONS_LAB_OK"),
    ("labs/04-indexing/run_indexing_lab.py", "INDEXING_LAB_OK"),
    ("labs/05-nosql-workloads/run_nosql_lab.py", "NOSQL_LAB_OK"),
    ("labs/06-vector-search/run_vector_lab.py", "VECTOR_LAB_OK"),
    ("labs/07-replication/run_replication_lab.py", "REPLICATION_LAB_OK"),
    ("labs/08-recovery/run_recovery_lab.py", "RECOVERY_LAB_OK"),
]


@pytest.mark.parametrize("guion,marca", LABORATORIOS)
def test_el_laboratorio_se_ejecuta(guion: str, marca: str) -> None:
    resultado = ejecutar(guion)
    assert resultado.returncode == 0, resultado.stderr
    assert marca in resultado.stdout


@pytest.mark.parametrize("guion,_marca", LABORATORIOS)
def test_el_laboratorio_no_importa_dependencias_externas(guion: str, _marca: str) -> None:
    """Si un laboratorio del nucleo empieza a necesitar `pip install`, deja de ser del nucleo."""
    arbol = ast.parse((RAIZ / guion).read_text(encoding="utf-8"))
    importados = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            importados.update(alias.name.split(".")[0] for alias in nodo.names)
        elif isinstance(nodo, ast.ImportFrom) and nodo.level == 0 and nodo.module:
            importados.add(nodo.module.split(".")[0])

    externos = sorted(importados - set(sys.stdlib_module_names))
    assert not externos, f"{guion} importa dependencias externas: {externos}"


@pytest.mark.parametrize("guion,_marca", LABORATORIOS)
def test_el_laboratorio_es_determinista(guion: str, _marca: str) -> None:
    """Dos ejecuciones seguidas deben poder compararse; si no, no es evidencia."""
    primera = ejecutar(guion)
    segunda = ejecutar(guion)
    assert primera.returncode == segunda.returncode == 0
    if guion.endswith("run_transactions_lab.py"):
        # El orden en que dos hilos ganan la carrera no es determinista, pero el
        # numero de reservas aceptadas si: es justo lo que el laboratorio afirma.
        pytest.skip("el reparto entre hilos varia; el invariante lo comprueba el propio guion")
    assert primera.stdout == segunda.stdout, "la salida cambia entre ejecuciones"
