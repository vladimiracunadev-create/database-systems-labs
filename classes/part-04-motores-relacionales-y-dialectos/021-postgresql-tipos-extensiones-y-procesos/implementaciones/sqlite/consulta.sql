-- motor: sqlite
-- doc: https://sqlite.org/json1.html
-- nota: json_each convierte el arreglo en filas para poder filtrarlo. Funciona,
--       y no hay indice que lo acelere: recorre la tabla entera. Con cientos de
--       filas da igual; con millones, no.

-- === preparacion ===
CREATE TABLE cursos (
    codigo    TEXT PRIMARY KEY,
    etiquetas TEXT NOT NULL   -- un arreglo JSON guardado como texto
);

INSERT INTO cursos (codigo, etiquetas) VALUES
    ('DB-101', '["sql","datos"]'),
    ('SE-201', '["proceso"]'),
    ('AR-301', '["datos","diseno"]');

-- === consulta ===
SELECT c.codigo AS curso
FROM cursos c
WHERE EXISTS (
    SELECT 1 FROM json_each(c.etiquetas) e WHERE e.value = 'datos'
)
ORDER BY c.codigo;
