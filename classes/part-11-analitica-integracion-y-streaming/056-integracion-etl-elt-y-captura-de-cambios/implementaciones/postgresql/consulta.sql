-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-insert.html
-- nota: la captura de cambios de PostgreSQL sale del WAL por decodificacion
--       logica, sin disparadores ni consultas periodicas:
--         CREATE PUBLICATION integracion FOR TABLE destino;
--         SELECT pg_create_logical_replication_slot('cdc', 'pgoutput');
--       Y el aviso que cuesta un incidente: una RANURA que nadie consume
--       retiene el WAL indefinidamente y llena el disco del primario. Vigilar
--       pg_replication_slots forma parte de operar una integracion.

-- === preparacion ===
DROP TABLE IF EXISTS destino;

CREATE TABLE destino (
    cliente text PRIMARY KEY,
    saldo   integer NOT NULL
);

INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- === consulta ===
SELECT cliente, saldo FROM destino ORDER BY cliente;
