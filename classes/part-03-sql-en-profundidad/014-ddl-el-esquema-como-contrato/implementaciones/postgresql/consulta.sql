-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-constraints.html
-- nota: el dominio da NOMBRE a la restriccion y la hace reutilizable: cualquier
--       columna declarada `nota_valida` hereda el rango, y cambiarlo en un solo
--       sitio lo cambia en todas.

-- === preparacion ===
DROP TABLE IF EXISTS notas;
DROP DOMAIN IF EXISTS nota_valida;

CREATE DOMAIN nota_valida AS integer CHECK (VALUE BETWEEN 0 AND 100);

CREATE TABLE notas (
    estudiante text NOT NULL CHECK (length(estudiante) > 0),
    curso      text NOT NULL,
    nota       nota_valida NOT NULL,
    PRIMARY KEY (estudiante, curso)
);

INSERT INTO notas (estudiante, curso, nota) VALUES ('Ada', 'DB-101', 90);
INSERT INTO notas (estudiante, curso, nota) VALUES ('Linus', 'DB-101', 58);

-- Los dos intentos prohibidos se ejecutan de verdad, capturando el error: la
-- prueba de que el contrato actua queda en el guion, no en un comentario.
DO $$
DECLARE rechazadas integer := 0;
BEGIN
    BEGIN
        INSERT INTO notas (estudiante, curso, nota) VALUES ('Grace', 'DB-101', 130);
    EXCEPTION WHEN check_violation THEN rechazadas := rechazadas + 1;
    END;
    BEGIN
        INSERT INTO notas (estudiante, curso, nota) VALUES ('', 'DB-101', 70);
    EXCEPTION WHEN check_violation THEN rechazadas := rechazadas + 1;
    END;
    IF rechazadas <> 2 THEN
        RAISE EXCEPTION 'el esquema acepto datos que su contrato prohibe';
    END IF;
END;
$$;

-- === consulta ===
SELECT estudiante, nota FROM notas ORDER BY estudiante;
