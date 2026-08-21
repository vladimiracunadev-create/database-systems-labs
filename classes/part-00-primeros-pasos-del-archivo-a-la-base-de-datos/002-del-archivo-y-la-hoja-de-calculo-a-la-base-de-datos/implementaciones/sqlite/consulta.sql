-- motor: sqlite
-- doc: https://sqlite.org/lang_createtable.html
-- nota: OR IGNORE deja ver el rechazo sin abortar el guion. Sin el, la tercera
--       insercion lanza un error, que es exactamente la garantia que se estaba
--       comprando al elegir una base de datos en vez de un archivo.

-- === preparacion ===
CREATE TABLE notas (
    estudiante TEXT NOT NULL,
    nota       INTEGER NOT NULL CHECK (nota BETWEEN 0 AND 100)
);

INSERT INTO notas (estudiante, nota) VALUES ('Ada', 90);
INSERT INTO notas (estudiante, nota) VALUES ('Linus', 58);
INSERT INTO notas (estudiante, nota) VALUES ('Grace', 72);
-- El examen era sobre 100. Un archivo aceptaria este 130 sin decir nada.
INSERT OR IGNORE INTO notas (estudiante, nota) VALUES ('Bob', 130);

-- === consulta ===
SELECT estudiante, nota FROM notas ORDER BY estudiante;
