-- motor: sqlite
-- doc: https://sqlite.org/stricttables.html
-- nota: la clausula STRICT es lo que hace que el tipo se comprueba de verdad.
--       Sin ella, la afinidad de tipos deja pasar una cadena en una columna
--       INTEGER si no puede convertirla.

-- === preparacion ===
CREATE TABLE notas (
    estudiante TEXT NOT NULL CHECK (length(estudiante) > 0),
    curso      TEXT NOT NULL,
    nota       INTEGER NOT NULL CHECK (nota BETWEEN 0 AND 100),
    PRIMARY KEY (estudiante, curso)
) STRICT;

INSERT INTO notas (estudiante, curso, nota) VALUES ('Ada', 'DB-101', 90);
INSERT INTO notas (estudiante, curso, nota) VALUES ('Linus', 'DB-101', 58);
-- Las dos siguientes rebotan contra el contrato. OR IGNORE deja verlo sin
-- abortar el guion; sin OR IGNORE, cada una lanza un error.
INSERT OR IGNORE INTO notas (estudiante, curso, nota) VALUES ('Grace', 'DB-101', 130);
INSERT OR IGNORE INTO notas (estudiante, curso, nota) VALUES ('', 'DB-101', 70);

-- === consulta ===
SELECT estudiante, nota FROM notas ORDER BY estudiante;
