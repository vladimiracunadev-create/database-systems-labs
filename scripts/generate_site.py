"""Genera el sitio estatico publicado en GitHub Pages.

Entrada:  curriculum.yaml · classes/**/README.md · classes/**/lesson.md
          catalog/*.json · docs/*.md · los documentos de la raiz
Salida:   site/ (portada, una pagina por clase y por parte, laboratorios,
          autoevaluacion, fuentes, motores, documentacion, 404, indice de
          busqueda, manifiesto, service worker, sitemap, robots e iconos)

Todo site/ es un artefacto derivado: se regenera entero en cada ejecucion y CI
comprueba con `--check` que no queda desactualizado. Nada de site/ se edita a
mano, ni siquiera las imagenes: los iconos y la portada social se dibujan en
`scripts/brand_assets.py`, tambien sin dependencias.

Uso:
    python scripts/generate_site.py
    python scripts/generate_site.py --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

import markdown
import yaml

import brand_assets
import motores_lib as ml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CLASSES = ROOT / "classes"

REPO = "https://github.com/vladimiracunadev-create/database-systems-labs"
BASE = "https://vladimiracunadev-create.github.io/database-systems-labs/"

MD_EXT = ["tables", "fenced_code", "sane_lists", "attr_list"]

NIVELES = {"fundamentos": "Fundamentos", "intermedio": "Intermedio", "avanzado": "Avanzado"}

# Barra de navegacion comun a todas las paginas: (clave, texto, destino).
NAV = [
    ("clases", "Clases", "classes/indice.html"),
    ("rutas", "Rutas por rol", "rutas/index.html"),
    ("laboratorios", "Laboratorios", "laboratorios.html"),
    ("certificaciones", "Certificaciones", "certificaciones/index.html"),
    ("autoevaluacion", "Autoevaluación", "autoevaluacion.html"),
    ("fuentes", "Fuentes", "fuentes.html"),
    ("motores", "Motores", "motores.html"),
    ("docs", "Documentación", "docs/index.html"),
]

# Documentos del repositorio que se publican tambien como pagina.
# (origen, destino en el sitio, titulo, para que sirve)
DOCUMENTOS = [
    ("docs/ARCHITECTURE.md", "docs/arquitectura.html", "Arquitectura del repositorio",
     "Qué es fuente y qué es artefacto derivado, y por qué la separación importa."),
    ("docs/LEARNING-MODEL.md", "docs/modelo-pedagogico.html", "Modelo pedagógico",
     "Cómo está construida cada clase y qué se exige para darla por superada."),
    ("docs/SOURCES.md", "docs/politica-de-fuentes.html", "Política de fuentes",
     "La regla que gobierna el repositorio y cómo se hace cumplir."),
    ("docs/DECISION-GUIDE.md", "docs/guia-de-decision.html", "Guía de decisión",
     "Cómo elegir motor y modelo a partir de la carga de trabajo, no de la moda."),
    ("docs/ENVIRONMENTS.md", "docs/entornos.html", "Entornos reproducibles",
     "Cómo levantar cada motor y volver al estado inicial sin residuos."),
    ("docs/SECURITY-AND-ETHICS.md", "docs/seguridad-y-etica.html", "Seguridad y ética",
     "Datos sintéticos, credenciales locales y límites del material."),
    ("labs/README.md", "docs/laboratorios-guia.html", "Guía de los laboratorios",
     "Qué mide cada laboratorio y por qué ninguno afirma nada en milisegundos."),
    ("assessments/README.md", "docs/evaluacion.html", "Cómo se evalúa",
     "Las cinco piezas de la nota y qué cuenta como evidencia."),
    ("assessments/rubric.md", "docs/rubrica.html", "Rúbrica de evaluación",
     "Diez dimensiones con sus cuatro niveles, para que la aplique una tercera persona."),
    ("assessments/examen-por-rol.md", "docs/examen-por-rol.html", "Examen final por rol",
     "Teoría, práctica y defensa para cada una de las siete rutas."),
    ("assessments/evidencias.md", "docs/evidencias.html", "Evidencias de laboratorio",
     "Qué cuenta como evidencia, con plantilla y criterio de corrección."),
    ("projects/README.md", "docs/proyectos.html", "Proyectos",
     "Dónde se junta todo: dominios, proyecto final y portafolio."),
    ("projects/portafolio.md", "docs/portafolio.html", "Portafolio verificable",
     "Cómo convertir la evidencia acumulada en algo que se pueda enseñar."),
    ("assessments/diagnostic.md", "docs/diagnostico.html", "Diagnóstico inicial",
     "Prueba de entrada para situar el punto de partida."),
    ("projects/capstone.md", "docs/proyecto-final.html", "Proyecto final",
     "El encargo integrador y lo que debe demostrar su defensa."),
    ("projects/canonical-domains.md", "docs/dominios.html", "Dominios canónicos",
     "Los dominios sobre los que se trabaja en todo el programa."),
    ("ROADMAP.md", "docs/roadmap.html", "Roadmap",
     "Qué falta, en qué orden y con qué criterio se cierra cada hito."),
    ("CHANGELOG.md", "docs/changelog.html", "Changelog",
     "Qué cambió en cada versión y por qué."),
    ("CONTRIBUTING.md", "docs/contribuir.html", "Contribuir",
     "Cómo proponer material sin romper la coherencia ni la regla de las fuentes."),
    ("SECURITY.md", "docs/seguridad.html", "Política de seguridad",
     "Cómo reportar un problema de seguridad en el material o en los scripts."),
    ("PROMPT_MAESTRO.md", "docs/prompt-maestro.html", "Prompt maestro",
     "El contrato para ampliar el programa con ayuda de un modelo de lenguaje."),
]

MERMAID = """  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
    for (const code of document.querySelectorAll("pre > code.language-mermaid")) {
      const caja = document.createElement("pre");
      caja.className = "mermaid";
      caja.textContent = code.textContent;
      code.parentElement.replaceWith(caja);
    }
    const claro = document.documentElement.dataset.tema === "claro" ||
      (!document.documentElement.dataset.tema &&
       window.matchMedia("(prefers-color-scheme: light)").matches);
    mermaid.initialize({ startOnLoad: true, theme: claro ? "default" : "dark",
                         themeVariables: { fontFamily: "Inter, system-ui, sans-serif" } });
  </script>
"""

# Se aplica antes de pintar para que el tema elegido no parpadee en la carga.
TEMA_INICIAL = ('<script>try{var t=localStorage.getItem("dsl:tema");'
                'if(t)document.documentElement.dataset.tema=t;}catch(e){}</script>')


def escapar(texto: str) -> str:
    return (texto.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace('"', "&quot;"))


def barra(prefijo: str, activo: str) -> str:
    enlaces = "\n".join(
        f'    <a href="{prefijo}{destino}"'
        f'{" aria-current=\"page\"" if clave == activo else ""}>{texto}</a>'
        for clave, texto, destino in NAV)
    return f"""<a class="saltar" href="#principal">Saltar al contenido</a>
<header class="nav">
  <a class="marca" href="{prefijo}index.html">
    <img src="{prefijo}assets/icon.svg" alt="" width="26" height="26">Database Systems Labs</a>
  <nav aria-label="Secciones del programa">
{enlaces}
    <a href="{REPO}" rel="noopener">GitHub</a>
  </nav>
  <button id="tema" class="tema" type="button" aria-label="Cambiar entre tema claro y oscuro">☾</button>
