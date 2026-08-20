-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/sql-mode.html
-- nota: aqui esta la trampa de la clase. Por omision,
--         SELECT estudiante || ' - ' || curso
--       NO concatena: || es el OR logico y la consulta devuelve 0 en cada fila,
--       sin error. Con SET sql_mode = 'PIPES_AS_CONCAT' pasaria a concatenar.
--       CONCAT() evita la ambiguedad y ademas es portable a SQL Server y Oracle.

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
    ('Grace', 'DB-101', 72),
    ('Linus', 'DB-101', 58),
    ('Ada',   'SE-201', 66);

-- === consulta ===
SELECT CONCAT(estudiante, ' - ', curso) AS etiqueta
FROM notas
WHERE curso = 'DB-101'
ORDER BY nota DESC
LIMIT 2;
