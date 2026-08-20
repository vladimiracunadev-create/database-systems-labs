-- motor: sqlite
-- doc: https://sqlite.org/fileformat.html
-- nota: SQLite guarda la FILA entera junta en la pagina. Para sumar `importe`
--       tiene que leer tambien `id` y `categoria` de cada una de las mil filas.
--       Con mil no se nota. Con cien millones, es el problema entero, y ningun
--       indice lo arregla: no se trata de encontrar las filas, se trata de
--       leerlas todas.

-- === preparacion ===
CREATE TABLE hechos (
    id        INTEGER PRIMARY KEY,
    categoria TEXT NOT NULL,
    importe   INTEGER NOT NULL
);

WITH RECURSIVE serie(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM serie WHERE n < 1000
)
INSERT INTO hechos (id, categoria, importe)
SELECT n, 'c' || (n % 2), n FROM serie;

-- === consulta ===
SELECT categoria, SUM(importe) AS importe
FROM hechos
GROUP BY categoria
ORDER BY categoria;
