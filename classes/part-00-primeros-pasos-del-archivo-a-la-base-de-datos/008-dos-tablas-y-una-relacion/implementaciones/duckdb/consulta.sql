-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/create_table
-- nota: la consulta que justifica partir la tabla unica es esta, sobre los datos
--       de origen:
--         SELECT correo, COUNT(*) FROM tabla_unica GROUP BY correo
--         HAVING COUNT(*) > 1;
--       Cada repeticion es una oportunidad de que dos filas digan cosas
--       distintas sobre el mismo hecho.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL
);
CREATE TABLE cursos (
    id       INTEGER PRIMARY KEY,
    codigo   VARCHAR NOT NULL UNIQUE,
    profesor VARCHAR NOT NULL
);
CREATE TABLE inscripciones (
    estudiante_id INTEGER NOT NULL,
    curso_id      INTEGER NOT NULL,
    PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus');
INSERT INTO cursos (id, codigo, profesor) VALUES
    (10, 'DB-101', 'A. Lovelace'),
    (20, 'SE-201', 'G. Hopper');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
-- Las tres tablas vuelven a juntarse al consultar. Cada hecho sigue guardado UNA
-- sola vez: el profesor de DB-101 esta en una fila, no en dos.
SELECT e.nombre, c.codigo, c.profesor
FROM inscripciones i
JOIN estudiantes e ON e.id = i.estudiante_id
JOIN cursos      c ON c.id = i.curso_id
ORDER BY e.nombre, c.codigo;
