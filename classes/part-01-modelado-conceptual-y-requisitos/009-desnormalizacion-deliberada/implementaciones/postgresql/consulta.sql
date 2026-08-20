-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-createtrigger.html
-- nota: el disparador corre DENTRO de la transaccion de la inscripcion: si la
--       transaccion se deshace, el contador vuelve solo. Esa es la diferencia
--       con mantenerlo desde otro sistema.

-- === preparacion ===
DROP TABLE IF EXISTS inscripciones, cursos;

CREATE TABLE cursos (
    id        integer PRIMARY KEY,
    codigo    text NOT NULL,
    inscritos integer NOT NULL DEFAULT 0
);
CREATE TABLE inscripciones (
    estudiante text NOT NULL,
    curso_id   integer NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante, curso_id)
);

CREATE OR REPLACE FUNCTION ajustar_contador() RETURNS trigger AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE cursos SET inscritos = inscritos + 1 WHERE id = NEW.curso_id;
    ELSE
        UPDATE cursos SET inscritos = inscritos - 1 WHERE id = OLD.curso_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER inscripciones_contador
AFTER INSERT OR DELETE ON inscripciones
FOR EACH ROW EXECUTE FUNCTION ajustar_contador();

INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20), ('Bob', 20);
DELETE FROM inscripciones WHERE estudiante = 'Bob' AND curso_id = 20;

-- === consulta ===
-- La comprobacion que en produccion debe correr periodicamente: el dato
-- guardado frente al dato calculado. El dia que dejen de coincidir, la
-- desnormalizacion dejo de ser deliberada.
SELECT c.codigo AS curso,
       c.inscritos AS contador,
       (SELECT COUNT(*) FROM inscripciones i WHERE i.curso_id = c.id) AS calculado
FROM cursos c
ORDER BY c.codigo;
