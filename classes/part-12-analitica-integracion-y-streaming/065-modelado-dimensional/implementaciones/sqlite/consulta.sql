-- motor: sqlite
-- doc: https://sqlite.org/lang_select.html
-- nota: el invariante que hace correcto al tipo 2 —una sola version vigente por
--       cliente— se puede IMPONER, no solo desear:
--         CREATE UNIQUE INDEX una_vigente ON dim_cliente (cliente)
--           WHERE vigente = 1;

-- === preparacion ===
-- La dimension con historia: una fila por VERSION del cliente, con su
-- periodo de validez y una clave sustituta propia. La clave de negocio
-- («A») se repite; la sustituta, no.
CREATE TABLE dim_cliente (
    sk       INTEGER PRIMARY KEY,
    cliente  TEXT NOT NULL,
    ciudad   TEXT NOT NULL,
    desde    TEXT NOT NULL,
    hasta    TEXT NOT NULL,
    vigente  INTEGER NOT NULL
);
INSERT INTO dim_cliente (sk, cliente, ciudad, desde, hasta, vigente) VALUES
    (1, 'A', 'Santiago', '2026-01-01', '2026-06-30', 0),
    (2, 'A', 'Valdivia', '2026-07-01', '9999-12-31', 1);

-- La tabla de hechos apunta a la VERSION, no al cliente. Ahi esta todo.
CREATE TABLE hechos_venta (
    id         INTEGER PRIMARY KEY,
    cliente_sk INTEGER NOT NULL,
    fecha      TEXT NOT NULL,
    importe    INTEGER NOT NULL
);
INSERT INTO hechos_venta (id, cliente_sk, fecha, importe) VALUES
    (1, 1, '2026-03-15', 100),   -- cuando A vivia en Santiago
    (2, 2, '2026-08-15', 200);   -- despues de mudarse a Valdivia

-- === consulta ===
-- Con dimension de tipo 2, cada venta se atribuye a la ciudad que el cliente
-- tenia EN ESE MOMENTO. Con una dimension de tipo 1 —sobrescribir la ciudad—
-- las dos ventas apareceran en Valdivia y el informe del primer trimestre
-- CAMBIARIA retroactivamente cada vez que alguien se muda.
SELECT d.ciudad, SUM(h.importe) AS importe
FROM hechos_venta h
JOIN dim_cliente d ON d.sk = h.cliente_sk
GROUP BY d.ciudad
ORDER BY d.ciudad;
