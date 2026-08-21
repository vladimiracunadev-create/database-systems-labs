-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/constraints.html
-- nota: DuckDB no tiene INSERT OR IGNORE; la forma equivalente es
--       ON CONFLICT DO NOTHING, que es tambien la del estandar reciente.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    correo VARCHAR NOT NULL UNIQUE
);

INSERT INTO estudiantes VALUES (1, 'ada@example.org');
INSERT INTO estudiantes VALUES (2, 'linus@example.org');
INSERT INTO estudiantes VALUES (3, 'ada@example.org') ON CONFLICT DO NOTHING;

-- === consulta ===
SELECT correo FROM estudiantes ORDER BY correo;
