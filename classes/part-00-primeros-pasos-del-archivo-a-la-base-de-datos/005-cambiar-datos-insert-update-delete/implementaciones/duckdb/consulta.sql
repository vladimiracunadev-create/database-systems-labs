-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/update
-- nota: aqui lo natural es comprobar el alcance sobre una COPIA de los datos
--       reales antes de tocar produccion: contar coincidencias de un WHERE
--       complicado sobre millones de filas cuesta segundos.

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
    ('Ada',   'SE-201', 66);

-- Subir 5 puntos SOLO a DB-101. Sin el WHERE, subirian las cuatro notas.
UPDATE notas SET nota = nota + 5 WHERE curso = 'DB-101';

-- Dar de baja a Linus. Sin el WHERE, la tabla quedaria vacia.
DELETE FROM notas WHERE estudiante = 'Linus';

-- === consulta ===
SELECT estudiante, curso, nota FROM notas ORDER BY estudiante, curso;
