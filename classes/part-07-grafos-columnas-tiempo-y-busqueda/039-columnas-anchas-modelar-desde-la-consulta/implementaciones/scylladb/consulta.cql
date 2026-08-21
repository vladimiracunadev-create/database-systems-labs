-- motor: scylladb
-- doc: https://opensource.docs.scylladb.com/stable/cql/ddl.html
-- nota: implementacion declarada, y deliberadamente IDENTICA a la de Cassandra:
--       ese es el argumento. ScyllaDB habla el mismo CQL y usa el mismo modelo
--       de datos, asi que el diseno migra sin tocar una linea. Lo que cambia
--       esta debajo: implementacion en C++ con un hilo fijado por nucleo y sin
--       recolector de basura, lo que elimina las pausas que en Cassandra hay
--       que ajustar a mano.
--       Lo que NO es identico: indices secundarios, vistas materializadas y
--       herramientas de operacion. La compatibilidad es alta, no total.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS telemetria
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS telemetria.lecturas_por_dispositivo;

CREATE TABLE telemetria.lecturas_por_dispositivo (
    dispositivo text,
    momento     timestamp,
    valor       int,
    PRIMARY KEY (dispositivo, momento)
) WITH CLUSTERING ORDER BY (momento DESC);

INSERT INTO telemetria.lecturas_por_dispositivo (dispositivo, momento, valor)
  VALUES ('sensor-1', '2026-08-19T10:01:00Z', 22);
INSERT INTO telemetria.lecturas_por_dispositivo (dispositivo, momento, valor)
  VALUES ('sensor-1', '2026-08-19T10:02:00Z', 23);

-- === consulta ===
SELECT momento, valor
FROM telemetria.lecturas_por_dispositivo
WHERE dispositivo = 'sensor-1'
LIMIT 2;
