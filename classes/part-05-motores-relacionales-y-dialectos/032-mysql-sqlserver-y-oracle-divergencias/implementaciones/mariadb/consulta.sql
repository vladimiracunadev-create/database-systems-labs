-- motor: mariadb
-- doc: https://mariadb.com/docs/server/reference/data-types/string-data-types/character-sets
-- nota: implementacion declarada. La sintaxis es la de MySQL, pero la
--       intercalacion por omision NO es la misma (utf8mb4_general_ci frente a
--       utf8mb4_0900_ai_ci): dos motores que se anuncian compatibles ordenan
--       distinto. Por eso el COLLATE explicito no es opcional al migrar.

-- === preparacion ===
DROP TABLE IF EXISTS registros;

CREATE TABLE registros (
    id     INT PRIMARY KEY,
    nombre VARCHAR(50) COLLATE utf8mb4_bin NOT NULL
);
INSERT INTO registros (id, nombre) VALUES (1, 'Ada'), (2, 'ada'), (3, 'ADA'), (4, 'Linus');

-- === consulta ===
SELECT COUNT(DISTINCT nombre) AS distintos FROM registros;
