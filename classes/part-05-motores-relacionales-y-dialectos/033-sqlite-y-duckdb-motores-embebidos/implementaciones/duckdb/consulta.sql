-- motor: duckdb
-- doc: https://duckdb.org/why_duckdb
-- nota: guarda COLUMNAS. Este agregado lee la columna `nota` y la columna
--       `curso`, y ninguna otra. Ademas, la misma consulta funciona sobre un
--       archivo sin cargarlo:
--         SELECT curso, COUNT(*), SUM(nota) FROM 'notas.parquet' GROUP BY curso;

-- === preparacion ===
CREATE TABLE notas (
    estudiante VARCHAR NOT NULL,
    curso      VARCHAR NOT NULL,
    nota       INTEGER NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
INSERT INTO notas (estudiante, curso, nota) VALUES
    ('Ada',   'DB-101', 90),
    ('Grace', 'DB-101', 72),
    ('Linus', 'DB-101', 58),
    ('Ada',   'SE-201', 66);

-- === consulta ===
SELECT curso, COUNT(*) AS filas, SUM(nota) AS suma
FROM notas
GROUP BY curso
ORDER BY curso;
