-- motor: sqlite
-- doc: https://sqlite.org/whentouse.html
-- nota: guarda FILAS completas, una detras de otra en la pagina. Para sumar la
--       columna `nota` hay que leer tambien `estudiante` y `curso` de cada fila:
--       con veinte columnas y un millon de filas, sumar una sola cuesta leerlo
--       casi todo.

-- === preparacion ===
CREATE TABLE notas (
    estudiante TEXT NOT NULL,
    curso      TEXT NOT NULL,
    nota       INTEGER NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
INSERT INTO notas (estudiante, curso, nota) VALUES
    ('Ada',   'DB-101', 90),
    ('Grace', 'DB-101', 72),
    ('Linus', 'DB-101', 58),
    ('Ada',   'SE-201', 66);

-- === consulta ===
SELECT curso, COUNT(*) AS filas, SUM(nota) AS suma
FROM notas
GROUP BY curso
ORDER BY curso;
