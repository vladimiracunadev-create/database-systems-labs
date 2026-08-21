-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-createtable.html
-- nota: identica a la de SQLite salvo el nombre del tipo. La diferencia esta
--       fuera de la sentencia: aqui hay un servidor, un usuario y una conexion.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones;

-- Un hecho por fila. La hoja de calculo guardaba «DB-101, SE-201» en una
-- celda; aqui cada inscripcion es una fila propia, y contar deja de ser buscar
-- texto.
CREATE TABLE inscripciones (
    estudiante text NOT NULL,
    curso      text NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
INSERT INTO inscripciones (estudiante, curso) VALUES
    ('Ada',   'DB-101'),
    ('Ada',   'SE-201'),
    ('Linus', 'DB-101');

-- === consulta ===
SELECT estudiante, curso FROM inscripciones ORDER BY estudiante, curso;
