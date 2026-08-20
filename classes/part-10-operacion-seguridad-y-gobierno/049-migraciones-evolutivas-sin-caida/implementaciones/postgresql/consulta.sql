-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-altertable.html
-- nota: casi todo ALTER TABLE pide un bloqueo ACCESS EXCLUSIVE, aunque sea un
--       instante. Si hay una consulta larga en marcha, el ALTER espera Y TODO
--       LO QUE LLEGUE DETRAS ESPERA CON EL. La forma segura es:
--         SET lock_timeout = '3s';
--         ALTER TABLE personas ADD COLUMN apellido text;
--       y reintentar si falla, en vez de confiar en que sera rapido.

-- === preparacion ===
DROP TABLE IF EXISTS personas;

CREATE TABLE personas (
    id     integer PRIMARY KEY,
    nombre text NOT NULL
);
INSERT INTO personas (id, nombre) VALUES
    (1, 'Ada Lovelace'), (2, 'Linus Torvalds');

-- EXPANDIR. La columna nueva nace ANULABLE y sin restricciones: la version
-- vieja de la aplicacion, que no la conoce, sigue insertando sin problemas.
ALTER TABLE personas ADD COLUMN apellido text;

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
