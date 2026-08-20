-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-constraints.html
-- nota: aqui el intento prohibido SI se ejecuta, dentro de un bloque que
--       captura el error: la prueba de que la restriccion actua queda en el
--       propio guion en vez de en un comentario.

-- === preparacion ===
DROP TABLE IF EXISTS evaluaciones, inscripciones, cursos;

CREATE TABLE cursos (
    id     integer PRIMARY KEY,
    codigo text NOT NULL
);
CREATE TABLE inscripciones (
    estudiante text NOT NULL,
    curso_id   integer NOT NULL REFERENCES cursos(id) ON DELETE CASCADE,
    PRIMARY KEY (estudiante, curso_id)
);
CREATE TABLE evaluaciones (
    id       integer PRIMARY KEY,
    curso_id integer NOT NULL REFERENCES cursos(id) ON DELETE RESTRICT,
    titulo   text NOT NULL
);

INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20);
INSERT INTO evaluaciones (id, curso_id, titulo) VALUES (1, 10, 'Examen final');

DELETE FROM cursos WHERE codigo = 'SE-201';

DO $$
BEGIN
    DELETE FROM cursos WHERE codigo = 'DB-101';
    RAISE EXCEPTION 'la restriccion no actuo: DB-101 no deberia poder borrarse';
EXCEPTION
    -- RESTRICT levanta restrict_violation (23001), no foreign_key_violation
    -- (23503): son dos codigos distintos y conviene no confundirlos.
    WHEN restrict_violation OR foreign_key_violation THEN
        RAISE NOTICE 'RESTRICT impidio el borrado, como debia';
END;
$$;

-- === consulta ===
SELECT c.codigo AS curso,
       COUNT(i.estudiante) AS inscripciones
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
