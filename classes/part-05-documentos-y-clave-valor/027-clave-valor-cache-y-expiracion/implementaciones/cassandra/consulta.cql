-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html
-- nota: implementacion declarada. Aqui la caducidad es POR CELDA, no por fila:
--       un atributo puede caducar y el resto de la fila seguir viva. Ningun
--       otro motor de esta lista ofrece esa granularidad.
--       El precio: cada celda vencida deja una lapida que hay que recorrer en
--       las lecturas hasta que la compactacion la retire.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS escuela
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS escuela.cache;

CREATE TABLE escuela.cache (
    clave text PRIMARY KEY,
    valor text
);

INSERT INTO escuela.cache (clave, valor) VALUES ('k1', 'con caducidad') USING TTL 3600;
INSERT INTO escuela.cache (clave, valor) VALUES ('k2', 'permanente');
-- k3 no se escribe.

-- === consulta ===
-- TTL() sobre una columna devuelve los segundos que le quedan, o null si no
-- caduca. La fila ausente sencillamente no aparece: los tres estados hay que
-- reconstruirlos en el cliente, igual que en los motores relacionales.
SELECT clave, TTL(valor) AS segundos FROM escuela.cache;
