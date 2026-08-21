-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/queries-with.html
-- nota: para grafos con ciclos, PostgreSQL tiene la clausula CYCLE, que lleva
--       la deteccion al propio lenguaje en vez de dejarla al UNION:
--         WITH RECURSIVE cadena(curso) AS (...) CYCLE curso SET hay_ciclo USING ruta

-- === preparacion ===
DROP TABLE IF EXISTS prerrequisitos;

CREATE TABLE prerrequisitos (
    curso    text NOT NULL,
    requiere text NOT NULL,
    PRIMARY KEY (curso, requiere)
);
INSERT INTO prerrequisitos (curso, requiere) VALUES
    ('AR-301', 'SE-201'),
    ('SE-201', 'DB-101'),
    ('DB-101', 'MA-100');

-- === consulta ===
-- La consulta recursiva del estandar: un caso base y un paso que se aplica
-- hasta que no aporta filas nuevas. Funciona, y hay que escribirla entera cada
-- vez, incluida la proteccion contra ciclos si el grafo puede tenerlos.
WITH RECURSIVE cadena(curso) AS (
    SELECT requiere FROM prerrequisitos WHERE curso = 'AR-301'
    UNION
    SELECT p.requiere
    FROM prerrequisitos p
    JOIN cadena c ON p.curso = c.curso
)
SELECT curso FROM cadena ORDER BY curso;
