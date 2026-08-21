-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/functions-window.html
-- nota: con pgvector instalado, las dos busquedas y la fusion caben en UNA
--       consulta y UNA transaccion:
--         WITH lexico AS (
--           SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank(buscado, q) DESC) AS pos
--           FROM documentos, to_tsquery('spanish', 'bases & datos') q
--           WHERE buscado @@ q LIMIT 50),
--         vectorial AS (
--           SELECT id, ROW_NUMBER() OVER (ORDER BY v <-> :consulta) AS pos
--           FROM documentos ORDER BY v <-> :consulta LIMIT 50)
--         SELECT id FROM (...) GROUP BY id ORDER BY SUM(1.0/(60+pos)) DESC;
--       Sin sistemas adicionales que sincronizar: esa es toda la ventaja.

-- === preparacion ===
DROP TABLE IF EXISTS ranking_lexico, ranking_vectorial;

-- Dos rankings del mismo documento: el lexico (indice invertido, encuentra
-- las palabras exactas) y el vectorial (embeddings, encuentra el significado).
-- No coinciden, y esa discrepancia es justamente lo que los hace
-- complementarios: el lexico acierta con nombres propios, codigos y siglas; el
-- vectorial, con sinonimos y parafrasis.
CREATE TABLE ranking_lexico (
    doc      text PRIMARY KEY,
    posicion integer NOT NULL
);
CREATE TABLE ranking_vectorial (
    doc      text PRIMARY KEY,
    posicion integer NOT NULL
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
