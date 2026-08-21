-- motor: clickhouse
-- doc: https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions
-- nota: implementacion declarada. La vista materializada de ClickHouse no es
--       una copia que se refresca: es un disparador de insercion que agrega al
--       llegar los datos. El agregado nunca se recalcula.
--       El precio: corregir una lectura mal enviada no es un UPDATE, es una
--       mutacion asincrona que reescribe partes enteras.

-- === preparacion ===
CREATE TABLE lecturas (
    momento DateTime,
    valor   Int32
) ENGINE = MergeTree ORDER BY momento;

CREATE MATERIALIZED VIEW lecturas_por_hora
ENGINE = SummingMergeTree ORDER BY hora
AS SELECT toStartOfHour(momento) AS hora, SUM(valor) AS total
FROM lecturas GROUP BY hora;

INSERT INTO lecturas VALUES
    ('2026-08-19 10:00:00', 20),
    ('2026-08-19 10:15:00', 21),
    ('2026-08-19 10:45:00', 25),
    ('2026-08-19 11:05:00', 22),
    ('2026-08-19 11:30:00', 23);

-- === consulta ===
SELECT formatDateTime(hora, '%Y-%m-%d %H:%M') AS hora, SUM(total) AS total
FROM lecturas_por_hora
GROUP BY hora
ORDER BY hora;
