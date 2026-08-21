-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/create-view.html
-- nota: MySQL NO tiene seguridad a nivel de fila. Lo mas parecido es una vista
--       con SQL SECURITY DEFINER y permisos:
--         GRANT SELECT ON learning.mis_notas TO 'app_acme'@'%';
--         REVOKE ALL ON learning.notas FROM 'app_acme'@'%';
--       Asi la vista deja de ser una convencion y pasa a ser una frontera. El
--       limite: para cien inquilinos hacen falta cien vistas o cien bases.

-- === preparacion ===
DROP VIEW IF EXISTS mis_notas;
DROP TABLE IF EXISTS notas;

CREATE TABLE notas (
    inquilino  VARCHAR(50) NOT NULL,
    estudiante VARCHAR(50) NOT NULL,
    nota       INT NOT NULL,
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
