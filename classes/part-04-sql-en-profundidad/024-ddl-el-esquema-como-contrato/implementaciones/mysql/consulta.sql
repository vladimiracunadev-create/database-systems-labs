-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/create-table-check-constraints.html
-- nota: antes de 8.0.16, MySQL analizaba los CHECK y los ignoraba en silencio.
--       Comprobar la version del servidor es parte de leer el esquema.

-- === preparacion ===
DROP TABLE IF EXISTS notas;

CREATE TABLE notas (
    estudiante VARCHAR(50) NOT NULL CHECK (CHAR_LENGTH(estudiante) > 0),
    curso      VARCHAR(50) NOT NULL,
    nota       INT NOT NULL CHECK (nota BETWEEN 0 AND 100),
    PRIMARY KEY (estudiante, curso)
);

INSERT INTO notas (estudiante, curso, nota) VALUES ('Ada', 'DB-101', 90);
INSERT INTO notas (estudiante, curso, nota) VALUES ('Linus', 'DB-101', 58);
INSERT IGNORE INTO notas (estudiante, curso, nota) VALUES ('Grace', 'DB-101', 130);
INSERT IGNORE INTO notas (estudiante, curso, nota) VALUES ('', 'DB-101', 70);

-- === consulta ===
SELECT estudiante, nota FROM notas ORDER BY estudiante;
