-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/indexes-types.html
-- nota: el indice de abajo es PARCIAL y ademas CUBRIENTE: con INCLUDE (id), el
--       plan pasa a «Index Only Scan» y no toca la tabla en ningun momento.
--       El resto del catalogo, para tenerlo a la vista:
--         GIN   arreglos, jsonb, busqueda de texto
--         GiST  geometria, rangos, vecino mas cercano
--         BRIN  tablas enormes ya ordenadas por la columna (fechas, series)
--         HASH  solo igualdad, sin orden ni rangos

-- === preparacion ===
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id     text PRIMARY KEY,
    estado text NOT NULL,
    fecha  text NOT NULL
);
INSERT INTO pedidos (id, estado, fecha) VALUES
    ('P-1', 'entregado', '2026-08-01'),
    ('P-2', 'pendiente', '2026-08-02'),
    ('P-3', 'entregado', '2026-08-03'),
    ('P-4', 'entregado', '2026-08-04'),
    ('P-5', 'pendiente', '2026-08-05'),
    ('P-6', 'entregado', '2026-08-06');

CREATE INDEX pedidos_pendientes ON pedidos (fecha) INCLUDE (id)
    WHERE estado = 'pendiente';

-- === consulta ===
SELECT id AS pedido, fecha
FROM pedidos
WHERE estado = 'pendiente'
ORDER BY fecha;
