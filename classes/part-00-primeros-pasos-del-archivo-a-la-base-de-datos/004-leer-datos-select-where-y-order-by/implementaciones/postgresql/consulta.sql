-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/queries-order.html
-- nota: la documentacion lo dice sin rodeos: sin ORDER BY, el orden de las
--       filas es indeterminado. No es un descuido del motor, es el modelo.

-- === preparacion ===
DROP TABLE IF EXISTS notas;

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
    ('Ada',   'SE-201', 66);

-- === consulta ===
-- Tres decisiones separadas: que filas (WHERE), que columnas (SELECT) y en que
-- orden se leen (ORDER BY). El orden hay que PEDIRLO: una tabla no lo tiene.
SELECT estudiante, nota
FROM notas
WHERE curso = 'DB-101' AND nota >= 60
ORDER BY estudiante;
