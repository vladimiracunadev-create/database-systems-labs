-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/indexes-partial.html
-- nota: aqui aparece un limite que sorprende. Un indice parcial
--         CREATE INDEX ... WHERE expira_en > now()
--       NO se puede crear: el predicado de un indice tiene que ser IMMUTABLE y
--       now() es STABLE. Si se pudiera, el indice quedaria obsoleto en cuanto
--       pasara el tiempo. Asi que el indice va sobre la columna y el filtro se
--       aplica en cada consulta, que es exactamente el trabajo que Redis evita.

-- === preparacion ===
DROP TABLE IF EXISTS cache;

CREATE TABLE cache (
    clave     text PRIMARY KEY,
    valor     text NOT NULL,
    expira_en timestamptz
);
CREATE INDEX cache_por_vencimiento ON cache (expira_en);

INSERT INTO cache (clave, valor, expira_en) VALUES
    ('k1', 'con caducidad', TIMESTAMPTZ '2099-01-01 00:00:00+00'),
    ('k2', 'permanente',    NULL);

-- === consulta ===
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
