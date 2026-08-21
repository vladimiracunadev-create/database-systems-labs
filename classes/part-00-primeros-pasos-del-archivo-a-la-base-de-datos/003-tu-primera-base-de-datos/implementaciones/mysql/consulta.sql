-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/insert.html
-- nota: casi identico. La diferencia que no se ve aqui y muerde despues: la
--       comparacion de texto ignora mayusculas por omision, asi que un UNIQUE
--       sobre un correo trata 'Ada@x.org' y 'ada@x.org' como el mismo valor.

-- === preparacion ===
DROP TABLE IF EXISTS estudiantes;

CREATE TABLE estudiantes (
    id     INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    correo VARCHAR(50)
);

INSERT INTO estudiantes (id, nombre, correo) VALUES (1, 'Ada', 'ada@example.org');
INSERT INTO estudiantes (id, nombre, correo) VALUES (2, 'Linus', 'linus@example.org');
-- Grace no tiene correo. NULL sin comillas: ausencia de valor, no la palabra.
INSERT INTO estudiantes (id, nombre, correo) VALUES (3, 'Grace', NULL);

-- === consulta ===
SELECT id, nombre FROM estudiantes ORDER BY nombre;
