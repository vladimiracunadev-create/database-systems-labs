-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/with.html
-- nota: la misma consulta funciona sobre un grafo exportado a Parquet sin
--       cargarlo, que es la via analitica cuando la pregunta es «cuantos
--       caminos hay» y no «dame este camino».

-- === preparacion ===
CREATE TABLE prerrequisitos (
    curso    VARCHAR NOT NULL,
    requiere VARCHAR NOT NULL,
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
