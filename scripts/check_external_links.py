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
    CADENA    el servidor existe y responde TLS, pero envia una cadena incompleta
              que este cliente no puede completar
    ROTO      404/410, certificado invalido, dominio sin DNS o 5xx sostenido

Solo ROTO devuelve codigo de salida distinto de cero. Se ejecuta a mano antes
de publicar una actualizacion del catalogo y, de forma programada, en el
workflow `enlaces.yml`.

Tres precauciones que nacieron de falsos positivos reales:

- El almacen de certificados se toma de `certifi` cuando esta instalado, que va
  mas al dia que el del sistema en una imagen de CI o en un Windows sin
  actualizar.
- El estado CADENA separa el caso de db-engines.com: el servidor responde, su
  certificado es valido y un navegador abre la pagina, pero la cadena que envia
  omite un intermedio. Windows y los navegadores lo recuperan solos por AIA;
  OpenSSL no lo hace y aborta. Informarlo como roto mandaba a buscar una fuente
  sustituta que no hacia falta; informarlo como OK habria escondido que la
  comprobacion no llego a completarse. Se declara, y no tumba el trabajo.
- El detalle del error dice *que* fallo. `URLError` cubre a la vez un dominio
  que no resuelve, un puerto cerrado y un certificado que no se puede verificar;
  informar los tres con la misma palabra obliga a diagnosticar a mano cada vez.

Uso:
    python scripts/check_external_links.py                  # los dos registros
    python scripts/check_external_links.py --solo motores   # solo la doc de motores
    python scripts/check_external_links.py --kind book
    python scripts/check_external_links.py --timeout 40
"""

from __future__ import annotations

import argparse
import json
import socket
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


def contexto_tls() -> ssl.SSLContext:
    """Contexto con el almacen de certificados mas reciente que haya disponible.

    `certifi` publica el almacen de Mozilla al dia. Cuando esta instalado se usa
    ese; si no, se cae al del sistema, que en una imagen de CI antigua o en un
    Windows sin actualizar puede no traer las raices que emiten los sitios que
    este repositorio cita. Verificar siempre: en ningun caso se desactiva la
    comprobacion del certificado, porque eso convertiria el comprobador en uno
    que no comprueba.
    """
    try:
        import certifi
    except ImportError:
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


# El unico fallo de verificacion que no acusa al servidor de tener el
# certificado mal: le falta un eslabon intermedio que el cliente no puede
# descargar. Un certificado caducado, con el nombre cambiado o autofirmado si
# es un problema real y tiene que salir en rojo.
CADENA_INCOMPLETA = "unable to get local issuer certificate"


def clasificar_error_de_red(error: Exception) -> tuple[str, str]:
    """(estado, detalle) para un fallo de conexion.

    `URLError` envuelve causas que exigen acciones distintas: si al servidor le
    falta un intermedio, la fuente esta viva y no hay nada que sustituir; si el
    dominio no resuelve, hay que buscar otra.
    """
    causa = getattr(error, "reason", None)
    if isinstance(causa, ssl.SSLCertVerificationError):
        if CADENA_INCOMPLETA in str(causa):
            return ("CADENA", "falta un intermedio")
        return ("ROTO", f"TLS {causa.verify_message or causa.reason}")
    if isinstance(causa, socket.gaierror):
        return ("ROTO", "dominio sin DNS")
    if isinstance(causa, (TimeoutError, socket.timeout)):
        return ("ROTO", "tiempo agotado")
    if isinstance(causa, ConnectionRefusedError):
        return ("ROTO", "conexion rechazada")
    if isinstance(causa, Exception):
        return ("ROTO", type(causa).__name__)
    return ("ROTO", type(error).__name__)


def consultar(url: str, timeout: int) -> tuple[str, str]:
    """Devuelve (estado, detalle) para una URL."""
    peticion = urllib.request.Request(
        url,
        headers={"User-Agent": AGENTE, "Accept": "*/*"},
        method="GET",
    )
    contexto = contexto_tls()
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
        return clasificar_error_de_red(error)


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

    resumen = {"OK": 0, "PROTEGIDO": 0, "CADENA": 0, "ROTO": 0}
    rotos: list[str] = []
    cadenas: list[str] = []

    for identificador, url in objetivos:
        estado, detalle = consultar(url, args.timeout)
        resumen[estado] += 1
        if estado == "ROTO":
            rotos.append(f"{identificador} [{detalle}] {url}")
        elif estado == "CADENA":
            cadenas.append(f"{identificador} [{detalle}] {url}")
        print(f"{estado:<9} {detalle:<18} {identificador}", flush=True)

    if cadenas:
        print("\nCadena TLS incompleta —el recurso existe y un navegador lo abre; "
              "el servidor omite un intermedio que este cliente no puede "
              "descargar, asi que la comprobacion no llega a completarse:")
        for linea in cadenas:
            print(f"  {linea}")
    print(
        f"\nOK={resumen['OK']} PROTEGIDO={resumen['PROTEGIDO']} "
        f"CADENA={resumen['CADENA']} ROTO={resumen['ROTO']} TOTAL={len(objetivos)}"
    )
    if rotos:
        print("\nEnlaces rotos:", file=sys.stderr)
        for linea in rotos:
            print(f"  {linea}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
