-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/insert
-- nota: insertar filas de una en una es lo que peor hace un motor columnar.
--       Funciona, y va contra su diseno: aqui se hace asi para que la sentencia
--       sea identica a la de los demas.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    correo VARCHAR
);

INSERT INTO estudiantes (id, nombre, correo) VALUES (1, 'Ada', 'ada@example.org');
INSERT INTO estudiantes (id, nombre, correo) VALUES (2, 'Linus', 'linus@example.org');
-- Grace no tiene correo. NULL sin comillas: ausencia de valor, no la palabra.
INSERT INTO estudiantes (id, nombre, correo) VALUES (3, 'Grace', NULL);

-- === consulta ===
SELECT id, nombre FROM estudiantes ORDER BY nombre;
