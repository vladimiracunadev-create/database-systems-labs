-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/data/partitioning/partitioned_writes.html
-- nota: el equivalente analitico del reparto es escribir Parquet particionado:
--         COPY pedidos TO 'salida' (FORMAT PARQUET, PARTITION_BY (cliente));
--       Y sufre el mismo sesgo: una carpeta con ocho archivos y dos con uno.

-- === preparacion ===
CREATE TABLE pedidos (
    id      INTEGER PRIMARY KEY,
    cliente VARCHAR NOT NULL
);
-- Diez pedidos, tres clientes, y uno de ellos concentra ocho. No es un caso
-- artificial: es la distribucion normal de cualquier negocio real.
INSERT INTO pedidos (id, cliente) VALUES
    (1, 'A'), (2, 'A'), (3, 'A'), (4, 'A'), (5, 'A'),
    (6, 'A'), (7, 'A'), (8, 'A'), (9, 'B'), (10, 'C');

-- === consulta ===
-- Si la clave de particion es el cliente, esto ES el reparto entre nodos: una
-- particion con ocho pedidos y dos con uno. Anadir nodos no arregla nada,
-- porque una clave no se puede partir. Si la clave fuera el id del pedido, el
-- reparto seria 4/3/3 y el problema no existiria... a cambio de que «todos los
-- pedidos del cliente A» pase a ser una consulta a TODOS los nodos.
SELECT cliente AS particion, COUNT(*) AS pedidos
FROM pedidos
GROUP BY cliente
ORDER BY pedidos DESC, cliente;
