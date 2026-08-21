-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/indexes.html
-- nota: aqui el indice apenas cambia nada, y esa es la comparacion. El filtro se
--       resuelve leyendo la columna comprimida y descartando bloques por sus
--       valores minimo y maximo: no hay arbol que recorrer.

-- === preparacion ===
CREATE TABLE notas (
    estudiante VARCHAR NOT NULL,
    curso      VARCHAR NOT NULL,
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
