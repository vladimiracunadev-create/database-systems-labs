-- motor: duckdb
-- doc: https://duckdb.org/docs/current/sql/query_syntax/from.html
-- nota: misma consulta estandar; lo que cambia es el motor que la ejecuta
--       (columnar y vectorizado), no el SQL.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL
);
CREATE TABLE cursos (
    id     INTEGER PRIMARY KEY,
    codigo VARCHAR NOT NULL
);
CREATE TABLE inscripciones (
    estudiante_id INTEGER NOT NULL,
    curso_id      INTEGER NOT NULL
);

INSERT INTO estudiantes VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO cursos VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
SELECT e.nombre,
       COALESCE(c.codigo, 'sin-curso') AS codigo
FROM estudiantes e
LEFT JOIN inscripciones i ON i.estudiante_id = e.id
LEFT JOIN cursos c        ON c.id = i.curso_id
ORDER BY e.nombre, codigo;
