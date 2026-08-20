-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/group-by-handling.html
-- nota: con ONLY_FULL_GROUP_BY activo (por omision desde 5.7) esta consulta es
--       legal porque cada columna no agregada esta en el GROUP BY. Sin ese
--       modo, MySQL aceptaba consultas ambiguas y devolvia cualquier fila.

DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS cursos;
DROP TABLE IF EXISTS profesores;

-- === preparacion ===
-- Forma normalizada: el nombre del profesor vive UNA vez.
CREATE TABLE profesores (
    id     INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);
CREATE TABLE cursos (
    id          INT PRIMARY KEY,
    codigo      VARCHAR(50) NOT NULL,
    profesor_id INT NOT NULL REFERENCES profesores(id)
);
CREATE TABLE inscripciones (
    estudiante VARCHAR(50) NOT NULL,
    curso_id   INT NOT NULL REFERENCES cursos(id),
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
