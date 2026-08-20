"""Laboratorio 03 - Transacciones y concurrencia.

Reproduce una actualizacion perdida con dos hilos reales sobre SQLite y la
corrige de tres formas distintas, midiendo el resultado de cada una.

La evidencia no es un tiempo: es el numero de reservas aceptadas frente a las
plazas que existian. Un tiempo depende de la maquina; un cupo vendido dos veces
es un error en cualquier maquina.

Sin dependencias externas: sqlite3 y threading de la biblioteca estandar.

Uso:
    python labs/03-transactions/run_transactions_lab.py
"""

from __future__ import annotations

import sqlite3
import tempfile
import threading
from contextlib import closing
from pathlib import Path

CAPACIDAD = 1          # una sola plaza libre: cualquier segunda reserva sobra
CLIENTES = 2           # dos procesos compitiendo por esa plaza
ESPERA_BLOQUEO = 10.0  # segundos que un cliente espera el bloqueo de escritura


def preparar(ruta: Path) -> None:
    """Deja la tabla con una plaza libre y sin reservas."""
    # `closing` ademas de `with`: en sqlite3 el gestor de contexto confirma la
    # transaccion pero no cierra la conexion, y un archivo abierto no se borra.
    with closing(sqlite3.connect(ruta)) as conexion, conexion:
        conexion.executescript(
            """
            DROP TABLE IF EXISTS course_capacity;
            CREATE TABLE course_capacity (
                course_id INTEGER PRIMARY KEY,
                capacity  INTEGER NOT NULL CHECK (capacity >= 0),
                occupied  INTEGER NOT NULL CHECK (occupied >= 0),
                version   INTEGER NOT NULL
            );
            """
        )
        conexion.execute(
            "INSERT INTO course_capacity VALUES (10, ?, 0, 1)", (CAPACIDAD,)
        )


def conectar(ruta: Path) -> sqlite3.Connection:
    # isolation_level=None: las transacciones se abren a mano, que es de lo que
    # trata el laboratorio. Con el valor por defecto, el driver decidiria por
    # nosotros y el experimento mediria al driver, no al motor.
    return sqlite3.connect(ruta, timeout=ESPERA_BLOQUEO, isolation_level=None)


# --------------------------------------------------------------------------- #
# Cuatro clientes: uno roto y tres correctos.
# Todos comparten la misma forma para que la comparacion sea justa: leen, se
# sincronizan en la barrera (que fuerza el entrelazado peligroso) y escriben.
# --------------------------------------------------------------------------- #

def cliente_lectura_modificacion_escritura(ruta: Path, barrera: threading.Barrier) -> str:
    """El error clasico: decidir con un valor que ya caduco."""
    conexion = conectar(ruta)
    try:
        ocupadas, capacidad = conexion.execute(
            "SELECT occupied, capacity FROM course_capacity WHERE course_id = 10"
        ).fetchone()
        barrera.wait()  # ambos clientes ya leyeron el mismo cero
        if ocupadas >= capacidad:
            return "rechazada"
        conexion.execute(
            "UPDATE course_capacity SET occupied = ? WHERE course_id = 10",
            (ocupadas + 1,),
        )
        return "aceptada"
    finally:
        conexion.close()


def cliente_actualizacion_atomica(ruta: Path, barrera: threading.Barrier) -> str:
    """La condicion viaja dentro del UPDATE: el motor la evalua sobre la fila viva."""
    conexion = conectar(ruta)
    try:
        barrera.wait()
        cursor = conexion.execute(
            """
            UPDATE course_capacity
            SET occupied = occupied + 1
            WHERE course_id = 10 AND occupied < capacity
            """
        )
        return "aceptada" if cursor.rowcount == 1 else "rechazada"
    finally:
        conexion.close()


def cliente_control_optimista(ruta: Path, barrera: threading.Barrier) -> str:
    """Version en la clausula WHERE: el perdedor lo detecta y reintenta."""
    conexion = conectar(ruta)
    conflictos = 0
    try:
        for intento in range(3):
            ocupadas, capacidad, version = conexion.execute(
                "SELECT occupied, capacity, version FROM course_capacity WHERE course_id = 10"
            ).fetchone()
            if intento == 0:
                barrera.wait()
            if ocupadas >= capacidad:
                return f"rechazada tras {conflictos} conflicto(s)"
            cursor = conexion.execute(
                """
                UPDATE course_capacity
                SET occupied = occupied + 1, version = version + 1
                WHERE course_id = 10 AND version = ?
                """,
                (version,),
            )
            if cursor.rowcount == 1:
                return "aceptada"
            conflictos += 1  # otro cliente cambio la fila: releer y volver a decidir
        return "agotados los reintentos"
    finally:
        conexion.close()


