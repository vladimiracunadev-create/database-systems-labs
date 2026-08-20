-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/expressions/collations.html
-- nota: al analizar un volcado que viene de MySQL, este recuento NO coincide
--       con el del origen. No es un fallo: es la intercalacion.

-- === preparacion ===
CREATE TABLE registros (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL
);
INSERT INTO registros (id, nombre) VALUES (1, 'Ada'), (2, 'ada'), (3, 'ADA'), (4, 'Linus');

-- === consulta ===
-- Cuantos nombres DISTINTOS hay. La respuesta correcta depende de algo que no
-- esta en la consulta: la intercalacion de la columna.
SELECT COUNT(DISTINCT nombre) AS distintos FROM registros;
