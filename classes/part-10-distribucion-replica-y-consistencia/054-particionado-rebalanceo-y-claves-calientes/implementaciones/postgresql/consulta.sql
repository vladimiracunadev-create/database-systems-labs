-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-partitioning.html
-- nota: con particionado declarativo, el sesgo se puede ver directamente en el
--       tamano de cada particion:
--         SELECT relname, pg_size_pretty(pg_relation_size(oid))
--         FROM pg_class WHERE relname LIKE 'pedidos_%';

-- === preparacion ===
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id      integer PRIMARY KEY,
    cliente text NOT NULL
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
