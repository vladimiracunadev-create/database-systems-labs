-- motor: sqlite
-- doc: https://sqlite.org/foreignkeys.html
-- nota: sin PRAGMA foreign_keys = ON, todo lo de abajo se declara y NADA se
--       comprueba: el borrado de SE-201 dejaria inscripciones huerfanas y el
--       de DB-101 no fallaria. El verificador activa el pragma en cada
--       conexion; una aplicacion real tiene que hacer lo mismo.

-- === preparacion ===
PRAGMA foreign_keys = ON;

CREATE TABLE cursos (
    id     INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL
);
-- Una inscripcion a un curso que ya no existe no significa nada: se va con el.
CREATE TABLE inscripciones (
    estudiante TEXT NOT NULL,
    curso_id   INTEGER NOT NULL REFERENCES cursos(id) ON DELETE CASCADE,
    PRIMARY KEY (estudiante, curso_id)
);
-- Una evaluacion es evidencia academica: NO puede evaporarse por un borrado.
CREATE TABLE evaluaciones (
    id       INTEGER PRIMARY KEY,
    curso_id INTEGER NOT NULL REFERENCES cursos(id) ON DELETE RESTRICT,
    titulo   TEXT NOT NULL
);

INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20);
INSERT INTO evaluaciones (id, curso_id, titulo) VALUES (1, 10, 'Examen final');

-- Cae con sus inscripciones.
DELETE FROM cursos WHERE codigo = 'SE-201';

-- Este borrado lo IMPIDE el motor: DB-101 tiene evaluaciones.
-- Descomentar la linea siguiente hace fallar el guion, que es la prueba:
-- DELETE FROM cursos WHERE codigo = 'DB-101';

-- === consulta ===
SELECT c.codigo AS curso,
       COUNT(i.estudiante) AS inscripciones
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
