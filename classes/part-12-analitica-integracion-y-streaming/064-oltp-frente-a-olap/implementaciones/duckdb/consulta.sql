-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/why_duckdb
-- nota: el lado ANALITICO. Lee dos columnas y ninguna mas, vectorizadas. Y la
--       misma consulta funciona sobre el fichero exportado por el sistema
--       transaccional, sin cargarlo:
--         SELECT ... FROM 'ventas.parquet' GROUP BY ...

-- === preparacion ===
CREATE TABLE ventas (
    id      INTEGER PRIMARY KEY,
    mes     INTEGER NOT NULL,
    importe INTEGER NOT NULL
);
INSERT INTO ventas (id, mes, importe) VALUES
    (1, 1, 100), (2, 2, 200), (3, 3, 300),
    (4, 4, 400), (5, 5, 500), (6, 6, 600),
    (7, 7, 700), (8, 8, 800), (9, 9, 900),
    (10, 10, 1000), (11, 11, 1100), (12, 12, 1200);

-- === consulta ===
-- Una consulta ANALITICA: toca TODAS las filas, POCAS columnas, y devuelve
-- cuatro numeros. La transaccional seria la contraria —«dame la venta 7»— y
-- toca UNA fila con TODAS sus columnas.
-- El mismo motor no puede estar optimizado para las dos cosas, y esa es la
-- razon de que existan dos sistemas y un proceso que copia de uno a otro.
SELECT CASE WHEN mes <= 3 THEN 'T1'
            WHEN mes <= 6 THEN 'T2'
            WHEN mes <= 9 THEN 'T3'
            ELSE 'T4'
       END AS trimestre,
       SUM(importe) AS importe
FROM ventas
GROUP BY trimestre
ORDER BY trimestre;
