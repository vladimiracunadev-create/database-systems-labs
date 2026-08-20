-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/fulltext-search.html
-- nota: se usa el MODO BOOLEANO a proposito. En modo de lenguaje natural,
--       InnoDB descarta las palabras que aparecen en mas del 50 % de las filas,
--       asi que con tres documentos «datos» se ignoraria y la busqueda
--       devolveria cualquier cosa. Es la sorpresa clasica de las pruebas
--       pequenas.

-- === preparacion ===
DROP TABLE IF EXISTS documentos;

CREATE TABLE documentos (
    id     VARCHAR(10) PRIMARY KEY,
    titulo TEXT NOT NULL,
    FULLTEXT KEY ft_titulo (titulo)
) ENGINE=InnoDB;

INSERT INTO documentos (id, titulo) VALUES
    ('d1', 'Introduccion a las bases de datos relacionales'),
    ('d2', 'Bases de datos distribuidas y replicacion'),
    ('d3', 'Redes de computadores y protocolos');

-- === consulta ===
SELECT id AS documento
FROM documentos
WHERE MATCH(titulo) AGAINST('+bases +datos' IN BOOLEAN MODE)
ORDER BY id;
