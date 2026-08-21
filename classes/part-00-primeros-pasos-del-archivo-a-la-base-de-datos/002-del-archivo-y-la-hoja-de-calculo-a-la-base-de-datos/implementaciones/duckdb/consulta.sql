-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/constraints.html
-- nota: DuckDB no tiene OR IGNORE para violaciones de CHECK: la fila invalida
--       aborta la sentencia. Por eso el intento prohibido va comentado;
--       descomentarlo hace fallar el guion, que es la prueba de que la regla
--       existe.

-- === preparacion ===
CREATE TABLE notas (
    estudiante VARCHAR NOT NULL,
    nota       INTEGER NOT NULL CHECK (nota BETWEEN 0 AND 100)
);

INSERT INTO notas VALUES ('Ada', 90);
INSERT INTO notas VALUES ('Linus', 58);
INSERT INTO notas VALUES ('Grace', 72);
-- INSERT INTO notas VALUES ('Bob', 130);   -- Constraint Error: CHECK
-- INSERT INTO notas VALUES ('Bob', 'alto');-- Conversion Error: aqui el TIPO
--                                          -- tambien se comprueba, cosa que
--                                          -- SQLite no hace sin STRICT.

-- === consulta ===
SELECT estudiante, nota FROM notas ORDER BY estudiante;
