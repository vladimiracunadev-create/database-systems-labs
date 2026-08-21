-- motor: sqlite
-- doc: https://sqlite.org/lang_createtable.html
-- nota: la clave primaria compuesta impide que la misma inscripcion se guarde
--       dos veces. En una hoja de calculo, nada lo impide.

-- === preparacion ===
-- Un hecho por fila. La hoja de calculo guardaba «DB-101, SE-201» en una
-- celda; aqui cada inscripcion es una fila propia, y contar deja de ser buscar
-- texto.
CREATE TABLE inscripciones (
    estudiante TEXT NOT NULL,
    curso      TEXT NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
INSERT INTO inscripciones (estudiante, curso) VALUES
    ('Ada',   'DB-101'),
    ('Ada',   'SE-201'),
    ('Linus', 'DB-101');

-- === consulta ===
SELECT estudiante, curso FROM inscripciones ORDER BY estudiante, curso;
