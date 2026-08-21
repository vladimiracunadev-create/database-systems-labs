-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/arrays.html
-- nota: el indice GIN es lo que hace viable esta forma. Sin el, @> recorre la
--       tabla; con el, va directo a las filas que contienen la etiqueta. Es un
--       indice invertido dentro de un motor relacional.

-- === preparacion ===
DROP TABLE IF EXISTS cursos;

CREATE TABLE cursos (
    codigo    text PRIMARY KEY,
    etiquetas text[] NOT NULL DEFAULT '{}'
);
CREATE INDEX cursos_etiquetas ON cursos USING GIN (etiquetas);

INSERT INTO cursos (codigo, etiquetas) VALUES
    ('DB-101', ARRAY['sql', 'datos']),
    ('SE-201', ARRAY['proceso']),
    ('AR-301', ARRAY['datos', 'diseno']);

-- === consulta ===
SELECT codigo AS curso
FROM cursos
WHERE etiquetas @> ARRAY['datos']
ORDER BY codigo;
