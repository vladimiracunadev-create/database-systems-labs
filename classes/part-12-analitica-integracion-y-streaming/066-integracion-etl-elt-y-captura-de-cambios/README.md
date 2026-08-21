# 066 — Integración: ETL, ELT, captura de cambios y el registro como nexo

> [Programa](../../../README.md) · [Parte 12](../README.md) · [← Anterior](../../part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) · [Siguiente →](../../part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md)

Parte 12 — Analítica, integración y streaming · Avanzado ·
3 horas estimadas · motores `postgresql`, `kafka` · laboratorio
[`labs/05-nosql-workloads`](../../../labs/05-nosql-workloads/README.md) · 4 fuentes.

**Conceptos centrales:** `ETL` · `ELT` · `CDC` · `escritura dual` · `idempotencia de carga`

**En este caso se comparan 8 motores**: 6 lo resuelven (5 con el resultado comprobado por máquina) y 2 no, con el motivo escrito.

---

## Propósito

Mover datos entre sistemas sin perderlos, sin duplicarlos y sin perder su significado. El registro de transacciones resulta ser la pieza que unifica replicación, integración y streaming.

## Resultados de aprendizaje

Al terminar podrás:

1. Comparar ETL y ELT y decidir con criterio.
2. Explicar por qué la extracción incremental por marca de tiempo pierde filas.
3. Describir la captura de cambios leyendo el registro del motor.
4. Diseñar una carga idempotente y reprocesable.
5. Reconocer el problema de la doble escritura y sus soluciones.

## Fundamentos

### ETL frente a ELT

| | ETL | ELT |
|---|---|---|
| Orden | Extraer, transformar, cargar | Extraer, cargar, **transformar dentro** |
| Dónde se transforma | Proceso intermedio | En el almacén |
| Reproceso | Reejecutar todo el canal | Volver a ejecutar SQL sobre lo crudo |
| Requiere | Motor de transformación | Almacén potente y barato |
| Trazabilidad | Se pierde el dato original | **Se conserva lo crudo** |

ELT es hoy la opción predominante porque el almacenamiento es barato y los motores columnares son rápidos. Su ventaja decisiva es la trazabilidad: conservar los datos crudos permite **rehacer** la transformación cuando se descubre que estaba mal, sin volver a pedirle nada al sistema origen.

En ETL, un error de transformación descubierto tres meses después es irrecuperable si el origen ya rotó sus datos.

### Por qué la extracción incremental por marca de tiempo pierde filas

El patrón más común y el más roto:

```sql
SELECT * FROM enrollments WHERE actualizado_en > :ultima_marca;
```

Falla por cuatro motivos, todos silenciosos:

1. **Transacciones largas.** Una fila con `actualizado_en = 10:00:05` confirmada a las 10:00:12, cuando la extracción ya leyó hasta las 10:00:10, no se ve nunca.
2. **Relojes.** Si `actualizado_en` lo pone la aplicación, dos servidores con desfase producen huecos.
3. **Borrados.** Una fila borrada no aparece en ninguna consulta. El destino conserva datos que ya no existen.
4. **Actualizaciones sin tocar la marca.** Una migración con `UPDATE ... SET x = y` que olvide `actualizado_en` es invisible.

El punto 1 es el que engaña: el canal no falla nunca y las filas simplemente faltan. Solo se detecta comparando conteos con el origen.

**Mitigación parcial:** solapar la ventana (`> ultima_marca - 5 minutos`) y hacer la carga idempotente. No resuelve el punto 3.

### Captura de cambios desde el registro

En lugar de consultar la tabla, se lee el **registro de transacciones** del motor —el mismo WAL de la clase 036 que sirve para recuperarse y para replicar—.

