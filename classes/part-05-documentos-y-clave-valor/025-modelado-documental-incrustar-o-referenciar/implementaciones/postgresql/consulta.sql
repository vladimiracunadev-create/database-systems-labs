-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/datatype-json.html
-- nota: jsonb no guarda texto: guarda una representacion binaria indexable con
--       GIN. Por eso aqui se puede incrustar SIN renunciar al indice, a las
--       transacciones ni a las claves foraneas del resto del esquema.

-- === preparacion ===
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id     text PRIMARY KEY,
    lineas jsonb NOT NULL
);
CREATE INDEX pedidos_lineas ON pedidos USING GIN (lineas);

INSERT INTO pedidos (id, lineas) VALUES (
    'P-1',
    '[{"producto":"teclado","importe":120},
      {"producto":"raton","importe":80},
      {"producto":"cable","importe":100}]'::jsonb
);

-- === consulta ===
SELECT l->>'producto' AS producto,
       (l->>'importe')::int AS importe
FROM pedidos p
CROSS JOIN LATERAL jsonb_array_elements(p.lineas) AS l
WHERE p.id = 'P-1'
ORDER BY producto;
