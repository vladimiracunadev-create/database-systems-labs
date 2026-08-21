-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/alter_table
-- nota: la consulta util antes de migrar es esta otra, sobre una copia de los
--       datos reales:
--         SELECT COUNT(*) FILTER (WHERE apellido IS NULL) AS sin_apellido,
--                COUNT(*) AS total FROM personas;
--       Migrar sin esa cuenta es empezar a ciegas.

-- === preparacion ===
CREATE TABLE personas (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL
);
INSERT INTO personas (id, nombre) VALUES
    (1, 'Ada Lovelace'), (2, 'Linus Torvalds');

-- EXPANDIR. La columna nueva nace ANULABLE y sin restricciones: la version
-- vieja de la aplicacion, que no la conoce, sigue insertando sin problemas.
ALTER TABLE personas ADD COLUMN apellido VARCHAR;

-- MIGRAR. Se rellena por lotes, sin bloquear la tabla entera. Mientras dura,
-- conviven las dos versiones del codigo: la vieja escribe solo `nombre` y la
-- nueva escribe las dos columnas.
UPDATE personas SET apellido = 'Lovelace' WHERE id = 1;
UPDATE personas SET apellido = 'Torvalds' WHERE id = 2;

-- CONTRAER. Solo cuando NO queda nadie ejecutando la version vieja se puede
-- endurecer la columna o retirar la antigua. Ese «solo cuando» es la parte que
-- se salta todo el mundo, y es la que produce la caida.
INSERT INTO personas (id, nombre, apellido) VALUES (3, 'Grace Hopper', 'Hopper');

-- === consulta ===
SELECT id, apellido FROM personas ORDER BY id;
