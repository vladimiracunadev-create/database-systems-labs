-- motor: oracle-database
-- doc: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/Data-Types.html
-- nota: implementacion declarada. Oracle si implementa || de la norma, y desde
--       12c admite FETCH FIRST. Antes habia que envolver la consulta:
--         SELECT * FROM (SELECT ... ORDER BY nota DESC) WHERE ROWNUM <= 2;
--       Y ojo con la cadena vacia: en Oracle '' ES NULL, asi que concatenar con
--       una columna vacia no da lo mismo que en el resto de motores.

-- === preparacion ===
CREATE TABLE notas (
    estudiante VARCHAR2(50) NOT NULL,
    curso      VARCHAR2(20) NOT NULL,
    nota       NUMBER NOT NULL,
    CONSTRAINT pk_notas PRIMARY KEY (estudiante, curso)
);
INSERT INTO notas (estudiante, curso, nota) VALUES ('Ada', 'DB-101', 90);
INSERT INTO notas (estudiante, curso, nota) VALUES ('Grace', 'DB-101', 72);
INSERT INTO notas (estudiante, curso, nota) VALUES ('Linus', 'DB-101', 58);
INSERT INTO notas (estudiante, curso, nota) VALUES ('Ada', 'SE-201', 66);
COMMIT;

-- === consulta ===
SELECT estudiante || ' - ' || curso AS etiqueta
FROM notas
WHERE curso = 'DB-101'
ORDER BY nota DESC
FETCH FIRST 2 ROWS ONLY;