```mermaid
flowchart LR
    A["Aplicación"] --> DB[("PostgreSQL")]
    DB --> W["WAL"]
    W --> D["Debezium<br/>ranura de replicación lógica"]
    D --> K["Kafka<br/>tema por tabla"]
    K --> S1["Almacén"]
    K --> S2["Motor de búsqueda"]
    K --> S3["Caché"]
    K --> S4["Servicio de auditoría"]
```

Ventajas frente a la consulta periódica:

| | Consulta por marca | Captura desde el registro |
|---|---|---|
| Borrados | **Invisibles** | Capturados |
| Transacciones largas | Pierde filas | Correcto: lee el orden de confirmación |
| Carga sobre el origen | Consultas periódicas | Mínima: lee el WAL |
| Latencia | Intervalo de sondeo | Segundos |
| Estado anterior | No disponible | Disponible (con `REPLICA IDENTITY FULL`) |
| Complejidad | Baja | Media-alta |

Kreps lo formuló como principio general: **el registro es la abstracción que unifica** replicación, integración y streaming. Un solo flujo ordenado de cambios alimenta todos los consumidores, cada uno a su ritmo.

Requisitos en PostgreSQL:

```sql
ALTER SYSTEM SET wal_level = logical;   -- requiere reinicio
CREATE PUBLICATION cdc_enrollments FOR TABLE enrollments, courses, students;
ALTER TABLE enrollments REPLICA IDENTITY FULL;   -- para tener el estado anterior
```

**Advertencia operativa:** una ranura de replicación con un consumidor detenido **impide reciclar el WAL** y llena el disco del primario. Es la causa número uno de incidentes con captura de cambios, y hay que vigilarla:

```sql
SELECT slot_name, active,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retenido
FROM pg_replication_slots;
```

### El problema de la doble escritura

```python
db.insert(inscripcion)        # ✓
kafka.publish(evento)         # ✗ falla → el evento nunca sale
```

Dos sistemas, ninguna atomicidad. Las tres soluciones, ya vistas en la clase 047:

1. **Bandeja de salida transaccional:** escribir estado y evento en la misma transacción local; un proceso publica desde la tabla de salida.
2. **Captura de cambios:** no publicar nada; el evento se deriva del cambio en la base.
3. **Origen de eventos:** el evento **es** el estado; la base se deriva de él.

La 2 es la más barata cuando ya existe la infraestructura de captura, porque elimina la doble escritura sin tocar el código de la aplicación.

## Ejemplo trabajado

Objetivo: mantener el almacén sincronizado con las inscripciones, con latencia inferior a un minuto y sin perder borrados.

**Enfoque A — consulta periódica. Detección del fallo:**

```sql
-- en el origen
SELECT count(*) FROM enrollments;                  -- 5 002 341
-- en el destino
SELECT count(*) FROM stg_enrollments;              -- 4 998 102
--                                                    faltan 4 239
```

Investigación: 3 100 corresponden a filas borradas en el origen que el destino conserva, y 1 139 a filas confirmadas por transacciones largas durante la ventana de extracción. El canal llevaba meses «funcionando».

**Enfoque B — captura desde el registro:**

```json
// Evento producido por Debezium
{
  "op": "u",
  "before": {"student_id": 11, "course_id": 42, "nota": 5.5, "estado": "activa"},
  "after":  {"student_id": 11, "course_id": 42, "nota": 6.0, "estado": "activa"},
  "source": {"lsn": 24857392, "ts_ms": 1755600000123, "table": "enrollments"}
}
```

`op` vale `c` (crear), `u` (actualizar), `d` (borrar) o `r` (instantánea inicial). El borrado deja de ser invisible.

**Carga idempotente en el almacén:**

```sql
-- Zona cruda: se guarda TODO el evento, sin transformar (principio ELT)
CREATE TABLE raw_enrollments (
  lsn        BIGINT PRIMARY KEY,     -- orden total del origen; hace la carga idempotente
  op         CHAR(1) NOT NULL,
  ts_ms      BIGINT  NOT NULL,
  before     JSONB,
  after      JSONB,
  ingerido_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Reprocesar el mismo evento no duplica: la clave primaria lo impide.
INSERT INTO raw_enrollments (lsn, op, ts_ms, before, after)
VALUES (:lsn, :op, :ts, :before::jsonb, :after::jsonb)
ON CONFLICT (lsn) DO NOTHING;
```

