-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/unnest.html
-- nota: la misma consulta funciona sobre un fichero anidado sin cargarlo:
--         SELECT ... FROM read_json_auto('pedidos.json'), UNNEST(lineas) ...

-- === preparacion ===
CREATE TABLE pedidos (
    id     VARCHAR PRIMARY KEY,
    lineas STRUCT(producto VARCHAR, categoria VARCHAR, importe INTEGER)[]
);

INSERT INTO pedidos VALUES
    ('P-1', [{'producto': 'teclado', 'categoria': 'perifericos', 'importe': 120},
             {'producto': 'raton',   'categoria': 'accesorios',  'importe': 80}]),
    ('P-2', [{'producto': 'cable',   'categoria': 'accesorios',  'importe': 100}]);

-- === consulta ===
SELECT l.categoria, SUM(l.importe) AS importe
FROM (SELECT UNNEST(lineas) AS l FROM pedidos)
GROUP BY l.categoria
ORDER BY l.categoria;
