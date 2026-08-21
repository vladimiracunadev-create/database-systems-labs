-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/data_types/numeric
-- nota: aqui el tipo se comprueba siempre: INSERT INTO productos VALUES
--       ('x', 'alto') falla. Y para dinero con centimos, el tipo correcto es
--       DECIMAL(10,2), no un numero de coma flotante: 0.1 + 0.2 no da 0.3.

-- === preparacion ===
-- El precio como NUMERO, no como texto. Sin simbolo de moneda: el simbolo se
-- pone al mostrar, y dentro del dato solo estorba.
CREATE TABLE productos (
    producto VARCHAR PRIMARY KEY,
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