</header>"""


def pie(prefijo: str, programa: dict) -> str:
    return f"""<footer>
  <p><strong>{escapar(programa['nombre'])}</strong> · versión {programa['version']} ·
  licencia {programa['licencia']} · actualizado el {programa['actualizado']}.
  Los productos citados conservan sus licencias y marcas.</p>
  <p>Sin rastreo y sin cuentas: el progreso de lectura se guarda solo en tu navegador.</p>
  <p><a href="{REPO}">Código fuente</a> ·
     <a href="{prefijo}fuentes.html">Bibliografía</a> ·
     <a href="{prefijo}laboratorios.html">Laboratorios</a> ·
     <a href="{prefijo}docs/index.html">Documentación</a> ·
     <a href="{prefijo}classes/indice.html">Todas las clases</a></p>
</footer>"""


def pagina(*, titulo: str, descripcion: str, cuerpo: str, prefijo: str, ruta: str,
           programa: dict, activo: str = "", extra_css: str = "", scripts: str = "",
           jsonld: str = "") -> str:
    """Envuelve el cuerpo en el armazon comun: cabeza, navegacion y pie."""
    datos = f'<script type="application/ld+json">{jsonld}</script>\n' if jsonld else ""
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark light">
<meta name="theme-color" content="#05090f">
<meta name="description" content="{escapar(descripcion)}">
<meta name="author" content="Vladimir Acuña">
<link rel="canonical" href="{BASE}{ruta}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Database Systems Labs">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{escapar(titulo)}">
<meta property="og:description" content="{escapar(descripcion)}">
<meta property="og:url" content="{BASE}{ruta}">
<meta property="og:image" content="{BASE}assets/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}assets/og-cover.png">
<link rel="icon" type="image/svg+xml" href="{prefijo}assets/icon.svg">
<link rel="apple-touch-icon" href="{prefijo}assets/icon-192.png">
<link rel="manifest" href="{prefijo}manifest.webmanifest">
<link rel="stylesheet" href="{prefijo}assets/styles.css">
{extra_css}{TEMA_INICIAL}
{datos}<title>{escapar(titulo)}</title>
</head>
<body>
{barra(prefijo, activo)}
{cuerpo}
{pie(prefijo, programa)}
<script src="{prefijo}assets/comun.js"></script>
{scripts}<script>if("serviceWorker" in navigator)window.addEventListener("load",()=>navigator.serviceWorker.register("{prefijo}service-worker.js"));</script>
</body>
</html>
"""


def ancla(texto: str) -> str:
    """Ancla al estilo de GitHub, para que los enlaces internos del markdown funcionen."""
    limpio = re.sub(r"<[^>]+>", "", texto).strip().lower()
    limpio = "".join(c for c in limpio
                     if c.isalnum() or c in " -_" or unicodedata.category(c).startswith("L"))
    return re.sub(r"\s", "-", limpio.strip())


def render_markdown(texto: str) -> str:
    html = markdown.markdown(texto, extensions=MD_EXT)

    def encabezado(m: re.Match[str]) -> str:
        n, contenido = m.group(1), m.group(2)
        return f'<h{n} id="{ancla(contenido)}">{contenido}</h{n}>'

    html = re.sub(r"<h([1-6])>(.*?)</h\1>", encabezado, html, flags=re.S)
    # Las tablas anchas se desplazan dentro de su caja; la pagina, nunca.
    html = html.replace("<table>", '<div class="tabla-scroll"><table>')
    html = html.replace("</table>", "</table></div>")
    return html


def reescribir_enlaces(texto: str, ruta_clase: str = "") -> str:
    """Convierte los enlaces relativos de un README de clase en enlaces del sitio."""
    # Archivos de la propia carpeta de la clase: `motores.yaml` y las
    # implementaciones por motor. El sitio no los publica —son codigo fuente—,
    # asi que el enlace va al archivo en GitHub, que es donde se leen mejor.
    if ruta_clase:
        texto = re.sub(
            r"\((motores\.yaml|implementaciones/[A-Za-z0-9_\-./]+)\)",
            lambda m: f"({REPO}/blob/main/{ruta_clase}/{m.group(1)})", texto)
    # clase -> clase (el nav superior e inferior de cada README)
    texto = re.sub(r"\((?:\.\./)+(?:classes/)?part-\d{2}-[^/)]+/(\d{3})-[^/)]+/README\.md\)",
                   r"(\1.html)", texto)
    # indice de la parte y del programa
    texto = texto.replace("(../README.md)", "(indice.html)")
    texto = re.sub(r"\((?:\.\./){2,3}README\.md\)", "(../index.html)", texto)
    # catalogo de fuentes
    texto = texto.replace("(../../../catalog/sources.json)", "(../fuentes.html)")
    # cualquier otro archivo del repositorio: al codigo fuente en GitHub
    texto = re.sub(r"\((?:\.\./)+([A-Za-z0-9_\-./]+\.(?:md|py|sql|json|yaml|yml))\)",
                   lambda m: f"({REPO}/blob/main/{m.group(1)})", texto)
    return texto


def enlaces_de_ruta(texto: str, indice: str = "guia.html", base: str = "rutas") -> str:
    """Lleva los enlaces de una guia de rol a sus paginas del sitio.

    Las guias viven en `rutas/` y enlazan al repositorio; el sitio publica las
    mismas piezas en otras direcciones. Lo que no tiene pagina propia se manda
    al archivo en GitHub, para que ningun enlace muera en un `.md` que el
    navegador solo sabria descargar.
    """
    # clase concreta -> pagina de clase
    texto = re.sub(r"\.\./classes/part-\d{2}-[^/)]+/(\d{3})-[^/)]+/README\.md",
                   r"../classes/\1.html", texto)
    # indice de parte -> pagina de parte
    texto = re.sub(r"\.\./classes/part-(\d{2})-[^/)]+/README\.md",
                   r"../classes/parte-\1.html", texto)
    reemplazos = {
        "../classes/README.md": "../classes/indice.html",
        "../labs/README.md": "../laboratorios.html",
        "../catalog/sources.json": "../fuentes.html",
        "../projects/capstone.md": "../docs/proyecto-final.html",
        "../docs/LEARNING-MODEL.md": "../docs/modelo-pedagogico.html",
        "../README.md": "../index.html",
    }
    for viejo, nuevo in reemplazos.items():
        texto = texto.replace(f"]({viejo})", f"]({nuevo})")
    # cualquier laboratorio concreto -> la pagina de laboratorios
    texto = re.sub(r"\]\(\.\./labs/[^)]+\)", "](../laboratorios.html)", texto)
    # el indice de la carpeta se publica con otro nombre
    texto = texto.replace("](README.md)", f"]({indice})")
    # guias de rol enlazadas desde otra carpeta del sitio
    texto = re.sub(r"\]\(\.\./rutas/([a-z0-9-]+)\.md\)", r"](../rutas/\1.html)", texto)
    # guias hermanas
    texto = re.sub(r"\]\((?!https?:|\.\./|#)([a-z0-9-]+)\.md\)", r"](\1.html)", texto)
    # lo que quede apuntando al repositorio, al codigo fuente
    texto = re.sub(r"\]\(\.\./([A-Za-z0-9_\-./]+\.(?:md|py|sql|json|yaml|yml))\)",
                   lambda m: f"]({REPO}/blob/main/{m.group(1)})", texto)
    # y los archivos de la propia carpeta que no tienen pagina (datos, guiones)
    texto = re.sub(r"\]\((?!https?:|\.\./|#)([A-Za-z0-9_\-]+\.(?:json|yaml|yml|py|sql))\)",
                   lambda m: f"]({REPO}/blob/main/{base}/{m.group(1)})", texto)
    return texto


