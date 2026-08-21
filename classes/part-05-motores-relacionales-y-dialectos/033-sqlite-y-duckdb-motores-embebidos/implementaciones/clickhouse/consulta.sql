-- motor: clickhouse
-- doc: https://clickhouse.com/docs/en/operations/utilities/clickhouse-local
-- nota: implementacion declarada. Se ejecuta con `clickhouse-local`, sin
--       servidor ni configuracion:
--         clickhouse-local --queries-file consulta.sql
--       Sirve para ver que «embebido» y «columnar» son dos ejes distintos:
--       SQLite es embebido y de filas, DuckDB embebido y columnar, ClickHouse
--       servidor columnar... y tambien columnar sin servidor con esta utilidad.

-- === preparacion ===
CREATE TABLE notas (
    estudiante String,
    curso      String,
    nota       Int32
) ENGINE = MergeTree ORDER BY (curso, estudiante);

INSERT INTO notas VALUES
    ('Ada',   'DB-101', 90),
    ('Grace', 'DB-101', 72),
    ('Linus', 'DB-101', 58),
    ('Ada',   'SE-201', 66);

-- === consulta ===
SELECT curso, COUNT(*) AS filas, SUM(nota) AS suma
FROM notas
GROUP BY curso
ORDER BY curso;
