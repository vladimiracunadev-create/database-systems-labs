-- motor: sqlite
-- doc: https://sqlite.org/windowfunctions.html
-- nota: ROW_NUMBER, RANK y DENSE_RANK no son lo mismo con empates: ROW_NUMBER
--       elige uno arbitrario salvo que el ORDER BY desempate, y por eso aqui
--       lleva `, estudiante` al final.

-- === preparacion ===
CREATE TABLE notas (
    estudiante TEXT NOT NULL,
    curso      TEXT NOT NULL,
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
