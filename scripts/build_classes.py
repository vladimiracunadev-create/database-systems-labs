"""Genera el `README.md` de cada clase a partir del curriculo y de su leccion.

Reparto de responsabilidades, para que 74 clases no se conviertan en 74 copias
del mismo encabezado que hay que arreglar una por una:

    curriculum.yaml            metadatos, resumen, prerrequisitos y la
                               introduccion pedagogica de cada parte
    classes/**/lesson.md       la materia, escrita a mano
    catalog/sources.json       de donde sale cada afirmacion
    catalog/glosario.json      que significa cada concepto y donde se introduce
    -> classes/**/README.md    documento publicable, generado
    -> classes/README.md       indice general con el resumen de cada clase
    -> classes/part-*/README.md portada pedagogica de la parte
    -> GLOSARIO.md             glosario unico del programa

El README es un artefacto derivado: se regenera y se compara en CI con
`--check`. Si alguien lo edita a mano, el trabajo se pierde en la siguiente
generacion; la materia se edita en `lesson.md` y la pauta en `curriculum.yaml`.

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


def cargar() -> tuple[dict, dict[str, dict], dict[str, dict]]:
    curriculo = yaml.safe_load((ROOT / "curriculum.yaml").read_text(encoding="utf-8"))
    registro = json.loads((ROOT / "catalog" / "sources.json").read_text(encoding="utf-8"))
    glosario = json.loads((ROOT / "catalog" / "glosario.json").read_text(encoding="utf-8"))
    return (curriculo,
            {f["id"]: f for f in registro["sources"]},
            {t["termino"]: t for t in glosario["terms"]})


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


def ancla(texto: str) -> str:
    """Ancla de GitHub para un encabezado: minusculas, sin puntuacion, guiones."""
    limpio = "".join(c for c in texto.lower() if c.isalnum() or c in " -_")
    return limpio.strip().replace(" ", "-")


def ruta_clase(indice: dict[str, tuple[dict, dict]], cid: str, desde: str) -> str:
    """Enlace relativo a la clase `cid` desde `desde` ('clase', 'parte' o 'raiz')."""
    parte, clase = indice[cid]
    carpeta = f"part-{parte['id']}-{parte['slug']}/{clase['id']}-{clase['slug']}/README.md"
    prefijo = {"clase": "../../", "parte": "../", "raiz": "classes/"}[desde]
    return f"{prefijo}{carpeta}"


def bloque_prerrequisitos(clase: dict, indice: dict[str, tuple[dict, dict]]) -> str:
    """Que hay que traer sabido a esta clase, con el enlace a donde se explicó."""
    previos = clase.get("prerrequisitos") or []
    if not previos:
        return ("## Antes de empezar\n\nNinguno. Esta es una clase de entrada: no supone "
                "nada anterior del programa más allá de saber abrir una terminal.\n")
    filas = "\n".join(
        f"| [{indice[c][1]['id']}]({ruta_clase(indice, c, 'clase')}) "
        f"| {celda(indice[c][1]['title'])} "
        f"| {celda(' · '.join(indice[c][1]['concepts']))} |"
        for c in previos)
    return f"""## Antes de empezar

Esta clase supone que ya trabajaste lo siguiente. Si algo de la última columna
no te suena, vuelve a esa clase antes de seguir: aquí se usa sin volver a
explicarlo.

| # | Clase previa | Lo que se da por sabido |
|---|---|---|
{filas}
"""


def bloque_vocabulario(clase: dict, glosario: dict[str, dict],
                       indice: dict[str, tuple[dict, dict]]) -> str:
    """Los conceptos de la clase, definidos antes de que aparezcan en el texto.

    Se genera desde `catalog/glosario.json` para que la misma palabra signifique
    lo mismo en las 74 clases y en el glosario general.
    """
    filas = []
    for concepto in clase["concepts"]:
        termino = glosario[concepto]
        origen = termino["clase"]
        procedencia = ("se introduce aquí" if origen == clase["id"] else
                       f"se introdujo en la [{origen}]({ruta_clase(indice, origen, 'clase')})")
        filas.append(
            f"| <a id=\"v-{ancla(concepto)}\"></a>**{celda(concepto)}** "
            f"| {celda(termino['definicion'])} | {procedencia} |")
    return f"""## Vocabulario de la clase

