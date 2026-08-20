-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/cql/types.html
-- nota: implementacion declarada. El indice secundario sobre una coleccion
--       existe, pero es LOCAL a cada nodo: la consulta pregunta a todos los
--       nodos del anillo. Con pocas etiquetas distintas es aceptable; con
--       muchas, es el antipatron clasico de Cassandra.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS escuela
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DROP TABLE IF EXISTS escuela.cursos;

CREATE TABLE escuela.cursos (
    codigo    text PRIMARY KEY,
    etiquetas set<text>
);
CREATE INDEX IF NOT EXISTS cursos_por_etiqueta ON escuela.cursos (VALUES(etiquetas));

INSERT INTO escuela.cursos (codigo, etiquetas) VALUES ('DB-101', {'sql', 'datos'});
INSERT INTO escuela.cursos (codigo, etiquetas) VALUES ('SE-201', {'proceso'});
INSERT INTO escuela.cursos (codigo, etiquetas) VALUES ('AR-301', {'datos', 'diseno'});

-- === consulta ===
-- La forma idiomatica seria una tabla cursos_por_etiqueta escrita a mano, con
-- la etiqueta como clave de particion: una sola particion, un solo nodo.
SELECT codigo FROM escuela.cursos WHERE etiquetas CONTAINS 'datos';
