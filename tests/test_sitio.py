"""El sitio publicado: lo que tiene que estar y lo que no puede faltar.

Un sitio a medias se publica igual de bien que uno completo. Estas pruebas
comprueban las piezas que ningun navegador reclama en voz alta —manifiesto,
service worker, sitemap, etiquetas sociales, iconos— y que por eso se caen sin
que nadie lo note.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from conftest import ejecutar, leer_curriculo

RAIZ = Path(__file__).resolve().parents[1]
SITE = RAIZ / "site"
BASE = "https://vladimiracunadev-create.github.io/database-systems-labs/"


@pytest.fixture(scope="module")
def curriculo() -> dict:
    return leer_curriculo(RAIZ)


def paginas() -> list[Path]:
    return sorted(SITE.rglob("*.html"))


def test_hay_una_pagina_por_clase(curriculo: dict) -> None:
    total = sum(len(p["classes"]) for p in curriculo["parts"])
    assert len(list((SITE / "classes").glob("[0-9][0-9][0-9].html"))) == total
    assert len(json.loads((SITE / "busqueda.json").read_text(encoding="utf-8"))) == total


@pytest.mark.parametrize("archivo", [
    "index.html", "laboratorios.html", "autoevaluacion.html", "fuentes.html",
    "motores.html", "404.html", "docs/index.html",
    "manifest.webmanifest", "service-worker.js", "sitemap.xml", "robots.txt",
    "assets/icon.svg", "assets/icon-192.png", "assets/icon-512.png", "assets/og-cover.png",
    "assets/styles.css", "assets/class.css", "assets/comun.js", "assets/app.js",
    "assets/class.js", ".nojekyll",
])
def test_el_archivo_existe(archivo: str) -> None:
    ruta = SITE / archivo
    assert ruta.exists(), f"falta {archivo}"
    if ruta.name != ".nojekyll":
        assert ruta.stat().st_size > 0, f"{archivo} está vacío"


def test_toda_pagina_trae_las_etiquetas_que_la_hacen_compartible() -> None:
    for pagina in paginas():
        html = pagina.read_text(encoding="utf-8")
        nombre = pagina.relative_to(SITE)
        for etiqueta in ('<meta charset="utf-8">',
                         'name="viewport"',
                         'name="description"',
                         'rel="canonical"',
                         'property="og:title"',
                         'property="og:image"',
                         'name="twitter:card"',
                         'rel="manifest"',
                         'rel="apple-touch-icon"'):
            assert etiqueta in html, f"{nombre}: falta {etiqueta}"
        assert "<title>" in html, f"{nombre}: sin título"


def test_toda_pagina_es_navegable_y_accesible() -> None:
    for pagina in paginas():
        html = pagina.read_text(encoding="utf-8")
        nombre = pagina.relative_to(SITE)
        assert 'class="saltar"' in html, f"{nombre}: sin enlace para saltar al contenido"
        assert 'id="principal"' in html, f"{nombre}: el enlace de salto no tiene destino"
        assert 'id="tema"' in html, f"{nombre}: sin conmutador de tema"
        assert '<html lang="es">' in html, f"{nombre}: sin idioma declarado"
        assert "assets/comun.js" in html, f"{nombre}: sin el guion comun"


def test_ningun_enlace_interno_apunta_al_vacio() -> None:
    """Cada href relativo del sitio tiene que resolver a un archivo existente."""
    rotos: list[str] = []
    for pagina in paginas():
        html = pagina.read_text(encoding="utf-8")
        for destino in re.findall(r'href="([^"]+)"', html):
            if destino.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            limpio = destino.split("#", 1)[0]
            if not limpio:
                continue
            if not (pagina.parent / limpio).resolve().exists():
                rotos.append(f"{pagina.relative_to(SITE)} -> {destino}")
    assert not rotos, "enlaces internos rotos: " + ", ".join(rotos[:10])


def test_el_sitemap_cubre_las_paginas_publicadas() -> None:
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap))
    # La 404 no se indexa; todo lo demas si.
    esperadas = {
        BASE + ("" if str(p.relative_to(SITE)) == "index.html"
                else str(p.relative_to(SITE)).replace("\\", "/"))
        for p in paginas() if p.name != "404.html"
    }
    assert urls == esperadas
    assert BASE + "sitemap.xml" in (SITE / "robots.txt").read_text(encoding="utf-8")


def test_el_manifiesto_declara_los_iconos_que_existen() -> None:
    manifiesto = json.loads((SITE / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert manifiesto["start_url"] and manifiesto["display"] == "standalone"
    assert manifiesto["lang"] == "es"
    for icono in manifiesto["icons"]:
        assert (SITE / icono["src"]).exists(), f"el manifiesto declara {icono['src']}"


def test_el_service_worker_cachea_lo_esencial() -> None:
    sw = (SITE / "service-worker.js").read_text(encoding="utf-8")
    rutas = json.loads(re.search(r"const ESENCIALES = (\[.*?\]);", sw, re.S).group(1))
    for ruta in rutas:
        if ruta == "./":
            continue
        assert (SITE / ruta.removeprefix("./")).exists(), f"el service worker cachea {ruta}"
    # La version sale del contenido: sin ella, el navegador serviria material viejo.
    assert re.search(r'const CACHE = "database-systems-labs-[0-9a-f]{12}"', sw)


def test_los_iconos_son_png_validos() -> None:
    for nombre, lado in [("icon-192.png", 192), ("icon-512.png", 512)]:
        datos = (SITE / "assets" / nombre).read_bytes()
        assert datos[:8] == b"\x89PNG\r\n\x1a\n", f"{nombre} no es un PNG"
        ancho = int.from_bytes(datos[16:20], "big")
        alto = int.from_bytes(datos[20:24], "big")
        assert (ancho, alto) == (lado, lado), f"{nombre} mide {ancho}x{alto}"

    portada = (SITE / "assets" / "og-cover.png").read_bytes()
    assert (int.from_bytes(portada[16:20], "big"),
            int.from_bytes(portada[20:24], "big")) == (1200, 630)


def test_la_marca_grafica_es_reproducible() -> None:
    """Dos dibujos del mismo icono deben dar el mismo archivo, byte a byte."""
    import sys
    sys.path.insert(0, str(RAIZ / "scripts"))
    import brand_assets

    assert brand_assets.icono(64) == brand_assets.icono(64)
    assert brand_assets.icono(64) != brand_assets.icono(128)


def test_la_pagina_de_laboratorios_los_cubre_todos(curriculo: dict) -> None:
    html = (SITE / "laboratorios.html").read_text(encoding="utf-8")
    for lab in curriculo["laboratorios"]:
        assert lab["titulo"] in html, f"el laboratorio {lab['id']} no aparece en el sitio"
        if lab["comando"]:
            assert lab["comando"] in html, f"falta el comando del laboratorio {lab['id']}"
            assert lab["marca"] in html
        for sid in lab["fuentes"]:
            assert f"fuentes.html#src-{sid}" in html, (
                f"el laboratorio {lab['id']} cita {sid} sin enlazar su ficha")


def test_la_autoevaluacion_recoge_las_preguntas_de_cada_clase(curriculo: dict) -> None:
    html = (SITE / "autoevaluacion.html").read_text(encoding="utf-8")
    preguntas = html.count("<li>")
    total_clases = sum(len(p["classes"]) for p in curriculo["parts"])
    # Cuatro preguntas por clase es el minimo que exige el modelo pedagogico.
    assert preguntas >= total_clases * 4, f"solo {preguntas} preguntas publicadas"
    assert f"classes/{curriculo['parts'][0]['classes'][0]['id']}.html" in html


def test_cada_documento_del_repositorio_publicado_tiene_su_pagina() -> None:
    generador = (RAIZ / "scripts" / "generate_site.py").read_text(encoding="utf-8")
    documentos = re.findall(r'\("([^"]+\.md)", "(docs/[^"]+\.html)"', generador)
    assert len(documentos) >= 10
    for origen, destino in documentos:
        assert (RAIZ / origen).exists(), f"{origen} no existe pero se publica"
        assert (SITE / destino).exists(), f"{destino} no se genero"


def test_la_portada_declara_datos_estructurados() -> None:
    html = (SITE / "index.html").read_text(encoding="utf-8")
    bruto = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    datos = json.loads(bruto.group(1))
    assert datos["@type"] == "Course"
    assert datos["isAccessibleForFree"] is True
    assert datos["url"] == BASE


def test_el_sitio_no_quedo_desactualizado() -> None:
    resultado = ejecutar("scripts/generate_site.py", "--check")
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