Los términos que siguen se usan más adelante con este significado exacto. La
definición completa, con sus términos relacionados, está en el
[glosario del programa](../../../GLOSARIO.md).

| Término | Qué significa | Procedencia |
|---|---|---|
{chr(10).join(filas)}
"""


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
           catalogo: dict[str, dict], total_clases: int,
           glosario: dict[str, dict], indice: dict[str, tuple[dict, dict]]) -> str:
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

## De qué trata esta clase

{clase['resumen']}

{mapa_conceptos(clase)}

---

{bloque_prerrequisitos(clase, indice)}
{bloque_vocabulario(clase, glosario, indice)}
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


MAPA_ESTUDIO = """## Cómo estudiar esta parte

El mismo método en las 74 clases, y conviene respetar el orden:

1. **Lee el vocabulario antes que la materia.** Cada clase define sus términos
   arriba precisamente para que no haya que deducirlos del contexto.
2. **Ejecuta el ejemplo trabajado mientras lees**, no después. La mitad de lo
   que se aprende aquí solo aparece cuando la salida no es la esperada.
3. **Compara los motores.** La sección comparada muestra el mismo problema
   resuelto —o descartado con argumento— en varios sistemas. Lee también las
   filas de los que no lo resuelven: descartar con motivo es la habilidad que
   se evalúa en el proyecto final.
4. **Responde las preguntas de evaluación por escrito.** Una respuesta que no
   se puede escribir en tres líneas todavía no está entendida.
5. **Haz el reto de transferencia.** Es el único ejercicio que comprueba si el
   concepto se puede aplicar a un caso que la clase no mostró.
6. **Guarda la evidencia**: comando, versión del motor, semilla y salida
   completa. Sin eso no hay nota, porque no hay nada que revisar.
"""


def mapa_parte(parte: dict) -> str:
    """Diagrama con las clases de la parte encadenadas en su orden de estudio."""
    def etiqueta(clase: dict) -> str:
        titulo = clase["title"].replace('"', "'")
        if len(titulo) > 44:
            titulo = titulo[:41].rstrip() + "…"
        return f'{clase["id"]}<br/>{titulo}'

    nodos = [f'    C{c["id"]}["{etiqueta(c)}"]' for c in parte["classes"]]
    flechas = [f'    C{a["id"]} --> C{b["id"]}'
               for a, b in zip(parte["classes"], parte["classes"][1:])]
    colores = {"fundamentos": "fund", "intermedio": "inter", "avanzado": "avan"}
    clases_css = [f'    class C{c["id"]} {colores[c["level"]]}' for c in parte["classes"]]
    return "\n".join([
        "```mermaid",
        "flowchart LR",
        *nodos,
        *flechas,
        "    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff",
        "    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff",
        "    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff",
        *clases_css,
        "```",
    ])


def fichas_de_clase(parte: dict, indice: dict[str, tuple[dict, dict]]) -> str:
    """Una ficha explicada por clase: para qué está, qué exige y qué introduce."""
    fichas = []
    for clase in parte["classes"]:
        destino = f"{clase['id']}-{clase['slug']}/README.md"
        previos = clase.get("prerrequisitos") or []

        def enlace_previo(cid: str) -> str:
            """Dentro de la misma parte basta la ruta corta; fuera hace falta subir."""
            otra, previa = indice[cid]
            if otra["id"] == parte["id"]:
                return f"[{cid}]({previa['id']}-{previa['slug']}/README.md)"
            return f"[{cid}]({ruta_clase(indice, cid, 'parte')})"

        requiere = ("requiere " + ", ".join(enlace_previo(c) for c in previos)
                    if previos else "sin prerrequisitos")
        conceptos = " · ".join(f"`{c}`" for c in clase["concepts"])
        fichas.append(
            f"### [{clase['id']} — {clase['title']}]({destino})\n\n"
            f"*{NIVEL_ETIQUETA[clase['level']]} · {clase['hours']} h · "
            f"{len(clase['sources'])} fuentes · {requiere}*\n\n"
            f"{clase['resumen']}\n\n"
            f"**Conceptos que introduce:** {conceptos}\n\n"
            f"[Ir a la clase →]({destino})\n")
    return "\n".join(fichas)


def vocabulario_de_parte(parte: dict, glosario: dict[str, dict]) -> str:
    """Todos los conceptos que la parte introduce, definidos y sin repetir."""
    destinos = {c["id"]: f"{c['id']}-{c['slug']}/README.md" for c in parte["classes"]}
    vistos: dict[str, str] = {}
    for clase in parte["classes"]:
        for concepto in clase["concepts"]:
            vistos.setdefault(concepto, clase["id"])
    filas = "\n".join(
        f"| **{celda(t)}** | {celda(glosario[t]['definicion'])} "
        f"| [{cid}]({destinos[cid]}) |"
        for t, cid in sorted(vistos.items(), key=lambda x: x[0].lower()))
    return f"""## Vocabulario de la parte

