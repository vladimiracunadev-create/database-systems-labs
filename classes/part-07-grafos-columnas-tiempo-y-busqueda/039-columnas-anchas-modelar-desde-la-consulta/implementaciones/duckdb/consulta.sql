-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/orderby.html
-- nota: la pregunta que hay que hacerle a DuckDB no es esta, sino esta otra:
--         SELECT dispositivo, COUNT(*) FROM lecturas
--         GROUP BY dispositivo ORDER BY 2 DESC LIMIT 10;
--       es decir, que particion va a crecer sin limite. Mejor saberlo antes.

-- === preparacion ===
CREATE TABLE lecturas (
    dispositivo VARCHAR NOT NULL,
    momento     VARCHAR NOT NULL,
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
