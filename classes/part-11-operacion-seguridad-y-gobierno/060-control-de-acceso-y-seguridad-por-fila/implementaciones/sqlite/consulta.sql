-- motor: sqlite
-- doc: https://sqlite.org/lang_createview.html
-- nota: la vista es una CONVENCION, no un control de acceso: nada impide que el
--       mismo proceso consulte `notas` directamente. En SQLite, quien tiene el
--       archivo lo tiene todo.

-- === preparacion ===
CREATE TABLE notas (
    inquilino  TEXT NOT NULL,
    estudiante TEXT NOT NULL,
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
