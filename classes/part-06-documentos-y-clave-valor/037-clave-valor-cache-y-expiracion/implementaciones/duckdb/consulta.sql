-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/functions/date.html
-- nota: aqui no se implementa una cache: se AUDITA. Sobre un volcado de la
--       cache real, esta consulta responde cuantas claves hay en cada estado,
--       que es la pregunta de operacion que nadie se hace a tiempo.

-- === preparacion ===
CREATE TABLE cache (
    clave     VARCHAR PRIMARY KEY,
    valor     VARCHAR NOT NULL,
    expira_en VARCHAR          -- nulo = sin caducidad
);

INSERT INTO cache (clave, valor, expira_en) VALUES
    ('k1', 'con caducidad', '2099-01-01T00:00:00Z'),
    ('k2', 'permanente',    NULL);
-- k3 no se inserta: la ausencia tambien es un estado, y hay que distinguirla.

-- === consulta ===
-- Los tres estados que un almacen clave-valor con caducidad distingue, y que
-- aqui hay que reconstruir a mano porque el motor no los conoce.
WITH consultadas(clave) AS (
    VALUES ('k1'), ('k2'), ('k3')
)
SELECT c.clave,
       CASE
           WHEN e.clave IS NULL     THEN 'ausente'
           WHEN e.expira_en IS NULL THEN 'permanente'
           ELSE 'expira'
       END AS estado
FROM consultadas c
LEFT JOIN cache e ON e.clave = c.clave
ORDER BY c.clave;
