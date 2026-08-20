-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html
-- nota: implementacion declarada, y deliberadamente distinta. CQL no tiene
--       JOIN: la reunion se paga en la escritura y se guarda ya resuelta la
--       tabla que la consulta necesita. El precio esta en el comentario final.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS escuela
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS escuela.cursos_por_estudiante;

-- La tabla es la consulta: una particion por estudiante, los codigos ordenados
-- dentro de ella. No modela entidades, modela una pregunta.
CREATE TABLE escuela.cursos_por_estudiante (
    nombre text,
    codigo text,
    PRIMARY KEY (nombre, codigo)
) WITH CLUSTERING ORDER BY (codigo ASC);

INSERT INTO escuela.cursos_por_estudiante (nombre, codigo) VALUES ('Ada', 'DB-101');
INSERT INTO escuela.cursos_por_estudiante (nombre, codigo) VALUES ('Ada', 'SE-201');
INSERT INTO escuela.cursos_por_estudiante (nombre, codigo) VALUES ('Linus', 'DB-101');
-- Grace no tiene inscripciones: el centinela tambien se escribe a mano, porque
-- aqui no hay reunion externa que lo genere.
INSERT INTO escuela.cursos_por_estudiante (nombre, codigo) VALUES ('Grace', 'sin-curso');

-- === consulta ===
-- El ORDER BY solo ordena DENTRO de una particion. Al recorrer varias, el orden
-- lo fija el token de la clave, no el nombre: por eso este SELECT lleva el
-- ordenamiento final del lado del cliente en cualquier uso serio.
SELECT nombre, codigo FROM escuela.cursos_por_estudiante;
