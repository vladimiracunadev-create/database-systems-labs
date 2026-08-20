-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/functions-subquery.html
-- nota: la documentacion avisa expresamente de que NOT IN sobre una subconsulta
--       con nulos no hace lo que parece. No es un fallo del motor: es la logica
--       de tres valores del estandar aplicada al pie de la letra.

DROP TABLE IF EXISTS inscripciones, estudiantes;

-- === preparacion ===
CREATE TABLE estudiantes (
    nombre text PRIMARY KEY
);
CREATE TABLE inscripciones (
    id         integer PRIMARY KEY,
    estudiante text,          -- admite nulo: el dato sucio del mundo real
    curso      text NOT NULL
);

INSERT INTO estudiantes (nombre) VALUES ('Ada'), ('Linus'), ('Grace');
INSERT INTO inscripciones (id, estudiante, curso) VALUES
    (1, 'Ada',   'DB-101'),
    (2, 'Linus', 'DB-101'),
    (3, NULL,    'SE-201');   -- una sola fila asi rompe el NOT IN

-- === consulta ===
-- La forma CORRECTA. La forma rota seria:
--   SELECT nombre FROM estudiantes
--   WHERE nombre NOT IN (SELECT estudiante FROM inscripciones);
-- que devuelve CERO filas. Al comparar 'Grace' con el nulo, el resultado no es
-- falso sino DESCONOCIDO; NOT IN exige que todas las comparaciones sean falsas,
-- y «desconocido» no lo es. El informe sale vacio y nadie ve un error.
SELECT e.nombre
FROM estudiantes e
WHERE NOT EXISTS (
    SELECT 1 FROM inscripciones i WHERE i.estudiante = e.nombre
)
ORDER BY e.nombre;
