-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-select.html
-- nota: la documentacion lo dice sin rodeos: sin ORDER BY el orden de las filas
--       es indeterminado. No es un descuido del motor; es el modelo.

DROP TABLE IF EXISTS accesos;

-- === preparacion ===
-- El registro de accesos es una BOLSA: admite repetidos y tiene orden de
-- llegada. Una relacion no es eso.
CREATE TABLE accesos (
    id         integer PRIMARY KEY,
    estudiante text NOT NULL,
    curso      text NOT NULL
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
