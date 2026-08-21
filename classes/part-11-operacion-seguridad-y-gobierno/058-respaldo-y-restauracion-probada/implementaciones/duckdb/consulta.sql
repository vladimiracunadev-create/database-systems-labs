-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/export
-- nota: aqui el respaldo es exportar a un formato ABIERTO:
--         EXPORT DATABASE 'copia' (FORMAT PARQUET);
--       La copia sobrevive a la desaparicion del motor que la creo, cosa que
--       ningun volcado propietario garantiza. A cambio: no hay punto en el
--       tiempo ni copia incremental.

-- === preparacion ===
CREATE TABLE notas (
    id         INTEGER PRIMARY KEY,
    estudiante VARCHAR NOT NULL,
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
