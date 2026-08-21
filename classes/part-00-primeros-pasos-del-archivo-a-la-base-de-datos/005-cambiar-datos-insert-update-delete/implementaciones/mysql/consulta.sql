-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/mysql-tips.html
-- nota: MySQL tiene una defensa especifica para este accidente:
--         SET sql_safe_updates = 1;
--       Con eso, un UPDATE o un DELETE sin WHERE sobre una columna indexada se
--       RECHAZA. El cliente de consola lo activa con --safe-updates, y las
--       conexiones de aplicacion no lo traen activado.

-- === preparacion ===
DROP TABLE IF EXISTS notas;

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
    ('Ada',   'SE-201', 66);

-- Subir 5 puntos SOLO a DB-101. Sin el WHERE, subirian las cuatro notas.
UPDATE notas SET nota = nota + 5 WHERE curso = 'DB-101';

-- Dar de baja a Linus. Sin el WHERE, la tabla quedaria vacia.
DELETE FROM notas WHERE estudiante = 'Linus';

-- === consulta ===
SELECT estudiante, curso, nota FROM notas ORDER BY estudiante, curso;
