-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/constraints
-- nota: la comprobacion que hay que hacer ANTES de declarar una clave sobre
--       datos que ya existen:
--         SELECT correo, COUNT(*) FROM estudiantes
--         GROUP BY correo HAVING COUNT(*) > 1;
--       Si devuelve filas, la clave no se puede crear todavia.

-- === preparacion ===
-- Dos estudiantes se llaman igual. No es un caso raro: es lo normal en
-- cuanto hay mas de cien personas.
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    correo VARCHAR NOT NULL UNIQUE
);
INSERT INTO estudiantes (id, nombre, correo) VALUES
    (1, 'Ada',   'ada@example.org'),
    (2, 'Ada',   'ada2@example.org'),
    (3, 'Linus', 'linus@example.org');

-- Corregir el correo de la SEGUNDA Ada. Con el id se puede senalar a una fila
-- concreta; con el nombre no:
--   UPDATE estudiantes SET correo = ... WHERE nombre = 'Ada';
-- habria cambiado las dos, y ademas habria fallado por violar el UNIQUE.
UPDATE estudiantes SET correo = 'nuevo@example.org' WHERE id = 2;

-- === consulta ===
SELECT id, nombre, correo FROM estudiantes ORDER BY id;
