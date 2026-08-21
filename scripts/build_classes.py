"""Genera el `README.md` de cada clase a partir del curriculo y de su leccion.

Reparto de responsabilidades, para que 64 clases no se conviertan en 64 copias
del mismo encabezado que hay que arreglar una por una:

    curriculum.yaml            metadatos (horas, nivel, conceptos, fuentes)
    classes/**/lesson.md       la materia, escrita a mano
    catalog/sources.json       de donde sale cada afirmacion
    -> classes/**/README.md    documento publicable, generado

El README es un artefacto derivado: se regenera y se compara en CI con
`--check`. Si alguien lo edita a mano, el trabajo se pierde en la siguiente
generacion; la materia se edita en `lesson.md`.

Uso:
    python scripts/build_classes.py            # escribe
    python scripts/build_classes.py --check    # falla si algo esta sin regenerar
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import motores_lib as ml  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CLASSES = ROOT / "classes"

NIVEL_ETIQUETA = {
    "fundamentos": "Fundamentos",
    "intermedio": "Intermedio",
    "avanzado": "Avanzado",
}

RUBRICA = """| Criterio | Peso | Qué se comprueba |
|---|---:|---|
| Comprensión conceptual | 25 % | Explica el mecanismo, no solo el resultado |
| Ejecución reproducible | 25 % | Otra persona obtiene lo mismo con las instrucciones dadas |
| Interpretación basada en evidencia | 25 % | Cada conclusión se apoya en una salida o una medición |
| Límites y riesgos declarados | 25 % | Dice qué no demuestra el ejercicio y qué faltaría en producción |"""


def cargar() -> tuple[dict, dict[str, dict]]:
    curriculo = yaml.safe_load((ROOT / "curriculum.yaml").read_text(encoding="utf-8"))
    registro = json.loads((ROOT / "catalog" / "sources.json").read_text(encoding="utf-8"))
    return curriculo, {f["id"]: f for f in registro["sources"]}


def indice_plano(curriculo: dict) -> list[tuple[dict, dict]]:
    """Todas las clases en orden, cada una junto a la parte que la contiene."""
    return [(parte, clase) for parte in curriculo["parts"] for clase in parte["classes"]]


def carpeta(parte: dict, clase: dict) -> Path:
    return CLASSES / f"part-{parte['id']}-{parte['slug']}" / f"{clase['id']}-{clase['slug']}"


def cita(fuente: dict) -> str:
    """Una linea de bibliografia con lo necesario para localizar la obra."""
    autores = ", ".join(fuente["authors"])
    partes = [f"**{autores}** ({fuente['year']})", f"[{fuente['title']}]({fuente['url']})"]
    if fuente.get("edition"):
        partes.append(fuente["edition"])
    if fuente.get("venue"):
        partes.append(fuente["venue"])
    if fuente.get("publisher"):
        partes.append(fuente["publisher"])
    if fuente.get("isbn"):
        partes.append(f"ISBN {fuente['isbn']}")
    if fuente.get("doi"):
        partes.append(f"DOI [{fuente['doi']}](https://doi.org/{fuente['doi']})")
    # «7.a ed.» ya termina en punto: unir con «. » dejaria «7.a ed..».
    referencia = ". ".join(p.rstrip(".") for p in partes)
    return f"- {referencia}.  \n  {fuente['note']}"


SELLO = {
    "nucleo": "✅ **verificado** — se ejecuta en CI sin servicios",
    "servicio": "✅ **verificado** — se ejecuta contra el motor real levantado con "
                "`docker compose`",
    "declarado": "⚪ **declarado** — se revisa a mano contra la documentación citada; "
                 "la máquina no lo ejecuta",
}


def celda(texto: str) -> str:
    """Texto seguro dentro de una celda de tabla.

    Una barra vertical en el texto —y aparece de verdad: `||` es el operador de
    concatenacion— parte la fila y markdownlint lo detecta como columnas de mas.
    """
    return texto.replace("|", "\\|")


def bloque_motores(comparacion: ml.Comparacion, catalogo: dict[str, dict]) -> str:
    """La sección comparada: el mismo caso resuelto —o no— en cada motor.

    Es la sección que distingue a este programa de un curso de SQL. No basta
    con enseñar el concepto: hay que mostrarlo funcionando en varios motores y
    decir, con la misma seriedad, en cuáles no se hace y qué se hace entonces.
    """
    caso = comparacion.caso
    nombre = lambda mid: catalogo.get(mid, {}).get("name", mid)  # noqa: E731
    etiqueta = {"nucleo": "núcleo", "servicio": "servicio", "declarado": "declarado"}

    if caso.conceptual:
        etiqueta = dict.fromkeys(etiqueta, "conceptual")

    resumen = "\n".join(
        f"| {nombre(m.id)} | {'sí' if m.aplica else '**no**'} "
        f"| {etiqueta[m.ejecucion] if m.aplica else '—'} "
        f"| {'[código](' + m.archivo + ')' if m.archivo else '—'} "
        f"| [doc oficial]({m.doc}) |"
        for m in comparacion.motores
    )

    bloques = []
    for motor in comparacion.aplicables:
        titulo = (f"#### {nombre(motor.id)} · [`{motor.archivo}`]({motor.archivo})"
                  if motor.archivo else f"#### {nombre(motor.id)}")
        cuerpo = [titulo, ""]
        if motor.archivo:
            codigo = comparacion.codigo(motor).strip()
            lenguaje = ml.LENGUAJE_BLOQUE.get(Path(motor.archivo).suffix, "text")
            cuerpo += [SELLO[motor.ejecucion], "", f"```{lenguaje}", codigo, "```", ""]
        if motor.como:
            cuerpo += [f"- **Cómo se hace aquí:** {motor.como}"]
        cuerpo += [
            f"- **Por qué sí:** {motor.porque_si}",
            f"- **Por qué no:** {motor.porque_no}",
            f"- 📄 Documentación oficial: <{motor.doc}>",
            "",
        ]
        bloques.append("\n".join(cuerpo))

    descartados = comparacion.descartados
    tabla_descartados = ""
    if descartados:
        cuerpo_descartados = "\n".join(
            f"| {nombre(m.id)} | {celda(m.porque_no)} "
            f"| {celda(m.alternativa or '—')} | [doc]({m.doc}) |"
            for m in descartados
        )
        tabla_descartados = (
            "\n### Los que no resuelven este caso — y qué se hace en su lugar\n\n"
            "Descartar un motor con un argumento es tan formativo como usarlo. "
            "Ninguna de estas filas dice que el motor sea peor: dice que este "
            "problema no es el suyo.\n\n"
            "| Motor | Por qué no | Qué se hace en su lugar | Fuente |\n"
            "|---|---|---|---|\n"
            f"{cuerpo_descartados}\n"
        )

    verificadas = sum(1 for m in comparacion.ejecutables)
    if caso.conceptual:
        contrato = f"""{caso.contrato}

