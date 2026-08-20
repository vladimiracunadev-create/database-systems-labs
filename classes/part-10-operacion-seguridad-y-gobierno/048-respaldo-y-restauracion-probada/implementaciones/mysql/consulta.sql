-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/backup-and-recovery.html
-- nota: mysqldump SIN --single-transaction bloquea las tablas y puede producir
--       una copia incoherente. Y la recuperacion a un punto en el tiempo exige
--       que log_bin este activado y que los registros se conserven: comprobarlo
--       forma parte del plan de respaldo, no del de rendimiento.

-- === preparacion ===
DROP TABLE IF EXISTS notas_restauradas;
DROP TABLE IF EXISTS notas;

CREATE TABLE notas (
    id         INT PRIMARY KEY,
    estudiante VARCHAR(50) NOT NULL,
    nota       INT NOT NULL
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
