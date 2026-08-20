-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/data_types/list.html
-- nota: LIST es un tipo nativo con tipo interno declarado, no texto: la columna
--       sigue siendo columnar y comprimible.

-- === preparacion ===
CREATE TABLE cursos (
    codigo    VARCHAR PRIMARY KEY,
    etiquetas VARCHAR[] NOT NULL
);

INSERT INTO cursos VALUES
    ('DB-101', ['sql', 'datos']),
    ('SE-201', ['proceso']),
    ('AR-301', ['datos', 'diseno']);

-- === consulta ===
SELECT codigo AS curso
FROM cursos
WHERE list_contains(etiquetas, 'datos')
ORDER BY codigo;
