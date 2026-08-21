-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/example-auto-increment.html
-- nota: InnoDB organiza FISICAMENTE la tabla por la clave primaria, asi que una
--       clave ancha —un UUID en texto— engorda todos los indices secundarios a
--       la vez. Aqui la eleccion de clave tiene un costo de almacenamiento que
--       en otros motores no tiene.

-- === preparacion ===
DROP TABLE IF EXISTS estudiantes;

-- Dos estudiantes se llaman igual. No es un caso raro: es lo normal en
-- cuanto hay mas de cien personas.
CREATE TABLE estudiantes (
    id     INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    correo VARCHAR(50) NOT NULL UNIQUE
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