El LSN es la pieza clave: es un **orden total** asignado por el origen. Sirve de clave de idempotencia (clase 037) y de criterio de desempate.

**Vista del estado actual, derivada de lo crudo:**

```sql
CREATE OR REPLACE VIEW cur_enrollments AS
SELECT DISTINCT ON (
         COALESCE(after->>'student_id', before->>'student_id'),
         COALESCE(after->>'course_id',  before->>'course_id'))
       COALESCE(after->>'student_id', before->>'student_id')::int AS student_id,
       COALESCE(after->>'course_id',  before->>'course_id')::int  AS course_id,
       (after->>'nota')::numeric(2,1) AS nota,
       after->>'estado'               AS estado,
       op = 'd'                       AS borrado,
       lsn
FROM raw_enrollments
ORDER BY 1, 2, lsn DESC;    -- el LSN mayor gana: es el último cambio
```

Propiedades que resultan de este diseño:

- **Idempotente:** reprocesar el mismo flujo no cambia el resultado.
- **Reprocesable:** si la transformación estaba mal, se corrige la vista y se recalcula sobre lo crudo. No hay que pedirle nada al origen.
- **Completo:** los borrados aparecen como `op = 'd'`.
- **Auditable:** el histórico completo de cambios queda disponible.

**Verificación diaria, que es lo que convierte el canal en fiable:**

```sql
-- Conteos comparados: origen frente a destino
SELECT (SELECT count(*) FROM enrollments)                                AS origen,
       (SELECT count(*) FROM cur_enrollments WHERE NOT borrado)          AS destino;

-- Frescura: ¿cuánto hace del último evento recibido?
SELECT now() - to_timestamp(max(ts_ms)/1000) AS retraso FROM raw_enrollments;
```

Ambas comprobaciones con alerta. Un canal de datos sin verificación de conteo es un canal del que nadie puede afirmar que funciona.

## Comparación

| Necesidad | Mecanismo |
|---|---|
| Carga histórica inicial | Instantánea completa |
| Sincronización continua sin borrados | Consulta por marca (con reservas) |
| Sincronización completa | Captura desde el registro |
| Estado + evento atómicos | Bandeja de salida |
| Varios destinos del mismo cambio | Registro compartido (Kafka) |
| Corregir una transformación pasada | ELT sobre datos crudos conservados |

## Errores frecuentes

1. **Extracción incremental sin solape ni verificación de conteos.** Pierde filas en silencio.
2. **Ignorar los borrados.** El destino acumula datos que ya no existen.
3. **Ranura de replicación sin vigilancia.** Llena el disco del primario.
4. **Cargas no idempotentes.** Un reintento duplica.
5. **Transformar antes de conservar lo crudo.** Un error de transformación es irreversible.
6. **Doble escritura a base y a cola.** Divergencia garantizada.
7. **Canal sin comprobación de frescura.** Se detiene y nadie lo nota.

## De la clase a la operación

Un canal de datos roto no da errores: da cifras ligeramente distintas que nadie relaciona con él. La verificación de conteo y de frescura, con alerta, es lo único que convierte el canal en una fuente en la que se puede confiar.

## Reto de transferencia

1. Compara conteos entre origen y destino de un canal real tuyo y explica la diferencia.
2. Configura replicación lógica y captura los tres tipos de operación.
3. Implementa la carga idempotente por LSN y demuestra que reprocesar no duplica.
4. Añade las comprobaciones de conteo y frescura con sus alertas.

## Preguntas de evaluación

