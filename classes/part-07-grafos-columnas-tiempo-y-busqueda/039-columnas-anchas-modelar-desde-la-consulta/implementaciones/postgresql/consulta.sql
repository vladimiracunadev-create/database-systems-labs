-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-partitioning.html
-- nota: el indice (dispositivo, momento DESC) da el mismo atajo que la clave de
--       agrupamiento de Cassandra: EXPLAIN muestra «Index Scan» sin nodo Sort.
--       La diferencia no esta en la lectura, esta en que la escritura sigue
--       pasando por un unico nodo primario.

-- === preparacion ===
DROP TABLE IF EXISTS lecturas;

CREATE TABLE lecturas (
    dispositivo text NOT NULL,
    momento     text NOT NULL,
    valor       integer NOT NULL,
    PRIMARY KEY (dispositivo, momento)
);
INSERT INTO lecturas (dispositivo, momento, valor) VALUES
    ('sensor-1', '2026-08-19T10:00:00Z', 21),
    ('sensor-1', '2026-08-19T10:01:00Z', 22),
    ('sensor-1', '2026-08-19T10:02:00Z', 23),
    ('sensor-2', '2026-08-19T10:00:00Z', 30),
    ('sensor-2', '2026-08-19T10:01:00Z', 31);

CREATE INDEX lecturas_recientes ON lecturas (dispositivo, momento DESC);

-- === consulta ===
-- Las dos ultimas lecturas de sensor-1, de la mas reciente a la mas antigua.
SELECT momento, valor
FROM lecturas
WHERE dispositivo = 'sensor-1'
ORDER BY momento DESC
LIMIT 2;
