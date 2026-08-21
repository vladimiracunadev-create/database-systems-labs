-- motor: sql-server
-- doc: https://learn.microsoft.com/sql/relational-databases/security/row-level-security
-- nota: implementacion declarada. SQL Server separa dos cosas que conviene no
--       confundir:
--         predicado de FILTRO   -> que filas se VEN
--         predicado de BLOQUEO  -> que filas se pueden ESCRIBIR
--       Sin el segundo, un usuario puede insertar filas de otro inquilino que
--       despues no podra ver: el dato se pierde de vista sin haberse borrado.

-- === preparacion ===
DROP SECURITY POLICY IF EXISTS dbo.politica_inquilino;
DROP FUNCTION IF EXISTS dbo.fn_inquilino;
DROP TABLE IF EXISTS dbo.notas;

CREATE TABLE dbo.notas (
    inquilino  NVARCHAR(50) NOT NULL,
    estudiante NVARCHAR(50) NOT NULL,
    nota       INT NOT NULL,
    CONSTRAINT pk_notas PRIMARY KEY (inquilino, estudiante)
);
INSERT INTO dbo.notas (inquilino, estudiante, nota) VALUES
    (N'acme', N'Ada', 90), (N'acme', N'Bea', 58), (N'globex', N'Cid', 77);
GO

-- SCHEMABINDING y una funcion simple: se ejecuta POR FILA.
CREATE FUNCTION dbo.fn_inquilino(@inquilino AS NVARCHAR(50))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS visible
       WHERE @inquilino = CAST(SESSION_CONTEXT(N'inquilino') AS NVARCHAR(50));
GO

CREATE SECURITY POLICY dbo.politica_inquilino
ADD FILTER PREDICATE dbo.fn_inquilino(inquilino) ON dbo.notas,
ADD BLOCK PREDICATE dbo.fn_inquilino(inquilino) ON dbo.notas AFTER INSERT
WITH (STATE = ON);
GO

-- === consulta ===
EXEC sp_set_session_context @key = N'inquilino', @value = N'acme';

SELECT estudiante, nota FROM dbo.notas ORDER BY estudiante;
