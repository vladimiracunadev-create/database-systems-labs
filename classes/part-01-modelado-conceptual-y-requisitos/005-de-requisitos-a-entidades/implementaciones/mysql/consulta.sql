-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/create-table-generated-columns.html
-- nota: sin indices parciales, el rodeo estandar es una columna generada que
--       vale el id del cliente solo cuando la direccion es principal y NULL en
--       el resto. Como los NULL no colisionan en un indice unico, la regla
--       queda igual de firme.

-- === preparacion ===
DROP TABLE IF EXISTS direcciones;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    id     INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE direcciones (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    ciudad     VARCHAR(50) NOT NULL,
    principal  TINYINT(1) NOT NULL DEFAULT 0,
    cliente_principal INT AS (IF(principal = 1, cliente_id, NULL)) STORED,
    UNIQUE KEY una_principal_por_cliente (cliente_principal),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
) ENGINE=InnoDB;

INSERT INTO clientes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO direcciones (cliente_id, ciudad, principal) VALUES
    (1, 'Santiago',   1),
    (1, 'Valdivia',   0),
    (2, 'Valparaiso', 1);
INSERT IGNORE INTO direcciones (cliente_id, ciudad, principal) VALUES (1, 'Arica', 1);

-- === consulta ===
SELECT c.nombre AS cliente,
       COUNT(d.id) AS principales
FROM clientes c
LEFT JOIN direcciones d ON d.cliente_id = c.id AND d.principal = 1
GROUP BY c.id, c.nombre
ORDER BY c.nombre;
