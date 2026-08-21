-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/tutorial-agg.html
-- nota: EXPLAIN (ANALYZE) sobre la version ingenua muestra «rows=6» en el nodo
--       de la reunion para DB-101: el doble conteo deja de ser un argumento y
--       pasa a ser un numero.

DROP TABLE IF EXISTS evaluaciones, inscripciones, cursos;

-- === preparacion ===
CREATE TABLE cursos (
    codigo text PRIMARY KEY
);
CREATE TABLE inscripciones (
    estudiante text NOT NULL,
    curso      text NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
CREATE TABLE evaluaciones (
    id     integer PRIMARY KEY,
    curso  text NOT NULL,
    titulo text NOT NULL
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
