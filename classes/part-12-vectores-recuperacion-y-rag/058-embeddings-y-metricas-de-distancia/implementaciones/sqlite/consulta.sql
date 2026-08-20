-- motor: sqlite
-- doc: https://sqlite.org/lang_expr.html
-- nota: esto es busqueda EXACTA por fuerza bruta: calcula la distancia a todos
--       los documentos, siempre. Y no hay indice B-Tree que ayude, porque el
--       orden depende de una funcion de TODAS las coordenadas, no del valor de
--       una columna. De ahi que los indices vectoriales sean otra familia
--       entera de estructuras.

-- === preparacion ===
-- Vectores de dimension 3, con enteros a proposito: asi la distancia
-- euclidea al cuadrado es un entero exacto y se puede comparar entre motores
-- sin discutir sobre decimales. En un sistema real serian 384, 768 o 1536
-- numeros en coma flotante.
CREATE TABLE documentos (
    id TEXT PRIMARY KEY,
    v1 INTEGER NOT NULL,
    v2 INTEGER NOT NULL,
    v3 INTEGER NOT NULL
);
INSERT INTO documentos (id, v1, v2, v3) VALUES
    ('A', 2, 0, 0),
    ('B', 0, 2, 0),
    ('C', 1, 1, 0);

-- === consulta ===
-- La consulta es el vector [2, 0, 0]. «Parecido» es una operacion aritmetica
-- sobre coordenadas, no una comparacion de texto: por eso la busqueda vectorial
-- encuentra lo que significa lo mismo aunque no comparta ni una palabra.
--
-- Se usa la distancia euclidea AL CUADRADO, que ordena igual que la euclidea y
-- se calcula sin raiz. Con vectores normalizados, ademas, ordena igual que el
-- coseno: por eso casi todos los sistemas normalizan al indexar.
SELECT id,
       (v1 - 2) * (v1 - 2) + (v2 - 0) * (v2 - 0) + (v3 - 0) * (v3 - 0) AS distancia
FROM documentos
ORDER BY distancia, id;
