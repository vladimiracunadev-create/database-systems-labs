-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/queries-table-expressions.html
-- nota: EXPLAIN (ANALYZE, BUFFERS) sobre esta misma consulta dice cual de los
--       tres algoritmos de reunion eligio el planificador.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones, cursos, estudiantes;

CREATE TABLE estudiantes (
    id     integer PRIMARY KEY,
    nombre text NOT NULL
);
CREATE TABLE cursos (
    id     integer PRIMARY KEY,
    codigo text NOT NULL UNIQUE
);
CREATE TABLE inscripciones (
    estudiante_id integer NOT NULL REFERENCES estudiantes(id),
    curso_id      integer NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
SELECT e.nombre,
       COALESCE(c.codigo, 'sin-curso') AS codigo
FROM estudiantes e
LEFT JOIN inscripciones i ON i.estudiante_id = e.id
LEFT JOIN cursos c        ON c.id = i.curso_id
ORDER BY e.nombre, codigo;
