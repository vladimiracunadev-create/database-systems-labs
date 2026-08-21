-- motor: sqlite
-- doc: https://sqlite.org/lang_createtable.html
-- nota: INTEGER PRIMARY KEY es un alias del identificador interno de fila, asi
--       que la identidad estable no cuesta ni una columna adicional.

-- === preparacion ===
-- Dos estudiantes se llaman igual. No es un caso raro: es lo normal en
-- cuanto hay mas de cien personas.
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE
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
