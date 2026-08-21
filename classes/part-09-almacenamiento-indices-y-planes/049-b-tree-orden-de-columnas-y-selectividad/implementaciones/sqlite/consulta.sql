-- motor: sqlite
-- doc: https://sqlite.org/optoverview.html
-- nota: para comprobarlo, anteponer EXPLAIN QUERY PLAN a la consulta:
--         SEARCH notas USING INDEX notas_curso_nota (curso=? AND nota>? AND nota<?)
--       Con el indice creado como (nota, curso) la misma linea diria
--         SEARCH notas USING INDEX ... (nota>? AND nota<?)
--       sin la igualdad: el motor recorreria las notas de TODOS los cursos.

-- === preparacion ===
CREATE TABLE notas (
    estudiante TEXT NOT NULL,
    curso      TEXT NOT NULL,
    nota       INTEGER NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
INSERT INTO notas (estudiante, curso, nota) VALUES
    ('Ada',   'DB-101', 90),
    ('Linus', 'DB-101', 58),
    ('Grace', 'DB-101', 72),
    ('Bob',   'DB-101', 61),
    ('Ada',   'SE-201', 66),
    ('Grace', 'SE-201', 78);

-- El orden de las columnas del indice NO es una preferencia de estilo. Con
-- (curso, nota) el motor entra por la igualdad y recorre un RANGO CONTIGUO de
-- notas. Con (nota, curso) tendria que recorrer todas las notas entre 60 y 90 de
-- TODOS los cursos y filtrar despues.
CREATE INDEX notas_curso_nota ON notas (curso, nota);

-- === consulta ===
SELECT estudiante, nota
FROM notas
WHERE curso = 'DB-101' AND nota BETWEEN 60 AND 90
ORDER BY nota, estudiante;
