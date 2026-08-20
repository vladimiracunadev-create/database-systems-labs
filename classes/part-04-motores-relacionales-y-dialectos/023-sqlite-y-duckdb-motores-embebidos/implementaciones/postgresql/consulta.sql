-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/tutorial-arch.html
-- nota: la misma respuesta, con un proceso servidor detras. Lo que se gana
--       —usuarios, permisos, conexiones remotas, replica, concurrencia— y lo
--       que se paga —instalar, configurar, actualizar, respaldar— es la
--       decision entera de esta clase.

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
SELECT curso, COUNT(*) AS filas, SUM(nota) AS suma
FROM notas
GROUP BY curso
ORDER BY curso;
