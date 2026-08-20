-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/functions/window_functions.html
-- nota: aqui es donde se AJUSTA la formula. Probar varios valores de k sobre un
--       conjunto de evaluacion completo es una consulta mas:
--         SELECT k, ... FROM UNNEST([10,30,60,100]) AS s(k), ...
--       y comparar el MRR resultante de cada uno. Elegir k = 60 porque lo dice
--       el articulo es razonable; comprobarlo con los datos propios es mejor.

-- === preparacion ===
-- Dos rankings del mismo documento: el lexico (indice invertido, encuentra
-- las palabras exactas) y el vectorial (embeddings, encuentra el significado).
-- No coinciden, y esa discrepancia es justamente lo que los hace
-- complementarios: el lexico acierta con nombres propios, codigos y siglas; el
-- vectorial, con sinonimos y parafrasis.
CREATE TABLE ranking_lexico (
    doc      VARCHAR PRIMARY KEY,
    posicion INTEGER NOT NULL
);
CREATE TABLE ranking_vectorial (
    doc      VARCHAR PRIMARY KEY,
    posicion INTEGER NOT NULL
);
INSERT INTO ranking_lexico (doc, posicion) VALUES ('A', 1), ('B', 2), ('C', 3);
INSERT INTO ranking_vectorial (doc, posicion) VALUES ('C', 1), ('A', 2), ('D', 3);

-- === consulta ===
-- Fusion por rango reciproco (RRF): cada lista aporta 1/(k + posicion) y se
-- suman. La clave es que usa POSICIONES, no puntuaciones: las de BM25 y las de
-- coseno no son comparables entre si —ni siquiera estan en la misma escala— y
-- normalizarlas exige conocer sus distribuciones. El rango, en cambio, siempre
-- significa lo mismo.
--
-- El k = 60 amortigua el peso de los primeros puestos. Es el valor del articulo
-- original de Cormack (2009) y el que casi todos los sistemas traen de fabrica.
--
-- Resultado: A gana por aparecer bien situado en LAS DOS listas, aunque no sea
-- el primero de ninguna de las dos. Eso es exactamente lo que se busca.
SELECT doc
FROM (
    SELECT doc, 1.0 / (60 + posicion) AS aporte FROM ranking_lexico
    UNION ALL
    SELECT doc, 1.0 / (60 + posicion) FROM ranking_vectorial
) todos
GROUP BY doc
ORDER BY SUM(aporte) DESC, doc;
