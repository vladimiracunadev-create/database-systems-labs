-- motor: sqlite
-- doc: https://sqlite.org/lang_datefunc.html
-- nota: la version equivocada esta a una palabra de distancia: cambiar
--       `tiempo_evento` por `tiempo_llegada` en el GROUP BY da 2 y 2. No hay
--       error, no hay aviso: hay un informe falso.

-- === preparacion ===
CREATE TABLE eventos (
    id             INTEGER PRIMARY KEY,
    tiempo_evento  TEXT NOT NULL,   -- cuando OCURRIO
    tiempo_llegada TEXT NOT NULL    -- cuando LLEGO al sistema
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
