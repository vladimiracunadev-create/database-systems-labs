-- motor: sqlite
-- doc: https://sqlite.org/backup.html
-- nota: en produccion la copia se hace SIN detener la base con
--         VACUUM INTO 'copia-2026-08-19.sqlite';
--       Lo que NO hay que hacer nunca es `cp base.sqlite copia.sqlite` mientras
--       alguien escribe: produce un archivo que parece valido y no lo es.

-- === preparacion ===
CREATE TABLE notas (
    id         INTEGER PRIMARY KEY,
    estudiante TEXT NOT NULL,
    nota       INTEGER NOT NULL
);
INSERT INTO notas (id, estudiante, nota) VALUES
    (1, 'Ada', 90), (2, 'Ada', 58), (3, 'Linus', 78),
    (4, 'Linus', 66), (5, 'Grace', 55), (6, 'Grace', 55);

-- La copia. En produccion seria pg_dump, mysqldump, mongodump o una
-- instantanea del volumen; aqui es una tabla, para que lo que se compare sea
-- el METODO de verificacion y no la herramienta.
CREATE TABLE notas_restauradas AS SELECT * FROM notas;

-- === consulta ===
-- La unica prueba que cuenta. Un respaldo que nadie ha restaurado no es un
-- respaldo: es un archivo. Y restaurarlo sin comparar tampoco prueba nada, asi
-- que la comprobacion es siempre la misma pareja: cuantas filas y que suman.
SELECT 'origen' AS copia, COUNT(*) AS filas, SUM(nota) AS suma FROM notas
UNION ALL
SELECT 'restaurado', COUNT(*), SUM(nota) FROM notas_restauradas
ORDER BY copia;
