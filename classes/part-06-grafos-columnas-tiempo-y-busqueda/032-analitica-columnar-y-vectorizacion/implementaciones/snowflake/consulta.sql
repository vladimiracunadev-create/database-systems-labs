-- motor: snowflake
-- doc: https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions
-- nota: implementacion declarada. Snowflake divide la tabla en micro-particiones
--       columnares de 50-500 MB y guarda metadatos de cada una —minimo, maximo,
--       numero de valores distintos—, de modo que una consulta filtrada puede
--       descartar particiones enteras sin leerlas. Ese es todo el secreto, y
--       depende de que los datos esten agrupados por la columna que se filtra.
--       El computo se factura por TIEMPO ENCENDIDO: dimensionar y suspender el
--       almacen es parte del diseno, no una tarea de operacion posterior.

-- === preparacion ===
CREATE OR REPLACE TABLE hechos (
    id        NUMBER,
    categoria STRING,
    importe   NUMBER
) CLUSTER BY (categoria);

INSERT INTO hechos (id, categoria, importe)
SELECT SEQ4() + 1,
       'c' || TO_VARCHAR(MOD(SEQ4() + 1, 2)),
       SEQ4() + 1
FROM TABLE(GENERATOR(ROWCOUNT => 1000));

-- === consulta ===
SELECT categoria, SUM(importe) AS importe
FROM hechos
GROUP BY categoria
ORDER BY categoria;
