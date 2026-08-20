-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/using-explain.html
-- nota: EXPLAIN (ANALYZE) sobre esta consulta nombra los operadores y permite
--       comprobar que la seleccion se aplico antes de la reunion.

DROP TABLE IF EXISTS notas, estudiantes;

-- === preparacion ===
CREATE TABLE estudiantes (
    id     integer PRIMARY KEY,
    nombre text NOT NULL
);
CREATE TABLE notas (
    estudiante_id integer NOT NULL,
    curso         text NOT NULL,
    nota          integer NOT NULL,
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
