"""Comprueba que cada fuente del registro sigue siendo alcanzable.

No forma parte de la validacion obligatoria de cada `push`: los sitios
academicos (ACM, Springer, ISO) responden 403 a cualquier cliente que no sea
un navegador, y un enlace bloqueado por un cortafuegos anti-robots no es un
enlace roto. Por eso el script distingue tres resultados:

    OK        el recurso respondio 2xx, o 3xx hacia otra ubicacion
    PROTEGIDO respondio 401/403/405/429: existe, pero rechaza clientes automaticos
    ROTO      404/410, error de red o 5xx sostenido

Solo ROTO devuelve codigo de salida distinto de cero. Se ejecuta a mano antes
de publicar una actualizacion del catalogo y, de forma programada, en el
workflow `enlaces.yml`.

Uso:
    python scripts/check_external_links.py            # todo el registro
    python scripts/check_external_links.py --kind book
    python scripts/check_external_links.py --timeout 40
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "catalog" / "sources.json"

# Sin un agente de navegador, varios dominios responden 403 incluso a peticiones
# legitimas; con el, la mayoria contesta 200 y el informe deja de ser ruido.
AGENTE = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
PROTEGIDO = {401, 403, 405, 429}


def consultar(url: str, timeout: int) -> tuple[str, str]:
    """Devuelve (estado, detalle) para una URL."""
    peticion = urllib.request.Request(
        url,
        headers={"User-Agent": AGENTE, "Accept": "*/*"},
        method="GET",
    )
    contexto = ssl.create_default_context()
    try:
        with urllib.request.urlopen(peticion, timeout=timeout, context=contexto) as respuesta:
            return ("OK", str(respuesta.status))
    except urllib.error.HTTPError as error:
        if error.code in PROTEGIDO:
            return ("PROTEGIDO", str(error.code))
        # Una redireccion que urllib no sigue (por ejemplo, la que milvus.io
        # sirve segun region) demuestra que el recurso existe: no es un enlace
        # roto y no debe tumbar la comprobacion.
        if 300 <= error.code < 400:
            return ("OK", f"{error.code} redirige")
        return ("ROTO", str(error.code))
    except (urllib.error.URLError, TimeoutError, ssl.SSLError, OSError) as error:
        return ("ROTO", type(error).__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", help="limita la comprobacion a un tipo de fuente")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    registro = json.loads(SOURCES.read_text(encoding="utf-8"))["sources"]
    if args.kind:
        registro = [f for f in registro if f["kind"] == args.kind]

    resumen = {"OK": 0, "PROTEGIDO": 0, "ROTO": 0}
    rotos: list[str] = []

    for fuente in registro:
        estado, detalle = consultar(fuente["url"], args.timeout)
        resumen[estado] += 1
        if estado == "ROTO":
            rotos.append(f"{fuente['id']} [{detalle}] {fuente['url']}")
        print(f"{estado:<9} {detalle:<18} {fuente['id']}", flush=True)

    print(
        f"\nOK={resumen['OK']} PROTEGIDO={resumen['PROTEGIDO']} "
        f"ROTO={resumen['ROTO']} TOTAL={len(registro)}"
    )
    if rotos:
        print("\nEnlaces rotos:", file=sys.stderr)
        for linea in rotos:
            print(f"  {linea}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
