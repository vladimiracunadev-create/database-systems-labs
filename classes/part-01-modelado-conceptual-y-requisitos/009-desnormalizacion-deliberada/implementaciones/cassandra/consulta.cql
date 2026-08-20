-- motor: cassandra
-- doc: https://cassandra.apache.org/doc/latest/cassandra/developing/cql/types.html
-- nota: implementacion declarada. Cassandra tiene un tipo de columna dedicado,
--       `counter`, porque en su modelo no se puede leer para escribir: el
--       contador se incrementa sin conocer su valor previo. El precio esta al
--       final del archivo y no es menor.

-- === preparacion ===
CREATE KEYSPACE IF NOT EXISTS escuela
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- Una tabla de contadores no admite columnas normales: solo la clave y los
-- contadores. Por eso el codigo del curso ES la clave.
CREATE TABLE IF NOT EXISTS escuela.contador_inscritos (
    curso     text PRIMARY KEY,
    inscritos counter
);

-- Y la lista de miembros va en su propia tabla, sin transaccion que la
-- mantenga de acuerdo con el contador.
CREATE TABLE IF NOT EXISTS escuela.inscripciones (
    curso      text,
    estudiante text,
    PRIMARY KEY (curso, estudiante)
);

UPDATE escuela.contador_inscritos SET inscritos = inscritos + 1 WHERE curso = 'DB-101';
INSERT INTO escuela.inscripciones (curso, estudiante) VALUES ('DB-101', 'Ada');
UPDATE escuela.contador_inscritos SET inscritos = inscritos + 1 WHERE curso = 'DB-101';
INSERT INTO escuela.inscripciones (curso, estudiante) VALUES ('DB-101', 'Linus');
UPDATE escuela.contador_inscritos SET inscritos = inscritos + 1 WHERE curso = 'SE-201';
INSERT INTO escuela.inscripciones (curso, estudiante) VALUES ('SE-201', 'Grace');

-- === consulta ===
-- No hay reunion: son dos preguntas separadas, y compararlas es trabajo del
-- cliente. Ademas, si el cliente reintenta un UPDATE de contador tras un tiempo
-- de espera agotado, el incremento puede aplicarse dos veces: los contadores de
-- Cassandra NO son idempotentes.
SELECT curso, inscritos FROM escuela.contador_inscritos;
SELECT curso, COUNT(*) FROM escuela.inscripciones GROUP BY curso;
