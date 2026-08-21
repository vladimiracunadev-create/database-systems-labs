-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/functions/timestamp.html
-- nota: aqui la marca SI es un TIMESTAMP de verdad, y time_bucket admite
--       ventanas arbitrarias:
--         time_bucket(INTERVAL '15 minutes', momento)
--       La misma consulta funciona sobre un Parquet sin cargarlo.

-- === preparacion ===
CREATE TABLE lecturas (
    momento TIMESTAMP NOT NULL,
    valor   INTEGER NOT NULL
);
INSERT INTO lecturas VALUES
    ('2026-08-19 10:00:00', 20),
    ('2026-08-19 10:15:00', 21),
    ('2026-08-19 10:45:00', 25),
    ('2026-08-19 11:05:00', 22),
    ('2026-08-19 11:30:00', 23);

-- === consulta ===
SELECT strftime(time_bucket(INTERVAL '1 hour', momento), '%Y-%m-%d %H:%M') AS hora,
       SUM(valor) AS total
FROM lecturas
GROUP BY hora
ORDER BY hora;
