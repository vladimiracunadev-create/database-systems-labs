-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/dialect/postgresql_compatibility.html

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
SELECT estudiante || ' - ' || curso AS etiqueta
FROM notas
WHERE curso = 'DB-101'
ORDER BY nota DESC
LIMIT 2;
