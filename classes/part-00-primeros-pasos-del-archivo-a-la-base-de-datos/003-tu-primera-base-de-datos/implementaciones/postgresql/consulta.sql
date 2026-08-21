-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-insert.html
-- nota: en cuanto hay mas de un cliente escribiendo, el identificador no lo
--       pone la aplicacion: lo pone el motor.
--         id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY
--       Aqui se escribe a mano para que las tres filas sean comparables con las
--       de los demas motores.

-- === preparacion ===
DROP TABLE IF EXISTS estudiantes;

CREATE TABLE estudiantes (
    id     integer PRIMARY KEY,
    nombre text NOT NULL,
    correo text
);

INSERT INTO estudiantes (id, nombre, correo) VALUES (1, 'Ada', 'ada@example.org');
INSERT INTO estudiantes (id, nombre, correo) VALUES (2, 'Linus', 'linus@example.org');
-- Grace no tiene correo. NULL sin comillas: ausencia de valor, no la palabra.
INSERT INTO estudiantes (id, nombre, correo) VALUES (3, 'Grace', NULL);

-- === consulta ===
SELECT id, nombre FROM estudiantes ORDER BY nombre;
