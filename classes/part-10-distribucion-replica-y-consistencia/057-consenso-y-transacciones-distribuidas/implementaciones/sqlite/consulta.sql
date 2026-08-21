-- motor: sqlite
-- doc: https://sqlite.org/lang_update.html
-- nota: la fila del vuelo NO desaparece: queda como 'compensado'. Esa
--       diferencia con un ROLLBACK es la clase entera. Y hay una segunda
--       leccion escondida: si el proceso muere entre el fallo del hotel y la
--       compensacion, nadie sabra que habia que compensar. El registro de la
--       saga tiene que ser duradero ANTES de dar el primer paso.

-- === preparacion ===
CREATE TABLE reservas (
    paso   TEXT PRIMARY KEY,
    estado TEXT NOT NULL
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
