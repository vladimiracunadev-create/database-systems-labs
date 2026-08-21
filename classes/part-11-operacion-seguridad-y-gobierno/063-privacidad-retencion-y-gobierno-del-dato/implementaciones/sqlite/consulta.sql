-- motor: sqlite
-- doc: https://sqlite.org/lang_delete.html
-- nota: el DELETE no reduce el archivo ni borra los bytes: el espacio queda en
--       la lista de paginas libres y los datos siguen legibles hasta que algo
--       los sobrescriba. Para borrado real hace falta VACUUM, y ni asi se
--       controla lo que el sistema de archivos haya copiado.

-- === preparacion ===
CREATE TABLE eventos (
    id     INTEGER PRIMARY KEY,
    correo TEXT NOT NULL,
    fecha  TEXT NOT NULL
);
INSERT INTO eventos (id, correo, fecha) VALUES
    (1, 'ada@example.org',   '2025-01-15'),
    (2, 'linus@example.org', '2026-08-10'),
    (3, 'grace@otro.org',    '2026-08-15');

-- RETENCION: lo que ya no hace falta se borra. Guardar «por si acaso» no es
-- prudencia, es responsabilidad acumulada: cada dato conservado de mas es un
-- dato que se puede filtrar y que alguien puede reclamar.
DELETE FROM eventos WHERE fecha < '2026-01-01';

-- === consulta ===
-- MINIMIZACION: el analisis necesita el dominio, no la persona. Enmascarar en
-- la CONSULTA no protege nada —el dato sigue ahi—; esto es lo que se hace al
-- exportar a un entorno que no deberia tener el dato original.
SELECT '***@' || SUBSTR(correo, INSTR(correo, '@') + 1) AS correo, fecha
FROM eventos
ORDER BY fecha;
