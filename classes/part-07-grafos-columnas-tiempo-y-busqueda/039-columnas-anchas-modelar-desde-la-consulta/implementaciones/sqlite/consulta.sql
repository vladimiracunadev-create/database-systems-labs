-- motor: sqlite
-- doc: https://sqlite.org/lang_createtable.html
-- nota: la clave primaria (dispositivo, momento) ordena las filas en el arbol B
--       exactamente como la clave de agrupamiento de Cassandra ordena las celdas
--       dentro de la particion. La idea es la misma; lo que falta aqui es el
--       reparto entre nodos.

-- === preparacion ===
CREATE TABLE lecturas (
    dispositivo TEXT NOT NULL,
    momento     TEXT NOT NULL,
    valor       INTEGER NOT NULL,
    PRIMARY KEY (dispositivo, momento)
);
INSERT INTO lecturas (dispositivo, momento, valor) VALUES
    ('sensor-1', '2026-08-19T10:00:00Z', 21),
    ('sensor-1', '2026-08-19T10:01:00Z', 22),
    ('sensor-1', '2026-08-19T10:02:00Z', 23),
    ('sensor-2', '2026-08-19T10:00:00Z', 30),
    ('sensor-2', '2026-08-19T10:01:00Z', 31);

-- === consulta ===
-- Las dos ultimas lecturas de sensor-1, de la mas reciente a la mas antigua.
SELECT momento, valor
FROM lecturas
WHERE dispositivo = 'sensor-1'
ORDER BY momento DESC
LIMIT 2;
