"""Genera la rubrica y el examen por rol desde `curriculum.yaml`.

La rubrica del proyecto final tiene que poder aplicarla una tercera persona que
no conozca el programa: por eso cada dimension describe sus cuatro niveles, dice
que evidencia la sostiene y enlaza las clases y los laboratorios donde se
aprende. Escribirla a mano en un `.md` la condenaria a desincronizarse del
curriculo en cuanto cambie una clase.

El examen por rol sale de la misma fuente: los bloques y sus puntos estan en
`evaluacion.examen`, y el contenido de cada rol —partes, clases clave y
laboratorios— sale de su ruta.

Salida: `assessments/rubric.md` y `assessments/examen-por-rol.md`.

Uso:
    python scripts/generar_evaluacion.py
    python scripts/generar_evaluacion.py --check
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / "assessments"


def cargar() -> dict:
    return yaml.safe_load((ROOT / "curriculum.yaml").read_text(encoding="utf-8"))


def enlace_clase(indice: dict[str, tuple[str, str, str]], cid: str) -> str:
    parte_id, parte_slug, slug = indice[cid]
    return f"[{cid}](../classes/part-{parte_id}-{parte_slug}/{cid}-{slug}/README.md)"


def enlace_lab(labs: dict, lid: str) -> str:
    return f"[{lid}](../{labs[lid]['ruta']}/README.md)"


def rubrica(curriculo: dict, indice: dict, labs: dict) -> str:
    evaluacion = curriculo["evaluacion"]
    escala = evaluacion["escala"]
    dimensiones = evaluacion["dimensiones"]

    resumen = "\n".join(
        f"| {d['nombre']} | {d['peso']} | {escala[d['minimo']]} ({d['minimo']}) | {d['pregunta']} |"
        for d in dimensiones)

    bloques = []
    for d in dimensiones:
        niveles = "\n".join(f"| {n} · {escala[n]} | {texto} |" for n, texto in sorted(d["niveles"].items()))
        apoyos = []
        if d.get("clases"):
            apoyos.append("Clases: " + " · ".join(enlace_clase(indice, c) for c in d["clases"]))
        if d.get("laboratorios"):
            apoyos.append("Laboratorios: " + " · ".join(enlace_lab(labs, l) for l in d["laboratorios"]))
        bloques.append(f"""### {d['nombre']} · {d['peso']} puntos

**La pregunta que responde:** {d['pregunta']}

**Evidencia que hay que ver:** {d['evidencia']}

| Nivel | Qué se observa |
|---|---|
{niveles}

Mínimo para aprobar: **{escala[d['minimo']]} ({d['minimo']})**. {" · ".join(apoyos)}""")

    faltas = "\n".join(f"- {f}" for f in evaluacion["faltas_criticas"])
    peso_total = sum(d["peso"] for d in dimensiones)

    return f"""# Rúbrica del proyecto final

Esta rúbrica está pensada para que **la aplique alguien que no conoce el programa**: cada
dimensión dice qué pregunta responde, qué evidencia hay que ver y qué separa un nivel del
siguiente. Dos correctores que la usen bien deberían llegar al mismo número sin hablar entre
ellos.

Escala común: {" · ".join(f"**{n}** {texto}" for n, texto in sorted(escala.items()))}.

**Aprobación:** {evaluacion['aprobacion']} de {peso_total} puntos **y** el mínimo declarado en
cada dimensión. Una nota alta con un mínimo incumplido no aprueba: significa que el trabajo es
bueno en lo que no compromete y flojo justo donde duele.

{evaluacion['nota']}

## Resumen

| Dimensión | Peso | Mínimo | Qué pregunta responde |
|---|---:|---|---|
{resumen}

## Dimensión por dimensión

{chr(10).join(f"{b}{chr(10)}" for b in bloques)}
## Faltas críticas

Suspenden con independencia de la nota. No son errores de ejecución: son incumplimientos del
contrato con el que se trabaja en este programa.

{faltas}

## Cómo se corrige, en la práctica

1. **Primero la evidencia, después el documento.** Si una afirmación no tiene salida, comando o
   traza que la respalde, se puntúa como si no estuviera.
2. **Reproduce una cosa.** Elige la afirmación más fuerte del trabajo e intenta repetirla con
   las instrucciones entregadas. Si no se puede, el nivel máximo de esa dimensión es 2.
3. **Pregunta por el límite.** Una entrega de nivel 4 sabe decir qué no demostró; una de nivel 2
   cree haberlo demostrado todo.
4. **Anota el nivel y una frase.** La frase es lo que convierte la nota en aprendizaje.

---

