"""Genera el sitio estatico publicado en GitHub Pages.

Entrada:  curriculum.yaml · classes/**/README.md · catalog/*.json · docs/*.md
Salida:   site/ (index, una pagina por clase y por parte, fuentes, motores,
          busqueda.json)

El sitio es un artefacto derivado: se regenera entero en cada ejecucion y CI
comprueba que no queda desactualizado. Nada de site/ se edita a mano.

Uso:
    python scripts/generate_site.py
    python scripts/generate_site.py --check
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CLASSES = ROOT / "classes"

MD_EXT = ["tables", "fenced_code", "sane_lists", "attr_list"]

NIVELES = {"fundamentos": "Fundamentos", "intermedio": "Intermedio", "avanzado": "Avanzado"}

MERMAID = """  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
    for (const code of document.querySelectorAll("pre > code.language-mermaid")) {
      const caja = document.createElement("pre");
      caja.className = "mermaid";
      caja.textContent = code.textContent;
      code.parentElement.replaceWith(caja);
    }
    mermaid.initialize({ startOnLoad: true, theme: "dark",
                         themeVariables: { fontFamily: "Inter, system-ui, sans-serif" } });
  </script>
"""


def pagina(*, titulo: str, descripcion: str, cuerpo: str, prefijo: str,
           extra_css: str = "", scripts: str = "") -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#05090f">
<meta name="description" content="{escapar(descripcion)}">
<link rel="icon" type="image/svg+xml" href="{prefijo}assets/icon.svg">
<link rel="stylesheet" href="{prefijo}assets/styles.css">
{extra_css}<title>{escapar(titulo)}</title>
</head>
<body>
{cuerpo}
{scripts}</body>
</html>
"""


def escapar(texto: str) -> str:
    return (texto.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace('"', "&quot;"))


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


def reescribir_enlaces(texto: str) -> str:
    """Convierte los enlaces relativos del repositorio en enlaces del sitio."""
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


REPO = "https://github.com/vladimiracunadev-create/database-systems-labs"


# --------------------------------------------------------------------------- #

def construir() -> dict[Path, str]:
    curriculo = yaml.safe_load((ROOT / "curriculum.yaml").read_text(encoding="utf-8"))
    fuentes = json.loads((ROOT / "catalog" / "sources.json").read_text(encoding="utf-8"))
    motores = json.loads((ROOT / "catalog" / "databases.json").read_text(encoding="utf-8"))
    salidas: dict[Path, str] = {}

    partes = curriculo["parts"]
    plano = [(p, c) for p in partes for c in p["classes"]]
    total_clases = len(plano)
    total_horas = sum(c["hours"] for _, c in plano)
    todos_motores = sorted({m for _, c in plano for m in c["engines"]})

    # ---------- paginas de clase ----------
    indice_busqueda = []
    for parte, clase in plano:
        carpeta = CLASSES / f"part-{parte['id']}-{parte['slug']}" / f"{clase['id']}-{clase['slug']}"
        md = reescribir_enlaces((carpeta / "README.md").read_text(encoding="utf-8"))
        cuerpo = f"""<nav class="topbar">
  <a href="../index.html">&#9678; Database Systems Labs</a>
  <span class="crumb">Parte {parte['id']} · {escapar(parte['title'])}</span>
</nav>
<main class="content">
{render_markdown(md)}
</main>"""
        salidas[SITE / "classes" / f"{clase['id']}.html"] = pagina(
            titulo=f"{clase['id']} — {clase['title']} · Database Systems Labs",
            descripcion=f"{clase['title']}. Parte {parte['id']}: {parte['title']}.",
            cuerpo=cuerpo, prefijo="../",
            extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
            scripts=MERMAID)

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
        cuerpo = f"""<nav class="topbar">
  <a href="../index.html">&#9678; Database Systems Labs</a>
  <span class="crumb">Parte {parte['id']}</span>
</nav>
<main class="content">
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
            extra_css='<link rel="stylesheet" href="../assets/class.css">\n')

    salidas[SITE / "classes" / "indice.html"] = pagina(
        titulo="Todas las clases · Database Systems Labs",
        descripcion="Índice completo de las clases del programa.",
        prefijo="../",
        extra_css='<link rel="stylesheet" href="../assets/class.css">\n',
        cuerpo="""<nav class="topbar"><a href="../index.html">&#9678; Database Systems Labs</a>
  <span class="crumb">Todas las clases</span></nav>
