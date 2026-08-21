"""Comprueba que cada fuente citada sigue siendo alcanzable.

Dos registros, no uno. El primero es `catalog/sources.json`: los libros, los
articulos y las normas de los que sale lo que afirma cada clase. El segundo son
los enlaces `doc:` de los `motores.yaml`: la pagina oficial que respalda cada
afirmacion sobre cada motor. Una opinion sobre PostgreSQL sin su pagina de
documentacion al lado es una opinion; con ella, es una cita.

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
    python scripts/check_external_links.py                  # los dos registros
    python scripts/check_external_links.py --solo motores   # solo la doc de motores
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

sys.path.insert(0, str(Path(__file__).resolve().parent))

import motores_lib as ml  # noqa: E402

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


def enlaces_de_motores() -> list[tuple[str, str]]:
    """Los `doc:` de todos los `motores.yaml`, sin repetir.

    Una misma pagina la citan varias clases; comprobarla una vez basta, y el
    identificador que se informa lleva las clases que la usan para poder
    arreglarlas todas de una vez si cae.
    """
    por_url: dict[str, list[str]] = {}
    for comparacion in ml.todas(ROOT):
        for motor in comparacion.motores:
            if motor.doc:
                por_url.setdefault(motor.doc, []).append(
                    f"{comparacion.clase}/{motor.id}")
    return [(f"{quien[0]}{'' if len(quien) == 1 else f' (+{len(quien) - 1})'}", url)
            for url, quien in sorted(por_url.items(), key=lambda kv: kv[1][0])]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", help="limita la comprobacion a un tipo de fuente")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--solo", choices=["fuentes", "motores"],
                        help="comprueba solo uno de los dos registros")
    args = parser.parse_args()

    objetivos: list[tuple[str, str]] = []
    if args.solo != "motores":
        registro = json.loads(SOURCES.read_text(encoding="utf-8"))["sources"]
        if args.kind:
            registro = [f for f in registro if f["kind"] == args.kind]
        objetivos += [(f["id"], f["url"]) for f in registro]
    if args.solo != "fuentes" and not args.kind:
        objetivos += enlaces_de_motores()

    resumen = {"OK": 0, "PROTEGIDO": 0, "ROTO": 0}
    rotos: list[str] = []

    for identificador, url in objetivos:
        estado, detalle = consultar(url, args.timeout)
        resumen[estado] += 1
        if estado == "ROTO":
            rotos.append(f"{identificador} [{detalle}] {url}")
        print(f"{estado:<9} {detalle:<18} {identificador}", flush=True)

    print(
        f"\nOK={resumen['OK']} PROTEGIDO={resumen['PROTEGIDO']} "
        f"ROTO={resumen['ROTO']} TOTAL={len(objetivos)}"
    )
    if rotos:
        print("\nEnlaces rotos:", file=sys.stderr)
        for linea in rotos:
            print(f"  {linea}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
