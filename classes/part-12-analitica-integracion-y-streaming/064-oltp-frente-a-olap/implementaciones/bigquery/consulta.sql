-- motor: bigquery
-- doc: https://cloud.google.com/bigquery/docs/introduction
-- nota: implementacion declarada. No hay servidor, ni indices, ni ajuste: solo
--       consultas y una factura. Se paga por BYTES LEIDOS, asi que esta
--       consulta cuesta dos columnas; con SELECT * costaria la tabla entera y
--       devolveria lo mismo.
--         bq query --dry_run   dice cuantos bytes antes de cobrarlos.

-- === preparacion ===
CREATE OR REPLACE TABLE analitica.ventas AS
SELECT n AS id, n AS mes, n * 100 AS importe
FROM UNNEST(GENERATE_ARRAY(1, 12)) AS n;

-- === consulta ===
SELECT CONCAT('T', CAST(DIV(mes - 1, 3) + 1 AS STRING)) AS trimestre,
       SUM(importe) AS importe
FROM analitica.ventas
GROUP BY trimestre
ORDER BY trimestre;
