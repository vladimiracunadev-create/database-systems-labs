-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/insert-on-duplicate.html
-- nota: la trampa de esta clausula: se dispara con CUALQUIER clave unica, no
--       solo con la que se tenia en mente. Si la tabla tuviera ademas
--       UNIQUE(correo), una fila con cliente nuevo y correo repetido
--       actualizaria la fila del correo, no insertaria: la carga «idempotente»
--       machacaria un registro distinto del esperado, en silencio.

-- === preparacion ===
DROP TABLE IF EXISTS destino;

CREATE TABLE destino (
    cliente VARCHAR(20) PRIMARY KEY,
    saldo   INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON DUPLICATE KEY UPDATE saldo = VALUES(saldo);

INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON DUPLICATE KEY UPDATE saldo = VALUES(saldo);

-- === consulta ===
SELECT cliente, saldo FROM destino ORDER BY cliente;
