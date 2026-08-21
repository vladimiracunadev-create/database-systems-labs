-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html
-- nota: InnoDB crea automaticamente el indice sobre la columna que referencia,
--       que es justo el que se olvida en otros motores. Y el aviso historico:
--       el motor MyISAM ACEPTA la declaracion de clave foranea y no la
--       comprueba; en bases antiguas, la restriccion existe en el esquema y no
--       en la realidad.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS cursos;
DROP TABLE IF EXISTS estudiantes;

CREATE TABLE estudiantes (
    id     INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);
CREATE TABLE cursos (
    id       INT PRIMARY KEY,
    codigo   VARCHAR(50) NOT NULL UNIQUE,
    profesor VARCHAR(50) NOT NULL
);
CREATE TABLE inscripciones (
    estudiante_id INT NOT NULL REFERENCES estudiantes(id),
    curso_id      INT NOT NULL REFERENCES cursos(id),
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
