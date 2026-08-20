-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/sql-prepared-statements.html
-- nota: durante anos, PDO traia ATTR_EMULATE_PREPARES activado por omision: el
--       controlador construia la sentencia con escape en el CLIENTE en vez de
--       enviar sentencia y valor por separado. Miles de aplicaciones creyeron
--       estar parametrizando mientras concatenaban.

-- === preparacion ===
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    nombre VARCHAR(50) PRIMARY KEY,
    rol    VARCHAR(50) NOT NULL
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