def cliente_bloqueo_pesimista(ruta: Path, barrera: threading.Barrier) -> str:
    """BEGIN IMMEDIATE toma el bloqueo de escritura antes de leer para decidir."""
    conexion = conectar(ruta)
    try:
        barrera.wait()
        conexion.execute("BEGIN IMMEDIATE")  # el segundo cliente espera aqui
        try:
            ocupadas, capacidad = conexion.execute(
                "SELECT occupied, capacity FROM course_capacity WHERE course_id = 10"
            ).fetchone()
            if ocupadas >= capacidad:
                conexion.execute("ROLLBACK")
                return "rechazada"
            conexion.execute(
                "UPDATE course_capacity SET occupied = occupied + 1 WHERE course_id = 10"
            )
            conexion.execute("COMMIT")
            return "aceptada"
        except Exception:
            conexion.execute("ROLLBACK")
            raise
    finally:
        conexion.close()


# --------------------------------------------------------------------------- #

def ejecutar(ruta: Path, cliente) -> tuple[list[str], int]:
    """Lanza CLIENTES hilos sobre el mismo cliente y devuelve (resultados, ocupadas)."""
    preparar(ruta)
    barrera = threading.Barrier(CLIENTES)
    resultados: list[str] = [""] * CLIENTES

    def trabajo(indice: int) -> None:
        resultados[indice] = cliente(ruta, barrera)

    hilos = [threading.Thread(target=trabajo, args=(i,)) for i in range(CLIENTES)]
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join(timeout=30)
        if hilo.is_alive():
            raise RuntimeError("un cliente se quedo bloqueado: revisa la barrera")

    with closing(sqlite3.connect(ruta)) as conexion:
        ocupadas = conexion.execute(
            "SELECT occupied FROM course_capacity WHERE course_id = 10"
        ).fetchone()[0]
    return resultados, ocupadas


def main() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / "reservas.sqlite"

        estrategias = [
            ("leer-modificar-escribir", cliente_lectura_modificacion_escritura),
            ("actualizacion atomica", cliente_actualizacion_atomica),
            ("control optimista", cliente_control_optimista),
            ("bloqueo pesimista", cliente_bloqueo_pesimista),
        ]

        print(f"Plazas: {CAPACIDAD} - clientes simultaneos: {CLIENTES}")
        print(f"{'estrategia':<26} {'aceptadas':>9} {'occupied':>9}  resultados")

        informe: dict[str, tuple[int, int]] = {}
        for nombre, cliente in estrategias:
            resultados, ocupadas = ejecutar(ruta, cliente)
            aceptadas = sum(1 for r in resultados if r.startswith("aceptada"))
            informe[nombre] = (aceptadas, ocupadas)
            print(f"{nombre:<26} {aceptadas:>9} {ocupadas:>9}  {resultados}")

        # 1. El fallo se reproduce: dos clientes se llevaron la misma plaza y el
        #    contador solo registro una de las dos reservas.
        aceptadas, ocupadas = informe["leer-modificar-escribir"]
        assert aceptadas == 2, "la actualizacion perdida no se reprodujo"
        assert ocupadas == 1, "una de las dos escrituras deberia haberse perdido"

        # 2. Las tres correcciones sostienen el invariante: una plaza, una reserva.
        for nombre in ("actualizacion atomica", "control optimista", "bloqueo pesimista"):
            aceptadas, ocupadas = informe[nombre]
            assert aceptadas == CAPACIDAD, f"{nombre}: {aceptadas} reservas para {CAPACIDAD} plaza"
            assert ocupadas == CAPACIDAD, f"{nombre}: occupied={ocupadas} no cuadra con las reservas"

        print()
        print("Invariante occupied <= capacity: violado por la primera, sostenido por las otras tres.")
        print("TRANSACTIONS_LAB_OK")


if __name__ == "__main__":
    main()
