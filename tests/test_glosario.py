"""El glosario y la pauta pedagógica, comprobados rompiéndolos a propósito.

Dos afirmaciones sostienen esta capa del repositorio:

    ningún concepto se usa sin estar definido en el glosario;
    ninguna clase se publica sin explicación ni prerrequisitos declarados.

Ver pasar al validador sobre un repositorio sano no demuestra que las haga
cumplir. Aquí se le quita una definición, se le añade una de más, se le rompe
una remisión y se le vacía un resumen, y se comprueba que en los cuatro casos
se da cuenta.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from conftest import escribir_curriculo, leer_curriculo, primera_clase, validar

RAIZ = Path(__file__).resolve().parents[1]


def leer_glosario(raiz: Path) -> dict:
    return json.loads((raiz / "catalog" / "glosario.json").read_text(encoding="utf-8"))


def escribir_glosario(raiz: Path, glosario: dict) -> None:
    (raiz / "catalog" / "glosario.json").write_text(
        json.dumps(glosario, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Cobertura: el glosario y el curriculo se cubren exactamente
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="module")
def curriculo() -> dict:
    return leer_curriculo(RAIZ)


@pytest.fixture(scope="module")
def glosario() -> dict:
    return leer_glosario(RAIZ)


def test_todo_concepto_del_curriculo_esta_definido(curriculo: dict, glosario: dict) -> None:
    conceptos = {c for p in curriculo["parts"] for cl in p["classes"] for c in cl["concepts"]}
    definidos = {t["termino"] for t in glosario["terms"]}
    assert not conceptos - definidos, (
        f"conceptos sin definición: {sorted(conceptos - definidos)}")


def test_toda_definicion_corresponde_a_un_concepto(curriculo: dict, glosario: dict) -> None:
    conceptos = {c for p in curriculo["parts"] for cl in p["classes"] for c in cl["concepts"]}
    definidos = {t["termino"] for t in glosario["terms"]}
    assert not definidos - conceptos, (
        f"definiciones que ninguna clase declara: {sorted(definidos - conceptos)}")


def test_las_remisiones_no_apuntan_al_vacio(glosario: dict) -> None:
    definidos = {t["termino"] for t in glosario["terms"]}
    colgadas = {(t["termino"], v) for t in glosario["terms"]
                for v in t["ver_tambien"] if v not in definidos}
    assert not colgadas, f"remisiones rotas: {sorted(colgadas)}"


def test_cada_termino_se_define_en_una_clase_que_lo_declara(
        curriculo: dict, glosario: dict) -> None:
    declarado: dict[str, set[str]] = {}
    for parte in curriculo["parts"]:
        for clase in parte["classes"]:
            for concepto in clase["concepts"]:
                declarado.setdefault(concepto, set()).add(clase["id"])
    descolocados = [(t["termino"], t["clase"]) for t in glosario["terms"]
                    if t["clase"] not in declarado.get(t["termino"], set())]
    assert not descolocados, f"términos definidos en una clase que no los declara: {descolocados}"


def test_el_glosario_publicado_contiene_todos_los_terminos(glosario: dict) -> None:
    publicado = (RAIZ / "GLOSARIO.md").read_text(encoding="utf-8")
    titulos = set(re.findall(r"^### (.+)$", publicado, flags=re.MULTILINE))
    esperados = {t["termino"] for t in glosario["terms"]}
    assert titulos == esperados, (
        "GLOSARIO.md está desincronizado; ejecuta `python scripts/build_classes.py`")


# --------------------------------------------------------------------------- #
# Pauta pedagogica: resumen, prerrequisitos e introduccion de parte
# --------------------------------------------------------------------------- #

def test_toda_clase_tiene_resumen_y_prerrequisitos(curriculo: dict) -> None:
    for parte in curriculo["parts"]:
        for clase in parte["classes"]:
            assert clase.get("resumen"), f"clase {clase['id']}: sin resumen"
            assert "prerrequisitos" in clase, f"clase {clase['id']}: sin prerrequisitos"


def test_los_prerrequisitos_siempre_apuntan_hacia_atras(curriculo: dict) -> None:
    orden = [c["id"] for p in curriculo["parts"] for c in p["classes"]]
    posicion = {cid: i for i, cid in enumerate(orden)}
    for parte in curriculo["parts"]:
        for clase in parte["classes"]:
            for previa in clase["prerrequisitos"]:
                assert posicion[previa] < posicion[clase["id"]], (
                    f"clase {clase['id']}: el prerrequisito {previa} no la precede")


def test_toda_parte_tiene_introduccion_resultados_y_errores(curriculo: dict) -> None:
    for parte in curriculo["parts"]:
        assert len(parte.get("introduccion") or []) >= 2, f"parte {parte['id']}"
        assert len(parte.get("resultados") or []) >= 3, f"parte {parte['id']}"
        assert len(parte.get("errores") or []) >= 3, f"parte {parte['id']}"


def test_la_portada_de_cada_parte_explica_todas_sus_clases(curriculo: dict) -> None:
    for parte in curriculo["parts"]:
        portada = (RAIZ / "classes" / f"part-{parte['id']}-{parte['slug']}"
                   / "README.md").read_text(encoding="utf-8")
        for clase in parte["classes"]:
            assert clase["resumen"] in portada, (
                f"la portada de la parte {parte['id']} no explica la clase {clase['id']}")
        for seccion in ("## De qué trata esta parte", "## Al terminar esta parte podrás",
                        "## Las clases, una por una", "## Errores frecuentes en esta parte",
                        "## Vocabulario de la parte", "## Fuentes usadas en esta parte"):
            assert seccion in portada, f"parte {parte['id']}: falta {seccion!r}"


def test_cada_clase_publica_su_vocabulario(curriculo: dict, glosario: dict) -> None:
    # La definición viaja dentro de una celda de tabla, así que la barra vertical
    # —que aparece de verdad: `{t | ¬P(t)}` es notación de conjuntos— va escapada.
    definiciones = {t["termino"]: t["definicion"].replace("|", "\\|")
                    for t in glosario["terms"]}
    for parte in curriculo["parts"]:
        for clase in parte["classes"]:
            readme = (RAIZ / "classes" / f"part-{parte['id']}-{parte['slug']}"
                      / f"{clase['id']}-{clase['slug']}" / "README.md").read_text(
                          encoding="utf-8")
            assert "## Vocabulario de la clase" in readme, f"clase {clase['id']}"
            assert "## Antes de empezar" in readme, f"clase {clase['id']}"
            for concepto in clase["concepts"]:
                assert definiciones[concepto] in readme, (
                    f"clase {clase['id']}: falta la definición de {concepto!r}")


# --------------------------------------------------------------------------- #
# El validador tiene que darse cuenta cuando esto se rompe
# --------------------------------------------------------------------------- #

def test_el_validador_detecta_un_concepto_sin_definicion(repo: Path) -> None:
    glosario = leer_glosario(repo)
    huerfano = glosario["terms"].pop(0)["termino"]
    escribir_glosario(repo, glosario)
    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "concepto sin entrada" in resultado.stderr
    assert huerfano in resultado.stderr


def test_el_validador_detecta_una_definicion_sin_concepto(repo: Path) -> None:
    glosario = leer_glosario(repo)
    glosario["terms"].append({
        "termino": "concepto inventado",
        "clase": "001",
        "fuente": "codd-1970",
        "definicion": "Una definición larga y perfectamente redactada de algo que "
                      "ninguna clase del programa declara entre sus conceptos.",
        "ver_tambien": [],
    })
    escribir_glosario(repo, glosario)
    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "concepto inventado" in resultado.stderr


def test_el_validador_detecta_una_remision_rota(repo: Path) -> None:
    glosario = leer_glosario(repo)
    glosario["terms"][0]["ver_tambien"] = ["termino que no existe"]
    escribir_glosario(repo, glosario)
    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "termino que no existe" in resultado.stderr


def test_el_validador_detecta_una_clase_sin_resumen(repo: Path) -> None:
    curriculo = leer_curriculo(repo)
    primera_clase(curriculo)["resumen"] = "Corto."
    escribir_curriculo(repo, curriculo)
    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "resumen de" in resultado.stderr


def test_el_validador_detecta_un_prerrequisito_circular(repo: Path) -> None:
    curriculo = leer_curriculo(repo)
    curriculo["parts"][0]["classes"][1]["prerrequisitos"] = ["074"]
    escribir_curriculo(repo, curriculo)
    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "no la precede" in resultado.stderr


def test_el_validador_detecta_una_parte_sin_introduccion(repo: Path) -> None:
    curriculo = leer_curriculo(repo)
    curriculo["parts"][0]["introduccion"] = ["Un solo párrafo."]
    escribir_curriculo(repo, curriculo)
    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "introduccion de 1 parrafos" in resultado.stderr
