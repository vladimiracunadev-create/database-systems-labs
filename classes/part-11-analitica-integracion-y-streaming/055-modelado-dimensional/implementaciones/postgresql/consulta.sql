-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/rangetypes.html
-- nota: aqui los dos invariantes del tipo 2 se pueden IMPONER:
--         1) una sola version vigente  -> indice unico parcial
--         2) periodos que no se solapan -> restriccion de exclusion con daterange
--       Sin ellos, el tipo 2 es una convencion que alguien acabara rompiendo, y
--       el sintoma sera un informe con ventas duplicadas.

-- === preparacion ===
DROP TABLE IF EXISTS hechos_venta, dim_cliente;

CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE dim_cliente (
    sk      integer PRIMARY KEY,
    cliente text NOT NULL,
    ciudad  text NOT NULL,
    validez daterange NOT NULL,
    vigente boolean NOT NULL,
    EXCLUDE USING gist (cliente WITH =, validez WITH &&)
);
CREATE UNIQUE INDEX una_version_vigente ON dim_cliente (cliente) WHERE vigente;

INSERT INTO dim_cliente (sk, cliente, ciudad, validez, vigente) VALUES
    (1, 'A', 'Santiago', daterange('2026-01-01', '2026-07-01', '[)'), false),
    (2, 'A', 'Valdivia', daterange('2026-07-01', 'infinity', '[)'), true);

CREATE TABLE hechos_venta (
    id         integer PRIMARY KEY,
    cliente_sk integer NOT NULL REFERENCES dim_cliente(sk),
    fecha      date NOT NULL,
    importe    integer NOT NULL
);
INSERT INTO hechos_venta (id, cliente_sk, fecha, importe) VALUES
    (1, 1, DATE '2026-03-15', 100),
    (2, 2, DATE '2026-08-15', 200);

-- === consulta ===
SELECT d.ciudad, SUM(h.importe) AS importe
FROM hechos_venta h
JOIN dim_cliente d ON d.sk = h.cliente_sk
GROUP BY d.ciudad
ORDER BY d.ciudad;
