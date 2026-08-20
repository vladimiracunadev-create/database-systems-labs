-- motor: sqlite
-- doc: https://sqlite.org/lang_with.html
-- nota: UNION —no UNION ALL— es lo que protege de los ciclos: descarta las
--       filas ya vistas. Con UNION ALL y un grafo ciclico, esta consulta no
--       termina nunca.

-- === preparacion ===
CREATE TABLE prerrequisitos (
    curso    TEXT NOT NULL,
    requiere TEXT NOT NULL,
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
