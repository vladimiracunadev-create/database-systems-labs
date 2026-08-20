-- motor: clickhouse
-- doc: https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree
-- nota: implementacion declarada. Aqui la idempotencia se consigue SIN UPDATE:
--       se insertan siempre filas nuevas con una version, y la fusion se queda
--       con la ultima. Encaja con un almacen que solo sabe anadir.
--       El precio, que hay que tener presente: la deduplicacion ocurre CUANDO
--       LA FUSION DECIDE, no al insertar. Hasta entonces conviven las dos
--       versiones y una consulta puede contarlas las dos. De ahi el FINAL de
--       abajo, que fuerza la vista deduplicada y es caro.

-- === preparacion ===
CREATE TABLE destino (
    cliente String,
    saldo   UInt32,
    version UInt64
) ENGINE = ReplacingMergeTree(version) ORDER BY cliente;

INSERT INTO destino VALUES ('C-1', 10, 1), ('C-2', 20, 1), ('C-3', 30, 1);
INSERT INTO destino VALUES ('C-1', 10, 1), ('C-2', 20, 1), ('C-3', 30, 1);

-- === consulta ===
SELECT cliente, saldo FROM destino FINAL ORDER BY cliente;
