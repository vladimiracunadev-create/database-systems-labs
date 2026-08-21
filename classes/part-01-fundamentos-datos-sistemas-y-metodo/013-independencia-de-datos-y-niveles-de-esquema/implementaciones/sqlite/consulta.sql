-- motor: sqlite
-- doc: https://sqlite.org/lang_createview.html
-- nota: la vista es el esquema externo; las dos tablas de debajo son el
--       conceptual. Cambia el segundo sin tocar el primero.

-- === preparacion ===
-- 1. El esquema conceptual de partida: el estado es un texto repetido en cada fila.
CREATE TABLE inscripciones_v1 (
    estudiante TEXT NOT NULL,
    estado     TEXT NOT NULL
);
INSERT INTO inscripciones_v1 (estudiante, estado) VALUES
    ('Ada', 'activa'), ('Linus', 'completada'), ('Grace', 'retirada');

-- 2. El esquema externo: lo unico que la aplicacion conoce.
CREATE VIEW panel_inscripciones AS
    SELECT estudiante, estado FROM inscripciones_v1;

-- 3. El administrador reorganiza: el estado pasa a codigo con tabla de referencia.
CREATE TABLE estados (
    codigo INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);
INSERT INTO estados (codigo, nombre) VALUES (1, 'activa'), (2, 'completada'), (3, 'retirada');

CREATE TABLE inscripciones_v2 (
    estudiante    TEXT NOT NULL,
    estado_codigo INTEGER NOT NULL REFERENCES estados(codigo)
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
