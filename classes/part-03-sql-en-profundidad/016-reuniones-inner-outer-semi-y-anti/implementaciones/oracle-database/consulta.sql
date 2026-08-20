-- motor: oracle-database
-- doc: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/SELECT.html
-- nota: implementacion declarada. Se escribe con la sintaxis estandar de
--       reunion, no con el operador heredado (+), que Oracle sigue aceptando
--       pero que no se puede combinar con ANSI JOIN en la misma consulta.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     NUMBER PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL
);
CREATE TABLE cursos (
    id     NUMBER PRIMARY KEY,
    codigo VARCHAR2(20) NOT NULL UNIQUE
);
CREATE TABLE inscripciones (
    estudiante_id NUMBER NOT NULL REFERENCES estudiantes(id),
    curso_id      NUMBER NOT NULL REFERENCES cursos(id),
    CONSTRAINT pk_inscripciones PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada');
INSERT INTO estudiantes (id, nombre) VALUES (2, 'Linus');
INSERT INTO estudiantes (id, nombre) VALUES (3, 'Grace');
INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101');
INSERT INTO cursos (id, codigo) VALUES (20, 'SE-201');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10);
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 20);
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (2, 10);
COMMIT;

-- === consulta ===
SELECT e.nombre,
       NVL(c.codigo, 'sin-curso') AS codigo
FROM estudiantes e
LEFT JOIN inscripciones i ON i.estudiante_id = e.id
LEFT JOIN cursos c        ON c.id = i.curso_id
ORDER BY e.nombre, codigo;
