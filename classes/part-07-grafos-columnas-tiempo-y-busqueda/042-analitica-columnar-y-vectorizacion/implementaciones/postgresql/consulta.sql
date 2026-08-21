-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/parallel-query.html
-- nota: el punto intermedio. Filas en disco, pero con agregacion en paralelo
--       (Parallel Seq Scan + Partial Aggregate + Gather) cuando la tabla es lo
--       bastante grande. Para verlo hacen falta mas de mil filas y
--         SET max_parallel_workers_per_gather = 4;
--         EXPLAIN (ANALYZE) SELECT ...

-- === preparacion ===
DROP TABLE IF EXISTS hechos;

CREATE TABLE hechos (
    id        integer PRIMARY KEY,
    categoria text NOT NULL,
    importe   integer NOT NULL
);

INSERT INTO hechos (id, categoria, importe)
SELECT n, 'c' || (n % 2), n FROM generate_series(1, 1000) AS s(n);

-- === consulta ===
SELECT categoria, SUM(importe) AS importe
FROM hechos
GROUP BY categoria
ORDER BY categoria;
