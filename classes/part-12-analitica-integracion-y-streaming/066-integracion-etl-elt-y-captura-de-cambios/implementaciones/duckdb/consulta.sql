-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/insert
-- nota: la T de ELT. En un proceso real, el origen no seria un VALUES sino un
--       fichero leido directamente:
--         INSERT INTO destino SELECT * FROM read_csv_auto('lote.csv')
--         ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- === preparacion ===
CREATE TABLE destino (
    cliente VARCHAR PRIMARY KEY,
    saldo   INTEGER NOT NULL
);

INSERT INTO destino VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

INSERT INTO destino VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- === consulta ===
SELECT cliente, saldo FROM destino ORDER BY cliente;