<main class="content"><h1>Todas las clases</h1>
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

    rutas = "\n".join(
        f"""<tr><td><strong>{escapar(r['titulo'])}</strong><br>
        <span class="fuente-meta">{escapar(r['descripcion'])}</span></td>
        <td>{' · '.join(r['partes'])}</td></tr>"""
        for r in curriculo["rutas"].values())

    cuerpo = f"""<header class="hero">
  <p class="eyebrow">Programa abierto · {curriculo['programa']['version']}</p>
  <h1>Ingeniería de <span class="gradient">bases de datos</span>, con la fuente de cada afirmación</h1>
  <p class="lead">{escapar(curriculo['programa']['resumen'])}</p>
  <div class="stats">
    <div class="stat"><strong>{total_clases}</strong><span>clases</span></div>
    <div class="stat"><strong>{len(partes)}</strong><span>partes</span></div>
    <div class="stat"><strong>{total_horas}</strong><span>horas estimadas</span></div>
    <div class="stat"><strong>{len(fuentes['sources'])}</strong><span>fuentes verificadas</span></div>
    <div class="stat"><strong>{len(motores['systems'])}</strong><span>motores en catálogo</span></div>
  </div>
  <div class="cta">
    <a class="btn btn-primary" href="classes/001.html">Empezar por la clase 001</a>
    <a class="btn btn-ghost" href="fuentes.html">Ver las fuentes</a>
    <a class="btn btn-ghost" href="motores.html">Catálogo de motores</a>
    <a class="btn btn-ghost" href="{REPO}">Repositorio</a>
  </div>
</header>

<div class="controls">
  <input id="q" type="search" placeholder="Buscar en las 64 clases…  (pulsa / )" autocomplete="off">
  <select id="parte"><option value="">Todas las partes</option>
{opciones_parte}
  </select>
  <select id="nivel"><option value="">Todos los niveles</option>
    <option value="fundamentos">Fundamentos</option>
    <option value="intermedio">Intermedio</option>
    <option value="avanzado">Avanzado</option>
  </select>
  <select id="motor"><option value="">Todos los motores</option>
{opciones_motor}
  </select>
</div>
<p class="contador" id="contador">{total_clases} clases</p>

<main>
{chr(10).join(bloques)}
  <p class="vacio hidden" id="vacio">Ninguna clase coincide con el filtro.</p>

  <section class="seccion">
    <h2>Rutas por objetivo</h2>
    <div class="tabla-scroll"><table>
      <thead><tr><th>Ruta</th><th>Partes</th></tr></thead>
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
    desactualizados.</p>
  </section>
</main>

<footer>
  <p>{escapar(curriculo['programa']['nombre'])} · licencia
  {curriculo['programa']['licencia']} · actualizado el {curriculo['programa']['actualizado']}.
  Los productos citados conservan sus licencias y marcas.</p>
  <p><a href="{REPO}">Código fuente</a> ·
     <a href="fuentes.html">Bibliografía</a> ·
     <a href="motores.html">Motores</a> ·
     <a href="classes/indice.html">Todas las clases</a></p>
</footer>"""

    salidas[SITE / "index.html"] = pagina(
        titulo="Database Systems Labs · programa de ingeniería de datos",
        descripcion=curriculo["programa"]["resumen"], cuerpo=cuerpo, prefijo="",
        scripts='  <script src="assets/app.js"></script>\n')

    # ---------- fuentes ----------
    usadas: dict[str, list[str]] = {}
    for _, c in plano:
        for sid in c["sources"]:
            usadas.setdefault(sid, []).append(c["id"])

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
            filas.append(f"""<div class="fuente">
  <div class="fuente-titulo"><a href="{escapar(f['url'])}">{escapar(f['title'])}</a></div>
  <div class="fuente-meta">{' · '.join(meta)}</div>
  <div class="fuente-nota">{escapar(f['note'])}</div>
  <div class="fuente-meta">Citada en: {enlaces or '—'}</div>
</div>""")
        secciones.append(f'<section class="seccion"><h2>{etiqueta} '
                         f'<span class="fuente-meta">({len(items)})</span></h2>'
                         + "\n".join(filas) + "</section>")

    salidas[SITE / "fuentes.html"] = pagina(
        titulo="Fuentes · Database Systems Labs",
        descripcion="Registro de libros, artículos, normas y documentación en que se apoya el programa.",
        prefijo="", extra_css='<link rel="stylesheet" href="assets/class.css">\n',
        cuerpo=f"""<nav class="topbar"><a href="index.html">&#9678; Database Systems Labs</a>
  <span class="crumb">Fuentes</span></nav>
<main class="content">
<h1>Fuentes</h1>
<p class="lead">{escapar(fuentes['policy'])}</p>
<p class="fuente-meta">{len(fuentes['sources'])} fuentes · verificadas el {fuentes['verified_on']}
· todas citadas por al menos una clase.</p>
{chr(10).join(secciones)}
</main>""")

    # ---------- motores ----------
    filas = "\n".join(
        f'<tr><td><a href="{escapar(s["official_docs"])}">{escapar(s["name"])}</a></td>'
        f'<td>{", ".join(s["families"])}</td>'
        f'<td>{", ".join(s["query"])}</td>'
        f'<td>{"núcleo ejecutable" if s["core_lab"] else "ficha comparativa"}</td></tr>'
        for s in motores["systems"])

    salidas[SITE / "motores.html"] = pagina(
        titulo="Catálogo de motores · Database Systems Labs",
        descripcion="Motores cubiertos por el programa, con su documentación oficial.",
        prefijo="", extra_css='<link rel="stylesheet" href="assets/class.css">\n',
        cuerpo=f"""<nav class="topbar"><a href="index.html">&#9678; Database Systems Labs</a>
  <span class="crumb">Motores</span></nav>
<main class="content">
<h1>Catálogo de motores</h1>
<p class="lead">{escapar(motores['policy'])}</p>
<p class="fuente-meta">Aparecer en el catálogo no equivale a dominar la tecnología:
el <strong>núcleo ejecutable</strong> tiene laboratorios completos; las
<strong>fichas comparativas</strong> remiten a la documentación oficial.</p>
<div class="tabla-scroll"><table>
<thead><tr><th>Motor</th><th>Familias</th><th>Lenguaje</th><th>Cobertura</th></tr></thead>
<tbody>
{filas}
</tbody></table></div>
</main>""")

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
        actual = ruta.read_text(encoding="utf-8") if ruta.exists() else None
        if actual == contenido:
            continue
        if args.check:
            pendientes.append(str(ruta.relative_to(ROOT)))
        else:
            ruta.parent.mkdir(parents=True, exist_ok=True)
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
