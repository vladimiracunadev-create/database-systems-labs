-- motor: oracle-database
-- doc: https://docs.oracle.com/en/database/oracle/oracle-database/23/nlspg/linguistic-sorting-and-matching.html
-- nota: implementacion declarada. Aqui el comportamiento se controla POR SESION
--       con NLS_SORT y NLS_COMP: la misma consulta puede devolver 2 o 4 segun
--       quien la lance. Dejarlo en BINARY es la unica forma de que el resultado
--       sea el mismo para todos.

-- === preparacion ===
ALTER SESSION SET NLS_SORT = 'BINARY';
ALTER SESSION SET NLS_COMP = 'BINARY';

CREATE TABLE registros (
    id     NUMBER PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL
);
INSERT INTO registros (id, nombre) VALUES (1, 'Ada');
INSERT INTO registros (id, nombre) VALUES (2, 'ada');
INSERT INTO registros (id, nombre) VALUES (3, 'ADA');
INSERT INTO registros (id, nombre) VALUES (4, 'Linus');
COMMIT;

-- === consulta ===
SELECT COUNT(DISTINCT nombre) AS distintos FROM registros;
