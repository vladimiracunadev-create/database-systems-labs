-- motor: sqlite
-- doc: https://sqlite.org/foreignkeys.html
-- nota: sin PRAGMA foreign_keys = ON, las claves foraneas de abajo se declaran y
--       NO se comprueban. El verificador de este repositorio activa el pragma en
--       cada conexion; una aplicacion real tiene que hacer lo mismo.
--       Con el activo, esto se rechaza:
--         INSERT INTO inscripciones VALUES (99, 10);  -- FOREIGN KEY constraint failed

PRAGMA foreign_keys = ON;

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);
CREATE TABLE cursos (
    id       INTEGER PRIMARY KEY,
    codigo   TEXT NOT NULL UNIQUE,
    profesor TEXT NOT NULL
);
CREATE TABLE inscripciones (
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id),
    curso_id      INTEGER NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus');
INSERT INTO cursos (id, codigo, profesor) VALUES
    (10, 'DB-101', 'A. Lovelace'),
    (20, 'SE-201', 'G. Hopper');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
-- Las tres tablas vuelven a juntarse al consultar. Cada hecho sigue guardado UNA
-- sola vez: el profesor de DB-101 esta en una fila, no en dos.
SELECT e.nombre, c.codigo, c.profesor
FROM inscripciones i
JOIN estudiantes e ON e.id = i.estudiante_id
JOIN cursos      c ON c.id = i.curso_id
ORDER BY e.nombre, c.codigo;
