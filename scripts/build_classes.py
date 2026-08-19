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

import yaml

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


def render(parte: dict, clase: dict, cuerpo: str, fuentes: dict[str, dict],
           anterior: tuple[dict, dict] | None, siguiente: tuple[dict, dict] | None) -> str:
    ruta_parte = f"part-{parte['id']}-{parte['slug']}"

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
    motores = ", ".join(f"`{m}`" for m in clase["engines"])
    bibliografia = "\n".join(cita(fuentes[i]) for i in clase["sources"])

    return f"""# {clase['id']} — {clase['title']}

> {nav}

| | |
|---|---|
| **Parte** | {parte['id']} — {parte['title']} |
| **Nivel** | {NIVEL_ETIQUETA[clase['level']]} |
| **Horas estimadas** | {clase['hours']} |
| **Motores** | {motores} |
| **Laboratorio** | [`{clase['lab']}`](../../../{clase['lab']}/README.md) |
| **Fuentes** | {len(clase['sources'])} |

**Conceptos centrales:** {conceptos}

---

{cuerpo.strip()}

---

## Laboratorio

```bash
python scripts/validate_repository.py
python {clase['lab']}/run_lab.py
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
    pendientes: list[str] = []
    faltan_lecciones: list[str] = []
    salidas: dict[Path, str] = {}

    for posicion, (parte, clase) in enumerate(plano):
        destino = carpeta(parte, clase)
        leccion = destino / "lesson.md"
        if not leccion.exists():
            faltan_lecciones.append(str(leccion.relative_to(ROOT)))
            continue
        salidas[destino / "README.md"] = render(
            parte, clase, leccion.read_text(encoding="utf-8"), fuentes,
            plano[posicion - 1] if posicion > 0 else None,
            plano[posicion + 1] if posicion + 1 < len(plano) else None,
        )

    for parte in curriculo["parts"]:
        ruta = CLASSES / f"part-{parte['id']}-{parte['slug']}" / "README.md"
        salidas[ruta] = indice_parte(parte, curriculo)
    salidas[CLASSES / "README.md"] = indice_general(curriculo)

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
