"""Genera las fichas de certificacion desde `certificaciones/_mapeo.json`.

El objetivo de este generador es que el porcentaje de cobertura que publica el
repositorio no sea una opinion redonda, sino el resultado de una cuenta que
cualquiera puede repetir:

    cobertura del dominio  = subareas cubiertas / subareas totales   (metodo `subareas`)
                             o la estimacion declarada               (metodo `dominio`)
    cobertura total        = suma de (peso del dominio x cobertura) / 100

Los pesos son los oficiales del temario de cada proveedor; cuando el proveedor
publica un rango (por ejemplo 15-20 %), se usa el punto medio y se dice.

Salida: `certificaciones/README.md` y una ficha por certificacion.

Uso:
    python scripts/generar_certificaciones.py
    python scripts/generar_certificaciones.py --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / "certificaciones"

NIVEL = {"entrada": "Entrada", "intermedio": "Intermedio", "avanzado": "Avanzado"}


def barra(porcentaje: float) -> str:
    """Diez casillas: una idea del tamano antes de leer el numero."""
    llenas = round(porcentaje / 10)
    return "█" * llenas + "░" * (10 - llenas)


def cobertura_dominio(dominio: dict, metodo: str) -> float:
    if metodo == "subareas":
        subareas = dominio["subareas"]
        return 100.0 * sum(1 for s in subareas if s["cubierto"]) / len(subareas)
    return float(dominio["cobertura"])


def cobertura_total(cert: dict) -> float:
    """Media de las coberturas ponderada por el peso de cada dominio.

    Cuando el proveedor publica los pesos como rangos, el punto medio no suma
    exactamente 100: se normaliza dividiendo por la suma real en vez de por
    cien, y la ficha lo dice.
    """
    suma = sum(d["peso"] for d in cert["dominios"])
    return sum(d["peso"] * cobertura_dominio(d, cert["metodo"])
               for d in cert["dominios"]) / suma


def ruta_clase(indice: dict[str, tuple[str, str, str]], cid: str) -> str:
    parte_id, parte_slug, slug = indice[cid]
    return f"../classes/part-{parte_id}-{parte_slug}/{cid}-{slug}/README.md"


def enlaces_clases(indice: dict, clases: list[str]) -> str:
    return " ".join(f"[{cid}]({ruta_clase(indice, cid)})" for cid in clases) or "—"


def ficha(cert: dict, mapeo: dict, indice: dict, rutas: dict, labs: dict) -> str:
    total = cobertura_total(cert)
    metodo = cert["metodo"]

    filas = []
    for dominio in cert["dominios"]:
        cobertura = cobertura_dominio(dominio, metodo)
        if metodo == "subareas":
            cubiertas = sum(1 for s in dominio["subareas"] if s["cubierto"])
            detalle = f"{cubiertas} de {len(dominio['subareas'])} subáreas"
        else:
            detalle = "estimación declarada"
        filas.append(f"| {dominio['nombre']} | {dominio['peso_oficial']} | {detalle} "
                     f"| {cobertura:.0f} % |")

    bloques = []
    for dominio in cert["dominios"]:
        if metodo == "subareas":
            lineas = "\n".join(
                f"| {s['nombre']} | {'sí' if s['cubierto'] else 'no'} "
                f"| {enlaces_clases(indice, s['clases'])} | {s['nota']} |"
                for s in dominio["subareas"])
            bloques.append(
                f"### {dominio['nombre']} · {dominio['peso_oficial']}\n\n"
                f"| Subárea oficial | ¿Cubierta? | Clases | Nota |\n|---|---|---|---|\n{lineas}")
        else:
            bloques.append(
                f"### {dominio['nombre']} · {dominio['peso_oficial']}\n\n"
                f"**Cobertura estimada: {dominio['cobertura']} %.** {dominio['nota']}\n\n"
                f"Clases que la sostienen: {enlaces_clases(indice, dominio['clases'])}")

    laboratorios = " · ".join(
        f"[{lid} — {labs[lid]['titulo']}]({labs[lid]['ruta']}/README.md)".replace(
            "](labs/", "](../labs/")
        for lid in cert["laboratorios"])
    ruta = rutas[cert["ruta"]]

    suma_pesos = sum(d["peso"] for d in cert["dominios"])
    nota_normalizacion = (
        "" if abs(suma_pesos - 100) < 0.01 else
        f"\n\nEl proveedor publica los pesos como rangos; se usa el punto medio de cada uno "
        f"y se normaliza dividiendo por su suma real ({suma_pesos:.1f}) en vez de por cien.")

    return f"""# {cert['nombre']}

> **Código:** {cert['codigo']} · **Proveedor:** {cert['proveedor']} ·
> **Nivel:** {NIVEL[cert['nivel']]} · **Renovación:** {cert['renovacion']} ·
> [Página oficial]({cert['url']}) · [Temario oficial]({cert['temario']})

[⬅️ Volver al índice de certificaciones](README.md)

