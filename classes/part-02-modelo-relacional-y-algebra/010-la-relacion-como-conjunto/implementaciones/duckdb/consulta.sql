-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/orderby.html
-- nota: al ejecutar en paralelo por trozos, sin ORDER BY el orden cambia entre
--       ejecuciones de verdad. Es el motor que mejor demuestra que una relacion
--       no tiene orden.

-- === preparacion ===
-- El registro de accesos es una BOLSA: admite repetidos y tiene orden de
-- llegada. Una relacion no es eso.
CREATE TABLE accesos (
    id         INTEGER PRIMARY KEY,
    estudiante VARCHAR NOT NULL,
    curso      VARCHAR NOT NULL
);
INSERT INTO accesos (id, estudiante, curso) VALUES
    (1, 'Linus', 'DB-101'),
    (2, 'Ada',   'DB-101'),
    (3, 'Ada',   'DB-101'),
    (4, 'Ada',   'SE-201'),
    (5, 'Linus', 'DB-101');

-- === consulta ===
-- DISTINCT convierte la bolsa en conjunto; ORDER BY impone un orden que la
-- relacion NO tiene: es una decision de presentacion, no del modelo.
SELECT DISTINCT estudiante, curso
FROM accesos
ORDER BY estudiante, curso;
