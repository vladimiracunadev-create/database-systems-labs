-- motor: sql-server
-- doc: https://learn.microsoft.com/sql/t-sql/functions/concat-transact-sql
-- nota: implementacion declarada. Se escribe con CONCAT y con OFFSET/FETCH
--       —las formas de la norma— en vez de con + y TOP, que es lo que aparece
--       en el codigo heredado. La diferencia importa: `'Ada' + 5` intenta
--       convertir la cadena a numero y falla; CONCAT convierte a texto.

-- === preparacion ===
DROP TABLE IF EXISTS dbo.notas;

CREATE TABLE dbo.notas (
    estudiante NVARCHAR(50) NOT NULL,
    curso      NVARCHAR(20) NOT NULL,
    nota       INT NOT NULL,
    CONSTRAINT pk_notas PRIMARY KEY (estudiante, curso)
);
INSERT INTO dbo.notas (estudiante, curso, nota) VALUES
    (N'Ada', N'DB-101', 90), (N'Grace', N'DB-101', 72),
    (N'Linus', N'DB-101', 58), (N'Ada', N'SE-201', 66);

-- === consulta ===
SELECT CONCAT(estudiante, N' - ', curso) AS etiqueta
FROM dbo.notas
WHERE curso = N'DB-101'
ORDER BY nota DESC
OFFSET 0 ROWS FETCH NEXT 2 ROWS ONLY;
