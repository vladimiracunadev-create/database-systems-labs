-- motor: sqlite
-- doc: https://sqlite.org/lang_upsert.html
-- nota: la carga se ejecuta DOS VECES a proposito, con el mismo lote. Si en vez
--       de ON CONFLICT hubiera un INSERT normal, la segunda pasada fallaria por
--       clave duplicada; con INSERT OR IGNORE no fallaria pero tampoco
--       actualizaria los saldos cambiados. El upsert es lo unico que hace las
--       dos cosas bien.

-- === preparacion ===
CREATE TABLE destino (
    cliente TEXT PRIMARY KEY,
    saldo   INTEGER NOT NULL
);

-- Primera pasada.
INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- Segunda pasada: EL MISMO LOTE. Alguien relanzo el trabajo.
INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- === consulta ===
SELECT cliente, saldo FROM destino ORDER BY cliente;
