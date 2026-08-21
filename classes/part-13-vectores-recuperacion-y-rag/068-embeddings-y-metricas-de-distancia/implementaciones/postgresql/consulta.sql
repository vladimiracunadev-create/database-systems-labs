-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/functions-math.html
-- nota: con la extension pgvector, esto se escribe asi:
--         CREATE EXTENSION vector;
--         CREATE TABLE documentos (id text PRIMARY KEY, v vector(3));
--         CREATE INDEX ON documentos USING hnsw (v vector_l2_ops);
--         SELECT id, v <-> '[2,0,0]' AS distancia
--         FROM documentos ORDER BY v <-> '[2,0,0]' LIMIT 10;
--       Aqui se usa aritmetica a mano porque la imagen de este repositorio no
--       trae la extension, y afirmar que la trae seria falso.
--
--       Lo que hace valiosa esa extension no es la distancia: es poder FILTRAR
--       por metadatos y buscar por vector en la MISMA consulta, sobre datos
--       que estan en la misma transaccion.

-- === preparacion ===
DROP TABLE IF EXISTS documentos;

CREATE TABLE documentos (
    id text PRIMARY KEY,
    v1 integer NOT NULL,
    v2 integer NOT NULL,
    v3 integer NOT NULL
);
INSERT INTO documentos (id, v1, v2, v3) VALUES
    ('A', 2, 0, 0), ('B', 0, 2, 0), ('C', 1, 1, 0);

-- === consulta ===
SELECT id,
       (v1 - 2) * (v1 - 2) + (v2 - 0) * (v2 - 0) + (v3 - 0) * (v3 - 0) AS distancia
FROM documentos
ORDER BY distancia, id;
