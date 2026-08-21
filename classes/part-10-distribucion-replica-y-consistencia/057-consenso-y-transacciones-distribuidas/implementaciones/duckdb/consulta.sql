-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/select.html
-- nota: la consulta que de verdad importa aqui es la de auditoria, la que se
--       ejecuta sobre el registro de todas las sagas:
--         SELECT saga_id FROM pasos WHERE estado = 'fallido'
--         AND saga_id NOT IN (SELECT saga_id FROM pasos WHERE estado = 'compensado');
--       Es decir: que sagas quedaron a medias. Ahi esta el dinero perdido.

-- === preparacion ===
CREATE TABLE reservas (
    paso   VARCHAR PRIMARY KEY,
    estado VARCHAR NOT NULL
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
