-- motor: clickhouse
-- doc: https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions
-- nota: implementacion declarada. ClickHouse resuelve el problema por el camino
--       contrario al de un procesador de flujos: no cierra ventanas, GUARDA
--       TODO y agrega por tiempo de evento cuando alguien pregunta. El evento
--       tardio simplemente se inserta y la proxima consulta ya lo incluye; no
--       hace falta marca de agua porque no hay nada que cerrar.
--
--       Y el precio, que en contabilidad no se acepta: el resultado de un
--       informe puede cambiar despues de publicado.

-- === preparacion ===
CREATE TABLE eventos (
    id             UInt32,
    tiempo_evento  DateTime,
    tiempo_llegada DateTime
) ENGINE = MergeTree ORDER BY tiempo_evento;

INSERT INTO eventos VALUES
    (1, '2026-08-19 10:05:00', '2026-08-19 10:05:02'),
    (2, '2026-08-19 10:30:00', '2026-08-19 10:30:01'),
    (3, '2026-08-19 10:50:00', '2026-08-19 11:10:00'),
    (4, '2026-08-19 11:20:00', '2026-08-19 11:20:03');

-- === consulta ===
SELECT formatDateTime(toStartOfHour(tiempo_evento), '%H:%M') AS ventana,
       COUNT(*) AS eventos
FROM eventos
GROUP BY ventana
ORDER BY ventana;
