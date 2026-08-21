-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/plpgsql-statements.html
-- nota: la puerta que sigue abierta no esta en la aplicacion, esta DENTRO de la
--       base. Esto es inyectable igual:
--         EXECUTE 'SELECT * FROM usuarios WHERE nombre = ''' || entrada || '''';
--       y la forma correcta es:
--         EXECUTE format('SELECT * FROM usuarios WHERE nombre = %L', entrada);
--       Ninguna revision del codigo de la aplicacion va a mirar ahi.

-- === preparacion ===
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    nombre text PRIMARY KEY,
    rol    text NOT NULL
);
INSERT INTO usuarios (nombre, rol) VALUES
    ('ada', 'admin'), ('linus', 'lector'), ('grace', 'lector');

-- === consulta ===
-- Alguien escribe esto en el formulario de busqueda:   ' OR '1'='1
--
-- CONCATENADO (lo que NO se debe hacer nunca), la consulta que llega al motor
-- deja de ser una busqueda y pasa a ser otra consulta distinta:
--     SELECT ... WHERE nombre = '' OR '1'='1'
--   -> devuelve LOS TRES usuarios, incluido el administrador.
--
-- PARAMETRIZADO, el motor recibe la consulta y el valor por caminos separados:
-- el texto nunca se analiza como SQL, se compara como dato. No existe ningun
-- usuario que se llame asi, y el resultado es cero.
--
-- Aqui el valor va como literal correctamente entrecomillado, que es lo que el
-- controlador construye por dentro al usar un parametro.
SELECT COUNT(*) AS encontrados
FROM usuarios
WHERE nombre = ''' OR ''1''=''1';
