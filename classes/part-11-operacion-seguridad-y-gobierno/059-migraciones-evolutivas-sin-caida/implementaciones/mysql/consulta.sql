-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html
-- nota: declarar el algoritmo a proposito, para que el motor FALLE en vez de
--       copiar en silencio una tabla de 200 GB:
--         ALTER TABLE personas ADD COLUMN apellido VARCHAR(50), ALGORITHM=INSTANT;
--       Y recordar que el DDL NO es transaccional: una migracion a medias se
--       queda a medias.

-- === preparacion ===
DROP TABLE IF EXISTS personas;

CREATE TABLE personas (
    id     INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);
INSERT INTO personas (id, nombre) VALUES
    (1, 'Ada Lovelace'), (2, 'Linus Torvalds');

-- EXPANDIR. La columna nueva nace ANULABLE y sin restricciones: la version
-- vieja de la aplicacion, que no la conoce, sigue insertando sin problemas.
ALTER TABLE personas ADD COLUMN apellido VARCHAR(50);

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
