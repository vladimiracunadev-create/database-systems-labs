-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/internals/storage.html
-- nota: aqui la suma lee DOS columnas y ninguna mas, ya comprimidas, en lotes
--       de miles de valores por operacion en vez de una llamada por fila. Es la
--       misma consulta y una arquitectura distinta.
--       Para verlo: EXPLAIN ANALYZE delante de la consulta.

-- === preparacion ===
CREATE TABLE hechos (
    id        INTEGER PRIMARY KEY,
    categoria VARCHAR NOT NULL,
    importe   INTEGER NOT NULL
);

INSERT INTO hechos
SELECT n, 'c' || (n % 2), n FROM generate_series(1, 1000) AS s(n);

-- === consulta ===
SELECT categoria, SUM(importe) AS importe
FROM hechos
GROUP BY categoria
ORDER BY categoria;
