-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/using-explain.html
-- nota: como se mide aqui:
--         EXPLAIN (ANALYZE, BUFFERS) SELECT ...
--       Lo que hay que mirar, en este orden:
--         1. «rows=X ... actual rows=Y»: si X e Y difieren en un orden de
--            magnitud, el problema son las ESTADISTICAS, no el indice.
--         2. «Rows Removed by Filter»: trabajo hecho y tirado.
--         3. «shared read» frente a «shared hit»: cuanto vino del disco.
--       Y un aviso: ANALYZE EJECUTA la consulta. Sobre un UPDATE o un DELETE
--       hay que envolverlo en BEGIN ... ROLLBACK.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones, estudiantes;

CREATE TABLE estudiantes (
    nombre text PRIMARY KEY
);
CREATE TABLE inscripciones (
    estudiante text NOT NULL,
    curso      text NOT NULL,
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
