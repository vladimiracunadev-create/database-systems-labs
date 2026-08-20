-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/indexes.html
-- nota: DuckDB no tiene indices unicos parciales, asi que aqui la regla se
--       AUDITA en vez de imponerse: la fila que sobra no se inserta porque el
--       guion no la inserta, no porque el motor la rechace. Es la diferencia
--       entre un almacen analitico y el sistema que custodia la verdad.

-- === preparacion ===
CREATE TABLE clientes (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL
);
CREATE TABLE direcciones (
    id         INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    ciudad     VARCHAR NOT NULL,
    principal  BOOLEAN NOT NULL DEFAULT false
);

INSERT INTO clientes VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO direcciones VALUES
    (1, 1, 'Santiago',   true),
    (2, 1, 'Valdivia',   false),
    (3, 2, 'Valparaiso', true);

-- === consulta ===
SELECT c.nombre AS cliente,
       COUNT(d.id) AS principales
FROM clientes c
LEFT JOIN direcciones d ON d.cliente_id = c.id AND d.principal
GROUP BY c.id, c.nombre
ORDER BY c.nombre;
