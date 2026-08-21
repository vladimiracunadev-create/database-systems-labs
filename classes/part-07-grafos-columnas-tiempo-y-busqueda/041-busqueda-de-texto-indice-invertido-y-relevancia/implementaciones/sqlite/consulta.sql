-- motor: sqlite
-- doc: https://sqlite.org/fts5.html
-- nota: FTS5 es un indice invertido completo dentro del archivo. La consulta
--       'bases datos' significa «los dos terminos», no la subcadena: por eso
--       encuentra «Bases» con mayuscula y no encuentra d3, que no habla de
--       datos. Un LIKE '%bases%' fallaria en ambas cosas.

-- === preparacion ===
CREATE VIRTUAL TABLE documentos USING fts5(id UNINDEXED, titulo);

INSERT INTO documentos (id, titulo) VALUES
    ('d1', 'Introduccion a las bases de datos relacionales'),
    ('d2', 'Bases de datos distribuidas y replicacion'),
    ('d3', 'Redes de computadores y protocolos');

-- === consulta ===
SELECT id AS documento
FROM documentos
WHERE documentos MATCH 'bases datos'
ORDER BY id;
