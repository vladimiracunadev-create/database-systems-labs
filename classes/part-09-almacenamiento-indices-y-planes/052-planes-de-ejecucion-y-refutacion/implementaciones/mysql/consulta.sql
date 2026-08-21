-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/explain.html
-- nota: como se mide aqui:
--         EXPLAIN ANALYZE SELECT ...        (8.0.18 y posteriores, con tiempos)
--         EXPLAIN FORMAT=JSON SELECT ...    (el coste que calculo el optimizador)
--       La columna `rows` del EXPLAIN clasico es una ESTIMACION, no un hecho:
--       se lee como si fuera un dato medido y no lo es.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS estudiantes;

CREATE TABLE estudiantes (
    nombre VARCHAR(50) PRIMARY KEY
);
CREATE TABLE inscripciones (
    estudiante VARCHAR(50) NOT NULL,
    curso      VARCHAR(50) NOT NULL,
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
