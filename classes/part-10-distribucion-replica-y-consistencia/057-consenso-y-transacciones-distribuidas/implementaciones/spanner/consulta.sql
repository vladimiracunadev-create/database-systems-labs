-- motor: spanner
-- doc: https://cloud.google.com/spanner/docs/transactions
-- nota: implementacion declarada, y deliberadamente distinta: aqui NO hay saga.
--       Si los dos datos caben en el mismo sistema, Spanner ofrece la
--       alternativa que la saga sustituye: una transaccion distribuida de
--       verdad, serializable, con confirmacion en dos fases sobre Paxos. El
--       coordinador tambien esta replicado por consenso, asi que no puede
--       quedarse colgado como el coordinador XA del que huye la saga.
--
--       Y el limite, que es el que importa: esto solo vale si los dos servicios
--       COMPARTEN base de datos. Una arquitectura de servicios independientes
--       evita eso a proposito, y por eso la saga sigue existiendo.

-- === preparacion ===
CREATE TABLE reservas (
    paso   STRING(MAX) NOT NULL,
    estado STRING(MAX) NOT NULL,
) PRIMARY KEY (paso);

-- === consulta ===
-- Una sola transaccion para las dos reservas. Si la segunda falla, la primera
-- NO ocurrio: no hay estado intermedio observable y no hay nada que compensar.
--
--   BEGIN;
--     INSERT INTO reservas (paso, estado) VALUES ('vuelo', 'confirmado');
--     INSERT INTO reservas (paso, estado) VALUES ('hotel', 'confirmado');
--   COMMIT;   -- o ROLLBACK entero
--
SELECT paso, estado FROM reservas ORDER BY paso;
