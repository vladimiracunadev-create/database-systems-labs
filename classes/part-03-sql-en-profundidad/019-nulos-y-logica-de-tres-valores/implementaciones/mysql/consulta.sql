-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/working-with-null.html
-- nota: el operador <=> compara con nulos de forma segura: NULL <=> NULL es
--       verdadero. No es estandar, pero evita salir a una subconsulta.

DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS estudiantes;

-- === preparacion ===
CREATE TABLE estudiantes (
    nombre VARCHAR(50) PRIMARY KEY
);
CREATE TABLE inscripciones (
    id         INT PRIMARY KEY,
    estudiante VARCHAR(50),          -- admite nulo: el dato sucio del mundo real
    curso      VARCHAR(50) NOT NULL
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
