"""Laboratorio 04 - Indices y planes de ejecucion.

Mide que hace un indice y que no hace, sobre un conjunto de datos generado de
forma determinista.

Las aserciones son sobre el PLAN y sobre el TRABAJO, nunca sobre el tiempo:

  - el plan (`EXPLAIN QUERY PLAN`) dice si el motor recorre la tabla o busca
    por el indice, y eso no cambia entre maquinas;
  - el trabajo se cuenta en instrucciones de la maquina virtual de SQLite
    mediante `set_progress_handler`, no con un cronometro.

Un laboratorio que afirmara "la consulta baja de 40 ms a 3 ms" seria irrepetible
en otra maquina; "la consulta pasa de recorrer 20000 filas a buscar por indice"
se sostiene en todas.

Sin dependencias externas: solo sqlite3 de la biblioteca estandar.

Uso:
    python labs/04-indexing/run_indexing_lab.py
"""

from __future__ import annotations

import sqlite3
from contextlib import closing

FILAS = 20_000
CURSOS = 50
ESTUDIANTES = 400
PASO_CONTADOR = 10  # cada cuantas instrucciones de la VM se llama al contador

CONSULTAS = {
    "curso + estudiante": (
        "SELECT COUNT(*), AVG(score) FROM activity WHERE course_id = ? AND student_id = ?",
        (7, 123),
    ),
    "curso (prefijo)": (
        "SELECT COUNT(*), AVG(score) FROM activity WHERE course_id = ?",
        (7,),
    ),
    "estudiante (no prefijo)": (
        "SELECT COUNT(*), AVG(score) FROM activity WHERE student_id = ?",
        (123,),
    ),
}


def poblar(conexion: sqlite3.Connection) -> None:
    """Datos deterministas: la misma tabla en cualquier maquina y cualquier dia."""
    conexion.executescript(
        """
        CREATE TABLE activity (
            activity_id INTEGER PRIMARY KEY,
            course_id   INTEGER NOT NULL,
            student_id  INTEGER NOT NULL,
            kind        TEXT    NOT NULL,
            score       REAL    NOT NULL
        );
        """
    )
    # 7919 es primo y no divide a CURSOS ni a ESTUDIANTES: reparte los valores
    # sin dejar correlacion entre curso y estudiante, que falsearia la
    # selectividad medida.
    filas = [
        (
            i,
            i % CURSOS,
            (i * 7919) % ESTUDIANTES,
            ("lectura", "entrega", "consulta")[i % 3],
            float((i * 37) % 101),
        )
        for i in range(FILAS)
    ]
    conexion.executemany("INSERT INTO activity VALUES (?, ?, ?, ?, ?)", filas)
    conexion.commit()


def plan(conexion: sqlite3.Connection, sql: str, parametros: tuple) -> str:
    filas = conexion.execute(f"EXPLAIN QUERY PLAN {sql}", parametros).fetchall()
    return " | ".join(fila[3] for fila in filas)


def trabajo(conexion: sqlite3.Connection, sql: str, parametros: tuple) -> int:
    """Instrucciones aproximadas de la VM que consume la consulta."""
    pasos = 0

    def contador() -> int:
        nonlocal pasos
        pasos += 1
        return 0  # devolver distinto de cero abortaria la consulta

    conexion.set_progress_handler(contador, PASO_CONTADOR)
    try:
        conexion.execute(sql, parametros).fetchall()
    finally:
        conexion.set_progress_handler(None, 0)
    return pasos * PASO_CONTADOR


def paginas(conexion: sqlite3.Connection) -> int:
    return conexion.execute("PRAGMA page_count").fetchone()[0]


def medir(conexion: sqlite3.Connection) -> dict[str, tuple[str, int]]:
    return {
        nombre: (plan(conexion, sql, parametros), trabajo(conexion, sql, parametros))
        for nombre, (sql, parametros) in CONSULTAS.items()
    }


def usa_indice(descripcion: str) -> bool:
    return "USING INDEX" in descripcion or "USING COVERING INDEX" in descripcion


def informar(titulo: str, medicion: dict[str, tuple[str, int]]) -> None:
    print(f"\n{titulo}")
    for nombre, (descripcion, pasos) in medicion.items():
        print(f"  {nombre:<24} {pasos:>9,} pasos   {descripcion}")