Esta comparación es **conceptual**: la decisión no se reduce a una consulta con
resultado, así que aquí no hay sello de máquina. Lo que se compara es lo que
cada motor **ofrece** y a qué precio, con la página oficial al lado de cada
afirmación."""
    else:
        cabecera_tabla = " | ".join(caso.columnas) if caso.columnas else "resultado"
        separador = "|".join("---" for _ in (caso.columnas or ["x"]))
        filas = "\n".join("| " + " | ".join(f"`{celda(v)}`" for v in fila) + " |"
                          for fila in caso.esperado)
        contrato = f"""{caso.contrato}

Salida esperada, idéntica en todos los motores que lo resuelven:

| {cabecera_tabla} |
|{separador}|
{filas}

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase {comparacion.clase}`: {verificadas} de
las {len(comparacion.aplicables)} implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado."""

    return f"""## 🌐 El mismo problema en cada motor

**Caso:** {caso.titulo}

{contrato}

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
{resumen}

### Los que resuelven el caso

{chr(10).join(bloques)}{tabla_descartados}
---

"""


# Color de la insignia de nivel, para que el vistazo distinga fundamentos de avanzado.
NIVEL_COLOR = {"fundamentos": "2e8b57", "intermedio": "1f6feb", "avanzado": "8250df"}


def _insignia(etiqueta: str, valor: str, color: str) -> str:
    """Una insignia de shields.io como imagen markdown (sin `<div>`).

    Se deja como línea de imágenes y no dentro de un `<div align=center>` a
    propósito: el generador del sitio no procesa markdown dentro de HTML en
    bloque, así que un `<div>` mostraría el markdown en crudo. Sin envoltorio,
    las insignias renderizan igual en GitHub y en el sitio.
    """
    return (f"![{etiqueta}](https://img.shields.io/badge/"
            f"{quote(etiqueta, safe='')}-{quote(valor, safe='')}-{color}?style=flat-square)")


def insignias(parte: dict, clase: dict, total: int) -> str:
    return " ".join([
        _insignia("🗂️ parte", str(parte["id"]), "2e8b57"),
        _insignia("🎚️ nivel", NIVEL_ETIQUETA[clase["level"]], NIVEL_COLOR[clase["level"]]),
        _insignia("⏱️ duración", f"{clase['hours']} h", "24292f"),
        _insignia("📗 clase", f"{clase['id']} / {total}", "6e7781"),
    ])


def mapa_conceptos(clase: dict) -> str:
    """Diagrama Mermaid que abre los conceptos centrales de la clase en abanico.

    Renderiza en GitHub y en el sitio (que convierte los bloques ```mermaid).
    Es la «gráfica por clase»: el mismo dato que la línea de conceptos, pero
    visto de un golpe.
    """
    conceptos = [str(c).replace('"', "'") for c in clase["concepts"] if c]
    nodos = "\n".join(f'    C --> K{i}["{c}"]' for i, c in enumerate(conceptos, 1))
    return (
        "```mermaid\n"
        "flowchart LR\n"
        f'    C["🗄️ Clase {clase["id"]}"]\n'
        f"{nodos}\n"
        "    classDef raiz fill:#0b3d2e,stroke:#3fb950,color:#fff\n"
        "    class C raiz\n"
        "```"
    )


def render(parte: dict, clase: dict, cuerpo: str, fuentes: dict[str, dict],
           anterior: tuple[dict, dict] | None, siguiente: tuple[dict, dict] | None,
           laboratorios: dict[str, dict], comparacion: ml.Comparacion | None,
           catalogo: dict[str, dict], total_clases: int) -> str:
    ruta_parte = f"part-{parte['id']}-{parte['slug']}"
    lab = laboratorios.get(clase["lab"], {})
    comando_lab = lab.get("comando") or (
        f"# {clase['lab']} se entrega escrito: no hay guion que ejecutar")

    def enlace(vecino: tuple[dict, dict] | None, texto: str) -> str:
        if vecino is None:
            return ""
        p, c = vecino
        destino = f"../../part-{p['id']}-{p['slug']}/{c['id']}-{c['slug']}/README.md"
        return f"[{texto}]({destino})"

    nav = " · ".join(
        x for x in [
            "[Programa](../../../README.md)",
            f"[Parte {parte['id']}](../README.md)",
            enlace(anterior, "← Anterior"),
            enlace(siguiente, "Siguiente →"),
        ] if x
    )

    conceptos = " · ".join(f"`{c}`" for c in clase["concepts"])
    motores_render = bloque_motores(comparacion, catalogo) if comparacion else ""
    if comparacion:
        ejecutadas = len(comparacion.ejecutables)
        resumen_motores = (
            f"\n\n**En este caso se comparan {len(comparacion.motores)} motores**: "
            f"{len(comparacion.aplicables)} lo resuelven "
            f"({ejecutadas} con el resultado comprobado por máquina) y "
            f"{len(comparacion.descartados)} no, con el motivo escrito.")
    else:
        resumen_motores = ""
    motores = ", ".join(f"`{m}`" for m in clase["engines"])
    bibliografia = "\n".join(cita(fuentes[i]) for i in clase["sources"])

    return f"""# {clase['id']} — {clase['title']}

