-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
-- nota: aqui la frontera NO esta en la consulta: la aplica el servidor. El
--       SELECT de abajo no lleva ningun WHERE sobre el inquilino y aun asi
--       devuelve solo dos filas.
--
--       TRES trampas, y las tres se descubren tarde:
--       1) El SUPERUSUARIO se salta TODAS las politicas, siempre, y no hay
--          FORCE que lo impida. Como el usuario de la aplicacion en un entorno
--          de desarrollo suele ser superusuario, la proteccion parece no
--          funcionar. Por eso este guion crea un rol sin privilegios y cambia a
--          el antes de consultar: sin ese SET ROLE, esta consulta devuelve las
--          TRES filas.
--       2) FORCE ROW LEVEL SECURITY: sin el, el DUENO de la tabla tambien se
--          salta sus propias politicas.
--       3) La politica se evalua por fila: si consulta otras tablas, puede
--          impedir el uso de indices y costar mas que la propia consulta.

-- === preparacion ===
DROP TABLE IF EXISTS notas;

CREATE TABLE notas (
    inquilino  text NOT NULL,
    estudiante text NOT NULL,
    nota       integer NOT NULL,
    PRIMARY KEY (inquilino, estudiante)
);
INSERT INTO notas (inquilino, estudiante, nota) VALUES
    ('acme',   'Ada', 90),
    ('acme',   'Bea', 58),
    ('globex', 'Cid', 77);

ALTER TABLE notas ENABLE ROW LEVEL SECURITY;
ALTER TABLE notas FORCE ROW LEVEL SECURITY;

CREATE POLICY solo_mi_inquilino ON notas
    USING (inquilino = current_setting('app.inquilino', true));

-- El rol de la aplicacion: sin privilegios especiales, que es la unica forma de
-- que las politicas se le apliquen.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_inquilino') THEN
        CREATE ROLE app_inquilino NOLOGIN;
    END IF;
END;
$$;
-- Y los permisos minimos: ver el esquema y leer la tabla. Nada mas.
DO $$
BEGIN
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO app_inquilino', current_schema());
END;
$$;
GRANT SELECT ON notas TO app_inquilino;

-- === consulta ===
-- La aplicacion fija su identidad al abrir la conexion. A partir de ahi,
-- ninguna consulta necesita —ni puede— saltarse el filtro.
SET app.inquilino = 'acme';
SET ROLE app_inquilino;

SELECT estudiante, nota FROM notas ORDER BY estudiante;
