-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/data_types/numeric.html
-- nota: la nota se guarda como entero a proposito. Con coma flotante, dos
--       motores pueden dar 402 y 401.99999999999994 para la misma suma, y la
--       comparacion entre ellos dejaria de significar nada.

-- === preparacion ===
CREATE TABLE notas (
    inscripcion INTEGER PRIMARY KEY,
    estudiante  VARCHAR NOT NULL,
    nota        INTEGER NOT NULL
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
