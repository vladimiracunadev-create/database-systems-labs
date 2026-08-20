-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/create-index.html
-- nota: MySQL NO tiene indices parciales. El rodeo estandar es una columna
--       generada que vale NULL en las filas que no interesan —los NULL no
--       ocupan entrada util en el arbol— e indexarla junto a la fecha. Funciona,
--       y hay que explicarlo cada vez que alguien lee el esquema.

-- === preparacion ===
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id     VARCHAR(10) PRIMARY KEY,
    estado VARCHAR(20) NOT NULL,
    fecha  VARCHAR(10) NOT NULL,
    fecha_pendiente VARCHAR(10)
        AS (IF(estado = 'pendiente', fecha, NULL)) STORED,
    KEY pedidos_pendientes (fecha_pendiente)
) ENGINE=InnoDB;

INSERT INTO pedidos (id, estado, fecha) VALUES
    ('P-1', 'entregado', '2026-08-01'),
    ('P-2', 'pendiente', '2026-08-02'),
    ('P-3', 'entregado', '2026-08-03'),
    ('P-4', 'entregado', '2026-08-04'),
    ('P-5', 'pendiente', '2026-08-05'),
    ('P-6', 'entregado', '2026-08-06');

-- === consulta ===
SELECT id AS pedido, fecha
FROM pedidos
WHERE estado = 'pendiente'
ORDER BY fecha;
