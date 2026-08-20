-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/update.html
-- nota: para DESCUBRIR dependencias funcionales en datos existentes:
--       SELECT curso, COUNT(DISTINCT profesor) FROM plano GROUP BY curso
--       HAVING COUNT(DISTINCT profesor) > 1;  -- si devuelve filas, la
--       dependencia esta rota y hay anomalias ya presentes.

-- === preparacion ===
-- Forma normalizada: el nombre del profesor vive UNA vez.
CREATE TABLE profesores (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL
);
CREATE TABLE cursos (
    id          INTEGER PRIMARY KEY,
    codigo      VARCHAR NOT NULL,
    profesor_id INTEGER NOT NULL
);
CREATE TABLE inscripciones (
    estudiante VARCHAR NOT NULL,
    curso_id   INTEGER NOT NULL,
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
