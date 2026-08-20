-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/functions-datetime.html
-- nota: la retencion barata no es DELETE, es DROP de una particion. Con
--       particionado declarativo por rango, tirar un mes entero cuesta lo mismo
--       que borrar un archivo:
--         CREATE TABLE lecturas (...) PARTITION BY RANGE (momento);
--         DROP TABLE lecturas_2026_07;

-- === preparacion ===
DROP TABLE IF EXISTS lecturas;

CREATE TABLE lecturas (
    momento timestamptz NOT NULL,
    valor   integer NOT NULL
);
INSERT INTO lecturas (momento, valor) VALUES
    (TIMESTAMPTZ '2026-08-19 10:00:00+00', 20),
    (TIMESTAMPTZ '2026-08-19 10:15:00+00', 21),
    (TIMESTAMPTZ '2026-08-19 10:45:00+00', 25),
    (TIMESTAMPTZ '2026-08-19 11:05:00+00', 22),
    (TIMESTAMPTZ '2026-08-19 11:30:00+00', 23);

-- === consulta ===
-- `AT TIME ZONE 'UTC'` fija la zona en la EXPRESION en vez de en la sesion. Si
-- dependiera de la sesion, la misma consulta agruparia en horas distintas segun
-- quien la lanzara, y ese es un error de informe muy dificil de ver.
SELECT to_char(date_trunc('hour', momento AT TIME ZONE 'UTC'),
               'YYYY-MM-DD HH24:MI') AS hora,
       SUM(valor) AS total
FROM lecturas
GROUP BY 1
ORDER BY 1;
