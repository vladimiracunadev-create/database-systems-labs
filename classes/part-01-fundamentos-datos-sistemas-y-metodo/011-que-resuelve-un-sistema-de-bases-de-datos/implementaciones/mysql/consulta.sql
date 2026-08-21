-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/create-index.html
-- nota: la columna se declara con intercalacion binaria para que la unicidad
--       distinga mayusculas de minusculas; con la intercalacion por omision,
--       'Ada@example.org' contaria como duplicado.

-- === preparacion ===
DROP TABLE IF EXISTS estudiantes;

CREATE TABLE estudiantes (
    id     INT PRIMARY KEY,
    correo VARCHAR(200) COLLATE utf8mb4_bin NOT NULL UNIQUE
) ENGINE=InnoDB;

INSERT INTO estudiantes (id, correo) VALUES (1, 'ada@example.org');
INSERT INTO estudiantes (id, correo) VALUES (2, 'linus@example.org');
INSERT IGNORE INTO estudiantes (id, correo) VALUES (3, 'ada@example.org');

-- === consulta ===
SELECT correo FROM estudiantes ORDER BY correo;
