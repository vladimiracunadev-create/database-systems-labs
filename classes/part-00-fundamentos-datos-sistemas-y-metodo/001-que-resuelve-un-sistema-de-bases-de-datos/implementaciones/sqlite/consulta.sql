-- motor: sqlite
-- doc: https://sqlite.org/lang_createtable.html
-- nota: INSERT OR IGNORE deja que el motor rechace el duplicado sin abortar el
--       guion. Sin OR IGNORE, la tercera insercion lanza un error: esa es
--       exactamente la garantia que se esta demostrando.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    correo TEXT NOT NULL UNIQUE
);

INSERT INTO estudiantes (id, correo) VALUES (1, 'ada@example.org');
INSERT INTO estudiantes (id, correo) VALUES (2, 'linus@example.org');
-- El programa no comprueba nada: lo intenta igual. El motor lo rechaza.
INSERT OR IGNORE INTO estudiantes (id, correo) VALUES (3, 'ada@example.org');

-- === consulta ===
SELECT correo FROM estudiantes ORDER BY correo;
