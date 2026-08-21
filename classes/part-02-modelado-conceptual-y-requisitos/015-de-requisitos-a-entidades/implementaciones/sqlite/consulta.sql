-- motor: sqlite
-- doc: https://sqlite.org/partialindex.html
-- nota: el indice unico parcial es la traduccion exacta de «como mucho una
--       principal por cliente». Sin el WHERE, la regla seria «como mucho una
--       direccion por cliente», que es otro requisito.

-- === preparacion ===
CREATE TABLE clientes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);
CREATE TABLE direcciones (
    id         INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    ciudad     TEXT NOT NULL,
    principal  INTEGER NOT NULL DEFAULT 0 CHECK (principal IN (0, 1))
);
CREATE UNIQUE INDEX una_principal_por_cliente
    ON direcciones (cliente_id) WHERE principal = 1;

INSERT INTO clientes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO direcciones (cliente_id, ciudad, principal) VALUES
    (1, 'Santiago',   1),
    (1, 'Valdivia',   0),   -- se mudo: la anterior se conserva
    (2, 'Valparaiso', 1);
-- Este intento viola la regla y el motor lo rechaza; sin el indice, pasaria.
INSERT OR IGNORE INTO direcciones (cliente_id, ciudad, principal) VALUES (1, 'Arica', 1);

-- === consulta ===
SELECT c.nombre AS cliente,
       COUNT(d.id) AS principales
FROM clientes c
LEFT JOIN direcciones d ON d.cliente_id = c.id AND d.principal = 1
GROUP BY c.id, c.nombre
ORDER BY c.nombre;
