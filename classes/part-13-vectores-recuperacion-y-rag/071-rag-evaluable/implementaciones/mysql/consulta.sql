-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/aggregate-functions.html
-- nota: mismo aviso sobre los nulos que en SQLite, y aqui con mas motivo: los
--       agregados de MySQL ignoran nulos en silencio, asi que un fallo de
--       recuperacion se convierte en una metrica inflada sin que nada avise.

-- === preparacion ===
DROP TABLE IF EXISTS evaluacion;

-- El resultado de una recuperacion sobre un conjunto de evaluacion: para cada
-- pregunta, en que posicion aparecio el documento que de verdad la responde.
-- Nulo significa que NO se recupero en absoluto.
CREATE TABLE evaluacion (
    pregunta            VARCHAR(20) PRIMARY KEY,
    posicion_relevante  INT
);
INSERT INTO evaluacion (pregunta, posicion_relevante) VALUES
    ('q1', 1),
    ('q2', 3),
    ('q3', NULL);   -- el sistema no encontro el documento correcto

-- === consulta ===
-- Dos metricas que hay que calcular ANTES de mirar ninguna respuesta generada:
--
--   aciertos en el top 3  cuantas preguntas tienen su documento entre los tres
--                         primeros. Si el documento correcto no llega al
--                         contexto, el modelo NO puede responder bien: como
--                         mucho, puede inventar algo plausible.
--   MRR                   media del inverso de la posicion. Premia que el
--                         documento correcto este ARRIBA, no solo presente.
--
-- Con estos datos: 2 de 3 en el top 3, y MRR = (1/1 + 1/3 + 0) / 3 = 0,44.
SELECT metrica, valor
FROM (
    SELECT 'preguntas' AS metrica,
           CAST(COUNT(*) AS CHAR) AS valor
    FROM evaluacion
    UNION ALL
    SELECT 'aciertos_top3',
           CAST(SUM(CASE WHEN posicion_relevante IS NOT NULL
                          AND posicion_relevante <= 3 THEN 1 ELSE 0 END) AS CHAR)
    FROM evaluacion
    UNION ALL
    SELECT 'mrr',
           CAST(ROUND(SUM(CASE WHEN posicion_relevante IS NULL THEN 0.0
                               ELSE 1.0 / posicion_relevante END) / COUNT(*), 2) AS CHAR)
    FROM evaluacion
) metricas
ORDER BY metrica;
