-- motor: sqlite
-- doc: https://sqlite.org/lang_select.html

-- === preparacion ===
CREATE TABLE cursos (
    codigo TEXT PRIMARY KEY
);
CREATE TABLE inscripciones (
    estudiante TEXT NOT NULL,
    curso      TEXT NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
CREATE TABLE evaluaciones (
    id     INTEGER PRIMARY KEY,
    curso  TEXT NOT NULL,
    titulo TEXT NOT NULL
);

INSERT INTO cursos (codigo) VALUES ('DB-101'), ('SE-201');
INSERT INTO inscripciones (estudiante, curso) VALUES
    ('Ada', 'DB-101'), ('Linus', 'DB-101'), ('Grace', 'SE-201');
INSERT INTO evaluaciones (id, curso, titulo) VALUES
    (1, 'DB-101', 'Control 1'), (2, 'DB-101', 'Control 2'), (3, 'DB-101', 'Examen'),
    (4, 'SE-201', 'Examen');

-- === consulta ===
-- La forma INGENUA seria reunir las dos tablas hijas y contar con DISTINCT:
--   FROM cursos c LEFT JOIN inscripciones i ... LEFT JOIN evaluaciones e ...
-- Para DB-101, esa reunion produce 2 x 3 = 6 filas intermedias, y sin DISTINCT
-- devolveria 6 inscritos y 6 evaluaciones. Con DISTINCT el numero sale bien y
-- el trabajo sigue estando ahi.
--
-- La forma CORRECTA agrega ANTES de reunir: cada subconsulta devuelve una fila
-- por curso, asi que ninguna reunion multiplica nada.
SELECT c.codigo AS curso,
       COALESCE(i.inscritos, 0) AS inscritos,
       COALESCE(e.evaluaciones, 0) AS evaluaciones
FROM cursos c
LEFT JOIN (SELECT curso, COUNT(*) AS inscritos
           FROM inscripciones GROUP BY curso) i ON i.curso = c.codigo
LEFT JOIN (SELECT curso, COUNT(*) AS evaluaciones
           FROM evaluaciones GROUP BY curso) e ON e.curso = c.codigo
ORDER BY c.codigo;
