-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-identity-columns.html
-- nota: las dos identidades conviven y las dos hacen falta:
--         id     integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY  -- referencias
--         correo text NOT NULL UNIQUE                              -- negocio
--       Aqui el id se escribe a mano para que las filas sean comparables con
--       las de los demas motores.

-- === preparacion ===
DROP TABLE IF EXISTS estudiantes;

-- Dos estudiantes se llaman igual. No es un caso raro: es lo normal en
-- cuanto hay mas de cien personas.
CREATE TABLE estudiantes (
    id     integer PRIMARY KEY,
    nombre text NOT NULL,
    correo text NOT NULL UNIQUE
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
