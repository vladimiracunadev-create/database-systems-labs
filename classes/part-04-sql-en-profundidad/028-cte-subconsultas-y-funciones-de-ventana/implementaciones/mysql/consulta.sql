-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/window-functions.html
-- nota: esta consulta NO funciona en MySQL 5.7: alli habia que emularla con
--       variables de sesion, cuyo resultado dependia del orden de evaluacion y
--       dejo de estar garantizado en 8.0.

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
