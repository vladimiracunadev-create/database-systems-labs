-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/create_view
-- nota: la auditoria que precede a cualquier control de acceso:
--         SELECT inquilino, COUNT(*) FROM notas GROUP BY inquilino;
--         SELECT COUNT(*) FROM notas WHERE inquilino IS NULL OR inquilino = '';
--       La segunda busca el agujero clasico del esquema multiinquilino: filas
--       sin inquilino, que las politicas no saben de quien son.

-- === preparacion ===
CREATE TABLE notas (
    inquilino  VARCHAR NOT NULL,
    estudiante VARCHAR NOT NULL,
    nota       INTEGER NOT NULL,
    PRIMARY KEY (inquilino, estudiante)
);
INSERT INTO notas (inquilino, estudiante, nota) VALUES
    ('acme',   'Ada', 90),
    ('acme',   'Bea', 58),
    ('globex', 'Cid', 77);

-- La vista ES la frontera. La aplicacion consulta `mis_notas`, nunca `notas`,
-- y el filtro por inquilino deja de depender de que cada consulta se acuerde
-- de escribirlo. Basta UNA consulta que lo olvide para filtrar los datos de
-- otro cliente.
CREATE VIEW mis_notas AS
SELECT estudiante, nota
FROM notas
WHERE inquilino = 'acme';

-- === consulta ===
SELECT estudiante, nota FROM mis_notas ORDER BY estudiante;
