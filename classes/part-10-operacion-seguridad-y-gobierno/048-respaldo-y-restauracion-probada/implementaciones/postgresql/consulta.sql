-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/continuous-archiving.html
-- nota: las dos familias, y hacen falta las dos:
--         pg_dump -Fc base > copia.dump        copia logica, portable
--         pg_basebackup + archive_command      punto en el tiempo
--       La segunda es la unica que salva de un DELETE sin WHERE a las once de
--       la noche: permite restaurar al segundo anterior.

-- === preparacion ===
DROP TABLE IF EXISTS notas_restauradas, notas;

CREATE TABLE notas (
    id         integer PRIMARY KEY,
    estudiante text NOT NULL,
    nota       integer NOT NULL
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
