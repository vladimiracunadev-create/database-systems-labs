-- motor: sqlite
-- doc: https://sqlite.org/json1.html
-- nota: json_each se comporta como una tabla virtual, asi que desanidar y
--       agrupar se escribe como cualquier otra consulta. Lo que no hay es
--       indice: esto recorre la tabla entera siempre.

-- === preparacion ===
CREATE TABLE pedidos (
    id     TEXT PRIMARY KEY,
    lineas TEXT NOT NULL
);

INSERT INTO pedidos (id, lineas) VALUES
    ('P-1', '[{"producto":"teclado","categoria":"perifericos","importe":120},
              {"producto":"raton","categoria":"accesorios","importe":80}]'),
    ('P-2', '[{"producto":"cable","categoria":"accesorios","importe":100}]');

-- === consulta ===
SELECT json_extract(l.value, '$.categoria') AS categoria,
       SUM(json_extract(l.value, '$.importe')) AS importe
FROM pedidos p, json_each(p.lineas) l
GROUP BY categoria
ORDER BY categoria;
