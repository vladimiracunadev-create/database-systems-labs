-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/data-modeling_queries.html
-- nota: implementacion declarada. Las dos partes de la clave primaria hacen
--       cosas distintas y conviene no confundirlas:
--         (dispositivo)  clave de PARTICION -> en que nodo vive la fila
--         momento        clave de AGRUPAMIENTO -> en que orden estan las filas
--                        DENTRO de esa particion, en el disco
--       Por eso LIMIT 2 lee dos celdas contiguas de un solo nodo.

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
  VALUES ('sensor-1', '2026-08-19T10:00:00Z', 21);
INSERT INTO telemetria.lecturas_por_dispositivo (dispositivo, momento, valor)
  VALUES ('sensor-1', '2026-08-19T10:01:00Z', 22);
INSERT INTO telemetria.lecturas_por_dispositivo (dispositivo, momento, valor)
  VALUES ('sensor-1', '2026-08-19T10:02:00Z', 23);
INSERT INTO telemetria.lecturas_por_dispositivo (dispositivo, momento, valor)
  VALUES ('sensor-2', '2026-08-19T10:00:00Z', 30);
INSERT INTO telemetria.lecturas_por_dispositivo (dispositivo, momento, valor)
  VALUES ('sensor-2', '2026-08-19T10:01:00Z', 31);

-- === consulta ===
-- Sin ORDER BY: el orden ya esta en el disco. Y sin ALLOW FILTERING: la
-- consulta toca UNA particion.
--
-- La pregunta inversa —«todas las lecturas de las 10:01, de cualquier sensor»—
-- NO se puede responder con esta tabla, y esa es la leccion. Haria falta
-- lecturas_por_minuto, escrita por la aplicacion en la misma operacion.
--
-- Y ojo con la particion infinita: un sensor que emite para siempre hace crecer
-- su particion sin limite. En produccion la clave seria ((dispositivo, dia)).
SELECT momento, valor
FROM telemetria.lecturas_por_dispositivo
WHERE dispositivo = 'sensor-1'
LIMIT 2;
