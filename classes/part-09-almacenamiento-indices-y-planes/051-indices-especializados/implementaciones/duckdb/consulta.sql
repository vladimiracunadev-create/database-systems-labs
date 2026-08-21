-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/indexes.html
-- nota: aqui no se crea ningun indice, y es a proposito. Cada grupo de filas
--       guarda el minimo y el maximo de cada columna, asi que descartar bloques
--       enteros es gratis: es la idea de BRIN aplicada por omision a todo.
--       Con una condicion: los datos tienen que estar ORDENADOS por la columna
--       que se filtra. Si no, no se descarta nada.

-- === preparacion ===
CREATE TABLE pedidos (
    id     VARCHAR PRIMARY KEY,
    estado VARCHAR NOT NULL,
    fecha  VARCHAR NOT NULL
);
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
