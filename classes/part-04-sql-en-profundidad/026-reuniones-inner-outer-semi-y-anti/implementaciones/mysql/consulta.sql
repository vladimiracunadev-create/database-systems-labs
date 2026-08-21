-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/join.html
-- nota: desde 8.0.18 MySQL tiene reunion hash; antes, un LEFT JOIN sin indice
--       degradaba a bucle anidado sobre la tabla completa.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS cursos;
DROP TABLE IF EXISTS estudiantes;

CREATE TABLE estudiantes (
    id     INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE cursos (
    id     INT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;
CREATE TABLE inscripciones (
    estudiante_id INT NOT NULL,
    curso_id      INT NOT NULL,
    PRIMARY KEY (estudiante_id, curso_id),
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id)
) ENGINE=InnoDB;

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
SELECT e.nombre,
       COALESCE(c.codigo, 'sin-curso') AS codigo
FROM estudiantes e
LEFT JOIN inscripciones i ON i.estudiante_id = e.id
LEFT JOIN cursos c        ON c.id = i.curso_id
ORDER BY e.nombre, codigo;
