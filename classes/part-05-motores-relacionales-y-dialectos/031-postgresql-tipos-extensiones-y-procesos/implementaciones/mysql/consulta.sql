-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/json.html
-- nota: el tipo JSON valida al escribir, pero NO se puede indexar directamente.
--       Para indexar esta busqueda haria falta un indice multivaluado:
--         ALTER TABLE cursos ADD INDEX idx_etiquetas
--           ((CAST(etiquetas AS CHAR(20) ARRAY)));

-- === preparacion ===
DROP TABLE IF EXISTS cursos;

CREATE TABLE cursos (
    codigo    VARCHAR(20) PRIMARY KEY,
    etiquetas JSON NOT NULL
) ENGINE=InnoDB;

INSERT INTO cursos (codigo, etiquetas) VALUES
    ('DB-101', JSON_ARRAY('sql', 'datos')),
    ('SE-201', JSON_ARRAY('proceso')),
    ('AR-301', JSON_ARRAY('datos', 'diseno'));

-- === consulta ===
SELECT codigo AS curso
FROM cursos
WHERE JSON_CONTAINS(etiquetas, JSON_QUOTE('datos'))
ORDER BY codigo;
