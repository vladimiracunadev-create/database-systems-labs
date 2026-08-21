-- motor: sqlite
-- doc: https://sqlite.org/datatype3.html
-- nota: para ver el problema, basta crear la misma tabla con `precio TEXT` y
--       repetir la consulta: el orden pasa a ser 100, 120, 80.
--       Y el aviso propio de SQLite: sin STRICT, una columna declarada INTEGER
--       acepta un texto si no puede convertirlo, y entonces el orden mezcla
--       criterios.

-- === preparacion ===
-- El precio como NUMERO, no como texto. Sin simbolo de moneda: el simbolo se
-- pone al mostrar, y dentro del dato solo estorba.
CREATE TABLE productos (
    producto TEXT PRIMARY KEY,
    precio   INTEGER NOT NULL CHECK (precio >= 0)
);
INSERT INTO productos (producto, precio) VALUES
    ('teclado', 120),
    ('raton',    80),
    ('cable',   100);

-- === consulta ===
-- Guardados como texto, el orden seria: 100, 120, 80 —porque '1' < '8'— y el
-- producto mas barato saldria el ultimo. Como numeros, el orden es el que
-- cualquiera espera.
SELECT producto, precio FROM productos ORDER BY precio;
