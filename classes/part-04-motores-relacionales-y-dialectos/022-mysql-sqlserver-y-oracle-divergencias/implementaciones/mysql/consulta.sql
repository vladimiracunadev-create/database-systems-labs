-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/charset-collation-names.html
-- nota: SIN el COLLATE utf8mb4_bin de abajo, esta consulta devuelve 2, no 4:
--       la intercalacion por omision utf8mb4_0900_ai_ci ignora mayusculas y
--       acentos. Es la divergencia mas cara de las migraciones a y desde MySQL.

-- === preparacion ===
DROP TABLE IF EXISTS registros;

CREATE TABLE registros (
    id     INT PRIMARY KEY,
    nombre VARCHAR(50) COLLATE utf8mb4_bin NOT NULL
);
INSERT INTO registros (id, nombre) VALUES (1, 'Ada'), (2, 'ada'), (3, 'ADA'), (4, 'Linus');

-- === consulta ===
-- Cuantos nombres DISTINTOS hay. La respuesta correcta depende de algo que no
-- esta en la consulta: la intercalacion de la columna.
SELECT COUNT(DISTINCT nombre) AS distintos FROM registros;
