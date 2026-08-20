-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html
-- nota: implementacion declarada. Aqui la retencion se declara AL ESCRIBIR, que
--       es cuando de verdad se sabe cuanto tiempo hace falta el dato:
--         USING TTL 7776000    -- noventa dias
--       Con la estrategia de compactacion por ventana temporal (TWCS), expirar
--       un periodo entero es tirar un archivo completo, sin recorrer filas.
--       El precio: cada dato expirado deja una lapida que se recorre en las
--       lecturas hasta que la compactacion la retire.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS gobierno
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS gobierno.eventos;

CREATE TABLE gobierno.eventos (
    id     int PRIMARY KEY,
    correo text,
    fecha  date
) WITH compaction = {'class': 'TimeWindowCompactionStrategy',
                     'compaction_window_unit': 'DAYS',
                     'compaction_window_size': 30};

INSERT INTO gobierno.eventos (id, correo, fecha)
  VALUES (2, 'linus@example.org', '2026-08-10') USING TTL 7776000;
INSERT INTO gobierno.eventos (id, correo, fecha)
  VALUES (3, 'grace@otro.org', '2026-08-15') USING TTL 7776000;

-- === consulta ===
-- CQL no tiene funciones de cadena para enmascarar: el enmascarado se hace en
-- la capa que exporta. Es una limitacion, y tambien un recordatorio de donde
-- deberia estar siempre.
SELECT id, correo, fecha, TTL(correo) AS segundos_restantes FROM gobierno.eventos;