Los {len(vistos)} términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
{filas}
"""


def fuentes_de_parte(parte: dict, fuentes: dict[str, dict]) -> str:
    """La bibliografia de la parte entera, sin repetir y con las clases que la citan."""
    usos: dict[str, list[str]] = {}
    for clase in parte["classes"]:
        for sid in clase["sources"]:
            usos.setdefault(sid, []).append(clase["id"])
    orden = sorted(usos, key=lambda s: (fuentes[s]["kind"], fuentes[s]["title"]))
    entradas = "\n".join(
        f"{cita(fuentes[sid])}  \n  *Se cita en las clases "
        f"{', '.join(usos[sid])}.*" for sid in orden)
    return f"""## Fuentes usadas en esta parte

{len(orden)} obras distintas sostienen lo que se afirma en estas
{len(parte['classes'])} clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

{entradas}
"""


def indice_parte(parte: dict, curriculo: dict, fuentes: dict[str, dict],
                 glosario: dict[str, dict], indice: dict[str, tuple[dict, dict]]) -> str:
    horas = sum(c["hours"] for c in parte["classes"])
    conceptos = {c for cl in parte["classes"] for c in cl["concepts"]}
    obras = {s for cl in parte["classes"] for s in cl["sources"]}
    titulos = {p["id"]: p for p in curriculo["parts"]}

    filas = "\n".join(
        f"| [{c['id']}]({c['id']}-{c['slug']}/README.md) "
        f"| [{c['title']}]({c['id']}-{c['slug']}/README.md) "
        f"| {NIVEL_ETIQUETA[c['level']]} | {c['hours']} | {len(c['sources'])} |"
        for c in parte["classes"])

    previas = parte.get("prerrequisitos") or []
    if previas:
        lista_previas = "\n".join(
            f"- [Parte {p} — {titulos[p]['title']}]"
            f"(../part-{p}-{titulos[p]['slug']}/README.md)" for p in previas)
        antes = ("Esta parte se apoya en lo trabajado antes. Si vienes de fuera del "
                 "programa, revisa al menos el vocabulario de:\n\n" + lista_previas)
    else:
        antes = ("Ninguno. Es la puerta de entrada al programa y no supone nada "
                 "anterior.")

    introduccion = "\n\n".join(parte["introduccion"])
    resultados = "\n".join(f"{i}. {r}" for i, r in enumerate(parte["resultados"], 1))
    errores = "\n".join(f"- {e}" for e in parte["errores"])
    otras = "\n".join(
        f"- [Parte {p['id']} — {p['title']}](../part-{p['id']}-{p['slug']}/README.md)"
        for p in curriculo["parts"] if p["id"] != parte["id"])

    return f"""# Parte {parte['id']} — {parte['title']}

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

