-- motor: clickhouse
-- doc: https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree
-- nota: implementacion declarada. Aqui el informe trimestral no se calcula: se
--       lee ya calculado, porque la vista materializada agrega AL INSERTAR.
--       El precio: no es transaccional, y corregir una venta mal registrada no
--       es un UPDATE sino una mutacion asincrona que reescribe partes.

-- === preparacion ===
CREATE TABLE ventas (
    id      UInt32,
    mes     UInt8,
    importe UInt32
) ENGINE = MergeTree ORDER BY (mes, id);

CREATE MATERIALIZED VIEW ventas_por_trimestre
ENGINE = SummingMergeTree ORDER BY trimestre
AS SELECT concat('T', toString(intDiv(mes - 1, 3) + 1)) AS trimestre,
          SUM(importe) AS importe
FROM ventas GROUP BY trimestre;

INSERT INTO ventas VALUES
    (1, 1, 100), (2, 2, 200), (3, 3, 300), (4, 4, 400), (5, 5, 500), (6, 6, 600),
    (7, 7, 700), (8, 8, 800), (9, 9, 900), (10, 10, 1000), (11, 11, 1100), (12, 12, 1200);

-- === consulta ===
SELECT trimestre, SUM(importe) AS importe
FROM ventas_por_trimestre
GROUP BY trimestre
ORDER BY trimestre;
