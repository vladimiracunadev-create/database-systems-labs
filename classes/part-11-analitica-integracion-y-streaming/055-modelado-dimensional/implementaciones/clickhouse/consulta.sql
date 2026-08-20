-- motor: clickhouse
-- doc: https://clickhouse.com/docs/en/sql-reference/dictionaries
-- nota: implementacion declarada, y con una advertencia importante. Los
--       DICCIONARIOS de ClickHouse resuelven la dimension sin reunion, con una
--       busqueda en memoria por clave... y devuelven el valor ACTUAL. Usarlos
--       con una dimension de tipo 2 reintroduce exactamente el error que el
--       tipo 2 existia para evitar: las ventas viejas se atribuyen a la ciudad
--       nueva.
--       La atribucion historica exige la reunion por rango de fechas de abajo,
--       que es justo lo que peor se le da a un motor columnar distribuido.

-- === preparacion ===
CREATE TABLE dim_cliente (
    sk      UInt32,
    cliente String,
    ciudad  String,
    desde   Date,
    hasta   Date,
    vigente UInt8
) ENGINE = MergeTree ORDER BY (cliente, desde);

CREATE TABLE hechos_venta (
    id         UInt32,
    cliente_sk UInt32,
    fecha      Date,
    importe    UInt32
) ENGINE = MergeTree ORDER BY (fecha, id);

INSERT INTO dim_cliente VALUES
    (1, 'A', 'Santiago', '2026-01-01', '2026-06-30', 0),
    (2, 'A', 'Valdivia', '2026-07-01', '2106-02-07', 1);
INSERT INTO hechos_venta VALUES (1, 1, '2026-03-15', 100), (2, 2, '2026-08-15', 200);

-- === consulta ===
SELECT d.ciudad, SUM(h.importe) AS importe
FROM hechos_venta AS h
INNER JOIN dim_cliente AS d ON d.sk = h.cliente_sk
GROUP BY d.ciudad
ORDER BY d.ciudad;
