-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-constraints.html
-- nota: la restriccion se implementa con un indice unico. Consultar
--       pg_indexes despues de crear la tabla lo hace visible.

-- === preparacion ===
DROP TABLE IF EXISTS estudiantes;

CREATE TABLE estudiantes (
    id     integer PRIMARY KEY,
    correo text NOT NULL UNIQUE
);

INSERT INTO estudiantes (id, correo) VALUES (1, 'ada@example.org');
INSERT INTO estudiantes (id, correo) VALUES (2, 'linus@example.org');
INSERT INTO estudiantes (id, correo) VALUES (3, 'ada@example.org')
    ON CONFLICT (correo) DO NOTHING;

-- === consulta ===
SELECT correo FROM estudiantes ORDER BY correo;
