-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/limit-optimization.html

DROP TABLE IF EXISTS notas;

-- === preparacion ===
CREATE TABLE notas (
    estudiante VARCHAR(50) NOT NULL,
    curso      VARCHAR(50) NOT NULL,
    nota       INT NOT NULL,
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
