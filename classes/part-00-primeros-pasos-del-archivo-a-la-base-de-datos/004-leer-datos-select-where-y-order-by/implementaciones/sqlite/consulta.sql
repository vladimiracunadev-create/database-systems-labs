-- motor: sqlite
-- doc: https://sqlite.org/lang_select.html
-- nota: probar a quitar el ORDER BY. Con cuatro filas el resultado parecera
--       correcto igualmente, y esa casualidad es la que hace que el error
--       sobreviva hasta produccion.

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
    ('Ada',   'SE-201', 66);

-- === consulta ===
-- Tres decisiones separadas: que filas (WHERE), que columnas (SELECT) y en que
-- orden se leen (ORDER BY). El orden hay que PEDIRLO: una tabla no lo tiene.
SELECT estudiante, nota
FROM notas
WHERE curso = 'DB-101' AND nota >= 60
ORDER BY estudiante;
