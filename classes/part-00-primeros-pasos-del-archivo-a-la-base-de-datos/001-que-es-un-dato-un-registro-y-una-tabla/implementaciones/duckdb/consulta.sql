-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/create_table
-- nota: la misma sentencia, otro motor. Lo que se aprende aqui no es de un
--       producto: es SQL.

-- === preparacion ===
-- Un hecho por fila. La hoja de calculo guardaba «DB-101, SE-201» en una
-- celda; aqui cada inscripcion es una fila propia, y contar deja de ser buscar
-- texto.
CREATE TABLE inscripciones (
    estudiante VARCHAR NOT NULL,
    curso      VARCHAR NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
INSERT INTO inscripciones (estudiante, curso) VALUES
    ('Ada',   'DB-101'),
    ('Ada',   'SE-201'),
    ('Linus', 'DB-101');

-- === consulta ===
SELECT estudiante, curso FROM inscripciones ORDER BY estudiante, curso;
