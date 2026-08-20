"""Utilidades comunes de las pruebas.

La idea de fondo: para probar que un validador sirve no basta con verlo pasar
sobre un repositorio sano. Hay que romperlo a proposito y comprobar que se da
cuenta. Como el validador trabaja sobre archivos, cada prueba en rojo necesita
su propia copia desechable del repositorio.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

RAIZ = Path(__file__).resolve().parents[1]

# Lo que no hace falta copiar: historial, cachés y configuración local.
IGNORAR = shutil.ignore_patterns(".git", "__pycache__", "node_modules", ".claude", ".venv")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Copia desechable del repositorio, para poder romperla sin consecuencias."""
    destino = tmp_path / "repo"
    shutil.copytree(RAIZ, destino, ignore=IGNORAR)
    return destino


def ejecutar(guion: str, *argumentos: str, raiz: Path = RAIZ) -> subprocess.CompletedProcess:
    """Ejecuta un script del repositorio y devuelve el resultado completo."""
    return subprocess.run(
        [sys.executable, str(raiz / guion), *argumentos],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=raiz,
    )


def validar(raiz: Path) -> subprocess.CompletedProcess:
    return ejecutar("scripts/validate_repository.py", "--verbose", raiz=raiz)


def leer_curriculo(raiz: Path) -> dict:
    return yaml.safe_load((raiz / "curriculum.yaml").read_text(encoding="utf-8"))


def escribir_curriculo(raiz: Path, curriculo: dict) -> None:
    (raiz / "curriculum.yaml").write_text(
        yaml.safe_dump(curriculo, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def leer_fuentes(raiz: Path) -> dict:
    return json.loads((raiz / "catalog" / "sources.json").read_text(encoding="utf-8"))


def escribir_fuentes(raiz: Path, fuentes: dict) -> None:
    (raiz / "catalog" / "sources.json").write_text(
        json.dumps(fuentes, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def primera_clase(curriculo: dict) -> dict:
    return curriculo["parts"][0]["classes"][0]


def ruta_leccion(raiz: Path, curriculo: dict, parte: dict, clase: dict) -> Path:
    return (
        raiz / "classes" / f"part-{parte['id']}-{parte['slug']}"
        / f"{clase['id']}-{clase['slug']}" / "lesson.md"
    )