def main() -> None:
    with closing(sqlite3.connect(":memory:")) as conexion:
        poblar(conexion)

        # --- 1. Sin indices: el motor no tiene alternativa a recorrer la tabla ---
        sin_indice = medir(conexion)
        informar("Sin indices (solo la clave primaria)", sin_indice)
        for nombre, (descripcion, _) in sin_indice.items():
            assert not usa_indice(descripcion), f"{nombre}: no deberia haber indice todavia"

        paginas_tabla = paginas(conexion)

        # --- 2. Indice compuesto (course_id, student_id) ---
        conexion.execute("CREATE INDEX idx_activity_curso_est ON activity(course_id, student_id)")
        conexion.execute("ANALYZE")
        compuesto = medir(conexion)
        informar("Con indice compuesto (course_id, student_id)", compuesto)

        # El prefijo izquierdo sirve siempre; la segunda columna sola, no de la
        # misma forma. Ese es todo el criterio para ordenar las columnas.
        assert usa_indice(compuesto["curso + estudiante"][0]), "la consulta por ambas columnas deberia usar el indice"
        assert usa_indice(compuesto["curso (prefijo)"][0]), "el prefijo izquierdo deberia usar el indice"

        factor = sin_indice["curso + estudiante"][1] / max(compuesto["curso + estudiante"][1], 1)
        assert factor >= 5, f"el indice solo redujo el trabajo {factor:.1f} veces"

        paginas_con_indice = paginas(conexion)
        assert paginas_con_indice > paginas_tabla, "el indice deberia ocupar paginas propias"

        # Filtrar por la segunda columna es el caso interesante. Con estadisticas
        # y una primera columna de baja cardinalidad, SQLite puede recorrer el
        # indice por saltos (`ANY(course_id)` en el plan: skip-scan) en vez de
        # descartarlo. Sigue sin ser lo mismo que un indice dedicado, y por eso
        # el laboratorio compara el trabajo en vez de dar por buena la forma del
        # plan: que aparezca el skip-scan depende de la version y de ANALYZE.
        if "ANY(" in compuesto["estudiante (no prefijo)"][0]:
            print("\n  Nota: el planificador eligio recorrer el indice por saltos (skip-scan).")

        # --- 3. El indice que faltaba para la tercera consulta ---
        conexion.execute("CREATE INDEX idx_activity_est ON activity(student_id)")
        conexion.execute("ANALYZE")
        ambos = medir(conexion)
        informar("Anadiendo indice (student_id)", ambos)
        assert "idx_activity_est" in ambos["estudiante (no prefijo)"][0], (
            "el indice dedicado deberia atender la consulta por estudiante"
        )
        assert ambos["estudiante (no prefijo)"][1] <= compuesto["estudiante (no prefijo)"][1], (
            "el indice dedicado no deberia costar mas trabajo que el compuesto"
        )

        # --- 4. Lo que el indice cuesta: cada escritura mantiene tambien el indice ---
        antes_sin = poblar_copia(indices=False)
        antes_con = poblar_copia(indices=True)
        print("\nCosto de escritura de 5000 inserciones")
        print(f"  sin indices secundarios   {antes_sin[0]:>9,} pasos   {antes_sin[1]:>5} paginas")
        print(f"  con dos indices           {antes_con[0]:>9,} pasos   {antes_con[1]:>5} paginas")
        assert antes_con[0] > antes_sin[0], "mantener dos indices no puede salir gratis en trabajo"
        assert antes_con[1] > antes_sin[1], "mantener dos indices no puede salir gratis en espacio"

        ahorro = compuesto["estudiante (no prefijo)"][1] / max(ambos["estudiante (no prefijo)"][1], 1)
        print(
            "\nConclusion, limitada a esta carga: el indice compuesto reduce el trabajo de la"
            f" consulta por curso y estudiante {factor:.0f} veces; para filtrar solo por"
            f" estudiante el indice dedicado hace {ahorro:.1f} veces menos trabajo que el"
            " compuesto, y cada indice encarece toda escritura."
        )
        print("INDEXING_LAB_OK")


def poblar_copia(indices: bool) -> tuple[int, int]:
    """Inserta 5000 filas con y sin indices secundarios; devuelve (pasos, paginas)."""
    with closing(sqlite3.connect(":memory:")) as conexion:
        conexion.executescript(
            """
            CREATE TABLE activity (
                activity_id INTEGER PRIMARY KEY,
                course_id   INTEGER NOT NULL,
                student_id  INTEGER NOT NULL,
                kind        TEXT    NOT NULL,
                score       REAL    NOT NULL
            );
            """
        )
        if indices:
            conexion.execute("CREATE INDEX idx_c ON activity(course_id, student_id)")
            conexion.execute("CREATE INDEX idx_e ON activity(student_id)")

        filas = [
            (i, i % CURSOS, (i * 7919) % ESTUDIANTES, "lectura", float(i % 101))
            for i in range(5_000)
        ]
        pasos = 0

        def contador() -> int:
            nonlocal pasos
            pasos += 1
            return 0

        conexion.set_progress_handler(contador, PASO_CONTADOR)
        try:
            conexion.executemany("INSERT INTO activity VALUES (?, ?, ?, ?, ?)", filas)
            conexion.commit()
        finally:
            conexion.set_progress_handler(None, 0)
        return pasos * PASO_CONTADOR, paginas(conexion)


if __name__ == "__main__":
    main()
