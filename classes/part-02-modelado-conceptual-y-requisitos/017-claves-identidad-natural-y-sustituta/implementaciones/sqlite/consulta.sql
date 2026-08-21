-- motor: sqlite
-- doc: https://sqlite.org/lang_createtable.html
-- nota: INTEGER PRIMARY KEY es un alias del rowid interno, asi que la clave
--       sustituta no ocupa una columna adicional.

-- === preparacion ===
-- La identidad es el id: estable, sin significado y nunca visible para el
-- usuario. El correo es un ATRIBUTO unico, no la identidad.
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    correo TEXT NOT NULL UNIQUE
);
CREATE TABLE inscripciones (
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id),
    curso         TEXT NOT NULL,
    PRIMARY KEY (estudiante_id, curso)
);

INSERT INTO estudiantes (id, correo) VALUES
    (1, 'ada@example.org'), (2, 'linus@example.org'), (3, 'grace@example.org');
INSERT INTO inscripciones (estudiante_id, curso) VALUES
    (1, 'DB-101'), (1, 'SE-201'), (2, 'DB-101');

-- El cambio que rompe los modelos con clave natural: una fila, ninguna
-- referencia tocada. Con el correo como clave foranea, habria que propagarlo a
-- inscripciones y a toda tabla que lo hubiera copiado.
UPDATE estudiantes SET correo = 'ada@nuevo.org' WHERE id = 1;

-- === consulta ===
SELECT e.correo,
       COUNT(i.curso) AS inscripciones
FROM estudiantes e
LEFT JOIN inscripciones i ON i.estudiante_id = e.id
GROUP BY e.id, e.correo
ORDER BY e.correo;
