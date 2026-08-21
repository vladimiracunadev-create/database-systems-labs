-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/sql-mode.html
-- nota: con el modo estricto —el valor por omision desde 5.7— un valor fuera de
--       rango se RECHAZA. Sin el, se recortaba en silencio: hay tablas antiguas
--       llenas de ceros que en realidad significan «no se pudo convertir».

-- === preparacion ===
DROP TABLE IF EXISTS productos;

-- El precio como NUMERO, no como texto. Sin simbolo de moneda: el simbolo se
-- pone al mostrar, y dentro del dato solo estorba.
CREATE TABLE productos (
    producto VARCHAR(50) PRIMARY KEY,
    precio   INT NOT NULL CHECK (precio >= 0)
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
