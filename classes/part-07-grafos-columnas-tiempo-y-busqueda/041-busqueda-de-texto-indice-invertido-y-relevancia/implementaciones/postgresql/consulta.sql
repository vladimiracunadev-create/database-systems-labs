-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/textsearch-intro.html
-- nota: la columna tsvector es GENERADA, asi que se mantiene sola y el indice
--       GIN nunca va por detras. Es la diferencia con un motor de busqueda
--       aparte: aqui el indice se actualiza DENTRO de la misma transaccion que
--       el dato.
--       Para ver que guarda de verdad el indice:
--         SELECT to_tsvector('spanish', 'Bases de datos distribuidas');
--         -> 'bas':1 'dat':3 'distribu':4    (raices, sin palabras vacias)

-- === preparacion ===
DROP TABLE IF EXISTS documentos;

CREATE TABLE documentos (
    id      text PRIMARY KEY,
    titulo  text NOT NULL,
    buscado tsvector GENERATED ALWAYS AS (to_tsvector('spanish', titulo)) STORED
);
CREATE INDEX documentos_buscado ON documentos USING GIN (buscado);

INSERT INTO documentos (id, titulo) VALUES
    ('d1', 'Introduccion a las bases de datos relacionales'),
    ('d2', 'Bases de datos distribuidas y replicacion'),
    ('d3', 'Redes de computadores y protocolos');

-- === consulta ===
SELECT id AS documento
FROM documentos
WHERE buscado @@ to_tsquery('spanish', 'bases & datos')
ORDER BY id;
