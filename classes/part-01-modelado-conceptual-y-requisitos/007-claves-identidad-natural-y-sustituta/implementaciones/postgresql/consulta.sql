-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-identity-columns.html
-- nota: las dos claves conviven, y las dos hacen falta: IDENTITY da la
--       identidad estable a la que apuntan las referencias, y UNIQUE sobre el
--       correo impide dos personas con el mismo correo.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones, estudiantes;

CREATE TABLE estudiantes (
    id     integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    correo text NOT NULL UNIQUE
);
CREATE TABLE inscripciones (
    estudiante_id integer NOT NULL REFERENCES estudiantes(id),
    curso         text NOT NULL,
    PRIMARY KEY (estudiante_id, curso)
);

INSERT INTO estudiantes (correo) VALUES
    ('ada@example.org'), ('linus@example.org'), ('grace@example.org');
INSERT INTO inscripciones (estudiante_id, curso)
SELECT id, 'DB-101' FROM estudiantes WHERE correo = 'ada@example.org'
UNION ALL
SELECT id, 'SE-201' FROM estudiantes WHERE correo = 'ada@example.org'
UNION ALL
SELECT id, 'DB-101' FROM estudiantes WHERE correo = 'linus@example.org';

UPDATE estudiantes SET correo = 'ada@nuevo.org' WHERE correo = 'ada@example.org';

-- === consulta ===
SELECT e.correo,
       COUNT(i.curso) AS inscripciones
FROM estudiantes e
LEFT JOIN inscripciones i ON i.estudiante_id = e.id
GROUP BY e.id, e.correo
ORDER BY e.correo;
