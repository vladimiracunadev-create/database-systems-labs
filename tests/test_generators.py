"""Los generadores y su modo `--check`.

`--check` es lo unico que impide que el sitio publicado y las clases del
repositorio digan cosas distintas. Estas pruebas comprueban las dos mitades:
que dice que si cuando todo esta al dia, y que dice que no cuando alguien edita
un artefacto derivado a mano o cambia la leccion sin regenerar.
"""

from __future__ import annotations

import filecmp
from pathlib import Path

import pytest

from conftest import ejecutar, leer_curriculo, ruta_leccion

RAIZ = Path(__file__).resolve().parents[1]

GENERADORES = [
    ("scripts/build_classes.py", "CLASSES_OK"),
    ("scripts/generate_site.py", "SITE_OK"),
]


@pytest.mark.parametrize("guion,marca", GENERADORES)
def test_los_artefactos_del_repositorio_estan_al_dia(guion: str, marca: str) -> None:
    resultado = ejecutar(guion, "--check")
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
    assert marca in resultado.stdout


@pytest.mark.parametrize("guion,marca", GENERADORES)
def test_generar_dos_veces_da_el_mismo_resultado(guion: str, marca: str, repo: Path) -> None:
    """Un generador que no es idempotente convierte cada ejecucion en un diff falso."""
    primera = ejecutar(guion, raiz=repo)
    assert primera.returncode == 0, primera.stderr
    segunda = ejecutar(guion, "--check", raiz=repo)
    assert segunda.returncode == 0, segunda.stdout + segunda.stderr
    assert marca in segunda.stdout


def test_editar_la_leccion_sin_regenerar_falla(repo: Path) -> None:
    curriculo = leer_curriculo(repo)
    parte = curriculo["parts"][0]
    clase = parte["classes"][0]
    leccion = ruta_leccion(repo, curriculo, parte, clase)
    leccion.write_text(
        leccion.read_text(encoding="utf-8").replace(
            "## Fundamentos", "## Fundamentos\n\nParrafo anadido a mano sin regenerar.\n"
        ),
        encoding="utf-8",
    )

    resultado = ejecutar("scripts/build_classes.py", "--check", raiz=repo)
    assert resultado.returncode == 1
    assert "desactualizados" in resultado.stdout + resultado.stderr


def test_editar_el_sitio_a_mano_falla(repo: Path) -> None:
    pagina = repo / "site" / "classes" / "001.html"
    pagina.write_text(
        pagina.read_text(encoding="utf-8").replace("</body>", "<p>editado a mano</p></body>"),
        encoding="utf-8",
    )

    resultado = ejecutar("scripts/generate_site.py", "--check", raiz=repo)
    assert resultado.returncode == 1
    assert "desactualizado" in resultado.stdout + resultado.stderr


def test_el_generador_de_clases_reconstruye_lo_que_se_borra(repo: Path) -> None:
    """Borrar un README de clase debe ser reparable con un solo comando."""
    curriculo = leer_curriculo(repo)
    parte = curriculo["parts"][0]
    clase = parte["classes"][0]
    readme = ruta_leccion(repo, curriculo, parte, clase).with_name("README.md")
    original = RAIZ / readme.relative_to(repo)
    readme.unlink()

    assert ejecutar("scripts/build_classes.py", "--check", raiz=repo).returncode == 1
    assert ejecutar("scripts/build_classes.py", raiz=repo).returncode == 0
    assert readme.exists()
    assert filecmp.cmp(readme, original, shallow=False), "el README regenerado no coincide"
