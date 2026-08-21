-- motor: snowflake
-- doc: https://docs.snowflake.com/en/sql-reference/sql/merge
-- nota: implementacion declarada. MERGE mantiene la dimension de tipo 2 en una
--       sola sentencia: cierra la version vigente e inserta la nueva.
--       Y una confusion frecuente que conviene deshacer: el VIAJE EN EL TIEMPO
--       de Snowflake permite consultar la tabla como estaba hace dias, pero NO
--       sustituye a la dimension de tipo 2. Sirve para recuperarse de un error,
--       no para atribuir hechos historicos: el viaje en el tiempo caduca, y la
--       historia del negocio no.

-- === preparacion ===
CREATE OR REPLACE TABLE dim_cliente (
    sk      NUMBER,
    cliente STRING,
    ciudad  STRING,
    desde   DATE,
    hasta   DATE,
    vigente BOOLEAN
);
CREATE OR REPLACE TABLE hechos_venta (
    id         NUMBER,
    cliente_sk NUMBER,
    fecha      DATE,
    importe    NUMBER
);

INSERT INTO dim_cliente VALUES
    (1, 'A', 'Santiago', '2026-01-01', '2026-06-30', FALSE),
    (2, 'A', 'Valdivia', '2026-07-01', '9999-12-31', TRUE);
INSERT INTO hechos_venta VALUES (1, 1, '2026-03-15', 100), (2, 2, '2026-08-15', 200);

-- El mantenimiento de la dimension, en una sentencia:
--   MERGE INTO dim_cliente d
--   USING nuevos_clientes n ON d.cliente = n.cliente AND d.vigente
--   WHEN MATCHED AND d.ciudad <> n.ciudad
--     THEN UPDATE SET d.vigente = FALSE, d.hasta = CURRENT_DATE()
--   WHEN NOT MATCHED
--     THEN INSERT (...) VALUES (...);

-- === consulta ===
SELECT d.ciudad, SUM(h.importe) AS importe
FROM hechos_venta h
JOIN dim_cliente d ON d.sk = h.cliente_sk
GROUP BY d.ciudad
ORDER BY d.ciudad;