{parte['summary']}

**{len(parte['classes'])} clases · {horas} horas · {len(conceptos)} conceptos · {len(obras)} fuentes**

## Antes de esta parte

{antes}

## De qué trata esta parte

{introduccion}

## Al terminar esta parte podrás

{resultados}

## Mapa de la parte

{mapa_parte(parte)}

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
{filas}

## Las clases, una por una

{fichas_de_clase(parte, indice)}
## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

{errores}

{vocabulario_de_parte(parte, glosario)}
{fuentes_de_parte(parte, fuentes)}
{MAPA_ESTUDIO}
## Otras partes

{otras}
"""


def primera_frase(texto: str) -> str:
    """La frase de apertura del resumen, para la columna de vistazo del índice."""
    frase = texto.strip().split(". ")[0].rstrip(".")
    return frase if len(frase) <= 150 else frase[:147].rstrip() + "…"


def indice_general(curriculo: dict) -> str:
    bloques = []
    for parte in curriculo["parts"]:
        horas = sum(c["hours"] for c in parte["classes"])
        conceptos = {c for cl in parte["classes"] for c in cl["concepts"]}
        filas = "\n".join(
            f"| [{c['id']}](part-{parte['id']}-{parte['slug']}/{c['id']}-{c['slug']}/README.md) "
            f"| {celda(c['title'])} | {celda(primera_frase(c['resumen']))} "
            f"| {NIVEL_ETIQUETA[c['level']]} | {c['hours']} |"
            for c in parte["classes"]
        )
        bloques.append(
            f"## [Parte {parte['id']} — {parte['title']}]"
            f"(part-{parte['id']}-{parte['slug']}/README.md)\n\n"
            f"{parte['summary']}\n\n"
            f"{parte['introduccion'][0]}\n\n"
            f"*{len(parte['classes'])} clases · {horas} horas · "
            f"{len(conceptos)} conceptos* — "
            f"[portada de la parte, con la explicación de cada clase]"
            f"(part-{parte['id']}-{parte['slug']}/README.md)\n\n"
            f"| # | Clase | En una línea | Nivel | Horas |\n"
            f"|---|---|---|---|---:|\n{filas}"
        )
    total = sum(len(p["classes"]) for p in curriculo["parts"])
    horas = sum(c["hours"] for p in curriculo["parts"] for c in p["classes"])
    conceptos = {c for p in curriculo["parts"] for cl in p["classes"] for c in cl["concepts"]}
    return f"""# Clases

{total} clases repartidas en {len(curriculo['parts'])} partes, {horas} horas
estimadas y {len(conceptos)} conceptos definidos en el
[glosario del programa](../GLOSARIO.md).

## Cómo se lee este índice

Cada parte tiene su **portada**, y ahí es donde empieza el trabajo: explica de
qué trata la parte, qué hay que traer sabido, qué sabrás hacer al terminar, una
ficha por clase, los errores frecuentes que desmonta, su vocabulario y la
bibliografía completa. Este índice es solo el mapa para llegar hasta allí.

La columna «en una línea» resume cada clase; la explicación completa está en la
portada de su parte y, con todo el detalle, en el README de la clase.

Cada clase declara sus fuentes al final y ninguna se publica sin al menos tres.
Este índice, los README de clase y el glosario se generan con
`python scripts/build_classes.py`; la materia se edita en el `lesson.md` de cada
carpeta y la pauta pedagógica en [`curriculum.yaml`](../curriculum.yaml).

