-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html
-- nota: implementacion declarada. Las transacciones ligeras hacen exactamente
--       esto, con acuerdo entre replicas mediante Paxos, y devuelven una columna
--       [applied] con true o false.
--       El precio no es menor: cuatro rondas de red entre replicas, del orden de
--       VEINTE VECES el costo de una escritura normal. En el camino caliente,
--       convierten un cluster de Cassandra en algo mas lento que un solo
--       PostgreSQL.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS banca
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS banca.cuentas;

CREATE TABLE banca.cuentas (
    id      text PRIMARY KEY,
    saldo   int,
    version int
);

INSERT INTO banca.cuentas (id, saldo, version) VALUES ('cuenta-1', 100, 1);

-- Cliente A: gana. Devuelve [applied] = True.
UPDATE banca.cuentas SET saldo = 70, version = 2 WHERE id = 'cuenta-1' IF version = 1;

-- Cliente B: pierde. Devuelve [applied] = False y, ademas, el valor actual de
-- la columna comparada, para que el cliente pueda reintentar sin releer.
UPDATE banca.cuentas SET saldo = 50, version = 2 WHERE id = 'cuenta-1' IF version = 1;

-- === consulta ===
SELECT id, saldo, version FROM banca.cuentas;
