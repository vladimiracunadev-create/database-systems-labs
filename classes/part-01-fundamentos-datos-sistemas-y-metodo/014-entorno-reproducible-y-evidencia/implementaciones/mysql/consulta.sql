-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/fixed-point-types.html
-- nota: al declarar la evidencia hay que declarar tambien la version del
--       servidor y los parametros que importan; la configuracion por omision
--       varia mucho entre imagenes y distribuciones.

DROP TABLE IF EXISTS notas;

-- === preparacion ===
CREATE TABLE notas (
    inscripcion INT PRIMARY KEY,
    estudiante  VARCHAR(50) NOT NULL,
    nota        INT NOT NULL
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
