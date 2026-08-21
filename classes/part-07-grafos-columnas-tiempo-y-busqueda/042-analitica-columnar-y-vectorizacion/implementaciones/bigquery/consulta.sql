-- motor: bigquery
-- doc: https://cloud.google.com/bigquery/docs/best-practices-costs
-- nota: implementacion declarada. Aqui la optimizacion no es de tiempo: es de
--       FACTURA. Se paga por bytes LEIDOS, y al ser columnar, leer dos columnas
--       cuesta dos columnas. La misma consulta con SELECT * sobre una tabla de
--       cien columnas cuesta cincuenta veces mas y devuelve lo mismo.
--       Antes de lanzarla en serio:
--         bq query --dry_run   -> dice cuantos bytes se van a leer, sin cobrar.

-- === preparacion ===
CREATE OR REPLACE TABLE analitica.hechos
PARTITION BY RANGE_BUCKET(id, GENERATE_ARRAY(0, 1000000, 100000))
CLUSTER BY categoria
AS
SELECT n AS id,
       CONCAT('c', CAST(MOD(n, 2) AS STRING)) AS categoria,
       n AS importe
FROM UNNEST(GENERATE_ARRAY(1, 1000)) AS n;

-- === consulta ===
SELECT categoria, SUM(importe) AS importe
FROM analitica.hechos
GROUP BY categoria
ORDER BY categoria;
