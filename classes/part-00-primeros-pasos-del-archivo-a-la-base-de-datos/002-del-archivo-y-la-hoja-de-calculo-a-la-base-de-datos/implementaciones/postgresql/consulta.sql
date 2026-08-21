-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-constraints.html
-- nota: el intento prohibido se ejecuta DE VERDAD, capturando el error: asi la
--       prueba de que la regla actua queda en el guion y no en un comentario.
--       Y con un dominio, «nota valida» se define una vez para todo el sistema:
--         CREATE DOMAIN nota_valida AS integer CHECK (VALUE BETWEEN 0 AND 100);

-- === preparacion ===
DROP TABLE IF EXISTS notas;

CREATE TABLE notas (
    estudiante text NOT NULL,
    nota       integer NOT NULL CHECK (nota BETWEEN 0 AND 100)
);

INSERT INTO notas (estudiante, nota) VALUES ('Ada', 90);
INSERT INTO notas (estudiante, nota) VALUES ('Linus', 58);
INSERT INTO notas (estudiante, nota) VALUES ('Grace', 72);

DO $$
BEGIN
    INSERT INTO notas (estudiante, nota) VALUES ('Bob', 130);
    RAISE EXCEPTION 'el esquema acepto una nota de 130 sobre 100';
EXCEPTION
    WHEN check_violation THEN
        RAISE NOTICE 'la regla actuo, como debia';
END;
$$;

-- === consulta ===
SELECT estudiante, nota FROM notas ORDER BY estudiante;
