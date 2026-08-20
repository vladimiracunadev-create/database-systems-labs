-- motor: sqlite
-- doc: https://sqlite.org/lang_update.html
-- nota: la prueba de la normalizacion esta en el UPDATE, no en el SELECT: una
--       sola escritura corrige el hecho en todas partes.

-- === preparacion ===
-- Forma normalizada: el nombre del profesor vive UNA vez.
CREATE TABLE profesores (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);
CREATE TABLE cursos (
    id          INTEGER PRIMARY KEY,
    codigo      TEXT NOT NULL,
    profesor_id INTEGER NOT NULL REFERENCES profesores(id)
);
CREATE TABLE inscripciones (
    estudiante TEXT NOT NULL,
    curso_id   INTEGER NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante, curso_id)
);

INSERT INTO profesores (id, nombre) VALUES (1, 'A. Lovelace'), (2, 'Grace Hopper');
INSERT INTO cursos (id, codigo, profesor_id) VALUES (10, 'DB-101', 1), (20, 'SE-201', 2);
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20);

-- La correccion de un dato es UNA escritura. En la tabla sin normalizar habria
-- que actualizar una fila por inscripcion, y bastaria olvidar una para que el
-- mismo profesor tuviera dos nombres.
UPDATE profesores SET nombre = 'Ada Lovelace' WHERE id = 1;

-- === consulta ===
SELECT c.codigo AS curso,
       p.nombre AS profesor,
       COUNT(i.estudiante) AS inscripciones
FROM cursos c
JOIN profesores p ON p.id = c.profesor_id
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo, p.nombre
ORDER BY c.codigo;
