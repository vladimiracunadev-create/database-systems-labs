-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/expressions/subqueries.html
-- nota: DuckDB descorrelaciona esta consulta y la convierte en reuniones. La
--       forma del calculo y la del algebra terminan en el mismo plan: eso es
--       la equivalencia de Codd, comprobada por el optimizador.

-- === preparacion ===
CREATE TABLE cursos (
    codigo VARCHAR PRIMARY KEY
);
CREATE TABLE estudiantes (
    nombre VARCHAR PRIMARY KEY
);
CREATE TABLE inscripciones (
    estudiante VARCHAR NOT NULL,
    curso      VARCHAR NOT NULL,
    PRIMARY KEY (estudiante, curso)
);

INSERT INTO cursos (codigo) VALUES ('DB-101'), ('SE-201');
INSERT INTO estudiantes (nombre) VALUES ('Ada'), ('Linus'), ('Grace');
INSERT INTO inscripciones (estudiante, curso) VALUES
    ('Ada', 'DB-101'), ('Ada', 'SE-201'), ('Linus', 'DB-101');

-- === consulta ===
-- «Los estudiantes inscritos en TODOS los cursos» es la division relacional, y
-- el calculo la escribe tal cual se lee: no existe ningun curso para el que no
-- exista su inscripcion. El doble NOT EXISTS no es un truco: es la traduccion
-- literal del cuantificador universal.
SELECT e.nombre
FROM estudiantes e
WHERE NOT EXISTS (
    SELECT 1 FROM cursos c
    WHERE NOT EXISTS (
        SELECT 1 FROM inscripciones i
        WHERE i.estudiante = e.nombre AND i.curso = c.codigo
    )
)
ORDER BY e.nombre;
