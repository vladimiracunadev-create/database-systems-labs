-- motor: clickhouse
-- doc: https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree
-- nota: implementacion declarada. La clausula ORDER BY del motor MergeTree no
--       es un orden de presentacion: es el ORDEN FISICO de los datos, y de el
--       dependen la compresion y los indices de salto, que descartan bloques
--       enteros sin leerlos.
--       Lo que este motor NO tiene: transacciones. No hay BEGIN, y corregir
--       filas es una mutacion asincrona que reescribe partes.

-- === preparacion ===
CREATE TABLE hechos (
    id        UInt32,
    categoria LowCardinality(String),
    importe   UInt32
) ENGINE = MergeTree ORDER BY (categoria, id);

INSERT INTO hechos
SELECT number + 1, concat('c', toString((number + 1) % 2)), number + 1
FROM numbers(1000);

-- === consulta ===
SELECT categoria, SUM(importe) AS importe
FROM hechos
GROUP BY categoria
ORDER BY categoria;
