-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/functions-datetime.html
-- nota: con tipos de fecha de verdad, la ventana se expresa con date_trunc y el
--       retraso se puede medir como intervalo. Lo que no hay es estado de
--       ventana ni marca de agua: aqui siempre estan todos los eventos, porque
--       se consulta una tabla, no un flujo.

-- === preparacion ===
DROP TABLE IF EXISTS eventos;

CREATE TABLE eventos (
    id             integer PRIMARY KEY,
    tiempo_evento  timestamptz NOT NULL,
    tiempo_llegada timestamptz NOT NULL
);
INSERT INTO eventos (id, tiempo_evento, tiempo_llegada) VALUES
    (1, '2026-08-19 10:05:00+00', '2026-08-19 10:05:02+00'),
    (2, '2026-08-19 10:30:00+00', '2026-08-19 10:30:01+00'),
    (3, '2026-08-19 10:50:00+00', '2026-08-19 11:10:00+00'),
    (4, '2026-08-19 11:20:00+00', '2026-08-19 11:20:03+00');

-- === consulta ===
SELECT to_char(date_trunc('hour', tiempo_evento AT TIME ZONE 'UTC'), 'HH24:MI') AS ventana,
       COUNT(*) AS eventos
FROM eventos
GROUP BY 1
ORDER BY 1;
