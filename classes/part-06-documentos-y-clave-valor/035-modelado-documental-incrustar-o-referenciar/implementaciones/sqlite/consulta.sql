-- motor: sqlite
-- doc: https://sqlite.org/json1.html
-- nota: forma INCRUSTADA con JSON. Para el motor eso es texto: no hay
--       restricciones sobre su contenido, ni claves foraneas, ni indice que lo
--       recorra. La forma referenciada seria una tabla `lineas` de toda la vida.

-- === preparacion ===
CREATE TABLE pedidos (
    id     TEXT PRIMARY KEY,
    lineas TEXT NOT NULL   -- arreglo JSON incrustado
);

INSERT INTO pedidos (id, lineas) VALUES (
    'P-1',
    '[{"producto":"teclado","importe":120},
      {"producto":"raton","importe":80},
      {"producto":"cable","importe":100}]'
);

-- === consulta ===
SELECT json_extract(l.value, '$.producto') AS producto,
       json_extract(l.value, '$.importe')  AS importe
FROM pedidos p, json_each(p.lineas) l
WHERE p.id = 'P-1'
ORDER BY producto;
