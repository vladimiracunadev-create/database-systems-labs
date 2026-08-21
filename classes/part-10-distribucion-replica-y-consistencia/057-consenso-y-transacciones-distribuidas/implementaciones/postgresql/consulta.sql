-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-prepare-transaction.html
-- nota: PostgreSQL SI implementa la confirmacion en dos fases:
--         BEGIN; ...; PREPARE TRANSACTION 'reserva-42';
--         COMMIT PREPARED 'reserva-42';   -- o ROLLBACK PREPARED
--       Y conviene saber por que casi nadie la usa: una transaccion preparada
--       retiene sus bloqueos INDEFINIDAMENTE si el coordinador desaparece, y
--       basta una olvidada para impedir el vacio de toda la base. Por eso
--       max_prepared_transactions vale 0 por omision: hay que activarlo a
--       proposito. La saga existe porque esa alternativa sale peor.

-- === preparacion ===
DROP TABLE IF EXISTS reservas;

CREATE TABLE reservas (
    paso   text PRIMARY KEY,
    estado text NOT NULL
);

-- Paso 1: el servicio de vuelos confirma. En SU base de datos, esto ya esta
-- hecho y CONFIRMADO: nadie de fuera puede deshacerlo.
INSERT INTO reservas (paso, estado) VALUES ('vuelo', 'confirmado');

-- Paso 2: el servicio de hoteles no tiene habitaciones. Falla.
INSERT INTO reservas (paso, estado) VALUES ('hotel', 'fallido');

-- Compensacion. Y aqui esta toda la clase: esto NO es un ROLLBACK. El vuelo se
-- confirmo de verdad, existio como reserva valida durante un tiempo, y alguien
-- pudo verlo. Deshacerlo exige ejecutar la ACCION INVERSA —cancelar—, que es
-- una operacion de negocio con sus propias reglas: puede tener penalizacion,
-- puede requerir autorizacion, y puede fallar tambien.
UPDATE reservas SET estado = 'compensado' WHERE paso = 'vuelo';

-- === consulta ===
SELECT paso, estado FROM reservas ORDER BY paso;
