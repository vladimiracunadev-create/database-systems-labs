-- motor: sqlite
-- doc: https://sqlite.org/lang_createtrigger.html
-- nota: el contador lo mantiene el motor, no el programa. Ningun camino de
--       escritura —ni la consola, ni otro servicio, ni una migracion— puede
--       olvidarse de actualizarlo.

-- === preparacion ===
CREATE TABLE cursos (
    id        INTEGER PRIMARY KEY,
    codigo    TEXT NOT NULL,
    inscritos INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE inscripciones (
    estudiante TEXT NOT NULL,
    curso_id   INTEGER NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante, curso_id)
);

CREATE TRIGGER inscripciones_mas AFTER INSERT ON inscripciones
BEGIN
    UPDATE cursos SET inscritos = inscritos + 1 WHERE id = NEW.curso_id;
END;

CREATE TRIGGER inscripciones_menos AFTER DELETE ON inscripciones
BEGIN
    UPDATE cursos SET inscritos = inscritos - 1 WHERE id = OLD.curso_id;
END;

INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20), ('Bob', 20);
-- Una baja: si el disparador de borrado no existiera, el contador se quedaria
-- en 2 y nadie lo notaria hasta que alguien contara a mano.
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
