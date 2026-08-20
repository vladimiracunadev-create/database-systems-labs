-- motor: sql-server
-- doc: https://learn.microsoft.com/sql/t-sql/queries/from-transact-sql
-- nota: implementacion declarada. El repositorio no la ejecuta en CI porque no
--       distribuye la imagen con licencia; se revisa a mano contra la
--       documentacion citada.

-- === preparacion ===
DROP TABLE IF EXISTS dbo.inscripciones;
DROP TABLE IF EXISTS dbo.cursos;
DROP TABLE IF EXISTS dbo.estudiantes;

CREATE TABLE dbo.estudiantes (
    id     INT PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL
);
CREATE TABLE dbo.cursos (
    id     INT PRIMARY KEY,
    codigo NVARCHAR(20) NOT NULL UNIQUE
);
CREATE TABLE dbo.inscripciones (
    estudiante_id INT NOT NULL REFERENCES dbo.estudiantes(id),
    curso_id      INT NOT NULL REFERENCES dbo.cursos(id),
    CONSTRAINT pk_inscripciones PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO dbo.estudiantes (id, nombre) VALUES (1, N'Ada'), (2, N'Linus'), (3, N'Grace');
INSERT INTO dbo.cursos (id, codigo) VALUES (10, N'DB-101'), (20, N'SE-201');
INSERT INTO dbo.inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
SELECT e.nombre,
       COALESCE(c.codigo, N'sin-curso') AS codigo
FROM dbo.estudiantes e
LEFT JOIN dbo.inscripciones i ON i.estudiante_id = e.id
LEFT JOIN dbo.cursos c        ON c.id = i.curso_id
ORDER BY e.nombre, codigo;
