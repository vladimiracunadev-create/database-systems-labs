-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/data-modeling_logical.html
-- nota: implementacion declarada. Aqui el reparto NO es una consulta: es la
--       clave primaria. `cliente` como clave de particion significa que los
--       ocho pedidos de A viven en el mismo nodo, y que anadir nodos no reparte
--       ese trabajo: una clave no se puede partir.
--
--       La correccion documentada es anadir un componente a la clave de
--       particion —el mes, un cubo numerico— y aceptar que las consultas
--       tendran que recorrerlos:
--         PRIMARY KEY ((cliente, mes), id)
--       Cambiarlo despues obliga a reescribir los datos.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS ventas
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS ventas.pedidos_por_cliente;

CREATE TABLE ventas.pedidos_por_cliente (
    cliente text,
    id      int,
    PRIMARY KEY (cliente, id)
);

INSERT INTO ventas.pedidos_por_cliente (cliente, id) VALUES ('A', 1);
INSERT INTO ventas.pedidos_por_cliente (cliente, id) VALUES ('A', 2);
INSERT INTO ventas.pedidos_por_cliente (cliente, id) VALUES ('B', 9);
INSERT INTO ventas.pedidos_por_cliente (cliente, id) VALUES ('C', 10);

-- === consulta ===
-- El token es lo que decide el nodo. Esta consulta muestra el reparto real:
SELECT cliente, token(cliente) AS token, COUNT(*) AS pedidos
FROM ventas.pedidos_por_cliente
GROUP BY cliente;

-- Y la herramienta que delata las particiones grandes desde fuera:
--   nodetool tablehistograms ventas.pedidos_por_cliente
