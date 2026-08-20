"""Laboratorio 05 - Eleccion por carga de trabajo (clave-valor, documento, columna ancha).

Los tres riesgos que este laboratorio obliga a medir en vez de suponer:

  1. una cache con expiracion devuelve datos viejos si nadie la invalida;
  2. incrustar y referenciar no se eligen por gusto, sino por la relacion entre
     lecturas y escrituras, y por como crece el agregado;
  3. una clave de particion mal elegida concentra la carga en un solo nodo.

Todo se cuenta: accesos, bytes reescritos y tamano de la particion mayor. No se
mide tiempo, porque el tiempo depende de la maquina y estos tres riesgos no.
El reloj es logico: el laboratorio nunca duerme, avanza el reloj a mano.

Sin dependencias externas ni servidores: solo la biblioteca estandar. Los
numeros modelan el comportamiento; las decisiones que sugieren hay que
verificarlas contra el motor real antes de llevarlas a produccion.

Uso:
    python labs/05-nosql-workloads/run_nosql_lab.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

LIMITE_DOCUMENTO = 16 * 1024 * 1024  # limite por documento de MongoDB (BSON)


# --------------------------------------------------------------------------- #
# 1. Clave-valor con expiracion: lo que una cache garantiza y lo que no.
# --------------------------------------------------------------------------- #

@dataclass
class ClaveValor:
    """Almacen clave-valor con TTL sobre un reloj logico."""

    ahora: int = 0
    datos: dict[str, tuple[str, int]] = field(default_factory=dict)
    aciertos: int = 0
    fallos: int = 0

    def set(self, clave: str, valor: str, ttl: int) -> None:
        self.datos[clave] = (valor, self.ahora + ttl)

    def get(self, clave: str) -> str | None:
        entrada = self.datos.get(clave)
        if entrada is None or entrada[1] <= self.ahora:
            self.datos.pop(clave, None)  # expiracion perezosa, como Redis
            self.fallos += 1
            return None
        self.aciertos += 1
        return entrada[0]

    def invalidar(self, clave: str) -> None:
        self.datos.pop(clave, None)

    def avanzar(self, segundos: int) -> None:
        self.ahora += segundos


def caso_clave_valor() -> tuple[int, int]:
    """Devuelve (lecturas obsoletas sin invalidar, lecturas obsoletas invalidando)."""
    print("1. Sesion en clave-valor con TTL de 300 s")

    # a) La expiracion funciona: dentro del TTL hay acierto, pasado el TTL no.
    cache = ClaveValor()
    cache.set("sesion:42", "perfil=alumno", ttl=300)
    cache.avanzar(299)
    assert cache.get("sesion:42") == "perfil=alumno", "dentro del TTL deberia ser un acierto"
    cache.avanzar(2)
    assert cache.get("sesion:42") is None, "pasado el TTL la clave deberia haber caducado"
    print(f"   expiracion: {cache.aciertos} acierto y {cache.fallos} fallo, como se esperaba")

    # b) El TTL NO es coherencia. La fuente de verdad cambia y la cache sigue
    #    respondiendo el valor viejo hasta que caduca.
    verdad = "perfil=alumno"
    sin_invalidar = ClaveValor()
    sin_invalidar.set("sesion:42", verdad, ttl=300)
    verdad = "perfil=suspendido"  # el permiso se revoca en la base de datos
    obsoletas_sin = 0
    for _ in range(5):
        sin_invalidar.avanzar(30)
        if sin_invalidar.get("sesion:42") != verdad:
            obsoletas_sin += 1

    # c) Con invalidacion explicita en la escritura, la ventana desaparece.
    con_invalidacion = ClaveValor()
    con_invalidacion.set("sesion:42", "perfil=alumno", ttl=300)
    con_invalidacion.invalidar("sesion:42")  # parte de la transaccion de revocacion
    obsoletas_con = 0
    for _ in range(5):
        con_invalidacion.avanzar(30)
        if (con_invalidacion.get("sesion:42") or verdad) != verdad:
            obsoletas_con += 1

    print(f"   lecturas obsoletas tras revocar el permiso: {obsoletas_sin} sin invalidar, "
          f"{obsoletas_con} invalidando")
    return obsoletas_sin, obsoletas_con


# --------------------------------------------------------------------------- #
# 2. Documento: incrustar o referenciar, decidido con la carga real.
# --------------------------------------------------------------------------- #

def bytes_de(objeto: object) -> int:
    return len(json.dumps(objeto, ensure_ascii=False).encode("utf-8"))


def caso_documento(numero: str, lecturas: int, escrituras_de_modulo: int) -> tuple[dict, dict]:
    """Compara incrustar y referenciar bajo la misma carga."""
    modulos = [
        {"module_id": i, "titulo": f"Modulo {i}", "duracion": 60 + i, "recursos": ["guia", "video"]}
        for i in range(12)
    ]
    curso = {"course_id": 10, "codigo": "DB-101", "titulo": "Fundamentos de datos"}

    incrustado = {**curso, "modulos": modulos}
    tamano_incrustado = bytes_de(incrustado)
    tamano_modulo = bytes_de(modulos[0])

    # Lectura de la ficha completa: incrustar la resuelve en un acceso;
    # referenciar necesita el curso mas cada modulo.
    accesos_incrustado = lecturas * 1
    accesos_referenciado = lecturas * (1 + len(modulos))

    # Escritura de un solo modulo: incrustar reescribe el documento entero;
    # referenciar toca solo el documento del modulo.
    bytes_incrustado = escrituras_de_modulo * tamano_incrustado
    bytes_referenciado = escrituras_de_modulo * tamano_modulo

    print(f"\n{numero}. Ficha de curso: {lecturas} lecturas completas y {escrituras_de_modulo} "
          f"actualizaciones de un modulo")
    print(f"   {'modelo':<14} {'accesos':>9} {'bytes escritos':>15} {'doc':>8}")
    print(f"   {'incrustado':<14} {accesos_incrustado:>9,} {bytes_incrustado:>15,} "
          f"{tamano_incrustado:>8,}")
    print(f"   {'referenciado':<14} {accesos_referenciado:>9,} {bytes_referenciado:>15,} "
          f"{tamano_modulo:>8,}")

    return (
        {"accesos": accesos_incrustado, "bytes": bytes_incrustado, "documento": tamano_incrustado},
        {"accesos": accesos_referenciado, "bytes": bytes_referenciado, "documento": tamano_modulo},
    )


def caso_crecimiento() -> int:
    """Un arreglo incrustado sin cota tiene fecha de caducidad: la calcula."""
    tamano_comentario = bytes_de({"autor": 1, "texto": "x" * 180, "fecha": "2026-08-19T10:00:00Z"})
    base = bytes_de({"course_id": 10, "codigo": "DB-101", "comentarios": []})
    caben = (LIMITE_DOCUMENTO - base) // tamano_comentario
    print(f"\n3. Crecimiento del agregado: con comentarios de {tamano_comentario} B, el documento "
          f"admite ~{caben:,} antes del limite de {LIMITE_DOCUMENTO // (1024 * 1024)} MiB")
    print("   Un arreglo que crece con el uso no se incrusta: se referencia o se acota.")
    return caben


# --------------------------------------------------------------------------- #
# 3. Columna ancha: la clave de particion decide donde se concentra la carga.
# --------------------------------------------------------------------------- #

def caso_clave_caliente() -> tuple[int, int]:
    """Un estudiante muy activo concentra la particion; el compartimentado la reparte."""
    eventos: list[tuple[int, int]] = []  # (student_id, mes)
    for i in range(60_000):
        # El estudiante 1 genera la mitad de la actividad: el caso real de una
        # cuenta institucional o un robot de integracion.
        estudiante = 1 if i % 2 == 0 else 2 + (i % 199)
        eventos.append((estudiante, i % 12))

    por_estudiante: dict[int, int] = {}
    por_estudiante_mes: dict[tuple[int, int], int] = {}
    for estudiante, mes in eventos:
        por_estudiante[estudiante] = por_estudiante.get(estudiante, 0) + 1
        por_estudiante_mes[(estudiante, mes)] = por_estudiante_mes.get((estudiante, mes), 0) + 1

    mayor_simple = max(por_estudiante.values())
    mayor_compuesta = max(por_estudiante_mes.values())
    print(f"\n4. Particion de {len(eventos):,} eventos")
    print(f"   clave (student_id):        particion mayor {mayor_simple:>7,} eventos")
    print(f"   clave (student_id, mes):   particion mayor {mayor_compuesta:>7,} eventos")
    return mayor_simple, mayor_compuesta


# --------------------------------------------------------------------------- #

def main() -> None:
    obsoletas_sin, obsoletas_con = caso_clave_valor()
    assert obsoletas_sin == 5, "el TTL por si solo deberia dejar servir el valor viejo"
    assert obsoletas_con == 0, "invalidar en la escritura deberia cerrar la ventana"

    # Carga de lectura dominante: incrustar gana en accesos y su costo de
    # escritura sigue siendo asumible.
    incrustado, referenciado = caso_documento("2a", lecturas=1_000, escrituras_de_modulo=10)
    assert incrustado["accesos"] < referenciado["accesos"], "incrustar deberia ahorrar accesos"
    assert incrustado["bytes"] > referenciado["bytes"], "incrustar deberia escribir mas bytes"

    # Carga de escritura dominante sobre el mismo modelo: la conclusion se da
    # la vuelta, y por eso no existe una respuesta buena sin carga declarada.
    incrustado_w, referenciado_w = caso_documento("2b", lecturas=10, escrituras_de_modulo=1_000)
    assert incrustado_w["bytes"] > referenciado_w["bytes"] * 5, (
        "con escritura dominante, incrustar deberia salir claramente mas caro"
    )

    caben = caso_crecimiento()
    assert caben < 100_000, "el arreglo incrustado deberia tener un techo alcanzable"

    mayor_simple, mayor_compuesta = caso_clave_caliente()
    assert mayor_simple > 4 * mayor_compuesta, "compartimentar deberia repartir la clave caliente"

    print("\nDecision, limitada a estas cargas: incrustar si la ficha se lee entera y no crece"
          " sin cota; referenciar si el subdocumento se actualiza solo o crece con el uso;"
          " invalidar siempre en la escritura; compartimentar la clave de particion caliente.")
    print("NOSQL_LAB_OK")


if __name__ == "__main__":
    main()
