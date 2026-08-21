-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/orderby
-- nota: aqui quitar el ORDER BY si cambia el orden entre ejecuciones, porque el
--       motor lee en paralelo por trozos. Es la mejor demostracion de que una
--       tabla no tiene orden.

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
    ('Ada',   'SE-201', 66);

-- === consulta ===
-- Tres decisiones separadas: que filas (WHERE), que columnas (SELECT) y en que
-- orden se leen (ORDER BY). El orden hay que PEDIRLO: una tabla no lo tiene.
SELECT estudiante, nota
FROM notas
WHERE curso = 'DB-101' AND nota >= 60
ORDER BY estudiante;
