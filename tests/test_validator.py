"""El validador, visto en rojo.

Cada prueba rompe el repositorio de una forma concreta y exige que
`validate_repository.py` lo detecte y lo diga. Si alguna de estas pruebas pasa
a verde por si sola, la regla que dice defender ha dejado de defenderse.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import (
    escribir_curriculo,
    escribir_fuentes,
    leer_curriculo,
    leer_fuentes,
    primera_clase,
    ruta_leccion,
    validar,
)


def test_repositorio_real_pasa() -> None:
    """El punto de partida: sobre el repositorio de verdad, verde."""
    resultado = validar(Path(__file__).resolve().parents[1])
    assert resultado.returncode == 0, resultado.stderr
    assert "REPOSITORY_OK" in resultado.stdout


def test_clase_con_una_sola_fuente(repo: Path) -> None:
    curriculo = leer_curriculo(repo)
    primera_clase(curriculo)["sources"] = ["ddia"]
    escribir_curriculo(repo, curriculo)

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "el minimo es 2" in resultado.stderr


def test_cita_a_una_fuente_inexistente(repo: Path) -> None:
    curriculo = leer_curriculo(repo)
    primera_clase(curriculo)["sources"] = ["ddia", "fuente-que-no-existe"]
    escribir_curriculo(repo, curriculo)

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "cita la fuente inexistente" in resultado.stderr


def test_fuente_registrada_que_nadie_cita(repo: Path) -> None:
    fuentes = leer_fuentes(repo)
    fuentes["sources"].append(
        {
            "id": "fuente-huerfana",
            "kind": "docs",
            "title": "Documentacion inventada",
            "authors": ["Nadie"],
            "year": 2026,
            "url": "https://example.org/",
            "note": "Existe en el registro y no la cita ninguna clase.",
        }
    )
    escribir_fuentes(repo, fuentes)

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "no citadas por ninguna clase" in resultado.stderr


def test_libro_sin_isbn(repo: Path) -> None:
    fuentes = leer_fuentes(repo)
    libro = next(f for f in fuentes["sources"] if f["kind"] == "book")
    libro.pop("isbn", None)
    escribir_fuentes(repo, fuentes)

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "libro sin ISBN" in resultado.stderr


def test_articulo_sin_doi_ni_sede(repo: Path) -> None:
    fuentes = leer_fuentes(repo)
    articulo = next(f for f in fuentes["sources"] if f["kind"] == "paper")
    articulo.pop("doi", None)
    articulo.pop("venue", None)
    escribir_fuentes(repo, fuentes)

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "sin DOI ni sede" in resultado.stderr


def test_motor_ausente_del_catalogo(repo: Path) -> None:
    curriculo = leer_curriculo(repo)
    primera_clase(curriculo)["engines"] = ["motor-inventado"]
    escribir_curriculo(repo, curriculo)

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "ausente de catalog/databases.json" in resultado.stderr


def test_leccion_sin_una_seccion_obligatoria(repo: Path) -> None:
    curriculo = leer_curriculo(repo)
    parte = curriculo["parts"][0]
    clase = parte["classes"][0]
    leccion = ruta_leccion(repo, curriculo, parte, clase)
    leccion.write_text(
        leccion.read_text(encoding="utf-8").replace("## Errores frecuentes", "## Notas sueltas"),
        encoding="utf-8",
    )

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "Errores frecuentes" in resultado.stderr


def test_leccion_demasiado_corta(repo: Path) -> None:
    curriculo = leer_curriculo(repo)
    parte = curriculo["parts"][0]
    clase = parte["classes"][0]
    leccion = ruta_leccion(repo, curriculo, parte, clase)
    secciones = [
        "## Propósito", "## Resultados de aprendizaje", "## Fundamentos",
        "## Ejemplo trabajado", "## Errores frecuentes", "## Reto de transferencia",
        "## Preguntas de evaluación",
    ]
    leccion.write_text("\n\n".join(secciones) + "\n\n```sql\nSELECT 1;\n```\n", encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "el minimo es 2500" in resultado.stderr


def test_enlace_relativo_roto(repo: Path) -> None:
    objetivo = repo / "docs" / "ARCHITECTURE.md"
    objetivo.write_text(
        objetivo.read_text(encoding="utf-8") + "\n[archivo que no existe](./no-existe.md)\n",
        encoding="utf-8",
    )

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "enlace roto" in resultado.stderr


def test_codificacion_corrupta(repo: Path) -> None:
    # Mojibake real: texto UTF-8 releido como latin-1, que es como aparece
    # cuando un editor mal configurado guarda un archivo con acentos.
    roto = "modelo relacional y algebra".replace("algebra", "álgebra")
    roto = roto.encode("utf-8").decode("latin-1")
    (repo / "docs" / "ENVIRONMENTS.md").write_text(roto, encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "codificacion corrupta" in resultado.stderr


def test_archivo_obligatorio_ausente(repo: Path) -> None:
    (repo / "assessments" / "rubric.md").unlink()

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "falta el archivo obligatorio" in resultado.stderr


@pytest.mark.parametrize("guion", [
    "labs/01-sql-foundations/run_lab.py",
    "labs/03-transactions/run_transactions_lab.py",
    "labs/04-indexing/run_indexing_lab.py",
    "labs/05-nosql-workloads/run_nosql_lab.py",
    "labs/06-vector-search/run_vector_lab.py",
    "labs/07-replication/run_replication_lab.py",
    "labs/08-recovery/run_recovery_lab.py",
])
def test_laboratorio_declarado_como_obligatorio(guion: str) -> None:
    """Los laboratorios ejecutables deben estar en la lista que el validador exige."""
    texto = (Path(__file__).resolve().parents[1] / "scripts" / "validate_repository.py").read_text(
        encoding="utf-8"
    )
    assert guion in texto, f"{guion} no figura entre los archivos obligatorios"
