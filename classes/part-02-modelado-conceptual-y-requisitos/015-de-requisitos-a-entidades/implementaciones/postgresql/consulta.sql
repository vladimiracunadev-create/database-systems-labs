-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/indexes-partial.html
-- nota: la documentacion oficial presenta el indice unico parcial como la
--       forma canonica de «como mucho uno que cumpla la condicion».

-- === preparacion ===
DROP TABLE IF EXISTS direcciones, clientes;

CREATE TABLE clientes (
    id     integer PRIMARY KEY,
    nombre text NOT NULL
);
CREATE TABLE direcciones (
    id         serial PRIMARY KEY,
    cliente_id integer NOT NULL REFERENCES clientes(id),
    ciudad     text NOT NULL,
    principal  boolean NOT NULL DEFAULT false
);
CREATE UNIQUE INDEX una_principal_por_cliente
    ON direcciones (cliente_id) WHERE principal;

INSERT INTO clientes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO direcciones (cliente_id, ciudad, principal) VALUES
    (1, 'Santiago',   true),
    (1, 'Valdivia',   false),
    (2, 'Valparaiso', true);
INSERT INTO direcciones (cliente_id, ciudad, principal) VALUES (1, 'Arica', true)
    ON CONFLICT DO NOTHING;

-- === consulta ===
SELECT c.nombre AS cliente,
       COUNT(d.id) AS principales
FROM clientes c
LEFT JOIN direcciones d ON d.cliente_id = c.id AND d.principal
GROUP BY c.id, c.nombre
ORDER BY c.nombre;
