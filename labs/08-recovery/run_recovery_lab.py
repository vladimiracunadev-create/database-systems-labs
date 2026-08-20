"""Laboratorio 08 - Respaldo, restauracion y punto en el tiempo.

La afirmacion que ordena este laboratorio: **un respaldo que nunca se ha
restaurado no es un respaldo, es un archivo**. Aqui se restaura de verdad.

El guion monta una base SQLite real, toma un respaldo con la API de copia del
propio motor, sigue escribiendo mientras archiva cada transaccion, provoca un
desastre —un `DELETE` sin `WHERE` confirmado por error— y despues reconstruye
la base a un instante anterior al desastre.

Lo que se mide no es tiempo de reloj, que dependeria de la maquina, sino:

  - RPO: cuantas transacciones se pierden con cada estrategia;
  - trabajo de recuperacion: cuantas operaciones hay que reproducir;
  - correccion: la base restaurada tiene exactamente las filas que debia.

Sin dependencias externas: sqlite3 de la biblioteca estandar.

Uso:
    python labs/08-recovery/run_recovery_lab.py
"""

from __future__ import annotations

import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

ESQUEMA = """
PRAGMA journal_mode = WAL;
CREATE TABLE IF NOT EXISTS reservas (
    reserva_id INTEGER PRIMARY KEY,
    curso      TEXT    NOT NULL,
    estudiante TEXT    NOT NULL,
    creada_en  INTEGER NOT NULL
);
"""

# Cada entrada del archivo es (instante logico, sentencia, parametros). Es el
# equivalente didactico de un archivo de registro (WAL archiving): la lista de
# cambios confirmados que permite avanzar desde el respaldo hasta cualquier
# instante posterior.
Archivo = list[tuple[int, str, tuple]]


def abrir(ruta: Path) -> sqlite3.Connection:
    conexion = sqlite3.connect(ruta, isolation_level=None)
    conexion.executescript(ESQUEMA)
    return conexion


def aplicar(conexion: sqlite3.Connection, sentencia: str, parametros: tuple) -> None:
    conexion.execute(sentencia, parametros)


def respaldar(origen: sqlite3.Connection, destino: Path) -> int:
    """Copia en caliente con la API del motor; devuelve el tamano en bytes."""
    with closing(sqlite3.connect(destino)) as copia:
        origen.backup(copia)  # consistente aunque haya escrituras en curso
    return destino.stat().st_size


def filas(conexion: sqlite3.Connection) -> int:
    return conexion.execute("SELECT COUNT(*) FROM reservas").fetchone()[0]


def huella(conexion: sqlite3.Connection) -> str:
    """Resumen del contenido, para comparar dos bases sin mirarlas a ojo."""
    datos = conexion.execute(
        "SELECT reserva_id, curso, estudiante FROM reservas ORDER BY reserva_id").fetchall()
    return "|".join(f"{r[0]}:{r[1]}:{r[2]}" for r in datos)


def restaurar(respaldo: Path, destino: Path, archivo: Archivo,
              hasta: int | None) -> tuple[sqlite3.Connection, int]:
    """Copia el respaldo y reproduce el archivo hasta `hasta` (inclusive)."""
    destino.write_bytes(respaldo.read_bytes())
    conexion = abrir(destino)
    reproducidas = 0
    for instante, sentencia, parametros in archivo:
        if hasta is not None and instante > hasta:
            break
        aplicar(conexion, sentencia, parametros)
        reproducidas += 1
    return conexion, reproducidas