def enlaces_de_documento(texto: str, origen: str, publicados: dict[str, str]) -> str:
    """Reescribe los enlaces de un documento publicado como pagina.

    Si el destino tambien se publica, apunta a su pagina; si no, al archivo en
    GitHub. Asi ningun enlace del sitio termina en un `.md` que el navegador se
    limitaria a descargar.
    """
    carpeta = Path(origen).parent

    def destino(m: re.Match[str]) -> str:
        etiqueta, ruta = m.group(1), m.group(2)
        if ruta.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        limpio, _, fragmento = ruta.partition("#")
        resuelto = str((carpeta / limpio).resolve().relative_to(ROOT)).replace("\\", "/")
        if resuelto in publicados:
            pagina_destino = publicados[resuelto]
            # Todos los documentos publicados viven en site/docs/.
            relativo = pagina_destino.removeprefix("docs/")
            return f"[{etiqueta}]({relativo}{'#' + fragmento if fragmento else ''})"
        return f"[{etiqueta}]({REPO}/blob/main/{resuelto})"

    return re.sub(r"\[([^\]]*)\]\(([^)]+)\)", destino, texto)


def cobertura_cert(cert: dict) -> float:
    """Cobertura ponderada de una certificacion; el calculo vive en un solo sitio."""
    import generar_certificaciones

    return generar_certificaciones.cobertura_total(cert)


def preguntas_de_leccion(texto: str) -> list[str]:
    """Extrae las preguntas de evaluacion de una leccion."""
    bloque = re.search(r"## Preguntas de evaluación\s*(.*?)(?=\n## |\Z)", texto, re.S)
    if not bloque:
        return []
    return [linea.group(1).strip()
            for linea in re.finditer(r"^\d+\.\s+(.*)$", bloque.group(1), re.M)]


# --------------------------------------------------------------------------- #

