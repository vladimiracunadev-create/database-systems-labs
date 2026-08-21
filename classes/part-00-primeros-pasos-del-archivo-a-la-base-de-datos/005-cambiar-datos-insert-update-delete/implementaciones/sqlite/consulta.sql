-- motor: sqlite
-- doc: https://sqlite.org/lang_update.html
-- nota: la comprobacion mas barata contra un WHERE mal escrito es contar antes:
--         SELECT COUNT(*) FROM notas WHERE curso = 'DB-101';   -- 3
--       y despues del cambio, changes() dice cuantas filas se tocaron de verdad.

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

-- Subir 5 puntos SOLO a DB-101. Sin el WHERE, subirian las cuatro notas.
UPDATE notas SET nota = nota + 5 WHERE curso = 'DB-101';

-- Dar de baja a Linus. Sin el WHERE, la tabla quedaria vacia.
DELETE FROM notas WHERE estudiante = 'Linus';

-- === consulta ===
SELECT estudiante, curso, nota FROM notas ORDER BY estudiante, curso;
