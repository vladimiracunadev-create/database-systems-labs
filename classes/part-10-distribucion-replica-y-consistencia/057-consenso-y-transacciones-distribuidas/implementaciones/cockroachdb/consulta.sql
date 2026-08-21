-- motor: cockroachdb
-- doc: https://www.cockroachlabs.com/docs/stable/transactions
-- nota: implementacion declarada. Misma alternativa que Spanner —transaccion
--       distribuida serializable sobre Raft— con protocolo de PostgreSQL, asi
--       que se puede probar sin reescribir la aplicacion.
--       Lo que SI hay que escribir es el ciclo de reintento: las transacciones
--       que abarcan varios rangos pueden abortarse por conflicto con el codigo
--       de error 40001, y reintentar no es opcional. Parte de la complejidad
--       que la saga hacia explicita vuelve por esta puerta.

-- === preparacion ===
DROP TABLE IF EXISTS reservas;

CREATE TABLE reservas (
    paso   STRING PRIMARY KEY,
    estado STRING NOT NULL
);

-- === consulta ===
--   BEGIN;
--     SAVEPOINT cockroach_restart;      -- punto de reintento
--     INSERT INTO reservas VALUES ('vuelo', 'confirmado');
--     INSERT INTO reservas VALUES ('hotel', 'confirmado');
--     RELEASE SAVEPOINT cockroach_restart;
--   COMMIT;
--
SELECT paso, estado FROM reservas ORDER BY paso;