def construir() -> dict[Path, str | bytes]:
    curriculo = yaml.safe_load((ROOT / "curriculum.yaml").read_text(encoding="utf-8"))
    fuentes = json.loads((ROOT / "catalog" / "sources.json").read_text(encoding="utf-8"))
    motores = json.loads((ROOT / "catalog" / "databases.json").read_text(encoding="utf-8"))
    programa = curriculo["programa"]
    salidas: dict[Path, str | bytes] = {}

    partes = curriculo["parts"]
    plano = [(p, c) for p in partes for c in p["classes"]]
    total_clases = len(plano)
    total_horas = sum(c["hours"] for _, c in plano)
    todos_motores = sorted({m for _, c in plano for m in c["engines"]})
    laboratorios = curriculo["laboratorios"]
    por_fuente = {f["id"]: f for f in fuentes["sources"]}

    def cita(sid: str, prefijo: str) -> str:
        f = por_fuente[sid]
        return (f'<a href="{prefijo}fuentes.html#src-{sid}">{escapar(f["title"])}</a>'
                f' <span class="fuente-meta">({f["year"]})</span>')

    # ---------- paginas de clase ----------
    indice_busqueda = []
    preguntas_por_clase: list[tuple[dict, dict, list[str]]] = []
    for i, (parte, clase) in enumerate(plano):
        carpeta = CLASSES / f"part-{parte['id']}-{parte['slug']}" / f"{clase['id']}-{clase['slug']}"
        md = reescribir_enlaces(
            (carpeta / "README.md").read_text(encoding="utf-8"),
            carpeta.relative_to(ROOT).as_posix())
        leccion = (carpeta / "lesson.md").read_text(encoding="utf-8")
        preguntas_por_clase.append((parte, clase, preguntas_de_leccion(leccion)))

        anterior = plano[i - 1][1] if i > 0 else None
        siguiente = plano[i + 1][1] if i + 1 < len(plano) else None
        pasos = []
        if anterior:
            pasos.append(f'<a class="anterior" href="{anterior["id"]}.html">'
                         f'<span class="sentido">← Anterior · {anterior["id"]}</span>'
                         f'{escapar(anterior["title"])}</a>')
        if siguiente:
            pasos.append(f'<a class="siguiente" href="{siguiente["id"]}.html">'
                         f'<span class="sentido">Siguiente · {siguiente["id"]} →</span>'
                         f'{escapar(siguiente["title"])}</a>')

        cuerpo = f"""<div class="avance" role="presentation"></div>
<nav class="migas" aria-label="Ruta de navegación">
  <a href="../index.html">Inicio</a><span aria-hidden="true">/</span>
  <a href="parte-{parte['id']}.html">Parte {parte['id']} · {escapar(parte['title'])}</a>
  <span aria-hidden="true">/</span><span>Clase {clase['id']}</span>
</nav>
<main class="content" id="principal">
{render_markdown(md)}
<button id="completar" class="completar" type="button" aria-pressed="false"
        data-clase="{clase['id']}">Marcar como completada</button>
<nav class="paso-a-paso" aria-label="Clase anterior y siguiente">
{chr(10).join(pasos)}
</nav>
</main>"""

        jsonld = json.dumps({
            "@context": "https://schema.org",
            "@type": "LearningResource",
            "name": f"{clase['id']} — {clase['title']}",
            "inLanguage": "es",
            "educationalLevel": NIVELES[clase["level"]],
            "timeRequired": f"PT{clase['hours']}H",
            "teaches": clase["concepts"],
            "isPartOf": {"@type": "Course", "name": programa["nombre"], "url": BASE},
            "license": "https://opensource.org/licenses/MIT",
        }, ensure_ascii=False)

        salidas[SITE / "classes" / f"{clase['id']}.html"] = pagina(
            titulo=f"{clase['id']} — {clase['title']} · Database Systems Labs",
            descripcion=f"{clase['title']}. Parte {parte['id']}: {parte['title']}.",
            cuerpo=cuerpo, prefijo="../", ruta=f"classes/{clase['id']}.html",
            programa=programa, activo="clases", jsonld=jsonld,
            extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
            scripts=MERMAID + '  <script src="../assets/class.js"></script>\n')

        texto_plano = re.sub(r"[^\w\s]", " ", md.lower())
        texto_plano = unicodedata.normalize("NFD", texto_plano)
        texto_plano = "".join(c for c in texto_plano if unicodedata.category(c) != "Mn")
        indice_busqueda.append({
            "id": clase["id"],
            "titulo": clase["title"],
            "parte": parte["id"],
            "nivel": clase["level"],
            "url": f"classes/{clase['id']}.html",
            "buscable": re.sub(r"\s+", " ", texto_plano)[:6000],
        })

    salidas[SITE / "busqueda.json"] = json.dumps(indice_busqueda, ensure_ascii=False)

    # ---------- indice por parte ----------
    for parte in partes:
        filas = "\n".join(
            f'<tr><td><a href="{c["id"]}.html">{c["id"]}</a></td>'
            f'<td><a href="{c["id"]}.html">{escapar(c["title"])}</a></td>'
            f'<td class="nivel-{c["level"]}">{NIVELES[c["level"]]}</td>'
            f'<td>{c["hours"]}</td><td>{len(c["sources"])}</td></tr>'
            for c in parte["classes"])
        horas = sum(c["hours"] for c in parte["classes"])
        otras = "\n".join(
            f'<li><a href="parte-{p["id"]}.html">Parte {p["id"]} — {escapar(p["title"])}</a></li>'
            for p in partes if p["id"] != parte["id"])
        cuerpo = f"""<nav class="migas" aria-label="Ruta de navegación">
  <a href="../index.html">Inicio</a><span aria-hidden="true">/</span>
  <span>Parte {parte['id']}</span>
</nav>
<main class="content" id="principal">
<h1>Parte {parte['id']} — {escapar(parte['title'])}</h1>
<p class="lead">{escapar(parte['summary'])}</p>
<p><strong>{len(parte['classes'])} clases · {horas} horas</strong></p>
<div class="tabla-scroll"><table>
<thead><tr><th>#</th><th>Clase</th><th>Nivel</th><th>Horas</th><th>Fuentes</th></tr></thead>
<tbody>
{filas}
</tbody></table></div>
<h2>Otras partes</h2>
<ul>
{otras}
</ul>
</main>"""
        salidas[SITE / "classes" / f"parte-{parte['id']}.html"] = pagina(
            titulo=f"Parte {parte['id']} — {parte['title']} · Database Systems Labs",
            descripcion=parte["summary"], cuerpo=cuerpo, prefijo="../",
            ruta=f"classes/parte-{parte['id']}.html", programa=programa, activo="clases",
            extra_css='<link rel="stylesheet" href="../assets/class.css">\n')

    salidas[SITE / "classes" / "indice.html"] = pagina(
        titulo="Todas las clases · Database Systems Labs",
        descripcion="Índice completo de las clases del programa, parte por parte.",
        prefijo="../", ruta="classes/indice.html", programa=programa, activo="clases",
        extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
        cuerpo="""<nav class="migas" aria-label="Ruta de navegación">
  <a href="../index.html">Inicio</a><span aria-hidden="true">/</span>
  <span>Todas las clases</span></nav>
<main class="content" id="principal"><h1>Todas las clases</h1>
<p class="lead">El catálogo completo, con búsqueda y filtros, está en la
<a href="../index.html">portada</a>.</p>
<ul>""" + "\n".join(
            f'<li><a href="parte-{p["id"]}.html">Parte {p["id"]} — {escapar(p["title"])}</a> '
            f'· {len(p["classes"])} clases</li>' for p in partes) + "</ul></main>")

    # ---------- portada ----------
    bloques = []
    for parte in partes:
        horas = sum(c["hours"] for c in parte["classes"])
        tarjetas = []
        for c in parte["classes"]:
            etiquetas = "".join(f'<span class="tag">{escapar(t)}</span>'
                                for t in c["concepts"][:3])
            tarjetas.append(f"""      <article class="card" data-clase="{c['id']}"
               data-parte="{parte['id']}" data-nivel="{c['level']}"
               data-motores="{','.join(c['engines'])}">
        <div class="meta"><span>{c['id']}</span>
          <span class="nivel-{c['level']}">{NIVELES[c['level']]} · {c['hours']} h</span></div>
        <h3><a href="classes/{c['id']}.html">{escapar(c['title'])}</a></h3>
        <div class="tags">{etiquetas}<span class="tag tag-n">{len(c['sources'])} fuentes</span></div>
      </article>""")
        bloques.append(f"""  <section class="part" data-parte="{parte['id']}">
    <div class="part-head">
      <h2><a href="classes/parte-{parte['id']}.html">Parte {parte['id']} — {escapar(parte['title'])}</a></h2>
      <p>{escapar(parte['summary'])}</p>
      <p class="part-meta">{len(parte['classes'])} clases · {horas} horas</p>
    </div>
    <div class="grid">
{chr(10).join(tarjetas)}
    </div>
  </section>""")

    opciones_parte = "\n".join(
        f'<option value="{p["id"]}">Parte {p["id"]} — {escapar(p["title"])}</option>'
        for p in partes)
    opciones_motor = "\n".join(f'<option value="{m}">{m}</option>' for m in todos_motores)

    horas_parte_portada = {p["id"]: sum(c["hours"] for c in p["classes"]) for p in partes}
    rutas = "\n".join(
        f"""<tr><td><strong><a href="rutas/{clave}.html">{escapar(r['titulo'])}</a></strong><br>
        <span class="fuente-meta">{escapar(r['descripcion'])}</span></td>
        <td>{' · '.join(r['partes'])}</td>
        <td class="nivel-{'fundamentos' if r['nivel'] == 'entrada' else r['nivel']}">{r['nivel']}</td>
        <td>{sum(horas_parte_portada[pid] for pid in r['partes'])} h</td></tr>"""
        for clave, r in curriculo["rutas"].items())

    ejecutables = [lab for lab in laboratorios if lab["comando"]]

    cuerpo = f"""<header class="hero">
  <p class="eyebrow">Programa abierto · {programa['version']}</p>
  <h1>Ingeniería de <span class="gradient">bases de datos</span>, con la fuente de cada afirmación</h1>
  <p class="lead">{escapar(programa['resumen'])}</p>
  <div class="stats">
    <div class="stat"><strong>{total_clases}</strong><span>clases</span></div>
    <div class="stat"><strong>{len(partes)}</strong><span>partes</span></div>
    <div class="stat"><strong>{total_horas}</strong><span>horas estimadas</span></div>
    <div class="stat"><strong>{len(fuentes['sources'])}</strong><span>fuentes verificadas</span></div>
    <div class="stat"><strong>{len(ejecutables)}</strong><span>laboratorios ejecutables</span></div>
    <div class="stat stat-progreso"><strong id="progreso">0/{total_clases}</strong><span>tu progreso</span></div>
  </div>
  <div class="cta">
    <a class="btn btn-primary" href="classes/001.html">Empezar por la clase 001</a>
    <a class="btn btn-ghost" href="rutas/index.html">Elegir ruta por rol</a>
    <a class="btn btn-ghost" href="laboratorios.html">Laboratorios ejecutables</a>
    <a class="btn btn-ghost" href="fuentes.html">Las {len(fuentes['sources'])} fuentes</a>
    <a class="btn btn-ghost" href="{REPO}" rel="noopener">Repositorio</a>
  </div>
</header>

<div class="controls">
  <input id="q" type="search" placeholder="Buscar en las {total_clases} clases…  (pulsa / )"
         autocomplete="off" aria-label="Buscar en las clases">
  <select id="parte" aria-label="Filtrar por parte"><option value="">Todas las partes</option>
{opciones_parte}
  </select>
  <select id="nivel" aria-label="Filtrar por nivel"><option value="">Todos los niveles</option>
    <option value="fundamentos">Fundamentos</option>
    <option value="intermedio">Intermedio</option>
    <option value="avanzado">Avanzado</option>
  </select>
  <select id="motor" aria-label="Filtrar por motor"><option value="">Todos los motores</option>
{opciones_motor}
  </select>
  <label class="interruptor">
    <input type="checkbox" id="pendientes"> solo pendientes</label>
</div>
<p class="contador" id="contador">{total_clases} clases</p>

<main id="principal">
{chr(10).join(bloques)}
  <p class="vacio hidden" id="vacio">Ninguna clase coincide con el filtro.</p>

  <section class="seccion">
    <h2>Rutas por rol</h2>
    <p>El mismo programa recorrido de siete maneras, según el cargo al que apuntes. Cada ruta
    declara qué partes hacer y en qué orden, qué clases no se saltan, con qué laboratorios se
    practica y qué hay que poder demostrar al terminar:
    <a href="rutas/index.html">ver las siete rutas</a>.</p>
    <div class="tabla-scroll"><table>
      <thead><tr><th>Ruta</th><th>Partes</th><th>Nivel</th><th>Horas</th></tr></thead>
      <tbody>
{rutas}
      </tbody>
    </table></div>
  </section>

  <section class="seccion">
    <h2>Cómo está construido</h2>
    <p>Cada clase declara sus fuentes y ninguna se publica sin ellas: la validación
    del repositorio bloquea una clase sin bibliografía y una cita que no exista en
    el <a href="fuentes.html">registro</a>. Los README de clase y este sitio son
    artefactos generados desde <code>curriculum.yaml</code> y los
    <code>lesson.md</code>; la integración continua comprueba que no quedan
    desactualizados, y un conjunto de pruebas rompe el repositorio a propósito
    para exigir que el validador lo detecte.</p>
    <p>Los <a href="laboratorios.html">{len(ejecutables)} laboratorios ejecutables</a>
    corren en cada cambio sobre Python 3.11, 3.12 y 3.13, sin instalar dependencias
    ni levantar servidores. Ninguno afirma nada en milisegundos: afirman invariantes,
    planes de ejecución, accesos y bytes.</p>
  </section>
</main>"""

    jsonld_curso = json.dumps({
        "@context": "https://schema.org",
        "@type": "Course",
        "name": programa["nombre"],
        "description": " ".join(programa["resumen"].split()),
        "url": BASE,
        "inLanguage": "es",
        "isAccessibleForFree": True,
        "license": "https://opensource.org/licenses/MIT",
        "numberOfCredits": total_horas,
        "provider": {"@type": "Person", "name": "Vladimir Acuña"},
        "hasCourseInstance": {
            "@type": "CourseInstance",
            "courseMode": "online",
            "courseWorkload": f"PT{total_horas}H",
        },
    }, ensure_ascii=False)

    salidas[SITE / "index.html"] = pagina(
        titulo="Database Systems Labs · programa de ingeniería de datos",
        descripcion=programa["resumen"], cuerpo=cuerpo, prefijo="", ruta="",
        programa=programa, jsonld=jsonld_curso,
        scripts='  <script src="assets/app.js"></script>\n')

    # ---------- laboratorios ----------
    clases_por_lab: dict[str, list[str]] = {}
    for _, c in plano:
        clases_por_lab.setdefault(c["lab"], []).append(c["id"])

    tarjetas_lab = []
    for lab in laboratorios:
        ejecutable = bool(lab["comando"])
        comando = (f'<pre><code>{escapar(lab["comando"])}</code></pre>'
                   if ejecutable else
                   '<p class="fuente-meta">Se entrega escrito: modelo, decisión y '
                   'justificación, sin ejecución automática.</p>')
        mide = "".join(f"<li>{escapar(m)}</li>" for m in lab["mide"])
        clases = " ".join(f'<a href="classes/{cid}.html">{cid}</a>'
                          for cid in clases_por_lab.get(lab["ruta"], []))
        citas = "".join(f"<li>{cita(sid, '')}</li>" for sid in lab["fuentes"])
        tarjetas_lab.append(f"""  <article class="lab">
    <span class="estado {'estado-ejecutable' if ejecutable else 'estado-diseno'}">
      {'ejecutable en CI' if ejecutable else 'de diseño'}</span>
    <h3>{lab['id']} — {escapar(lab['titulo'])}</h3>
    <p class="lab-meta">{lab['duracion']} minutos ·
      <a href="{REPO}/blob/main/{lab['ruta']}/README.md" rel="noopener">guía del laboratorio</a></p>
    <p>{escapar(' '.join(lab['resumen'].split()))}</p>
{comando}
    <p class="rotulo">Qué mide</p>
    <ul>{mide}</ul>
    <p class="lab-meta">Marca de éxito: <code>{escapar(lab['marca']) or '—'}</code></p>
    <p class="lab-meta">Clases que lo usan: {clases or '—'}</p>
    <p class="rotulo">De dónde sale el criterio</p>
    <ul>{citas}</ul>
  </article>""")

    salidas[SITE / "laboratorios.html"] = pagina(
        titulo="Laboratorios · Database Systems Labs",
        descripcion=(f"{len(ejecutables)} de {len(laboratorios)} laboratorios se ejecutan "
                     "sin dependencias y se comprueban en integración continua."),
        prefijo="", ruta="laboratorios.html", programa=programa, activo="laboratorios",
        extra_css='<link rel="stylesheet" href="assets/class.css">\n',
        cuerpo=f"""<header class="hero">
  <p class="eyebrow">Evidencia reproducible</p>
  <h1>Laboratorios que <span class="gradient">se ejecutan</span>, no que se leen</h1>
  <p class="lead">{len(ejecutables)} de los {len(laboratorios)} laboratorios corren sin instalar
  nada y sin levantar ningún servidor, y se comprueban en cada cambio sobre Python 3.11,
  3.12 y 3.13. Ninguno afirma nada en milisegundos: un tiempo depende de la máquina, así
  que lo que se afirma son invariantes, planes de ejecución, accesos y bytes.</p>
  <div class="cta">
    <a class="btn btn-primary" href="{REPO}#empezar" rel="noopener">Cómo ejecutarlos</a>
    <a class="btn btn-ghost" href="docs/laboratorios-guia.html">Guía y método</a>
    <a class="btn btn-ghost" href="docs/entornos.html">Entornos con contenedores</a>
  </div>
</header>
<main id="principal">
<div class="labs">
{chr(10).join(tarjetas_lab)}
</div>
</main>""")

    # ---------- autoevaluacion ----------
    total_preguntas = sum(len(p) for _, _, p in preguntas_por_clase)
    bloques_preguntas = []
    for parte, clase, preguntas in preguntas_por_clase:
        if not preguntas:
            continue
        elementos = "".join(f"<li>{escapar(p)}</li>" for p in preguntas)
        bloques_preguntas.append(f"""  <article class="pregunta" data-parte="{parte['id']}">
    <p class="fuente-meta">Parte {parte['id']} · clase
      <a href="classes/{clase['id']}.html">{clase['id']}</a> ·
      {NIVELES[clase['level']]}</p>
    <strong>{escapar(clase['title'])}</strong>
    <ol>{elementos}</ol>
  </article>""")

    salidas[SITE / "autoevaluacion.html"] = pagina(
        titulo="Autoevaluación · Database Systems Labs",
        descripcion=(f"Las {total_preguntas} preguntas de evaluación del programa, "
                     "reunidas en una sola página para preparar la defensa."),
        prefijo="", ruta="autoevaluacion.html", programa=programa, activo="autoevaluacion",
        extra_css='<link rel="stylesheet" href="assets/class.css">\n',
        cuerpo=f"""<header class="hero">
  <p class="eyebrow">Banco de preguntas</p>
  <h1>{total_preguntas} preguntas que <span class="gradient">exigen explicar</span></h1>
  <p class="lead">Ninguna se responde con una palabra ni con un dato memorizado: todas piden
  el mecanismo, la traza o el límite. Son las mismas preguntas que cierran cada clase,
  reunidas aquí para repasar y para preparar la defensa del proyecto final. El criterio de
  corrección está en la <a href="docs/rubrica.html">rúbrica</a>.</p>
  <p class="lead"><strong>Un resultado correcto sin explicación no demuestra transferencia.</strong></p>
</header>
<main id="principal">
{chr(10).join(bloques_preguntas)}
</main>""")

    # ---------- rutas por rol ----------
    horas_por_parte = {p["id"]: sum(c["hours"] for c in p["classes"]) for p in partes}
    titulo_parte = {p["id"]: p["title"] for p in partes}
    por_lab = {lab["id"]: lab for lab in laboratorios}

    tarjetas_ruta = []
    for clave, ruta in curriculo["rutas"].items():
        horas_ruta = sum(horas_por_parte[pid] for pid in ruta["partes"])
        clases_ruta = sum(len(p["classes"]) for p in partes if p["id"] in ruta["partes"])
        etiquetas_parte = " ".join(
            f'<a class="tag" href="../classes/parte-{pid}.html" '
            f'title="{escapar(titulo_parte[pid])}">{pid}</a>' for pid in ruta["partes"])
        claves = " ".join(f'<a href="../classes/{cid}.html">{cid}</a>'
                          for cid in ruta["clases_clave"])
        labs_ruta = " · ".join(escapar(por_lab[lid]["titulo"]) for lid in ruta["laboratorios"])
        cargos = ", ".join(escapar(c) for c in ruta["cargos"])
        citas_ruta = "".join(f"<li>{cita(sid, '../')}</li>" for sid in ruta["fuentes"])
        tarjetas_ruta.append(f"""  <article class="lab" id="{clave}">
    <span class="estado estado-{ruta['nivel']}">{ruta['nivel']}</span>
    <h3><a href="{clave}.html">{escapar(ruta['titulo'])}</a></h3>
    <p class="lab-meta">{len(ruta['partes'])} partes · {clases_ruta} clases ·
      {horas_ruta} horas estimadas</p>
    <p>{escapar(' '.join(ruta['foco'].split()))}</p>
    <p class="rotulo">Recorrido</p>
    <div class="tags">{etiquetas_parte}</div>
    <p class="lab-meta">Clases que no se saltan: {claves}</p>
    <p class="lab-meta">Laboratorios: {labs_ruta}</p>
    <p class="lab-meta">Cargos a los que apunta: {cargos}</p>
    <p class="rotulo">De dónde sale el criterio</p>
    <ul>{citas_ruta}</ul>
    <p><a class="btn btn-ghost" href="{clave}.html">Guía de carrera completa →</a></p>
  </article>""")

    salidas[SITE / "rutas" / "index.html"] = pagina(
        titulo="Rutas por rol · Database Systems Labs",
        descripcion=(f"{len(curriculo['rutas'])} recorridos por cargo: qué partes hacer, en qué "
                     "orden, con qué laboratorios y qué hay que poder demostrar."),
        prefijo="../", ruta="rutas/index.html", programa=programa, activo="rutas",
        extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
        cuerpo=f"""<header class="hero">
  <p class="eyebrow">Recorridos por cargo</p>
  <h1>{len(curriculo['rutas'])} rutas: el mismo programa, <span class="gradient">siete oficios</span></h1>
  <p class="lead">Las {total_clases} clases no son para todos a la vez. Cada ruta ordena el
  recorrido según el puesto al que apuntas —qué partes, en qué orden, qué clases no puedes
  saltarte y qué tienes que poder demostrar al terminar— y cita de dónde sale su criterio.
  Todas empiezan por la Parte 00 y terminan en el proyecto final.</p>
  <p class="lead"><strong>Este programa da conocimiento y método verificables, no
  experiencia.</strong> Lo segundo se gana trabajando; lo primero puede demostrarse con
  evidencia reproducible, y de eso trata cada ruta.</p>
</header>
<main id="principal">
<div class="labs">
{chr(10).join(tarjetas_ruta)}
</div>
</main>""")

    indice_rutas = enlaces_de_ruta((ROOT / "rutas" / "README.md").read_text(encoding="utf-8"))
    salidas[SITE / "rutas" / "guia.html"] = pagina(
        titulo="Cómo elegir tu ruta · Database Systems Labs",
        descripcion="Cómo elegir el recorrido cuando ninguno de los siete roles encaja del todo.",
        prefijo="../", ruta="rutas/guia.html", programa=programa, activo="rutas",
        extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
        cuerpo=f"""<nav class="migas" aria-label="Ruta de navegación">
  <a href="../index.html">Inicio</a><span aria-hidden="true">/</span>
  <a href="index.html">Rutas por rol</a><span aria-hidden="true">/</span>
  <span>Cómo elegir</span>
</nav>
<main class="content" id="principal">
{render_markdown(indice_rutas)}
</main>""")

    for clave, ruta in curriculo["rutas"].items():
        guia = enlaces_de_ruta((ROOT / ruta["guia"]).read_text(encoding="utf-8"))
        horas_ruta = sum(horas_por_parte[pid] for pid in ruta["partes"])
        salidas[SITE / "rutas" / f"{clave}.html"] = pagina(
            titulo=f"{ruta['titulo']} · Rutas · Database Systems Labs",
            descripcion=" ".join(ruta["foco"].split()),
            prefijo="../", ruta=f"rutas/{clave}.html", programa=programa, activo="rutas",
            extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
            scripts='  <script src="../assets/class.js"></script>\n',
            jsonld=json.dumps({
                "@context": "https://schema.org",
                "@type": "LearningResource",
                "name": f"Ruta: {ruta['titulo']}",
                "learningResourceType": "Career pathway",
                "inLanguage": "es",
                "educationalLevel": ruta["nivel"],
                "timeRequired": f"PT{horas_ruta}H",
                "teaches": ruta["cargos"],
                "isPartOf": {"@type": "Course", "name": programa["nombre"], "url": BASE},
            }, ensure_ascii=False),
            cuerpo=f"""<div class="avance" role="presentation"></div>
<nav class="migas" aria-label="Ruta de navegación">
  <a href="../index.html">Inicio</a><span aria-hidden="true">/</span>
  <a href="index.html">Rutas por rol</a><span aria-hidden="true">/</span>
  <span>{escapar(ruta['titulo'])}</span>
</nav>
<main class="content" id="principal">
{render_markdown(guia)}
</main>""")

    # ---------- certificaciones ----------
    mapeo = json.loads((ROOT / "certificaciones" / "_mapeo.json").read_text(encoding="utf-8"))
    certificaciones = mapeo["certificaciones"]

    tarjetas_cobertura = chr(10).join(
        f'    <div class="stat"><strong>{cobertura_cert(c):.0f} %</strong>'
        f'<span>{escapar(c["codigo"])}</span></div>' for c in certificaciones)

    indice_certs = enlaces_de_ruta(
        (ROOT / "certificaciones" / "README.md").read_text(encoding="utf-8"),
        indice="index.html", base="certificaciones")
    salidas[SITE / "certificaciones" / "index.html"] = pagina(
        titulo="Certificaciones · Database Systems Labs",
        descripcion=("Qué parte del temario de cada certificación de bases de datos cubre este "
                     "programa, calculado desde los pesos oficiales del examen."),
        prefijo="../", ruta="certificaciones/index.html", programa=programa,
        activo="certificaciones",
        extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
        cuerpo=f"""<header class="hero">
  <p class="eyebrow">Temario medido, no prometido</p>
  <h1>Certificaciones: <span class="gradient">cuánto cubre</span> este programa</h1>
  <p class="lead">Para cada examen se cruza su temario oficial —con los pesos que publica el
  proveedor— contra las clases del programa, y se calcula qué parte queda cubierta. El cálculo
  es reproducible y la brecha se declara: saber qué te falta vale más que un porcentaje
  redondo.</p>
  <div class="stats">
{tarjetas_cobertura}
  </div>
</header>
<main class="content" id="principal">
{render_markdown(indice_certs)}
</main>""")

    for cert in certificaciones:
        ficha = enlaces_de_ruta(
            (ROOT / "certificaciones" / f"{cert['id']}.md").read_text(encoding="utf-8"),
            indice="index.html", base="certificaciones")
        salidas[SITE / "certificaciones" / f"{cert['id']}.html"] = pagina(
            titulo=f"{cert['nombre']} ({cert['codigo']}) · Database Systems Labs",
            descripcion=" ".join(cert["resumen"].split())[:300],
            prefijo="../", ruta=f"certificaciones/{cert['id']}.html", programa=programa,
            activo="certificaciones",
            extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
            scripts='  <script src="../assets/class.js"></script>\n',
            cuerpo=f"""<div class="avance" role="presentation"></div>
<nav class="migas" aria-label="Ruta de navegación">
  <a href="../index.html">Inicio</a><span aria-hidden="true">/</span>
  <a href="index.html">Certificaciones</a><span aria-hidden="true">/</span>
  <span>{escapar(cert['codigo'])}</span>
</nav>
<main class="content" id="principal">
{render_markdown(ficha)}
</main>""")

    # ---------- documentacion ----------
    publicados = {origen: destino for origen, destino, _, _ in DOCUMENTOS}
    for origen, destino, titulo, resumen in DOCUMENTOS:
        texto = (ROOT / origen).read_text(encoding="utf-8")
        texto = enlaces_de_documento(texto, origen, publicados)
        salidas[SITE / destino] = pagina(
            titulo=f"{titulo} · Database Systems Labs", descripcion=resumen,
            prefijo="../", ruta=destino, programa=programa, activo="docs",
            extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
            scripts=MERMAID,
            cuerpo=f"""<nav class="migas" aria-label="Ruta de navegación">
  <a href="../index.html">Inicio</a><span aria-hidden="true">/</span>
  <a href="index.html">Documentación</a><span aria-hidden="true">/</span>
  <span>{escapar(titulo)}</span>
</nav>
<main class="content" id="principal">
{render_markdown(texto)}
<p class="fuente-meta">Fuente de esta página:
  <a href="{REPO}/blob/main/{origen}" rel="noopener"><code>{origen}</code></a></p>
</main>""")

    lista_docs = "\n".join(
        f'<div class="fuente"><div class="fuente-titulo">'
        f'<a href="{destino.removeprefix("docs/")}">{escapar(titulo)}</a></div>'
        f'<div class="fuente-nota">{escapar(resumen)}</div>'
        f'<div class="fuente-meta"><code>{origen}</code></div></div>'
        for origen, destino, titulo, resumen in DOCUMENTOS)

    salidas[SITE / "docs" / "index.html"] = pagina(
        titulo="Documentación · Database Systems Labs",
        descripcion="Arquitectura, método, política de fuentes, entornos, rúbrica y roadmap.",
        prefijo="../", ruta="docs/index.html", programa=programa, activo="docs",
        extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
        cuerpo=f"""<nav class="migas" aria-label="Ruta de navegación">
  <a href="../index.html">Inicio</a><span aria-hidden="true">/</span>
  <span>Documentación</span>
</nav>
<main class="content" id="principal">
<h1>Documentación</h1>
<p class="lead">Cómo está construido el programa, con qué método enseña, qué regla lo
gobierna y qué falta por hacer. Cada página se publica desde el mismo archivo del
repositorio que la integración continua valida.</p>
{lista_docs}
</main>""")

    # ---------- fuentes ----------
    usadas: dict[str, list[str]] = {}
    for _, c in plano:
        for sid in c["sources"]:
            usadas.setdefault(sid, []).append(c["id"])
    labs_por_fuente: dict[str, list[str]] = {}
    for lab in laboratorios:
        for sid in lab["fuentes"]:
            labs_por_fuente.setdefault(sid, []).append(lab["id"])

    secciones = []
    for kind, etiqueta in [("book", "Libros"), ("paper", "Artículos e informes"),
                           ("standard", "Normas y marcos"), ("docs", "Documentación oficial")]:
        items = [f for f in fuentes["sources"] if f["kind"] == kind]
        filas = []
        for f in sorted(items, key=lambda x: (x["authors"][0], x["year"])):
            meta = [", ".join(f["authors"]), str(f["year"])]
            for campo in ("edition", "venue", "publisher"):
                if f.get(campo):
                    meta.append(f[campo])
            if f.get("isbn"):
                meta.append(f"ISBN {f['isbn']}")
            if f.get("doi"):
                meta.append(f'DOI <a href="https://doi.org/{f["doi"]}">{f["doi"]}</a>')
            clases = usadas.get(f["id"], [])
            enlaces = " ".join(f'<a href="classes/{cid}.html">{cid}</a>' for cid in clases)
            labs = labs_por_fuente.get(f["id"], [])
            enlaces_lab = (" · laboratorios: "
                           + " ".join(f'<a href="laboratorios.html">{lid}</a>' for lid in labs)
                           if labs else "")
            filas.append(f"""<div class="fuente" id="src-{f['id']}">
  <div class="fuente-titulo"><a href="{escapar(f['url'])}">{escapar(f['title'])}</a></div>
  <div class="fuente-meta">{' · '.join(meta)}</div>
  <div class="fuente-nota">{escapar(f['note'])}</div>
  <div class="fuente-meta">Citada en: {enlaces or '—'}{enlaces_lab}</div>
</div>""")
        secciones.append(f'<section class="seccion"><h2>{etiqueta} '
                         f'<span class="fuente-meta">({len(items)})</span></h2>'
                         + "\n".join(filas) + "</section>")

    salidas[SITE / "fuentes.html"] = pagina(
        titulo="Fuentes · Database Systems Labs",
        descripcion="Registro de libros, artículos, normas y documentación en que se apoya el programa.",
        prefijo="", ruta="fuentes.html", programa=programa, activo="fuentes",
        extra_css='<link rel="stylesheet" href="assets/class.css">\n',
        cuerpo=f"""<main class="content" id="principal">
<h1>Fuentes</h1>
<p class="lead">{escapar(fuentes['policy'])}</p>
<p class="fuente-meta">{len(fuentes['sources'])} fuentes · verificadas el {fuentes['verified_on']}
· todas citadas por al menos una clase o un laboratorio.</p>
{chr(10).join(secciones)}
</main>""")

    # ---------- motores ----------
    # La tabla no se escribe a mano: se cuenta sobre las comparaciones reales,
    # asi que ninguna cifra de cobertura puede quedarse vieja.
    comparaciones = ml.todas(ROOT)
    cobertura: dict[str, dict[str, int]] = {}
    for comparacion in comparaciones:
        for motor in comparacion.motores:
            registro = cobertura.setdefault(
                motor.id, {"clases": 0, "resuelve": 0, "ejecutadas": 0, "descartado": 0})
            registro["clases"] += 1
            if motor.aplica:
                registro["resuelve"] += 1
                if motor.ejecutable:
                    registro["ejecutadas"] += 1
            else:
                registro["descartado"] += 1

    ejecutadas_total = sum(c["ejecutadas"] for c in cobertura.values())
    implementaciones_total = sum(c["resuelve"] for c in cobertura.values())

    def sello(mid: str) -> str:
        c = cobertura.get(mid)
        if not c or not c["resuelve"]:
            return '<span class="etiqueta">solo catálogo</span>'
        if c["ejecutadas"]:
            return (f'<span class="etiqueta etiqueta-ok">{c["ejecutadas"]} ejecutadas</span>')
        return '<span class="etiqueta">declarado</span>'

    filas = "\n".join(
        f'<tr><td><a href="{escapar(s["official_docs"])}">{escapar(s["name"])}</a></td>'
        f'<td>{", ".join(s["families"])}</td>'
        f'<td>{", ".join(s["query"])}</td>'
        f'<td>{cobertura.get(s["id"], {}).get("resuelve", 0)}</td>'
        f'<td>{cobertura.get(s["id"], {}).get("descartado", 0)}</td>'
        f'<td>{sello(s["id"])}</td></tr>'
        for s in sorted(motores["systems"],
                        key=lambda x: (-cobertura.get(x["id"], {}).get("resuelve", 0), x["name"])))

    salidas[SITE / "motores.html"] = pagina(
        titulo="Catálogo de motores · Database Systems Labs",
        descripcion="Motores cubiertos por el programa, con su documentación oficial "
                    "y cuántas veces resuelven —o no— el caso de una clase.",
        prefijo="", ruta="motores.html", programa=programa, activo="motores",
        extra_css='<link rel="stylesheet" href="assets/class.css">\n',
        cuerpo=f"""<main class="content" id="principal">
<h1>Catálogo de motores</h1>
<p class="lead">{escapar(motores['policy'])}</p>

<p>Cada clase del programa declara un caso y lo resuelve —o explica por qué no—
en varios motores. Esta tabla cuenta ese trabajo: en cuántas clases cada motor
<strong>resuelve</strong> el caso, en cuántas se <strong>descarta con un
argumento</strong>, y cuántas de sus implementaciones ejecuta la máquina de
verdad contra el motor real.</p>

<p class="fuente-meta">Total: <strong>{implementaciones_total} implementaciones</strong>
en {len(comparaciones)} clases, de las que <strong>{ejecutadas_total} se ejecutan</strong>
en integración continua. El resto se muestra y se revisa contra la documentación
citada, y así se dice en cada clase. Descartar un motor con un motivo cuenta
tanto como usarlo: por eso la columna «se descarta» está aquí y no escondida.</p>

<div class="tabla-scroll"><table>
<thead><tr><th>Motor</th><th>Familias</th><th>Lenguaje</th>
<th>Resuelve el caso</th><th>Se descarta</th><th>Prueba</th></tr></thead>
<tbody>
{filas}
</tbody></table></div>
</main>""")

    # ---------- 404 ----------
    salidas[SITE / "404.html"] = pagina(
        titulo="Página no encontrada · Database Systems Labs",
        descripcion="La dirección solicitada no existe en este programa.",
        prefijo="", ruta="404.html", programa=programa,
        cuerpo=f"""<main class="error" id="principal">
  <p class="eyebrow">Error 404</p>
  <h1>Esa página <span class="gradient">no existe</span></h1>
  <p class="lead">El enlace puede estar mal escrito o apuntar a material que se
  reorganizó. Las {total_clases} clases siguen donde estaban.</p>
  <div class="cta">
    <a class="btn btn-primary" href="index.html">Ir a la portada</a>
    <a class="btn btn-ghost" href="classes/indice.html">Todas las clases</a>
    <a class="btn btn-ghost" href="fuentes.html">Fuentes</a>
  </div>
</main>""")

    # ---------- manifiesto, service worker, sitemap y robots ----------
    salidas[SITE / "manifest.webmanifest"] = json.dumps({
        "name": programa["nombre"],
        "short_name": "DB Systems Labs",
        "description": " ".join(programa["resumen"].split()),
        "lang": "es",
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "background_color": "#05090f",
        "theme_color": "#05090f",
        "icons": [
            {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png",
             "purpose": "any"},
            {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "any"},
            {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "maskable"},
            {"src": "assets/icon.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
    }, ensure_ascii=False, indent=2) + "\n"

    paginas_html = sorted(str(r.relative_to(SITE)).replace("\\", "/")
                          for r in salidas if r.suffix == ".html")
    urls = "\n".join(
        f"  <url><loc>{BASE}{'' if ruta == 'index.html' else ruta}</loc>"
        f"<changefreq>monthly</changefreq></url>"
        for ruta in paginas_html if ruta != "404.html")
    salidas[SITE / "sitemap.xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n")

    salidas[SITE / "robots.txt"] = (
        "User-agent: *\nAllow: /\n"
        f"Sitemap: {BASE}sitemap.xml\n")

    # La version de la cache sale del contenido: cuando cambia una pagina, el
    # navegador descarta la cache vieja sin que nadie recuerde subir un numero.
    huella = hashlib.sha256()
    for ruta in sorted(salidas, key=str):
        contenido = salidas[ruta]
        huella.update(contenido.encode("utf-8") if isinstance(contenido, str) else contenido)
    version = huella.hexdigest()[:12]

    esenciales = json.dumps(
        ["./", "./index.html", "./laboratorios.html", "./autoevaluacion.html",
         "./fuentes.html", "./motores.html", "./busqueda.json",
         "./assets/styles.css", "./assets/class.css", "./assets/comun.js",
         "./assets/app.js", "./assets/class.js", "./assets/icon.svg"])
    salidas[SITE / "service-worker.js"] = f"""// Cache del sitio para consulta sin conexion.
// La version sale de la huella del contenido generado: si cambia una pagina,
// cambia el nombre de la cache y la anterior se descarta entera.
const CACHE = "database-systems-labs-{version}";
const ESENCIALES = {esenciales};

self.addEventListener("install", (evento) => {{
  self.skipWaiting();
  evento.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(ESENCIALES)));
}});

self.addEventListener("activate", (evento) => {{
  evento.waitUntil(caches.keys().then((claves) => Promise.all(
    claves.filter((clave) => clave !== CACHE).map((clave) => caches.delete(clave)),
  )).then(() => self.clients.claim()));
}});

// Red primero: el material cambia y una copia vieja confunde mas de lo que
// ayuda. La cache solo responde cuando no hay conexion.
self.addEventListener("fetch", (evento) => {{
  if (evento.request.method !== "GET") return;
  evento.respondWith(fetch(evento.request).then((respuesta) => {{
    const copia = respuesta.clone();
    caches.open(CACHE).then((cache) => cache.put(evento.request, copia));
    return respuesta;
  }}).catch(() => caches.match(evento.request).then(
    (guardada) => guardada || caches.match("./index.html"),
  )));
}});
"""

    # ---------- marca grafica ----------
    for nombre, contenido in brand_assets.generar().items():
        salidas[SITE / "assets" / nombre] = contenido

    salidas[SITE / ".nojekyll"] = ""
    return salidas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="no escribe: falla si el sitio esta desactualizado")
    args = parser.parse_args()

    salidas = construir()
    pendientes = []
    for ruta, contenido in salidas.items():
        binario = isinstance(contenido, bytes)
        if ruta.exists():
            actual = ruta.read_bytes() if binario else ruta.read_text(encoding="utf-8")
        else:
            actual = None
        if actual == contenido:
            continue
        if args.check:
            pendientes.append(str(ruta.relative_to(ROOT)))
        else:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            if binario:
                ruta.write_bytes(contenido)
            else:
                ruta.write_text(contenido, encoding="utf-8", newline="\n")

    if args.check and pendientes:
        print("Sitio desactualizado; ejecuta `python scripts/generate_site.py`:",
              file=sys.stderr)
        for ruta in pendientes[:20]:
            print(f"  {ruta}", file=sys.stderr)
        return 1

    paginas = sum(1 for r in salidas if r.suffix == ".html")
    print(f"SITE_OK {paginas} paginas HTML, {len(salidas)} archivos "
          f"{'verificados' if args.check else 'generados'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
