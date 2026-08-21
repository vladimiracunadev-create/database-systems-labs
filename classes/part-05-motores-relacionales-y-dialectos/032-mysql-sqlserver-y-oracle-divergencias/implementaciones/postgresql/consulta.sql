-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/collation.html
-- nota: la comparacion por omision distingue mayusculas. Lo que hay que vigilar
--       aqui es otra cosa: la intercalacion viene de la biblioteca del sistema,
--       y una actualizacion de glibc puede cambiar el orden y dejar los indices
--       B-Tree de texto en un estado incoherente. De ahi el proveedor `icu`.

-- === preparacion ===
DROP TABLE IF EXISTS registros;

CREATE TABLE registros (
    id     integer PRIMARY KEY,
    nombre text NOT NULL
);
INSERT INTO registros (id, nombre) VALUES (1, 'Ada'), (2, 'ada'), (3, 'ADA'), (4, 'Linus');

-- === consulta ===
-- Cuantos nombres DISTINTOS hay. La respuesta correcta depende de algo que no
-- esta en la consulta: la intercalacion de la columna.
SELECT COUNT(DISTINCT nombre) AS distintos FROM registros;
