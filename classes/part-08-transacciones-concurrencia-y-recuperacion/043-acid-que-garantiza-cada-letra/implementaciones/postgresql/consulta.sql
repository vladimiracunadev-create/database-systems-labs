-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/tutorial-transactions.html
-- nota: aqui el DDL tambien es transaccional. Esto es legal y se deshace entero:
--         BEGIN; ALTER TABLE cuentas ADD COLUMN divisa text; ROLLBACK;
--       En MySQL y en Oracle, ese ALTER confirma la transaccion y no hay vuelta
--       atras. Es la razon por la que las migraciones de esquema son mucho mas
--       seguras en PostgreSQL.

-- === preparacion ===
DROP TABLE IF EXISTS cuentas;

CREATE TABLE cuentas (
    id    text PRIMARY KEY,
    saldo integer NOT NULL CHECK (saldo >= 0)
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
