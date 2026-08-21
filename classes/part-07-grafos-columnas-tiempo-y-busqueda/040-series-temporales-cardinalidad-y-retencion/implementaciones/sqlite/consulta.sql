-- motor: sqlite
-- doc: https://sqlite.org/lang_datefunc.html
-- nota: SQLite NO tiene tipo de fecha. Estas marcas son texto ISO-8601, que se
--       ordena y se compara bien por casualidad del formato. Mezclar texto ISO
--       con segundos desde la epoca en la misma columna no da error: da un
--       resultado equivocado.

-- === preparacion ===
CREATE TABLE lecturas (
    momento TEXT NOT NULL,
    valor   INTEGER NOT NULL
);
INSERT INTO lecturas (momento, valor) VALUES
    ('2026-08-19T10:00:00Z', 20),
    ('2026-08-19T10:15:00Z', 21),
    ('2026-08-19T10:45:00Z', 25),
    ('2026-08-19T11:05:00Z', 22),
    ('2026-08-19T11:30:00Z', 23);

-- === consulta ===
SELECT strftime('%Y-%m-%d %H:00', momento) AS hora,
       SUM(valor) AS total
FROM lecturas
GROUP BY hora
ORDER BY hora;
