-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/data_types/struct.html
-- nota: aqui lo anidado no es texto: STRUCT y LIST son tipos con tipo interno
--       declarado, asi que la columna sigue siendo columnar y UNNEST la abre
--       sin analizar ninguna cadena.

-- === preparacion ===
CREATE TABLE pedidos (
    id     VARCHAR PRIMARY KEY,
    lineas STRUCT(producto VARCHAR, importe INTEGER)[]
);

INSERT INTO pedidos VALUES ('P-1', [
    {'producto': 'teclado', 'importe': 120},
    {'producto': 'raton',   'importe': 80},
    {'producto': 'cable',   'importe': 100}
]);

-- === consulta ===
SELECT l.producto, l.importe
FROM (SELECT UNNEST(lineas) AS l FROM pedidos WHERE id = 'P-1')
ORDER BY l.producto;
