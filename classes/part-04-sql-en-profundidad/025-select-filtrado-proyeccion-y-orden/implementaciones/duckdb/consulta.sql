-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/select.html
-- nota: quitar el ORDER BY aqui devuelve dos filas distintas entre ejecuciones,
--       porque el motor lee en paralelo por trozos. Es la demostracion mas
--       clara de que LIMIT sin ORDER BY no significa nada.

-- === preparacion ===
CREATE TABLE notas (
    estudiante VARCHAR NOT NULL,
    curso      VARCHAR NOT NULL,
    nota       INTEGER NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
INSERT INTO notas (estudiante, curso, nota) VALUES
    ('Ada',   'DB-101', 90),
    ('Linus', 'DB-101', 58),
    ('Grace', 'DB-101', 72),
    ('Ada',   'SE-201', 66),
    ('Grace', 'SE-201', 78);

-- === consulta ===
-- Las cuatro decisiones de un SELECT, en el orden en que el motor las aplica:
--   FROM      de donde salen las filas
--   WHERE     cuales sobreviven      (seleccion)
--   SELECT    que columnas se ven    (proyeccion)
--   ORDER BY  en que orden se leen   (presentacion, NO parte de la relacion)
--   LIMIT     cuantas se devuelven   (sin ORDER BY, LIMIT devuelve CUALQUIERA)
SELECT estudiante, nota
FROM notas
WHERE curso = 'DB-101' AND nota >= 60
ORDER BY nota DESC
LIMIT 2;