1. Explica con una traza cómo una transacción larga hace perder filas a la extracción por marca.
2. ¿Por qué los borrados son invisibles en ese enfoque y no en la captura desde el registro?
3. ¿Qué ocurre si el consumidor de una ranura de replicación se detiene una semana?
4. Da una transformación tuya que hoy sería imposible corregir retroactivamente, y cómo lo arreglarías.

---

## 🌐 El mismo problema en cada motor

**Caso:** Cargar el mismo lote dos veces y que el destino no se entere

Todo proceso de integración se reintenta: la red falla, el trabajo se cae a
mitad, alguien lo relanza «por si acaso». Si cargar dos veces el mismo lote
duplica las filas, el sistema es una bomba de relojería. Por eso la
propiedad que define una carga bien hecha no es la velocidad: es la
**idempotencia**.

El caso carga tres clientes y **repite la carga entera** con el mismo lote.
El destino tiene que quedar con tres filas y los mismos saldos, no con seis.
La forma de conseguirlo es la misma en todas partes —escribir por clave, no
añadir— y lo que cambia es cómo se llama en cada motor y qué pasa cuando la
clave no basta.

Salida esperada, idéntica en todos los motores que lo resuelven:

| cliente | saldo |
|---|---|
| `C-1` | `10` |
| `C-2` | `20` |
| `C-3` | `30` |

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase 066`: 5 de
las 6 implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| PostgreSQL | sí | servicio | [código](implementaciones/postgresql/consulta.sql) | [doc oficial](https://www.postgresql.org/docs/current/sql-insert.html) |
| MySQL | sí | servicio | [código](implementaciones/mysql/consulta.sql) | [doc oficial](https://dev.mysql.com/doc/refman/8.4/en/insert-on-duplicate.html) |
| SQLite | sí | núcleo | [código](implementaciones/sqlite/consulta.sql) | [doc oficial](https://sqlite.org/lang_upsert.html) |
| DuckDB | sí | núcleo | [código](implementaciones/duckdb/consulta.sql) | [doc oficial](https://duckdb.org/docs/stable/sql/statements/insert) |
| MongoDB | sí | servicio | [código](implementaciones/mongodb/consulta.js) | [doc oficial](https://www.mongodb.com/docs/manual/changeStreams/) |
| ClickHouse | sí | declarado | [código](implementaciones/clickhouse/consulta.sql) | [doc oficial](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree) |
| Apache Kafka | **no** | — | — | [doc oficial](https://kafka.apache.org/documentation/#semantics) |
| Redis | **no** | — | — | [doc oficial](https://redis.io/docs/latest/commands/sadd/) |

### Los que resuelven el caso

#### PostgreSQL · [`implementaciones/postgresql/consulta.sql`](implementaciones/postgresql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-insert.html
-- nota: la captura de cambios de PostgreSQL sale del WAL por decodificacion
--       logica, sin disparadores ni consultas periodicas:
--         CREATE PUBLICATION integracion FOR TABLE destino;
--         SELECT pg_create_logical_replication_slot('cdc', 'pgoutput');
--       Y el aviso que cuesta un incidente: una RANURA que nadie consume
--       retiene el WAL indefinidamente y llena el disco del primario. Vigilar
--       pg_replication_slots forma parte de operar una integracion.

-- === preparacion ===
DROP TABLE IF EXISTS destino;

CREATE TABLE destino (
    cliente text PRIMARY KEY,
    saldo   integer NOT NULL
);

INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- === consulta ===
SELECT cliente, saldo FROM destino ORDER BY cliente;
```

- **Por qué sí:** `INSERT ... ON CONFLICT DO UPDATE` resuelve la carga idempotente en una sentencia, y su **decodificación lógica** convierte al WAL en una fuente de captura de cambios: Debezium y compañía leen de ahí sin consultar la base ni añadir disparadores.
- **Por qué no:** Esa captura obliga a gestionar las **ranuras de réplica**: una ranura que nadie consume retiene el WAL indefinidamente y llena el disco del primario. Es la avería clásica de una integración abandonada.
- 📄 Documentación oficial: <https://www.postgresql.org/docs/current/sql-insert.html>