{(chr(10) * 2).join(bloques)}
"""


def glosario_md(curriculo: dict, glosario: dict[str, dict], fuentes: dict[str, dict],
                indice: dict[str, tuple[dict, dict]]) -> str:
    """El glosario unico del programa, agrupado por inicial y con enlaces cruzados."""
    def clave(termino: str) -> str:
        tabla = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
        return termino.translate(tabla).lower()

    terminos = sorted(glosario.values(), key=lambda t: clave(t["termino"]))
    grupos: dict[str, list[dict]] = {}
    for termino in terminos:
        grupos.setdefault(clave(termino["termino"])[0].upper(), []).append(termino)

    navegacion = " · ".join(f"[{letra}](#{letra.lower()})" for letra in grupos)
    secciones = []
    for letra, entradas in grupos.items():
        cuerpo = []
        for t in entradas:
            parte, clase = indice[t["clase"]]
            destino = ruta_clase(indice, t["clase"], "raiz")
            relacionados = ", ".join(
                f"[{v}](#{ancla(v)})" for v in t["ver_tambien"]) or "—"
            fuente = fuentes[t["fuente"]]
            autores = ", ".join(fuente["authors"])
            cuerpo.append(
                f"### {t['termino']}\n\n"
                f"{t['definicion']}\n\n"
                f"- **Se trabaja en:** [{clase['id']} — {clase['title']}]({destino}) "
                f"(parte {parte['id']})\n"
                f"- **Ver también:** {relacionados}\n"
                f"- **Fuente:** {autores} ({fuente['year']}), "
                f"[{fuente['title']}]({fuente['url']})\n")
        # `.rstrip()`: cada entrada ya termina en salto y las secciones se unen
        # con linea en blanco; sin esto quedarian dos y markdownlint lo rechaza.
        secciones.append(f"## {letra}\n\n" + "\n".join(cuerpo).rstrip())

    total_clases = sum(len(p["classes"]) for p in curriculo["parts"])
    return f"""# Glosario del programa

{len(terminos)} términos: todos los conceptos que las {total_clases} clases
declaran, definidos una sola vez y con la misma palabra significando lo mismo de
principio a fin. Cada entrada dice dónde se trabaja el término, con qué otros se
relaciona y de qué obra procede la definición.

> [Programa](README.md) · [Índice de clases](classes/README.md) ·
> [Registro de fuentes](catalog/sources.json) ·
> [Modelo de aprendizaje](docs/LEARNING-MODEL.md)

Este archivo se genera desde [`catalog/glosario.json`](catalog/glosario.json) con
`python scripts/build_classes.py`. Editarlo a mano no sirve de nada: el cambio se
pierde en la siguiente generación. `scripts/validate_repository.py` comprueba que
no haya ningún concepto del currículo sin definición ni ninguna definición sin
concepto.

**Índice alfabético:** {navegacion}

{(chr(10) * 2).join(secciones)}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="no escribe: falla si algun archivo generado esta desactualizado")
    args = parser.parse_args()

    curriculo, fuentes, glosario = cargar()
    plano = indice_plano(curriculo)
    indice = {clase["id"]: (parte, clase) for parte, clase in plano}
    laboratorios = {lab["ruta"]: lab for lab in curriculo["laboratorios"]}
    catalogo = ml.cargar_catalogo()

    # Un concepto sin definicion romperia el README a mitad de generacion con un
    # KeyError opaco: se avisa aqui, con el nombre del concepto y su clase.
    sin_definir = sorted({(c["id"], k) for _, c in plano
                          for k in c["concepts"] if k not in glosario})
    if sin_definir:
        print("Conceptos sin entrada en catalog/glosario.json:", file=sys.stderr)
        for cid, concepto in sin_definir:
            print(f"  clase {cid}: {concepto!r}", file=sys.stderr)
        return 1
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
            laboratorios, comparacion, catalogo, len(plano), glosario, indice,
        )

    for parte in curriculo["parts"]:
        ruta = CLASSES / f"part-{parte['id']}-{parte['slug']}" / "README.md"
        salidas[ruta] = indice_parte(parte, curriculo, fuentes, glosario, indice)
    salidas[CLASSES / "README.md"] = indice_general(curriculo)
    salidas[ROOT / "GLOSARIO.md"] = glosario_md(curriculo, glosario, fuentes, indice)

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
