-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/prepared_statements
-- nota: la trampa propia de la analitica: los IDENTIFICADORES —nombres de tabla
--       y de columna— no se pueden parametrizar en NINGUN motor, y en un guion
--       de analisis suelen venir de fuera. Ahi la defensa no es un parametro:
--       es una lista blanca de nombres permitidos.

-- === preparacion ===
CREATE TABLE usuarios (
    nombre VARCHAR PRIMARY KEY,
    rol    VARCHAR NOT NULL
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