#### MySQL · [`implementaciones/mysql/consulta.sql`](implementaciones/mysql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/insert-on-duplicate.html
-- nota: la trampa de esta clausula: se dispara con CUALQUIER clave unica, no
--       solo con la que se tenia en mente. Si la tabla tuviera ademas
--       UNIQUE(correo), una fila con cliente nuevo y correo repetido
--       actualizaria la fila del correo, no insertaria: la carga «idempotente»
--       machacaria un registro distinto del esperado, en silencio.

-- === preparacion ===
DROP TABLE IF EXISTS destino;

CREATE TABLE destino (
    cliente VARCHAR(20) PRIMARY KEY,
    saldo   INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON DUPLICATE KEY UPDATE saldo = VALUES(saldo);

INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON DUPLICATE KEY UPDATE saldo = VALUES(saldo);

-- === consulta ===
SELECT cliente, saldo FROM destino ORDER BY cliente;
```

- **Por qué sí:** `INSERT ... ON DUPLICATE KEY UPDATE` hace lo mismo, y el registro binario en formato de fila (`ROW`) es una fuente de captura de cambios madura y muy usada.
- **Por qué no:** `ON DUPLICATE KEY UPDATE` se dispara con **cualquier** clave única, no solo con la que se esperaba: con dos restricciones únicas, la sentencia puede actualizar una fila distinta de la que se pretendía, en silencio.
- 📄 Documentación oficial: <https://dev.mysql.com/doc/refman/8.4/en/insert-on-duplicate.html>

#### SQLite · [`implementaciones/sqlite/consulta.sql`](implementaciones/sqlite/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: sqlite
-- doc: https://sqlite.org/lang_upsert.html
-- nota: la carga se ejecuta DOS VECES a proposito, con el mismo lote. Si en vez
--       de ON CONFLICT hubiera un INSERT normal, la segunda pasada fallaria por
--       clave duplicada; con INSERT OR IGNORE no fallaria pero tampoco
--       actualizaria los saldos cambiados. El upsert es lo unico que hace las
--       dos cosas bien.

-- === preparacion ===
CREATE TABLE destino (
    cliente TEXT PRIMARY KEY,
    saldo   INTEGER NOT NULL
);

-- Primera pasada.
INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- Segunda pasada: EL MISMO LOTE. Alguien relanzo el trabajo.
INSERT INTO destino (cliente, saldo) VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- === consulta ===
SELECT cliente, saldo FROM destino ORDER BY cliente;
```

- **Por qué sí:** Tiene la misma cláusula `ON CONFLICT DO UPDATE` con la sintaxis de PostgreSQL: la idempotencia se puede estudiar y probar sin infraestructura.
- **Por qué no:** No hay captura de cambios: para saber qué cambió hay que compararlo todo, o llevar una columna de marca de tiempo y confiar en que nadie la olvide al escribir.
- 📄 Documentación oficial: <https://sqlite.org/lang_upsert.html>

#### DuckDB · [`implementaciones/duckdb/consulta.sql`](implementaciones/duckdb/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/insert
-- nota: la T de ELT. En un proceso real, el origen no seria un VALUES sino un
--       fichero leido directamente:
--         INSERT INTO destino SELECT * FROM read_csv_auto('lote.csv')
--         ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- === preparacion ===
CREATE TABLE destino (
    cliente VARCHAR PRIMARY KEY,
    saldo   INTEGER NOT NULL
);

INSERT INTO destino VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

INSERT INTO destino VALUES ('C-1', 10), ('C-2', 20), ('C-3', 30)
ON CONFLICT (cliente) DO UPDATE SET saldo = excluded.saldo;

-- === consulta ===
SELECT cliente, saldo FROM destino ORDER BY cliente;
```

- **Por qué sí:** Es la herramienta natural de la **T** de ELT: transforma leyendo directamente ficheros CSV o Parquet, y admite el mismo `ON CONFLICT`. Buena parte de los procesos que antes exigían un clúster caben aquí.
- **Por qué no:** No es un destino operativo ni un orquestador: no hay reintentos, ni registro de ejecuciones, ni gestión de dependencias entre tareas. Es el motor de transformación, no el proceso.
- 📄 Documentación oficial: <https://duckdb.org/docs/stable/sql/statements/insert>

#### MongoDB · [`implementaciones/mongodb/consulta.js`](implementaciones/mongodb/consulta.js)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```javascript
// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/changeStreams/
// nota: la captura de cambios aqui son los FLUJOS DE CAMBIOS, con reanudacion
//       por testigo:
//         const flujo = db.destino.watch([], { resumeAfter: testigo });
//       Y su limite: el testigo caduca con el oplog. Si el consumidor esta
//       parado mas tiempo del que cubre el oplog, no puede reanudar y hay que
//       recargarlo todo. Dimensionar el oplog es parte del diseno.

// === preparacion ===
db.destino.drop();

const lote = [
  { cliente: "C-1", saldo: 10 },
  { cliente: "C-2", saldo: 20 },
  { cliente: "C-3", saldo: 30 },
];

function cargar(lote) {
  for (const fila of lote) {
    db.destino.updateOne(
      { _id: fila.cliente },
      { $set: { saldo: fila.saldo } },
      { upsert: true },
    );
  }
}

cargar(lote);
cargar(lote); // el mismo lote, otra vez

// === consulta ===
db.destino
  .find()
  .sort({ _id: 1 })
  .forEach((d) => print(d._id + "|" + d.saldo));
```

- **Por qué sí:** `updateOne` con `upsert: true` es idempotente por definición, y los **flujos de cambios** (`watch`) dan captura de cambios con reanudación por testigo: se puede retomar exactamente donde se dejó tras una caída.
- **Por qué no:** Ese testigo de reanudación caduca con el registro de operaciones: si el consumidor está parado más tiempo del que cubre el `oplog`, no puede reanudar y hay que **recargarlo todo**. Dimensionar el `oplog` es parte del diseño de la integración.
- 📄 Documentación oficial: <https://www.mongodb.com/docs/manual/changeStreams/>

#### ClickHouse · [`implementaciones/clickhouse/consulta.sql`](implementaciones/clickhouse/consulta.sql)

⚪ **declarado** — se revisa a mano contra la documentación citada; la máquina no lo ejecuta

```sql
-- motor: clickhouse
-- doc: https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree
-- nota: implementacion declarada. Aqui la idempotencia se consigue SIN UPDATE:
--       se insertan siempre filas nuevas con una version, y la fusion se queda
--       con la ultima. Encaja con un almacen que solo sabe anadir.
--       El precio, que hay que tener presente: la deduplicacion ocurre CUANDO
--       LA FUSION DECIDE, no al insertar. Hasta entonces conviven las dos
--       versiones y una consulta puede contarlas las dos. De ahi el FINAL de
--       abajo, que fuerza la vista deduplicada y es caro.

-- === preparacion ===
CREATE TABLE destino (
    cliente String,
    saldo   UInt32,
    version UInt64
) ENGINE = ReplacingMergeTree(version) ORDER BY cliente;

INSERT INTO destino VALUES ('C-1', 10, 1), ('C-2', 20, 1), ('C-3', 30, 1);
INSERT INTO destino VALUES ('C-1', 10, 1), ('C-2', 20, 1), ('C-3', 30, 1);

-- === consulta ===
SELECT cliente, saldo FROM destino FINAL ORDER BY cliente;
```

- **Por qué sí:** Su motor `ReplacingMergeTree` da idempotencia sin `UPDATE`: se insertan siempre filas nuevas con una versión, y la fusión se queda con la última. Encaja con un almacén que solo sabe añadir.
- **Por qué no:** La deduplicación ocurre **cuando la fusión decide**, no al insertar: hasta entonces conviven las dos versiones y una consulta puede contarlas las dos. Hay que escribir `FINAL` —que es caro— o agregar de forma que los duplicados no importen.
- 📄 Documentación oficial: <https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree>

### Los que no resuelven este caso — y qué se hace en su lugar

Descartar un motor con un argumento es tan formativo como usarlo. Ninguna de estas filas dice que el motor sea peor: dice que este problema no es el suyo.

| Motor | Por qué no | Qué se hace en su lugar | Fuente |
|---|---|---|---|
| Apache Kafka | No es un destino donde cargar ni un motor donde consultar: es el registro por el que viajan los cambios. La idempotencia de esta clase se resuelve en el consumidor, no en él. | El **patrón de bandeja de salida**: cada servicio escribe el cambio y el evento en la misma transacción local, y un conector de captura de cambios lee el registro del motor y lo publica. Así nunca hay un cambio sin evento ni un evento sin cambio, que es el fallo que hunde a las integraciones escritas a mano. | [doc](https://kafka.apache.org/documentation/#semantics) |
| Redis | `SET` es idempotente de forma trivial, así que el caso no enseña nada aquí: escribir dos veces la misma clave con el mismo valor deja el mismo estado por construcción. | Donde sí aporta es como **registro de lotes ya procesados** (`SADD lotes:procesados <id>`), que es la forma más barata de que un reintento no vuelva a aplicar lo que ya se aplicó. | [doc](https://redis.io/docs/latest/commands/sadd/) |

---

## Laboratorio

```bash
python scripts/validate_repository.py
python labs/05-nosql-workloads/run_nosql_lab.py
```

Guarda como evidencia la salida completa, la versión del motor y la semilla o
los parámetros usados. Una captura sin comando no es evidencia: no se puede
repetir.

## Evaluación

| Criterio | Peso | Qué se comprueba |
|---|---:|---|
| Comprensión conceptual | 25 % | Explica el mecanismo, no solo el resultado |
| Ejecución reproducible | 25 % | Otra persona obtiene lo mismo con las instrucciones dadas |
| Interpretación basada en evidencia | 25 % | Cada conclusión se apoya en una salida o una medición |
| Límites y riesgos declarados | 25 % | Dice qué no demuestra el ejercicio y qué faltaría en producción |

La clase se da por superada cuando la respuesta explica el mecanismo, muestra
la salida que la respalda y declara al menos un límite del ejercicio.

## Fuentes de esta clase

Todo lo afirmado arriba procede de estas obras. Los identificadores viven en
[`catalog/sources.json`](../../../catalog/sources.json) y el estado de los
enlaces se comprueba con `python scripts/check_external_links.py`.

- **Jay Kreps** (2013). [The Log: What Every Software Engineer Should Know About Real-Time Data's Unifying Abstraction](https://web.archive.org/web/2023/https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying). LinkedIn Engineering.  
  El registro append-only como nexo entre replicación, integración y streaming. Se cita la copia archivada: LinkedIn retiro el original.
- **Debezium Community** (2026). [Debezium Documentation](https://debezium.io/documentation/).  
  Captura de cambios leyendo el registro de transacciones del motor.
- **dbt Labs** (2026). [dbt Documentation](https://docs.getdbt.com/).  
  Transformaciones versionadas y pruebas de datos en el almacen.
- **Apache Software Foundation** (2026). [Apache Iceberg Documentation](https://iceberg.apache.org/docs/latest/).  
  Formato de tabla con instantaneas y evolución de esquema sobre almacenamiento de objetos.

---

> [Programa](../../../README.md) · [Parte 12](../README.md) · [← Anterior](../../part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) · [Siguiente →](../../part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md)
