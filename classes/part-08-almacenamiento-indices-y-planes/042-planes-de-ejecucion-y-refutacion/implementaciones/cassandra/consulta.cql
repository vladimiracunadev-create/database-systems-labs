-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/managing/tools/cqlsh.html
-- nota: implementacion declarada. Aqui no hay plan que leer porque no hay
--       optimizador que elija: la consulta hace lo que el modelo permite. Lo que
--       si hay es TRACING, que muestra la traza DISTRIBUIDA:
--         - que nodo coordino la consulta
--         - a que replicas pregunto y cuanto tardo cada una
--         - cuantas SSTables se abrieron
--         - cuantas lapidas se recorrieron  <- el diagnostico mas util del motor
--
--       Y la consecuencia incomoda: si va lenta, la culpa es del modelo de
--       datos. El diagnostico es barato; la correccion es crear otra tabla y
--       migrar los datos.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS escuela
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS escuela.inscripciones_por_estudiante;

CREATE TABLE escuela.inscripciones_por_estudiante (
    estudiante text,
    curso      text,
    PRIMARY KEY (estudiante, curso)
);

INSERT INTO escuela.inscripciones_por_estudiante (estudiante, curso) VALUES ('Ada', 'DB-101');
INSERT INTO escuela.inscripciones_por_estudiante (estudiante, curso) VALUES ('Ada', 'SE-201');
INSERT INTO escuela.inscripciones_por_estudiante (estudiante, curso) VALUES ('Linus', 'DB-101');

-- === consulta ===
TRACING ON;
SELECT DISTINCT estudiante FROM escuela.inscripciones_por_estudiante;
TRACING OFF;