Generado desde `curriculum.yaml` por
[`scripts/generar_evaluacion.py`](../scripts/generar_evaluacion.py). Se edita ahí, no aquí.
"""


def examen(curriculo: dict, indice: dict, labs: dict) -> str:
    evaluacion = curriculo["evaluacion"]
    ex = evaluacion["examen"]
    horas_parte = {p["id"]: sum(c["hours"] for c in p["classes"]) for p in curriculo["parts"]}
    titulo_parte = {p["id"]: p["title"] for p in curriculo["parts"]}

    filas_bloques = "\n".join(
        f"| **{b['nombre']}** | {b['puntos']} | {' '.join(b['formato'].split())} |"
        for b in ex["bloques"])
    minimos = " · ".join(
        f"{b['nombre']} ≥ {b['minimo']}/{b['puntos']}"
        for b in ex["bloques"] if b.get("minimo"))

    secciones = []
    for clave, ruta in curriculo["rutas"].items():
        partes = " · ".join(f"{pid} ({titulo_parte[pid]})" for pid in ruta["partes"][:4])
        horas = sum(horas_parte[pid] for pid in ruta["partes"])
        clases = " · ".join(enlace_clase(indice, c) for c in ruta["clases_clave"])
        laboratorios = " · ".join(
            f"[{lid} — {labs[lid]['titulo']}](../{labs[lid]['ruta']}/README.md)"
            for lid in ruta["laboratorios"])
        ejecutables = [lid for lid in ruta["laboratorios"] if labs[lid]["comando"]]
        practica = (f"Ejecuta {', '.join(ejecutables)} y extiende uno con un caso propio."
                    if ejecutables else
                    "Entrega el modelado del laboratorio de diseño con su decisión justificada.")
        secciones.append(f"""## {ruta['titulo']}

Nivel {ruta['nivel']} · {len(ruta['partes'])} partes · {horas} horas ·
[guía de la ruta](../rutas/{clave}.md)

- **Teoría ({ex['bloques'][0]['puntos']} pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes {partes}…
  Las clases que no se saltan: {clases}.
- **Práctica ({ex['bloques'][1]['puntos']} pt):** {practica} Laboratorios de la ruta:
  {laboratorios}.
- **Informe ({ex['bloques'][2]['puntos']} pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** {', '.join(ruta['cargos'])}.""")

    return f"""# Examen final por rol

Cada [ruta por rol](../rutas/README.md) cierra con el mismo examen: teoría, práctica y defensa.
No es un formulario de opción múltiple, porque este programa no evalúa memoria: **un resultado
correcto sin explicación no demuestra transferencia**.

## Estructura común

| Bloque | Puntos | Formato |
|---|---:|---|
{filas_bloques}

**Aprobado:** {ex['aprobacion']} de 100{f" · {minimos}" if minimos else ""}.

La teoría y el informe se corrigen con la [rúbrica del proyecto final](rubric.md); la práctica,
con la evidencia entregada. Las [faltas críticas](rubric.md#faltas-críticas) suspenden aquí
también.

## Por qué la práctica pesa la mitad

Porque es lo único que no se puede fingir. Una respuesta teórica se puede leer en cualquier
sitio; una salida de laboratorio con su comando, su entorno y su explicación solo la tiene quien
la ejecutó y entendió.

{chr(10).join(f"{s}{chr(10)}" for s in secciones)}
## Qué entregar

Un repositorio —o una carpeta— con:

```text
evidencia/
  01-teoria.md          seis preguntas respondidas, con el mecanismo explicado
  02-practica/
    comando.txt         lo que ejecutaste, literal
    salida.txt          la salida completa, sin recortar
    entorno.md          versión del motor, del sistema y de Python
    explicacion.md      por qué el resultado es el que es, y qué NO demuestra
  03-informe.md         decisión, evidencia y límites
```

Una captura sin comando no es evidencia: no se puede repetir.

---

Generado desde `curriculum.yaml` por
[`scripts/generar_evaluacion.py`](../scripts/generar_evaluacion.py). Se edita ahí, no aquí.
"""


def construir() -> dict[Path, str]:
    curriculo = cargar()
    indice = {
        clase["id"]: (parte["id"], parte["slug"], clase["slug"])
        for parte in curriculo["parts"] for clase in parte["classes"]
    }
    labs = {lab["id"]: lab for lab in curriculo["laboratorios"]}
    return {
        DESTINO / "rubric.md": rubrica(curriculo, indice, labs),
        DESTINO / "examen-por-rol.md": examen(curriculo, indice, labs),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="no escribe: falla si la evaluacion esta desactualizada")
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
        print("Evaluacion desactualizada; ejecuta `python scripts/generar_evaluacion.py`:",
              file=sys.stderr)
        for ruta in pendientes:
            print(f"  {ruta}", file=sys.stderr)
        return 1

    print(f"EVALUACION_OK {len(salidas)} archivos "
          f"{'verificados' if args.check else 'generados'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
