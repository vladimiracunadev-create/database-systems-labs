-- motor: sql-server
-- doc: https://learn.microsoft.com/sql/relational-databases/collations/collation-and-unicode-support
-- nota: implementacion declarada. La intercalacion por omision se elige AL
--       INSTALAR la instancia y afecta tambien a los nombres de objetos y a
--       tempdb. Fijarla en la columna, como aqui, es la unica forma de que el
--       resultado no dependa de la maquina.

-- === preparacion ===
DROP TABLE IF EXISTS dbo.registros;

CREATE TABLE dbo.registros (
    id     INT PRIMARY KEY,
    nombre NVARCHAR(50) COLLATE Latin1_General_BIN2 NOT NULL
);
INSERT INTO dbo.registros (id, nombre) VALUES
    (1, N'Ada'), (2, N'ada'), (3, N'ADA'), (4, N'Linus');

-- === consulta ===
SELECT COUNT(DISTINCT nombre) AS distintos FROM dbo.registros;
