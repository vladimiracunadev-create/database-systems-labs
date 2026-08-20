-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-createview.html
-- nota: en produccion el paso 4 se hace con CREATE OR REPLACE VIEW, que
--       sustituye la definicion de forma atomica y sin dejar un instante en
--       el que la vista no exista.

DROP VIEW IF EXISTS panel_inscripciones;
DROP TABLE IF EXISTS inscripciones_v1, inscripciones_v2, estados;

-- === preparacion ===
-- 1. El esquema conceptual de partida: el estado es un texto repetido en cada fila.
CREATE TABLE inscripciones_v1 (
    estudiante text NOT NULL,
    estado     text NOT NULL
);
INSERT INTO inscripciones_v1 (estudiante, estado) VALUES
    ('Ada', 'activa'), ('Linus', 'completada'), ('Grace', 'retirada');

-- 2. El esquema externo: lo unico que la aplicacion conoce.
CREATE VIEW panel_inscripciones AS
    SELECT estudiante, estado FROM inscripciones_v1;

-- 3. El administrador reorganiza: el estado pasa a codigo con tabla de referencia.
CREATE TABLE estados (
    codigo integer PRIMARY KEY,
    nombre text NOT NULL
);
INSERT INTO estados (codigo, nombre) VALUES (1, 'activa'), (2, 'completada'), (3, 'retirada');

CREATE TABLE inscripciones_v2 (
    estudiante    text NOT NULL,
    estado_codigo integer NOT NULL REFERENCES estados(codigo)
);
INSERT INTO inscripciones_v2 (estudiante, estado_codigo)
SELECT i.estudiante, e.codigo
FROM inscripciones_v1 i
JOIN estados e ON e.nombre = i.estado;

-- 4. La vista absorbe el cambio. La aplicacion no se entera.
DROP VIEW panel_inscripciones;
DROP TABLE inscripciones_v1;
CREATE VIEW panel_inscripciones AS
    SELECT i.estudiante, e.nombre AS estado
    FROM inscripciones_v2 i
    JOIN estados e ON e.codigo = i.estado_codigo;

-- === consulta ===
-- Exactamente la misma consulta que antes del cambio: ni una letra distinta.
SELECT estudiante, estado FROM panel_inscripciones ORDER BY estudiante;