{cert['resumen']}

## 📊 Cobertura del programa: {total:.0f} %

`{barra(total)}` {total:.1f} % — media ponderada por el peso oficial de cada dominio.

**Método:** {mapeo['metodos'][metodo]}{nota_normalizacion}

| Dominio del examen | Peso oficial | Base del cálculo | Cobertura |
|---|---|---|---:|
{chr(10).join(filas)}

Temario vigente comprobado el **{cert['temario_vigente']}**.

## Mapeo dominio a dominio

{chr(10).join(f"{b}\n" for b in bloques)}
## 🎯 La brecha, y cómo cerrarla

{cert['brecha']}

## 🧭 Por dónde empezar aquí

- **Ruta recomendada:** [{ruta['titulo']}](../rutas/{cert['ruta']}.md) — {' '.join(ruta['foco'].split())}
- **Laboratorios que la preparan:** {laboratorios}
- **Para quién tiene sentido:** {cert['para_quien']}

---

> {mapeo['aviso']}
"""


def indice(mapeo: dict, certs: list[dict]) -> str:
    filas = []
    for cert in certs:
        total = cobertura_total(cert)
        etiqueta = "medida por subáreas" if cert["metodo"] == "subareas" else "estimada por dominio"
        filas.append(f"| [{cert['nombre']}]({cert['id']}.md) | {cert['codigo']} "
                     f"| {NIVEL[cert['nivel']]} | `{barra(total)}` {total:.0f} % | {etiqueta} |")

    fuera = "\n".join(
        f"- **[{item['nombre']}]({item['url']})** — {item['motivo']}"
        for item in mapeo["sin_mapeo"])

    return f"""# 🎓 Certificaciones

{mapeo['politica']}

| Certificación | Código | Nivel | Cobertura del programa | Cómo se calcula |
|---|---|---|---|---|
{chr(10).join(filas)}

## Cómo se calcula la cobertura

Hay dos métodos, y cada ficha dice cuál usa:

1. **Por subáreas.** {mapeo['metodos']['subareas']}
2. **Por dominio.** {mapeo['metodos']['dominio']}

En ambos casos el total es `Σ (peso del dominio × cobertura del dominio) / 100`. Cuando el
proveedor publica el peso como rango —«15–20 %»— se usa el punto medio. El cálculo lo hace
[`scripts/generar_certificaciones.py`](../scripts/generar_certificaciones.py) desde
[`_mapeo.json`](_mapeo.json), y la integración continua comprueba que estas fichas no quedan
desactualizadas.

**Lo que la cobertura significa y lo que no.** Mide qué parte del temario prepara este
programa. No mide tu probabilidad de aprobar: un examen de proveedor pregunta además por
nombres de servicios, consolas y límites de producto que aquí no se enseñan a propósito, y una
credencial práctica exige horas de laboratorio propio. Un 70 % de cobertura significa «te
faltará estudiar el 30 %, y ya sabes cuál es».

## Certificaciones que no se mapean, y por qué

Este repositorio no publica un porcentaje que no pueda comprobar en la fuente oficial. Estas
credenciales son relevantes para el campo, pero su ponderación no está disponible de forma
verificable:

{fuera}

## Antes de inscribirte

- Comprueba la **versión vigente** del temario: los proveedores lo actualizan y estas fichas
  llevan la fecha en que se verificaron.
- Mira primero la [ruta por rol](../rutas/README.md) que te corresponde: la credencial ordena
  el estudio, pero lo que te contrata es lo que puedes demostrar.
- Ninguna certificación sustituye a un [laboratorio](../labs/README.md) ejecutado y explicado.

---

> {mapeo['aviso']}
"""


def construir() -> dict[Path, str]:
    mapeo = json.loads((DESTINO / "_mapeo.json").read_text(encoding="utf-8"))
    curriculo = yaml.safe_load((ROOT / "curriculum.yaml").read_text(encoding="utf-8"))

    posicion = {
        clase["id"]: (parte["id"], parte["slug"], clase["slug"])
        for parte in curriculo["parts"] for clase in parte["classes"]
    }
    labs = {lab["id"]: lab for lab in curriculo["laboratorios"]}
    certs = mapeo["certificaciones"]

    salidas = {DESTINO / "README.md": indice(mapeo, certs)}
    for cert in certs:
        salidas[DESTINO / f"{cert['id']}.md"] = ficha(
            cert, mapeo, posicion, curriculo["rutas"], labs)
    return salidas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="no escribe: falla si alguna ficha esta desactualizada")
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
        print("Fichas de certificacion desactualizadas; ejecuta "
              "`python scripts/generar_certificaciones.py`:", file=sys.stderr)
        for ruta in pendientes:
            print(f"  {ruta}", file=sys.stderr)
        return 1

    print(f"CERTS_OK {len(salidas) - 1} certificaciones, {len(salidas)} archivos "
          f"{'verificados' if args.check else 'generados'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