{insignias(parte, clase, total_clases)}

> {nav}

Parte {parte['id']} — {parte['title']} · {NIVEL_ETIQUETA[clase['level']]} ·
{clase['hours']} horas estimadas · motores {motores} · laboratorio
[`{clase['lab']}`](../../../{clase['lab']}/README.md) · {len(clase['sources'])} fuentes.

**Conceptos centrales:** {conceptos}{resumen_motores}

{mapa_conceptos(clase)}

---

{cuerpo.strip()}

---

{motores_render}## Laboratorio

```bash
python scripts/validate_repository.py
{comando_lab}
```

Guarda como evidencia la salida completa, la versión del motor y la semilla o
los parámetros usados. Una captura sin comando no es evidencia: no se puede
repetir.

## Evaluación

{RUBRICA}

La clase se da por superada cuando la respuesta explica el mecanismo, muestra
la salida que la respalda y declara al menos un límite del ejercicio.

## Fuentes de esta clase

Todo lo afirmado arriba procede de estas obras. Los identificadores viven en
[`catalog/sources.json`](../../../catalog/sources.json) y el estado de los
enlaces se comprueba con `python scripts/check_external_links.py`.

{bibliografia}

---

> {nav}
"""


def indice_parte(parte: dict, curriculo: dict) -> str:
    filas = "\n".join(
        f"| [{c['id']}]({c['id']}-{c['slug']}/README.md) "
        f"| [{c['title']}]({c['id']}-{c['slug']}/README.md) "
        f"| {NIVEL_ETIQUETA[c['level']]} | {c['hours']} | {len(c['sources'])} |"
        for c in parte["classes"]
    )
    horas = sum(c["hours"] for c in parte["classes"])
    otras = "\n".join(
        f"- [Parte {p['id']} — {p['title']}](../part-{p['id']}-{p['slug']}/README.md)"
        for p in curriculo["parts"] if p["id"] != parte["id"]
    )
    return f"""# Parte {parte['id']} — {parte['title']}