def main() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        base = Path(carpeta) / "produccion.sqlite"
        respaldo = Path(carpeta) / "respaldo-completo.sqlite"

        # --- 1. Estado inicial y respaldo completo -------------------------- #
        conexion = abrir(base)
        for i in range(1, 21):
            aplicar(conexion, "INSERT INTO reservas VALUES (?, ?, ?, ?)",
                    (i, "DB-101", f"estudiante-{i}", i))
        filas_al_respaldar = filas(conexion)
        tamano = respaldar(conexion, respaldo)
        print(f"Respaldo completo tomado con {filas_al_respaldar} filas "
              f"({tamano:,} bytes)")

        # --- 2. La vida sigue: 12 transacciones mas, todas archivadas ------- #
        archivo: Archivo = []
        for i in range(21, 33):
            sentencia = "INSERT INTO reservas VALUES (?, ?, ?, ?)"
            parametros = (i, "SE-201", f"estudiante-{i}", i)
            aplicar(conexion, sentencia, parametros)
            archivo.append((i, sentencia, parametros))
        filas_antes_del_desastre = filas(conexion)
        huella_buena = huella(conexion)
        instante_bueno = archivo[-1][0]

        # --- 3. El desastre: un borrado sin filtro, confirmado -------------- #
        desastre = (99, "DELETE FROM reservas WHERE curso = ?", ("SE-201",))
        aplicar(conexion, desastre[1], desastre[2])
        archivo.append(desastre)
        filas_tras_el_desastre = filas(conexion)
        conexion.close()
        print(f"Antes del desastre: {filas_antes_del_desastre} filas · "
              f"despues: {filas_tras_el_desastre}")

        # --- 4. Tres estrategias de recuperacion ---------------------------- #
        print(f"\n{'estrategia':<38} {'filas':>6} {'RPO (perdidas)':>15} "
              f"{'reproducidas':>13} {'correcta':>9}")

        # a) Solo el respaldo: rapido, pero pierde todo lo posterior.
        solo_respaldo, reproducidas_a = restaurar(
            respaldo, Path(carpeta) / "r-a.sqlite", archivo, hasta=0)
        filas_a = filas(solo_respaldo)
        correcta_a = huella(solo_respaldo) == huella_buena
        print(f"{'solo el respaldo completo':<38} {filas_a:>6} "
              f"{filas_antes_del_desastre - filas_a:>15} {reproducidas_a:>13} "
              f"{'si' if correcta_a else 'NO':>9}")
        solo_respaldo.close()

        # b) Respaldo + archivo entero: reproduce tambien el desastre.
        todo, reproducidas_b = restaurar(
            respaldo, Path(carpeta) / "r-b.sqlite", archivo, hasta=None)
        filas_b = filas(todo)
        correcta_b = huella(todo) == huella_buena
        print(f"{'respaldo + archivo completo':<38} {filas_b:>6} "
              f"{filas_antes_del_desastre - filas_b:>15} {reproducidas_b:>13} "
              f"{'si' if correcta_b else 'NO':>9}")
        todo.close()

        # c) Punto en el tiempo: hasta el instante anterior al desastre.
        punto, reproducidas_c = restaurar(
            respaldo, Path(carpeta) / "r-c.sqlite", archivo, hasta=instante_bueno)
        filas_c = filas(punto)
        correcta_c = huella(punto) == huella_buena
        print(f"{'punto en el tiempo (antes del error)':<38} {filas_c:>6} "
              f"{filas_antes_del_desastre - filas_c:>15} {reproducidas_c:>13} "
              f"{'si' if correcta_c else 'NO':>9}")
        punto.close()

        # --- 5. Lo que el laboratorio afirma -------------------------------- #
        # El respaldo solo pierde las 12 transacciones posteriores: ese es su RPO.
        assert filas_a == filas_al_respaldar, "el respaldo deberia traer el estado congelado"
        assert filas_antes_del_desastre - filas_a == 12, "el RPO del respaldo son 12 transacciones"
        assert not correcta_a, "restaurar solo el respaldo no puede reproducir el estado bueno"

        # Reproducir el archivo entero devuelve el desastre con toda fidelidad.
        assert filas_b == filas_tras_el_desastre, "el archivo completo incluye el borrado"
        assert not correcta_b, "reproducir el desastre no es recuperarse de el"

        # El punto en el tiempo es la unica que devuelve el estado bueno.
        assert correcta_c, "la restauracion a un punto en el tiempo deberia coincidir"
        assert filas_c == filas_antes_del_desastre
        assert filas_antes_del_desastre - filas_c == 0, "RPO cero hasta el instante elegido"
        assert reproducidas_c == 12, "hacen falta las 12 transacciones buenas del archivo"

        print("\nRPO y RTO no son lo mismo: el respaldo solo tiene RPO alto y trabajo minimo;")
        print("el punto en el tiempo tiene RPO cero hasta el instante elegido y cuesta")
        print("reproducir el archivo. Elegir es declarar cuanto dato puedes perder.")
        print("RECOVERY_LAB_OK")


if __name__ == "__main__":
    main()
