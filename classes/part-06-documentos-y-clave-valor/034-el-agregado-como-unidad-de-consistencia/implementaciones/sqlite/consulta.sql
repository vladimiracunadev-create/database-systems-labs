-- motor: sqlite
-- doc: https://sqlite.org/lang_transaction.html
-- nota: el limite del agregado es una CONVENCION, no una propiedad del
--       esquema. Nada impide un UPDATE suelto que rompa el invariante.

-- === preparacion ===
CREATE TABLE pedidos (
    id    TEXT PRIMARY KEY,
    total INTEGER NOT NULL
);
CREATE TABLE lineas (
    pedido_id TEXT NOT NULL REFERENCES pedidos(id),
    producto  TEXT NOT NULL,
    importe   INTEGER NOT NULL,
    PRIMARY KEY (pedido_id, producto)
);

-- El agregado nace entero, dentro de UNA transaccion.
BEGIN;
INSERT INTO pedidos (id, total) VALUES ('P-1', 200);
INSERT INTO lineas (pedido_id, producto, importe) VALUES ('P-1', 'teclado', 120);
INSERT INTO lineas (pedido_id, producto, importe) VALUES ('P-1', 'raton', 80);
COMMIT;

-- Y cambia entero: la linea nueva y el total suben juntos o no sube ninguno.
BEGIN;
INSERT INTO lineas (pedido_id, producto, importe) VALUES ('P-1', 'cable', 100);
UPDATE pedidos SET total = total + 100 WHERE id = 'P-1';
COMMIT;

-- === consulta ===
-- El invariante del agregado: el total guardado y la suma de sus lineas. Si
-- alguna vez dejan de coincidir, la transaccion no estaba haciendo su trabajo.
SELECT p.id AS pedido,
       p.total AS total_guardado,
       (SELECT SUM(l.importe) FROM lineas l WHERE l.pedido_id = p.id) AS total_calculado
FROM pedidos p
ORDER BY p.id;
