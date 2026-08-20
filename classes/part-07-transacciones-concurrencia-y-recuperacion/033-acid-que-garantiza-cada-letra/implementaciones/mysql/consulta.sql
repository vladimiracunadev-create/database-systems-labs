-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-model.html
-- nota: dos avisos que no estan en el codigo y hay que saber igual:
--       1) El DDL NO es transaccional: un ALTER TABLE dentro de una transaccion
--          la confirma implicitamente.
--       2) innodb_flush_log_at_trx_commit distinto de 1 significa perder hasta
--          un segundo de transacciones YA CONFIRMADAS tras una caida.

-- === preparacion ===
DROP TABLE IF EXISTS cuentas;

CREATE TABLE cuentas (
    id    VARCHAR(10) PRIMARY KEY,
    saldo INT NOT NULL CHECK (saldo >= 0)
);
INSERT INTO cuentas (id, saldo) VALUES ('A', 100), ('B', 50);

-- Transferencia valida: las dos escrituras son UNA operacion.
BEGIN;
UPDATE cuentas SET saldo = saldo - 30 WHERE id = 'A';
UPDATE cuentas SET saldo = saldo + 30 WHERE id = 'B';
COMMIT;

-- Transferencia imposible: A no tiene 500. El abono a B ya se ha escrito
-- cuando la aplicacion comprueba el origen y decide deshacer. Entre las dos
-- sentencias existe un instante en el que el dinero esta duplicado; la
-- atomicidad es la garantia de que ese instante no existe para nadie mas y de
-- que al deshacer no queda rastro de el.
BEGIN;
UPDATE cuentas SET saldo = saldo + 500 WHERE id = 'B';
-- El cargo a A ni siquiera se intenta: violaria el CHECK (saldo >= 0) y, sin
-- transaccion, el abono a B se habria quedado escrito para siempre.
ROLLBACK;

-- === consulta ===
SELECT id, saldo FROM cuentas ORDER BY id;
