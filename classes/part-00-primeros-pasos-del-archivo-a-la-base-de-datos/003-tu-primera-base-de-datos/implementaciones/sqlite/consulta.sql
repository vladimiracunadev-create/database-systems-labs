-- motor: sqlite
-- doc: https://sqlite.org/lang_insert.html
-- nota: el resultado NO sale en orden de insercion, sale en el que pidio el
--       ORDER BY. Sin esa clausula, ningun motor esta obligado a devolver nada
--       en un orden concreto.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT
);

INSERT INTO estudiantes (id, nombre, correo) VALUES (1, 'Ada', 'ada@example.org');
INSERT INTO estudiantes (id, nombre, correo) VALUES (2, 'Linus', 'linus@example.org');
-- Grace no tiene correo. NULL sin comillas: ausencia de valor, no la palabra.
INSERT INTO estudiantes (id, nombre, correo) VALUES (3, 'Grace', NULL);

-- === consulta ===
SELECT id, nombre FROM estudiantes ORDER BY nombre;
