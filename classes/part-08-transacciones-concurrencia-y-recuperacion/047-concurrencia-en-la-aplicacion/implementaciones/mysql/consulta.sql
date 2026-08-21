-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/information-functions.html
-- nota: ROW_COUNT() detecta el conflicto, con una trampa: por omision cuenta las
--       filas CAMBIADAS, no las coincidentes. Un UPDATE que escribe el mismo
--       valor devuelve 0 y parece un conflicto inexistente. Depende de la
--       bandera CLIENT_FOUND_ROWS del conector.

-- === preparacion ===
DROP TABLE IF EXISTS cuentas;

CREATE TABLE cuentas (
    id      VARCHAR(20) PRIMARY KEY,
    saldo   INT NOT NULL,
    version INT NOT NULL
);
INSERT INTO cuentas (id, saldo, version) VALUES ('cuenta-1', 100, 1);

-- Cliente A leyo la cuenta (saldo 100, version 1) y descuenta 30.
-- La condicion `version = 1` es el contrato: «escribo solo si nadie ha tocado
-- esto desde que lo lei».
UPDATE cuentas
SET saldo = saldo - 30, version = version + 1
WHERE id = 'cuenta-1' AND version = 1;

-- Cliente B habia leido la MISMA version 1, antes de que A escribiera, y
-- descuenta 50. Su UPDATE no afecta a ninguna fila: la version ya no es 1.
-- Sin esta condicion, el descuento de A se perderia en silencio y el saldo
-- quedaria en 50 en vez de 70: eso es una ACTUALIZACION PERDIDA.
UPDATE cuentas
SET saldo = saldo - 50, version = version + 1
WHERE id = 'cuenta-1' AND version = 1;

-- === consulta ===
-- Si saliera 20 y version 3, los dos habrian escrito. Si saliera 50, se habria
-- perdido el descuento de A. Que salga 70 y version 2 es la prueba de que
-- exactamente uno gano y el otro se entero.
SELECT id, saldo, version FROM cuentas ORDER BY id;
