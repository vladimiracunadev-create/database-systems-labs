-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/triggers.html
-- nota: los disparadores de InnoDB se ejecutan en la misma transaccion, asi
--       que contador e inscripcion se confirman o se deshacen juntos.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS cursos;

CREATE TABLE cursos (
    id        INT PRIMARY KEY,
    codigo    VARCHAR(20) NOT NULL,
    inscritos INT NOT NULL DEFAULT 0
) ENGINE=InnoDB;
CREATE TABLE inscripciones (
    estudiante VARCHAR(50) NOT NULL,
    curso_id   INT NOT NULL,
    PRIMARY KEY (estudiante, curso_id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id)
) ENGINE=InnoDB;

CREATE TRIGGER inscripciones_mas AFTER INSERT ON inscripciones
FOR EACH ROW UPDATE cursos SET inscritos = inscritos + 1 WHERE id = NEW.curso_id;

CREATE TRIGGER inscripciones_menos AFTER DELETE ON inscripciones
FOR EACH ROW UPDATE cursos SET inscritos = inscritos - 1 WHERE id = OLD.curso_id;

INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20), ('Bob', 20);
DELETE FROM inscripciones WHERE estudiante = 'Bob' AND curso_id = 20;

-- === consulta ===
-- La comprobacion que en produccion debe correr periodicamente: el dato
-- guardado frente al dato calculado. El dia que dejen de coincidir, la
-- desnormalizacion dejo de ser deliberada.
SELECT c.codigo AS curso,
       c.inscritos AS contador,
       (SELECT COUNT(*) FROM inscripciones i WHERE i.curso_id = c.id) AS calculado
FROM cursos c
ORDER BY c.codigo;
