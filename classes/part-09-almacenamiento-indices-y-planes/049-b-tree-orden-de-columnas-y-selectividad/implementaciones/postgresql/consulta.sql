-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/indexes-multicolumn.html
-- nota: la medicion que cierra la discusion:
--         EXPLAIN (ANALYZE, BUFFERS) SELECT ...
--       Con (curso, nota): «Index Cond» lleva las dos condiciones.
--       Con (nota, curso): la igualdad baja a «Filter» y aparece
--       «Rows Removed by Filter», que es exactamente el trabajo desperdiciado.
--       Y con INCLUDE (estudiante) el indice cubre la consulta entera y el plan
--       pasa a «Index Only Scan»: no se toca la tabla.

-- === preparacion ===
DROP TABLE IF EXISTS notas;

CREATE TABLE notas (
    estudiante text NOT NULL,
    curso      text NOT NULL,
    nota       integer NOT NULL,
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
