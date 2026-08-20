-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/create_sequence.html
-- nota: util para el argumento numerico de la discusion: contar cuantas filas
--       habria que tocar si el correo fuera la clave foranea.

-- === preparacion ===
-- La identidad es el id: estable, sin significado y nunca visible para el
-- usuario. El correo es un ATRIBUTO unico, no la identidad.
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    correo VARCHAR NOT NULL UNIQUE
);
CREATE TABLE inscripciones (
    estudiante_id INTEGER NOT NULL,
    curso         VARCHAR NOT NULL,
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
