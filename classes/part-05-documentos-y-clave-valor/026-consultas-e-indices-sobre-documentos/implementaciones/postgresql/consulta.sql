-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/functions-json.html
-- nota: lo que aqui se puede hacer y en un almacen documental puro no: esta
--       misma consulta podria reunir los documentos con tablas normales del
--       mismo esquema, en la misma transaccion.

-- === preparacion ===
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id     text PRIMARY KEY,
    lineas jsonb NOT NULL
);
CREATE INDEX pedidos_lineas ON pedidos USING GIN (lineas);

INSERT INTO pedidos (id, lineas) VALUES
    ('P-1', '[{"producto":"teclado","categoria":"perifericos","importe":120},
              {"producto":"raton","categoria":"accesorios","importe":80}]'::jsonb),
    ('P-2', '[{"producto":"cable","categoria":"accesorios","importe":100}]'::jsonb);

-- === consulta ===
SELECT l->>'categoria' AS categoria,
       SUM((l->>'importe')::int) AS importe
FROM pedidos p
CROSS JOIN LATERAL jsonb_array_elements(p.lineas) AS l
GROUP BY l->>'categoria'
ORDER BY categoria;
