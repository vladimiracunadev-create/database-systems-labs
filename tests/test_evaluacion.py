"""La evaluación: que la rúbrica sea aplicable y que el examen cuadre.

Una rúbrica mal cuadrada no se nota al leerla —se nota cuando dos personas
corrigen el mismo trabajo y sacan notas distintas—. Estas pruebas comprueban lo
que hace que eso no pase: pesos que suman, niveles descritos, mínimos dentro de
la escala y documentos generados que no contradicen al currículo.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from conftest import ejecutar, leer_curriculo, validar

RAIZ = Path(__file__).resolve().parents[1]
EVAL = RAIZ / "assessments"
PROY = RAIZ / "projects"


@pytest.fixture(scope="module")
def curriculo() -> dict:
    return leer_curriculo(RAIZ)


@pytest.fixture(scope="module")
def evaluacion(curriculo: dict) -> dict:
    return curriculo["evaluacion"]


def test_la_rubrica_y_el_examen_estan_al_dia() -> None:
    resultado = ejecutar("scripts/generar_evaluacion.py", "--check")
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
    assert "EVALUACION_OK" in resultado.stdout


def test_los_pesos_de_la_rubrica_suman_cien(evaluacion: dict) -> None:
    assert sum(d["peso"] for d in evaluacion["dimensiones"]) == 100


def test_los_componentes_de_la_nota_suman_cien(evaluacion: dict) -> None:
    componentes = ["diagnostico", "evidencias_de_laboratorio", "retos_de_transferencia",
                   "decisiones_de_arquitectura", "proyecto_final"]
    assert sum(evaluacion[c] for c in componentes) == 100


def test_cada_dimension_describe_sus_cuatro_niveles(evaluacion: dict) -> None:
    escala = set(evaluacion["escala"])
    for dimension in evaluacion["dimensiones"]:
        assert set(dimension["niveles"]) == escala, f"{dimension['id']}: faltan niveles"
        for texto in dimension["niveles"].values():
            # «Existe un respaldo.» es un nivel 1 legítimo y corto: lo que se
            # exige es que describa algo observable y que no repita a otro.
            assert isinstance(texto, str) and len(texto.strip()) > 12, (
                f"{dimension['id']}: nivel sin describir")
        assert len(set(dimension["niveles"].values())) == 4, (
            f"{dimension['id']}: hay dos niveles con la misma descripción")
        assert dimension["minimo"] in escala
        assert dimension["evidencia"].strip() and dimension["pregunta"].strip()


def test_los_minimos_exigentes_estan_donde_duele(evaluacion: dict) -> None:
    """Seguridad, recuperación y transacciones no admiten nivel 2: son las que arruinan."""
    minimos = {d["id"]: d["minimo"] for d in evaluacion["dimensiones"]}
    for critica in ("seguridad", "recuperacion", "transacciones", "modelado"):
        assert minimos[critica] >= 3, f"{critica} debería exigir al menos nivel Sólido"


def test_la_rubrica_publicada_contiene_cada_dimension(evaluacion: dict) -> None:
    texto = (EVAL / "rubric.md").read_text(encoding="utf-8")
    for dimension in evaluacion["dimensiones"]:
        assert dimension["nombre"] in texto
        assert dimension["pregunta"] in texto
        for nivel in dimension["niveles"].values():
            assert nivel in texto, f"{dimension['id']}: falta un nivel en la rúbrica publicada"
    for falta in evaluacion["faltas_criticas"]:
        assert falta in texto


def test_el_examen_cubre_las_siete_rutas(curriculo: dict) -> None:
    texto = (EVAL / "examen-por-rol.md").read_text(encoding="utf-8")
    for clave, ruta in curriculo["rutas"].items():
        assert ruta["titulo"] in texto, f"la ruta {clave} no aparece en el examen"
        assert f"../rutas/{clave}.md" in texto
    puntos = sum(b["puntos"] for b in curriculo["evaluacion"]["examen"]["bloques"])
    assert puntos == 100
    assert f"**Aprobado:** {curriculo['evaluacion']['examen']['aprobacion']} de 100" in texto


def test_el_diagnostico_tiene_clave_y_encamina(curriculo: dict) -> None:
    texto = (EVAL / "diagnostic.md").read_text(encoding="utf-8")
    preguntas = re.findall(r"^\d+\. ¿|^\d+\. [A-ZÉ]", texto, re.M)
    assert len(preguntas) >= 10, "el diagnóstico debería tener al menos diez preguntas"
    assert "Clave de corrección" in texto
    # Sin encaminar, un diagnóstico solo sirve para desanimar.
    assert "Por dónde empezar" in texto
    assert "../rutas/README.md" in texto


def test_las_evidencias_cubren_todos_los_laboratorios(curriculo: dict) -> None:
    texto = (EVAL / "evidencias.md").read_text(encoding="utf-8")
    for lab in curriculo["laboratorios"]:
        assert lab["ruta"] in texto, f"el laboratorio {lab['id']} no aparece en evidencias.md"


def test_el_proyecto_final_declara_fases_y_defensa() -> None:
    texto = (PROY / "capstone.md").read_text(encoding="utf-8")
    assert "Definición de terminado" in texto
    assert "La defensa" in texto
    assert "../assessments/rubric.md" in texto
    # Una fase sin entregable es una intención.
    fases = re.findall(r"^\| \d+ \| ", texto, re.M)
    assert len(fases) >= 8, "el proyecto final debería declarar sus fases con entregable"


def test_los_dominios_declaran_su_invariante() -> None:
    texto = (PROY / "canonical-domains.md").read_text(encoding="utf-8")
    dominios = re.findall(r"^## \d+\. ", texto, re.M)
    assert len(dominios) == 5
    assert texto.count("**Invariante que no puede romperse:**") == 5
    assert texto.count("**Dificultad real:**") == 5


def test_el_sitio_publica_la_evaluacion_y_los_proyectos() -> None:
    for pagina in ["docs/evaluacion.html", "docs/rubrica.html", "docs/examen-por-rol.html",
                   "docs/evidencias.html", "docs/proyectos.html", "docs/portafolio.html",
                   "docs/diagnostico.html", "docs/proyecto-final.html", "docs/dominios.html"]:
        ruta = RAIZ / "site" / pagina
        assert ruta.exists(), f"falta {pagina}"
        assert ruta.stat().st_size > 2000


def test_el_validador_detecta_una_rubrica_descuadrada(repo: Path) -> None:
    import yaml

    curriculo = yaml.safe_load((repo / "curriculum.yaml").read_text(encoding="utf-8"))
    curriculo["evaluacion"]["dimensiones"][0]["peso"] += 5
    (repo / "curriculum.yaml").write_text(
        yaml.safe_dump(curriculo, allow_unicode=True, sort_keys=False), encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "los pesos de la rubrica suman 105" in resultado.stderr


def test_el_validador_detecta_una_dimension_sin_nivel(repo: Path) -> None:
    import yaml

    curriculo = yaml.safe_load((repo / "curriculum.yaml").read_text(encoding="utf-8"))
    del curriculo["evaluacion"]["dimensiones"][1]["niveles"][4]
    (repo / "curriculum.yaml").write_text(
        yaml.safe_dump(curriculo, allow_unicode=True, sort_keys=False), encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "no describe los cuatro niveles" in resultado.stderr


def test_el_validador_detecta_un_examen_que_no_suma(repo: Path) -> None:
    import yaml

    curriculo = yaml.safe_load((repo / "curriculum.yaml").read_text(encoding="utf-8"))
    curriculo["evaluacion"]["examen"]["bloques"][0]["puntos"] = 40
    (repo / "curriculum.yaml").write_text(
        yaml.safe_dump(curriculo, allow_unicode=True, sort_keys=False), encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "bloques del examen suman" in resultado.stderr