> [Programa](../../README.md) · [Índice de clases](../README.md)

{parte['summary']}

**{len(parte['classes'])} clases · {horas} horas**

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
{filas}

## Otras partes

{otras}
"""


def indice_general(curriculo: dict) -> str:
    bloques = []
    for parte in curriculo["parts"]:
        horas = sum(c["hours"] for c in parte["classes"])
        filas = "\n".join(
            f"| [{c['id']}](part-{parte['id']}-{parte['slug']}/{c['id']}-{c['slug']}/README.md) "
            f"| {c['title']} | {NIVEL_ETIQUETA[c['level']]} | {c['hours']} |"
            for c in parte["classes"]
        )
        bloques.append(
            f"## [Parte {parte['id']} — {parte['title']}]"
            f"(part-{parte['id']}-{parte['slug']}/README.md)\n\n"
            f"{parte['summary']}\n\n"
            f"*{len(parte['classes'])} clases · {horas} horas*\n\n"
            f"| # | Clase | Nivel | Horas |\n|---|---|---|---:|\n{filas}"
        )
    total = sum(len(p["classes"]) for p in curriculo["parts"])
    horas = sum(c["hours"] for p in curriculo["parts"] for c in p["classes"])
    return f"""# Clases

{total} clases repartidas en {len(curriculo['parts'])} partes, {horas} horas estimadas.

Cada clase declara sus fuentes al final. Este índice y los README de clase se
generan con `python scripts/build_classes.py`; la materia se edita en el
`lesson.md` de cada carpeta.

{(chr(10) * 2).join(bloques)}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="no escribe: falla si algun archivo generado esta desactualizado")
    args = parser.parse_args()

    curriculo, fuentes = cargar()
    plano = indice_plano(curriculo)
    laboratorios = {lab["ruta"]: lab for lab in curriculo["laboratorios"]}
    catalogo = ml.cargar_catalogo()
    pendientes: list[str] = []
    faltan_lecciones: list[str] = []
    mal_declaradas: list[str] = []
    salidas: dict[Path, str] = {}

    for posicion, (parte, clase) in enumerate(plano):
        destino = carpeta(parte, clase)
        leccion = destino / "lesson.md"
        if not leccion.exists():
            faltan_lecciones.append(str(leccion.relative_to(ROOT)))
            continue
        ruta_motores = destino / "motores.yaml"
        comparacion = ml.cargar(ruta_motores, catalogo) if ruta_motores.exists() else None
        if comparacion and comparacion.errores:
            mal_declaradas.extend(comparacion.errores)
            continue
        salidas[destino / "README.md"] = render(
            parte, clase, leccion.read_text(encoding="utf-8"), fuentes,
            plano[posicion - 1] if posicion > 0 else None,
            plano[posicion + 1] if posicion + 1 < len(plano) else None,
            laboratorios, comparacion, catalogo, len(plano),
        )

    for parte in curriculo["parts"]:
        ruta = CLASSES / f"part-{parte['id']}-{parte['slug']}" / "README.md"
        salidas[ruta] = indice_parte(parte, curriculo)
    salidas[CLASSES / "README.md"] = indice_general(curriculo)

    if mal_declaradas:
        print("Comparaciones de motores mal declaradas:", file=sys.stderr)
        for error in mal_declaradas:
            print(f"  {error}", file=sys.stderr)
        return 1

    if faltan_lecciones:
        print("Faltan lecciones:", file=sys.stderr)
        for ruta in faltan_lecciones:
            print(f"  {ruta}", file=sys.stderr)
        return 1

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
        print("Archivos generados desactualizados; ejecuta "
              "`python scripts/build_classes.py`:", file=sys.stderr)
        for ruta in pendientes:
            print(f"  {ruta}", file=sys.stderr)
        return 1

    print(f"CLASSES_OK {len(plano)} clases, {len(salidas)} archivos "
          f"{'verificados' if args.check else 'generados'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
