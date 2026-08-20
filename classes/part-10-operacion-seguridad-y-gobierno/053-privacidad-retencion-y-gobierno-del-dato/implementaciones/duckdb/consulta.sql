-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/functions/char
-- nota: aqui es donde el dato SALE hacia otro entorno —analitica, pruebas, un
--       cuaderno— y de donde ya no vuelve. Enmascarar en la consulta es fragil:
--       basta escribir otra consulta para llevarse el original. El enmascarado
--       tiene que estar en el proceso que exporta.

-- === preparacion ===
CREATE TABLE eventos (
    id     INTEGER PRIMARY KEY,
    correo VARCHAR NOT NULL,
    fecha  VARCHAR NOT NULL
);
INSERT INTO eventos (id, correo, fecha) VALUES
    (1, 'ada@example.org',   '2025-01-15'),
    (2, 'linus@example.org', '2026-08-10'),
    (3, 'grace@otro.org',    '2026-08-15');

-- RETENCION: lo que ya no hace falta se borra. Guardar «por si acaso» no es
-- prudencia, es responsabilidad acumulada: cada dato conservado de mas es un
-- dato que se puede filtrar y que alguien puede reclamar.
DELETE FROM eventos WHERE fecha < '2026-01-01';

-- === consulta ===
-- MINIMIZACION: el analisis necesita el dominio, no la persona. Enmascarar en
-- la CONSULTA no protege nada —el dato sigue ahi—; esto es lo que se hace al
-- exportar a un entorno que no deberia tener el dato original.
SELECT '***@' || SUBSTR(correo, INSTR(correo, '@') + 1) AS correo, fecha
FROM eventos
ORDER BY fecha;
