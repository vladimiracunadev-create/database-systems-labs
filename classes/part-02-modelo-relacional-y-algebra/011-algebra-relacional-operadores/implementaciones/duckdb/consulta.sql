-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/guides/meta/explain.html
-- nota: anteponer EXPLAIN a esta consulta muestra el arbol de operadores con
--       el filtro ya empujado a la hoja: la equivalencia algebraica aplicada.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL
);
CREATE TABLE notas (
    estudiante_id INTEGER NOT NULL,
    curso         VARCHAR NOT NULL,
    nota          INTEGER NOT NULL,
    PRIMARY KEY (estudiante_id, curso)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO notas (estudiante_id, curso, nota) VALUES
    (1, 'DB-101', 90),
    (2, 'DB-101', 58),
    (3, 'DB-101', 72),
    (1, 'SE-201', 66),
    (3, 'SE-201', 78);

-- === consulta ===
-- Tres operadores del algebra, en este orden:
--   sigma  (seleccion)  WHERE curso = 'DB-101' AND nota >= 60
--   |X|    (reunion)    JOIN estudiantes ON ...
--   pi     (proyeccion) SELECT nombre, nota
-- El motor puede reordenarlos si el resultado no cambia; eso es exactamente lo
-- que autoriza el algebra y lo que hace el optimizador.
SELECT e.nombre, n.nota
FROM notas n
JOIN estudiantes e ON e.id = n.estudiante_id
WHERE n.curso = 'DB-101' AND n.nota >= 60
ORDER BY e.nombre;
