-- motor: sqlite
-- doc: https://sqlite.org/lang_select.html
-- nota: quitar el ORDER BY no rompe la consulta, y ese es el peligro: devuelve
--       un orden que parece estable hasta que un indice nuevo cambia el plan.

-- === preparacion ===
-- El registro de accesos es una BOLSA: admite repetidos y tiene orden de
-- llegada. Una relacion no es eso.
CREATE TABLE accesos (
    id         INTEGER PRIMARY KEY,
    estudiante TEXT NOT NULL,
    curso      TEXT NOT NULL
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
