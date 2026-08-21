-- motor: sqlite
-- doc: https://sqlite.org/foreignkeys.html
-- nota: SQLite solo comprueba las claves foraneas si PRAGMA foreign_keys esta
--       activo; el verificador lo activa, y en una aplicacion real hay que
--       hacerlo en cada conexion.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);
CREATE TABLE cursos (
    id     INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL
);
-- La tabla intermedia ES la relacion. La clave compuesta impone «una fila por
-- par»: sin ella, el mismo estudiante podria inscribirse dos veces al mismo
-- curso y todos los recuentos quedarian inflados.
CREATE TABLE inscripciones (
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id),
    curso_id      INTEGER NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201'), (30, 'AR-301');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
-- El LEFT JOIN es lo que conserva AR-301 con cero: la participacion parcial
-- solo se ve si el modelo no descarta a quien no participa.
SELECT c.codigo AS curso,
       COUNT(i.estudiante_id) AS estudiantes
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
