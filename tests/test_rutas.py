"""Las rutas por rol: que prometan un recorrido que existe.

Una ruta es una promesa —«haz estas partes en este orden y podrás demostrar
esto»— y las promesas envejecen solas: una clase se renombra, una parte cambia
de horas, un laboratorio deja de ser ejecutable. Estas pruebas obligan a que la
promesa siga siendo verdad.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from conftest import leer_curriculo, validar

RAIZ = Path(__file__).resolve().parents[1]
SITE = RAIZ / "site"


@pytest.fixture(scope="module")
def curriculo() -> dict:
    return leer_curriculo(RAIZ)


def rutas(curriculo: dict) -> list[tuple[str, dict]]:
    return list(curriculo["rutas"].items())


def test_hay_una_guia_por_ruta(curriculo: dict) -> None:
    for clave, ruta in rutas(curriculo):
        guia = RAIZ / ruta["guia"]
        assert guia.exists(), f"{clave}: falta {ruta['guia']}"
        assert guia.name == f"{clave}.md", f"{clave}: la guia no se llama como la ruta"


def test_la_guia_declara_las_horas_que_suman_sus_partes(curriculo: dict) -> None:
    horas_parte = {p["id"]: sum(c["hours"] for c in p["classes"]) for p in curriculo["parts"]}
    for clave, ruta in rutas(curriculo):
        horas = sum(horas_parte[pid] for pid in ruta["partes"])
        texto = (RAIZ / ruta["guia"]).read_text(encoding="utf-8")
        assert f"{horas} horas" in texto, (
            f"{clave}: la guia no dice las {horas} horas que suman sus partes")


def test_la_guia_enlaza_sus_clases_clave(curriculo: dict) -> None:
    for clave, ruta in rutas(curriculo):
        texto = (RAIZ / ruta["guia"]).read_text(encoding="utf-8")
        for cid in ruta["clases_clave"]:
            assert re.search(rf"/{cid}-[a-z0-9-]+/README\.md", texto), (
                f"{clave}: la clase clave {cid} no se enlaza en la guia")


def test_la_guia_enlaza_sus_laboratorios(curriculo: dict) -> None:
    por_id = {lab["id"]: lab for lab in curriculo["laboratorios"]}
    for clave, ruta in rutas(curriculo):
        texto = (RAIZ / ruta["guia"]).read_text(encoding="utf-8")
        for lid in ruta["laboratorios"]:
            assert por_id[lid]["ruta"] in texto, (
                f"{clave}: el laboratorio {lid} no aparece en la guia")


def test_toda_ruta_declara_cargos_y_nivel(curriculo: dict) -> None:
    for clave, ruta in rutas(curriculo):
        assert ruta["cargos"], f"{clave}: sin cargos declarados"
        assert ruta["nivel"] in {"entrada", "intermedio", "avanzado"}
        assert ruta["foco"].strip(), f"{clave}: sin foco"


def test_toda_ruta_empieza_por_los_fundamentos_y_termina_en_el_proyecto(curriculo: dict) -> None:
    """La primera parte es el cimiento y la ultima el cierre: nadie puede saltárselos.

    Los identificadores no se escriben a mano: se leen del curriculo. Asi, el
    dia que se inserte una parte nueva al principio —como ocurrio con los
    primeros pasos— la prueba sigue comprobando lo que quiere comprobar.
    """
    primera = curriculo["parts"][0]["id"]
    ultima = curriculo["parts"][-1]["id"]
    for clave, ruta in rutas(curriculo):
        assert primera in ruta["partes"], f"{clave}: no incluye los fundamentos"
        assert ultima in ruta["partes"], f"{clave}: no termina en el proyecto final"


def test_las_rutas_cubren_todas_las_partes(curriculo: dict) -> None:
    """Una parte que ninguna ruta recorre es material que nadie sabe cuándo estudiar."""
    cubiertas = {pid for r in curriculo["rutas"].values() for pid in r["partes"]}
    todas = {p["id"] for p in curriculo["parts"]}
    assert cubiertas == todas, f"partes fuera de toda ruta: {sorted(todas - cubiertas)}"


def test_cada_ruta_tiene_su_pagina_en_el_sitio(curriculo: dict) -> None:
    assert (SITE / "rutas" / "index.html").exists()
    assert (SITE / "rutas" / "guia.html").exists()
    for clave, ruta in rutas(curriculo):
        pagina = SITE / "rutas" / f"{clave}.html"
        assert pagina.exists(), f"falta la página de la ruta {clave}"
        html = pagina.read_text(encoding="utf-8")
        assert ruta["titulo"] in html
        # Las guías enlazan clases del repositorio; en el sitio deben apuntar a
        # la página de la clase, no al `.md` que el navegador descargaría.
        assert "README.md" not in html, f"{clave}: quedó un enlace al repositorio sin traducir"
        for cid in ruta["clases_clave"]:
            assert f"../classes/{cid}.html" in html, (
                f"{clave}: la página no enlaza la clase clave {cid}")


def test_el_indice_del_sitio_lista_las_siete_rutas(curriculo: dict) -> None:
    html = (SITE / "rutas" / "index.html").read_text(encoding="utf-8")
    for clave, ruta in rutas(curriculo):
        assert f'href="{clave}.html"' in html
        assert ruta["titulo"] in html
    for sid in {s for r in curriculo["rutas"].values() for s in r["fuentes"]}:
        assert f"../fuentes.html#src-{sid}" in html, f"la fuente {sid} no se enlaza"


def test_la_portada_enlaza_las_rutas(curriculo: dict) -> None:
    html = (SITE / "index.html").read_text(encoding="utf-8")
    for clave in curriculo["rutas"]:
        assert f'href="rutas/{clave}.html"' in html


def test_el_validador_detecta_una_ruta_rota(repo: Path) -> None:
    """Prueba en rojo: si una ruta apunta a una clase que no existe, tiene que fallar."""
    import yaml

    curriculo = yaml.safe_load((repo / "curriculum.yaml").read_text(encoding="utf-8"))
    curriculo["rutas"]["arquitectura"]["clases_clave"].append("999")
    (repo / "curriculum.yaml").write_text(
        yaml.safe_dump(curriculo, allow_unicode=True, sort_keys=False), encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "la clase clave 999 no existe" in resultado.stderr


def test_el_validador_detecta_una_guia_ausente(repo: Path) -> None:
    (repo / "rutas" / "arquitectura.md").unlink()

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "falta la guia" in resultado.stderr


def test_el_validador_detecta_horas_desincronizadas(repo: Path) -> None:
    """Si las horas de una parte cambian, la guía que las declara debe fallar."""
    import yaml

    curriculo = yaml.safe_load((repo / "curriculum.yaml").read_text(encoding="utf-8"))
    curriculo["parts"][0]["classes"][0]["hours"] += 1
    (repo / "curriculum.yaml").write_text(
        yaml.safe_dump(curriculo, allow_unicode=True, sort_keys=False), encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "horas que suman sus partes" in resultado.stderr
