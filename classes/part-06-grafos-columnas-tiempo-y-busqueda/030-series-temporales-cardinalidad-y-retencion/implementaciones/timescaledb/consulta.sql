-- motor: timescaledb
-- doc: https://docs.timescale.com/use-timescale/latest/time-buckets/
-- nota: implementacion declarada. Es PostgreSQL con la parte temporal resuelta:
--       hipertabla que particiona sola, time_bucket con ventanas arbitrarias,
--       agregado continuo que se mantiene al dia y politicas declarativas de
--       retencion y compresion. Todo lo de abajo sigue siendo SQL, y se puede
--       reunir con el resto del esquema.

-- === preparacion ===
CREATE EXTENSION IF NOT EXISTS timescaledb;

DROP TABLE IF EXISTS lecturas CASCADE;

CREATE TABLE lecturas (
    momento timestamptz NOT NULL,
    valor   integer NOT NULL
);
SELECT create_hypertable('lecturas', by_range('momento'));

INSERT INTO lecturas (momento, valor) VALUES
    ('2026-08-19 10:00:00+00', 20),
    ('2026-08-19 10:15:00+00', 21),
    ('2026-08-19 10:45:00+00', 25),
    ('2026-08-19 11:05:00+00', 22),
    ('2026-08-19 11:30:00+00', 23);

-- El agregado que NO hay que recalcular: se mantiene solo al llegar datos.
CREATE MATERIALIZED VIEW lecturas_por_hora
WITH (timescaledb.continuous) AS
SELECT time_bucket(INTERVAL '1 hour', momento) AS hora,
       SUM(valor) AS total
FROM lecturas
GROUP BY hora;

-- Y la retencion, declarada en vez de programada a mano:
SELECT add_retention_policy('lecturas', INTERVAL '90 days');

-- === consulta ===
SELECT to_char(hora, 'YYYY-MM-DD HH24:MI') AS hora, total
FROM lecturas_por_hora
ORDER BY hora;
