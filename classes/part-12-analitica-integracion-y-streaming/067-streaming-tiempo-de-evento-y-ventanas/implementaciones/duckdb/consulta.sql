-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/functions/timestamp.html
-- nota: la consulta que de verdad hay que ejecutar aqui es la que decide el
--       periodo de gracia del flujo, sobre el historico real:
--         SELECT quantile_cont(
--                  epoch(tiempo_llegada::TIMESTAMP) - epoch(tiempo_evento::TIMESTAMP),
--                  0.99) AS retraso_p99
--         FROM eventos;
--       Sin ese numero, el periodo de gracia se elige a ojo.

-- === preparacion ===
CREATE TABLE eventos (
    id             INTEGER PRIMARY KEY,
    tiempo_evento  VARCHAR NOT NULL,   -- cuando OCURRIO
    tiempo_llegada VARCHAR NOT NULL    -- cuando LLEGO al sistema
);
INSERT INTO eventos (id, tiempo_evento, tiempo_llegada) VALUES
    (1, '2026-08-19T10:05:00Z', '2026-08-19T10:05:02Z'),
    (2, '2026-08-19T10:30:00Z', '2026-08-19T10:30:01Z'),
    -- El evento tardio: ocurrio a las 10:50 y llego a las 11:10, veinte
    -- minutos despues y con la ventana de las 10 ya «cerrada».
    (3, '2026-08-19T10:50:00Z', '2026-08-19T11:10:00Z'),
    (4, '2026-08-19T11:20:00Z', '2026-08-19T11:20:03Z');

-- === consulta ===
-- Agrupar por TIEMPO DE EVENTO: el tardio cuenta en la ventana de las 10, que
-- es cuando ocurrio. Cambiar `tiempo_evento` por `tiempo_llegada` daria 2 y 2,
-- y ese informe seria falso: diria que a las 10 pasaron dos cosas cuando
-- pasaron tres.
SELECT SUBSTR(tiempo_evento, 12, 2) || ':00' AS ventana,
       COUNT(*) AS eventos
FROM eventos
GROUP BY ventana
ORDER BY ventana;
