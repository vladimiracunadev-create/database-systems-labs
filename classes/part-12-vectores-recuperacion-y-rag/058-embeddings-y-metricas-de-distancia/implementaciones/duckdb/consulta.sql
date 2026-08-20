-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/functions/array
-- nota: aqui el vector es un tipo, no tres columnas. La forma idiomatica seria
--         CREATE TABLE documentos (id VARCHAR, v FLOAT[3]);
--         SELECT id, array_distance(v, [2,0,0]::FLOAT[3]) AS d
--         FROM documentos ORDER BY d;
--       Se escribe con enteros y aritmetica explicita para que el resultado sea
--       exacto y comparable con el resto de motores, sin discutir decimales.

-- === preparacion ===
CREATE TABLE documentos (
    id VARCHAR PRIMARY KEY,
    v1 INTEGER NOT NULL,
    v2 INTEGER NOT NULL,
    v3 INTEGER NOT NULL
);
INSERT INTO documentos VALUES ('A', 2, 0, 0), ('B', 0, 2, 0), ('C', 1, 1, 0);

-- === consulta ===
SELECT id,
       (v1 - 2) * (v1 - 2) + (v2 - 0) * (v2 - 0) + (v3 - 0) * (v3 - 0) AS distancia
FROM documentos
ORDER BY distancia, id;
