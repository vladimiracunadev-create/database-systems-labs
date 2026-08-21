-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-partitioning.html
-- nota: con particionado por rango de fecha, la retencion deja de ser un DELETE
--       de millones de filas y pasa a ser
--         DROP TABLE eventos_2025_01;
--       instantaneo y sin hinchar nada. Y el aviso incomodo: las copias de
--       seguridad conservan lo borrado durante meses, asi que un «derecho al
--       olvido» de verdad tiene que contemplarlas.

-- === preparacion ===
DROP TABLE IF EXISTS eventos;

CREATE TABLE eventos (
    id     integer PRIMARY KEY,
    correo text NOT NULL,
    fecha  date NOT NULL
);
INSERT INTO eventos (id, correo, fecha) VALUES
    (1, 'ada@example.org',   DATE '2025-01-15'),
    (2, 'linus@example.org', DATE '2026-08-10'),
    (3, 'grace@otro.org',    DATE '2026-08-15');

DELETE FROM eventos WHERE fecha < DATE '2026-01-01';

-- === consulta ===
SELECT '***@' || split_part(correo, '@', 2) AS correo,
       to_char(fecha, 'YYYY-MM-DD') AS fecha
FROM eventos
ORDER BY fecha;
