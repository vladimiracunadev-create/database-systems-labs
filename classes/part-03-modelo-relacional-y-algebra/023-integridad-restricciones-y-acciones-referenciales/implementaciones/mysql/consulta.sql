-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html
-- nota: InnoDB comprueba las claves foraneas siempre, sin activar nada. Lo que
--       NO hace es disparar los triggers de las tablas hijas al cascadear: un
--       contador mantenido por trigger se desfasa justo ahi.

-- === preparacion ===
DROP TABLE IF EXISTS evaluaciones;
DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS cursos;

CREATE TABLE cursos (
    id     INT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE inscripciones (
    estudiante VARCHAR(50) NOT NULL,
    curso_id   INT NOT NULL,
    PRIMARY KEY (estudiante, curso_id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
) ENGINE=InnoDB;
CREATE TABLE evaluaciones (
    id       INT PRIMARY KEY,
    curso_id INT NOT NULL,
    titulo   VARCHAR(50) NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20);
INSERT INTO evaluaciones (id, curso_id, titulo) VALUES (1, 10, 'Examen final');

DELETE FROM cursos WHERE codigo = 'SE-201';

-- El borrado de DB-101 fallaria con el error 1451. Se deja fuera del guion
-- para que el resto se ejecute; probarlo a mano es parte del laboratorio.

-- === consulta ===
SELECT c.codigo AS curso,
       COUNT(i.estudiante) AS inscripciones
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
