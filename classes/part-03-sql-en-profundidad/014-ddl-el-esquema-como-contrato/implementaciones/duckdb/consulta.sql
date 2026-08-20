-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/constraints.html
-- nota: DuckDB no tiene INSERT OR IGNORE para violaciones de CHECK: la fila
--       invalida aborta la sentencia. Por eso los dos intentos prohibidos van
--       comentados; descomentar cualquiera de los dos hace fallar el guion, que
--       es precisamente la prueba de que el contrato existe.

-- === preparacion ===
CREATE TABLE notas (
    estudiante VARCHAR NOT NULL CHECK (length(estudiante) > 0),
    curso      VARCHAR NOT NULL,
    nota       INTEGER NOT NULL CHECK (nota BETWEEN 0 AND 100),
    PRIMARY KEY (estudiante, curso)
);

INSERT INTO notas VALUES ('Ada', 'DB-101', 90);
INSERT INTO notas VALUES ('Linus', 'DB-101', 58);
-- INSERT INTO notas VALUES ('Grace', 'DB-101', 130);  -- Constraint Error: CHECK
-- INSERT INTO notas VALUES ('',      'DB-101', 70);   -- Constraint Error: CHECK

-- === consulta ===
SELECT estudiante, nota FROM notas ORDER BY estudiante;
