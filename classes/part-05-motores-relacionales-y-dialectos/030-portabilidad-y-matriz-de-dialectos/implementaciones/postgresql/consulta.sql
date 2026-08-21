-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/functions-string.html
-- nota: PostgreSQL tambien acepta la forma de la norma,
--         FETCH FIRST 2 ROWS ONLY
--       que es la que hay que usar si el destino puede ser Oracle o SQL Server.

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
    ('Grace', 'DB-101', 72),
    ('Linus', 'DB-101', 58),
    ('Ada',   'SE-201', 66);

-- === consulta ===
SELECT estudiante || ' - ' || curso AS etiqueta
FROM notas
WHERE curso = 'DB-101'
ORDER BY nota DESC
LIMIT 2;
