-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/guides/meta/explain_analyze.html
-- nota: como se mide aqui:
--         EXPLAIN ANALYZE SELECT ...
--       Dibuja el arbol con el tiempo de cada operador. Aviso: el optimizador
--       reescribe tanto que este EXISTS acabara convertido en una reunion, y el
--       plan no se parecera a lo escrito.

-- === preparacion ===
CREATE TABLE estudiantes (
    nombre VARCHAR PRIMARY KEY
);
CREATE TABLE inscripciones (
    estudiante VARCHAR NOT NULL,
    curso      VARCHAR NOT NULL,
    PRIMARY KEY (estudiante, curso)
);
INSERT INTO estudiantes (nombre) VALUES ('Ada'), ('Linus'), ('Grace');
INSERT INTO inscripciones (estudiante, curso) VALUES
    ('Ada', 'DB-101'), ('Ada', 'SE-201'), ('Linus', 'DB-101');

-- === consulta ===
-- «Quien tiene al menos una inscripcion» se puede escribir de tres formas que
-- devuelven LO MISMO y cuestan cosas distintas:
--
--   A) SELECT DISTINCT e.nombre FROM estudiantes e
--      JOIN inscripciones i ON i.estudiante = e.nombre;
--      -> multiplica filas y luego las deduplica: trabajo hecho y deshecho.
--
--   B) SELECT nombre FROM estudiantes
--      WHERE nombre IN (SELECT estudiante FROM inscripciones);
--      -> el optimizador suele convertirlo en semirreunion; suele.
--
--   C) la de abajo: semirreunion explicita. El motor se detiene en la primera
--      coincidencia y no multiplica nada.
--
-- Que las tres den lo mismo es una propiedad del algebra relacional. Cual es
-- mas barata NO se decide leyendo: se decide midiendo con EXPLAIN, y por eso
-- esta clase se llama «refutacion».
SELECT e.nombre
FROM estudiantes e
WHERE EXISTS (
    SELECT 1 FROM inscripciones i WHERE i.estudiante = e.nombre
)
ORDER BY e.nombre;
