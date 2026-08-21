-- motor: sqlite
-- doc: https://sqlite.org/lang_expr.html
-- nota: en Python, la forma correcta es la de siempre:
--         cur.execute("SELECT COUNT(*) FROM usuarios WHERE nombre = ?", (entrada,))
--       Y el detalle que empuja al error: executescript() NO admite parametros,
--       asi que quien necesita varias sentencias acaba concatenando.

-- === preparacion ===
CREATE TABLE usuarios (
    nombre TEXT PRIMARY KEY,
    rol    TEXT NOT NULL
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
