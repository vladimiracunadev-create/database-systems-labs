-- motor: sqlite
-- doc: https://sqlite.org/partialindex.html
-- nota: el indice tiene DOS entradas, no seis. En una tabla de diez millones de
--       pedidos con mil pendientes, la diferencia entre el indice completo y el
--       parcial es de cuatro ordenes de magnitud, y el parcial cabe en memoria.
--       Para comprobar que se usa: EXPLAIN QUERY PLAN delante de la consulta.

-- === preparacion ===
CREATE TABLE pedidos (
    id     TEXT PRIMARY KEY,
    estado TEXT NOT NULL,
    fecha  TEXT NOT NULL
);
INSERT INTO pedidos (id, estado, fecha) VALUES
    ('P-1', 'entregado', '2026-08-01'),
    ('P-2', 'pendiente', '2026-08-02'),
    ('P-3', 'entregado', '2026-08-03'),
    ('P-4', 'entregado', '2026-08-04'),
    ('P-5', 'pendiente', '2026-08-05'),
    ('P-6', 'entregado', '2026-08-06');

CREATE INDEX pedidos_pendientes ON pedidos (fecha) WHERE estado = 'pendiente';

-- === consulta ===
SELECT id AS pedido, fecha
FROM pedidos
WHERE estado = 'pendiente'
ORDER BY fecha;
