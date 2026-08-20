-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/datatype-numeric.html
-- nota: acompanar la cifra con EXPLAIN (ANALYZE, BUFFERS) convierte el
--       resultado en evidencia: dice tambien cuanto trabajo costo obtenerlo.

DROP TABLE IF EXISTS notas;

-- === preparacion ===
CREATE TABLE notas (
    inscripcion integer PRIMARY KEY,
    estudiante  text NOT NULL,
    nota        integer NOT NULL
);

-- La semilla: seis filas fijas, siempre las mismas, siempre en este orden.
INSERT INTO notas (inscripcion, estudiante, nota) VALUES
    (1, 'Ada',   90),
    (2, 'Ada',   58),
    (3, 'Linus', 78),
    (4, 'Linus', 66),
    (5, 'Grace', 55),
    (6, 'Grace', 55);

-- === consulta ===
SELECT COUNT(*) AS filas, SUM(nota) AS suma_notas FROM notas;
