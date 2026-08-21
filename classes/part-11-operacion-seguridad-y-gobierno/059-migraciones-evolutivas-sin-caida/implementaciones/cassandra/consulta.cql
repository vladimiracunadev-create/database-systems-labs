-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/cql/ddl.html
-- nota: implementacion declarada. ADD es barato: no reescribe datos y las filas
--       viejas devuelven null en la columna nueva.
--       Lo que NO se puede alterar nunca: la clave primaria, el tipo de una
--       columna existente y el orden de agrupamiento. Para eso hay que crear
--       otra tabla, migrar los datos y cambiar la aplicacion. La decision de
--       modelado se toma una vez.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS escuela
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS escuela.personas;

CREATE TABLE escuela.personas (
    id     int PRIMARY KEY,
    nombre text
);
INSERT INTO escuela.personas (id, nombre) VALUES (1, 'Ada Lovelace');
INSERT INTO escuela.personas (id, nombre) VALUES (2, 'Linus Torvalds');

-- EXPANDIR
ALTER TABLE escuela.personas ADD apellido text;

-- MIGRAR
UPDATE escuela.personas SET apellido = 'Lovelace' WHERE id = 1;
UPDATE escuela.personas SET apellido = 'Torvalds' WHERE id = 2;

INSERT INTO escuela.personas (id, nombre, apellido) VALUES (3, 'Grace Hopper', 'Hopper');

-- === consulta ===
SELECT id, apellido FROM escuela.personas;
