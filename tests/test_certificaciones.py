"""El mapeo de certificaciones: que el porcentaje publicado se pueda recalcular.

Un número de cobertura es una afirmación como cualquier otra del repositorio.
Aquí se comprueba que sale de la cuenta declarada, que los pesos son los
oficiales del temario y que cada dominio marcado como cubierto nombra las
clases que lo cubren.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

from conftest import ejecutar, leer_curriculo, validar

RAIZ = Path(__file__).resolve().parents[1]
CERTS = RAIZ / "certificaciones"
sys.path.insert(0, str(RAIZ / "scripts"))

import generar_certificaciones as generador  # noqa: E402


@pytest.fixture(scope="module")
def mapeo() -> dict:
    return json.loads((CERTS / "_mapeo.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def curriculo() -> dict:
    return leer_curriculo(RAIZ)


def test_las_fichas_estan_al_dia() -> None:
    resultado = ejecutar("scripts/generar_certificaciones.py", "--check")
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
    assert "CERTS_OK" in resultado.stdout


def test_la_cobertura_publicada_es_la_calculada(mapeo: dict) -> None:
    """El porcentaje de la ficha tiene que coincidir con el de la fórmula."""
    for cert in mapeo["certificaciones"]:
        esperado = generador.cobertura_total(cert)
        texto = (CERTS / f"{cert['id']}.md").read_text(encoding="utf-8")
        publicado = re.search(r"## 📊 Cobertura del programa: (\d+) %", texto)
        assert publicado, f"{cert['id']}: la ficha no publica su cobertura"
        assert int(publicado.group(1)) == round(esperado), (
            f"{cert['id']}: publica {publicado.group(1)} % y la cuenta da {esperado:.1f} %")


def test_la_cobertura_por_subareas_es_una_proporcion(mapeo: dict) -> None:
    for cert in mapeo["certificaciones"]:
        if cert["metodo"] != "subareas":
            continue
        for dominio in cert["dominios"]:
            cubiertas = sum(1 for s in dominio["subareas"] if s["cubierto"])
            esperado = 100.0 * cubiertas / len(dominio["subareas"])
            assert generador.cobertura_dominio(dominio, "subareas") == esperado


def test_los_pesos_salen_del_temario_oficial(mapeo: dict) -> None:
    """Cada peso numérico debe corresponder al rango oficial que declara la ficha."""
    for cert in mapeo["certificaciones"]:
        assert cert["pesos_oficiales"] is True
        for dominio in cert["dominios"]:
            oficial = dominio["peso_oficial"].replace("%", "").strip()
            if "–" in oficial or "-" in oficial:
                bajo, alto = re.split(r"[–-]", oficial)
                medio = (float(bajo) + float(alto)) / 2
                assert dominio["peso"] == medio, (
                    f"{cert['id']}: {dominio['nombre']} debería usar el punto medio {medio}")
            else:
                assert dominio["peso"] == float(oficial)


def test_toda_clase_citada_existe(mapeo: dict, curriculo: dict) -> None:
    ids = {c["id"] for p in curriculo["parts"] for c in p["classes"]}
    for cert in mapeo["certificaciones"]:
        for dominio in cert["dominios"]:
            citadas = [c for s in dominio.get("subareas", []) for c in s["clases"]]
            citadas += dominio.get("clases", [])
            for cid in citadas:
                assert cid in ids, f"{cert['id']}: la clase {cid} no existe"


def test_lo_no_cubierto_se_declara(mapeo: dict) -> None:
    """La brecha es la parte útil: ninguna ficha puede omitirla."""
    for cert in mapeo["certificaciones"]:
        assert cert["brecha"].strip(), f"{cert['id']}: sin brecha declarada"
        texto = (CERTS / f"{cert['id']}.md").read_text(encoding="utf-8")
        assert "La brecha, y cómo cerrarla" in texto
        assert cert["temario_vigente"] in texto, f"{cert['id']}: la ficha no fecha el temario"


def test_las_no_mapeadas_explican_por_que(mapeo: dict) -> None:
    assert mapeo["sin_mapeo"], "si no hay certificaciones fuera del mapeo, sospecha"
    indice = (CERTS / "README.md").read_text(encoding="utf-8")
    for item in mapeo["sin_mapeo"]:
        assert item["motivo"].strip()
        assert item["nombre"] in indice


def test_cada_ficha_tiene_pagina_en_el_sitio(mapeo: dict) -> None:
    assert (RAIZ / "site" / "certificaciones" / "index.html").exists()
    for cert in mapeo["certificaciones"]:
        pagina = RAIZ / "site" / "certificaciones" / f"{cert['id']}.html"
        assert pagina.exists(), f"falta la página de {cert['id']}"
        html = pagina.read_text(encoding="utf-8")
        assert cert["codigo"] in html
        assert "README.md" not in html, f"{cert['id']}: enlace al repositorio sin traducir"


def test_el_validador_detecta_una_clase_inexistente_en_el_mapeo(repo: Path) -> None:
    ruta = repo / "certificaciones" / "_mapeo.json"
    mapeo = json.loads(ruta.read_text(encoding="utf-8"))
    mapeo["certificaciones"][0]["dominios"][0]["subareas"][1]["clases"].append("999")
    ruta.write_text(json.dumps(mapeo, ensure_ascii=False, indent=2), encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "la clase 999 no existe" in resultado.stderr


def test_el_validador_detecta_una_subarea_cubierta_sin_clases(repo: Path) -> None:
    ruta = repo / "certificaciones" / "_mapeo.json"
    mapeo = json.loads(ruta.read_text(encoding="utf-8"))
    subarea = mapeo["certificaciones"][0]["dominios"][0]["subareas"][1]
    subarea["clases"] = []
    ruta.write_text(json.dumps(mapeo, ensure_ascii=False, indent=2), encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "sin decir por que clases" in resultado.stderr


def test_el_validador_detecta_pesos_que_no_suman(repo: Path) -> None:
    ruta = repo / "certificaciones" / "_mapeo.json"
    mapeo = json.loads(ruta.read_text(encoding="utf-8"))
    mapeo["certificaciones"][0]["dominios"] = mapeo["certificaciones"][0]["dominios"][:2]
    ruta.write_text(json.dumps(mapeo, ensure_ascii=False, indent=2), encoding="utf-8")

    resultado = validar(repo)
    assert resultado.returncode == 1
    assert "falta o sobra un dominio" in resultado.stderr
