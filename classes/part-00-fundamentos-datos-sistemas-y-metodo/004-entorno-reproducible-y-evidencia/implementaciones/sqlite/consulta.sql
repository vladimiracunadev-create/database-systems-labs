-- motor: sqlite
-- doc: https://sqlite.org/inmemorydb.html
-- nota: el verificador abre la base en memoria, asi que cada ejecucion parte
--       del mismo estado exacto. Esa es la condicion de una medicion repetible.

-- === preparacion ===
CREATE TABLE notas (
    inscripcion INTEGER PRIMARY KEY,
    estudiante  TEXT NOT NULL,
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
