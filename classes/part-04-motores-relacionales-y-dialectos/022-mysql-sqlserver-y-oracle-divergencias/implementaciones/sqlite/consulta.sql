-- motor: sqlite
-- doc: https://sqlite.org/datatype3.html
-- nota: la intercalacion por omision es BINARY: compara byte a byte. Cambiar
--       la columna a `TEXT COLLATE NOCASE` haria que esta consulta devolviera 2.

-- === preparacion ===
CREATE TABLE registros (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);
INSERT INTO registros (id, nombre) VALUES (1, 'Ada'), (2, 'ada'), (3, 'ADA'), (4, 'Linus');

-- === consulta ===
-- Cuantos nombres DISTINTOS hay. La respuesta correcta depende de algo que no
-- esta en la consulta: la intercalacion de la columna.
SELECT COUNT(DISTINCT nombre) AS distintos FROM registros;
