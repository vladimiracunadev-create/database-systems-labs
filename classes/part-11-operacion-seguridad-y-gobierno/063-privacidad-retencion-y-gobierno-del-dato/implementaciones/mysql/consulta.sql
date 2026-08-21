-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/partitioning-management-range-list.html
-- nota: la politica se puede dejar declarada DENTRO de la base:
--         CREATE EVENT retencion_eventos ON SCHEDULE EVERY 1 DAY
--         DO DELETE FROM eventos WHERE fecha < CURRENT_DATE - INTERVAL 1 YEAR;
--       Con un aviso: el programador de eventos viene DESACTIVADO por omision
--       (event_scheduler), asi que la politica puede estar escrita y no
--       ejecutarse nunca.

-- === preparacion ===
DROP TABLE IF EXISTS eventos;

CREATE TABLE eventos (
    id     INT PRIMARY KEY,
    correo VARCHAR(200) NOT NULL,
    fecha  DATE NOT NULL
) ENGINE=InnoDB;

INSERT INTO eventos (id, correo, fecha) VALUES
    (1, 'ada@example.org',   '2025-01-15'),
    (2, 'linus@example.org', '2026-08-10'),
    (3, 'grace@otro.org',    '2026-08-15');

DELETE FROM eventos WHERE fecha < '2026-01-01';

-- === consulta ===
SELECT CONCAT('***@', SUBSTRING_INDEX(correo, '@', -1)) AS correo,
       DATE_FORMAT(fecha, '%Y-%m-%d') AS fecha
FROM eventos
ORDER BY fecha;
