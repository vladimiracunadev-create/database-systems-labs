-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html
-- nota: implementacion declarada. Aqui el ORDER BY no ordena: DESCRIBE el orden
--       que ya tienen las filas en el disco dentro de la particion. Por eso
--       LIMIT 2 lee dos celdas contiguas y nada mas.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS escuela
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS escuela.notas_por_curso;

CREATE TABLE escuela.notas_por_curso (
    curso      text,
    nota       int,
    estudiante text,
    PRIMARY KEY (curso, nota, estudiante)
) WITH CLUSTERING ORDER BY (nota DESC, estudiante ASC);

INSERT INTO escuela.notas_por_curso (curso, nota, estudiante) VALUES ('DB-101', 90, 'Ada');
INSERT INTO escuela.notas_por_curso (curso, nota, estudiante) VALUES ('DB-101', 58, 'Linus');
INSERT INTO escuela.notas_por_curso (curso, nota, estudiante) VALUES ('DB-101', 72, 'Grace');
INSERT INTO escuela.notas_por_curso (curso, nota, estudiante) VALUES ('SE-201', 66, 'Ada');
INSERT INTO escuela.notas_por_curso (curso, nota, estudiante) VALUES ('SE-201', 78, 'Grace');

-- === consulta ===
-- El filtro por `nota` es legal porque `nota` es columna de agrupamiento. Si
-- se filtrara por `estudiante`, haria falta ALLOW FILTERING: la forma que tiene
-- Cassandra de avisar de que va a escanear la particion entera.
SELECT estudiante, nota
FROM escuela.notas_por_curso
WHERE curso = 'DB-101' AND nota >= 60
LIMIT 2;
