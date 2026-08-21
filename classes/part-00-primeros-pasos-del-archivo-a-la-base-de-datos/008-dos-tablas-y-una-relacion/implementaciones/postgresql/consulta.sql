-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/tutorial-fk.html
-- nota: las claves foraneas se comprueban siempre, sin activar nada. Y hay que
--       indexar la columna que REFERENCIA: la referenciada ya tiene indice por
--       ser clave primaria, la otra no, y los borrados en cascada recorren la
--       tabla hija entera sin el.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones, cursos, estudiantes;

CREATE TABLE estudiantes (
    id     integer PRIMARY KEY,
    nombre text NOT NULL
);
CREATE TABLE cursos (
    id       integer PRIMARY KEY,
    codigo   text NOT NULL UNIQUE,
    profesor text NOT NULL
);
CREATE TABLE inscripciones (
    estudiante_id integer NOT NULL REFERENCES estudiantes(id),
    curso_id      integer NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus');
INSERT INTO cursos (id, codigo, profesor) VALUES
    (10, 'DB-101', 'A. Lovelace'),
    (20, 'SE-201', 'G. Hopper');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
-- Las tres tablas vuelven a juntarse al consultar. Cada hecho sigue guardado UNA
-- sola vez: el profesor de DB-101 esta en una fila, no en dos.
SELECT e.nombre, c.codigo, c.profesor
FROM inscripciones i
JOIN estudiantes e ON e.id = i.estudiante_id
JOIN cursos      c ON c.id = i.curso_id
ORDER BY e.nombre, c.codigo;
