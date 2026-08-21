-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/datatype.html
-- nota: es el mas severo de la lista, y eso evita errores: se niega a comparar
--       un texto con un numero en vez de convertir por su cuenta. Para dinero,
--       `numeric` es de precision arbitraria y suma sin error.

-- === preparacion ===
DROP TABLE IF EXISTS productos;

-- El precio como NUMERO, no como texto. Sin simbolo de moneda: el simbolo se
-- pone al mostrar, y dentro del dato solo estorba.
CREATE TABLE productos (
    producto text PRIMARY KEY,
    precio   integer NOT NULL CHECK (precio >= 0)
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
