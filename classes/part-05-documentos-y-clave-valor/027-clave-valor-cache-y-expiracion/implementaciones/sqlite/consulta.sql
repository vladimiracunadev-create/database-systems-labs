-- motor: sqlite
-- doc: https://sqlite.org/lang_datefunc.html
-- nota: esta es la version larga de lo que Redis hace con una letra. La
--       caducidad son tres cosas que hay que escribir a mano: la columna, el
--       filtro en CADA lectura y el borrado periodico
--         DELETE FROM cache WHERE expira_en IS NOT NULL AND expira_en <= datetime('now');
--       Olvidar cualquiera de las tres deja datos vencidos a la vista.

-- === preparacion ===
CREATE TABLE cache (
    clave     TEXT PRIMARY KEY,
    valor     TEXT NOT NULL,
    expira_en TEXT          -- nulo = sin caducidad
);

INSERT INTO cache (clave, valor, expira_en) VALUES
    ('k1', 'con caducidad', '2099-01-01T00:00:00Z'),
    ('k2', 'permanente',    NULL);
-- k3 no se inserta: la ausencia tambien es un estado, y hay que distinguirla.

-- === consulta ===
-- Los tres estados que un almacen clave-valor con caducidad distingue, y que
-- aqui hay que reconstruir a mano porque el motor no los conoce.
WITH consultadas(clave) AS (
    VALUES ('k1'), ('k2'), ('k3')
)
SELECT c.clave,
       CASE
           WHEN e.clave IS NULL     THEN 'ausente'
           WHEN e.expira_en IS NULL THEN 'permanente'
           ELSE 'expira'
       END AS estado
FROM consultadas c
LEFT JOIN cache e ON e.clave = c.clave
ORDER BY c.clave;
