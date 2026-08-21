-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/tutorial-window.html
-- nota: la forma propia de PostgreSQL es
--         SELECT DISTINCT ON (curso) curso, estudiante, nota
--         FROM notas ORDER BY curso, nota DESC, estudiante;
--       que suele ser mas barata. Ata la consulta a PostgreSQL, y eso hay que
--       decidirlo, no descubrirlo al migrar.

DROP TABLE IF EXISTS notas;

-- === preparacion ===
CREATE TABLE notas (
    estudiante text NOT NULL,
    curso      text NOT NULL,
    nota       integer NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
INSERT INTO notas (estudiante, curso, nota) VALUES
    ('Ada',   'DB-101', 90),
    ('Linus', 'DB-101', 58),
    ('Grace', 'DB-101', 72),
    ('Ada',   'SE-201', 66),
    ('Grace', 'SE-201', 78);

-- === consulta ===
-- La CTE nombra el paso intermedio y la ventana hace lo que GROUP BY no puede:
-- calcular por grupo SIN colapsar las filas del grupo. Por eso la nota y el
-- nombre siguen disponibles al filtrar por la posicion.
WITH clasificacion AS (
    SELECT curso,
           estudiante,
           nota,
           ROW_NUMBER() OVER (PARTITION BY curso ORDER BY nota DESC, estudiante) AS puesto
    FROM notas
)
SELECT curso, estudiante, nota
FROM clasificacion
WHERE puesto = 1
ORDER BY curso;
