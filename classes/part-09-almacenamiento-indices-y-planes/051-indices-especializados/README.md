# 051 — Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes

> [Programa](../../../README.md) · [Parte 09](../README.md) · [← Anterior](../../part-09-almacenamiento-indices-y-planes/050-lsm-tree-compactacion-y-amplificacion/README.md) · [Siguiente →](../../part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md)

Parte 09 — Almacenamiento, índices y planes · Avanzado ·
3 horas estimadas · motores `postgresql` · laboratorio
[`labs/04-indexing`](../../../labs/04-indexing/README.md) · 3 fuentes.

**Conceptos centrales:** `índice parcial` · `índice de expresión` · `GIN` · `BRIN` · `costo de mantenimiento`

**En este caso se comparan 7 motores**: 5 lo resuelven (5 con el resultado comprobado por máquina) y 2 no, con el motivo escrito.

---

## Propósito

Salir del B-Tree. Hay consultas —contención de arreglos, texto, rangos, geometría, tablas enormes correlacionadas— para las que existe una estructura mucho mejor, y saber cuál evita rediseños innecesarios.

## Resultados de aprendizaje

Al terminar podrás:

1. Elegir el tipo de índice según el operador de la consulta.
2. Diseñar índices parciales y calcular su ahorro.
3. Usar índices de expresión y saber cuándo son obligatorios.
4. Explicar cuándo BRIN supera a B-Tree por dos órdenes de magnitud en tamaño.
5. Medir el costo de mantenimiento de cada índice.

## Fundamentos

### El catálogo

| Tipo | Operadores que acelera | Tamaño | Uso típico |
|---|---|---|---|
| **B-Tree** | `=`, `<`, `>`, `BETWEEN`, `LIKE 'p%'`, `ORDER BY` | Medio | Todo lo ordenable |
| **Hash** | Solo `=` | Menor que B-Tree | Igualdad pura sobre claves anchas |
| **GIN** | `@>`, `?`, `@@`, `&&` (arreglos, `jsonb`, texto) | Grande | Contención y búsqueda de texto |
| **GiST** | `&&`, `<@`, `<->` (rangos, geometría, vecino más cercano) | Medio | Rangos, geografía, exclusión |
| **SP-GiST** | Estructuras no equilibradas | Medio | Redes, cuadtrees |
| **BRIN** | `<`, `>`, `BETWEEN` con datos correlacionados | **Diminuto** | Tablas enormes ordenadas por inserción |

La pregunta que guía la elección no es «qué columna» sino **«qué operador»**. `WHERE etiquetas @> ARRAY['sql']` no lo acelera ningún B-Tree, por bien que se elija la columna.

### BRIN: el índice que cabe en un suspiro

Un índice de rango de bloques guarda, por cada grupo de páginas (128 por defecto), el valor mínimo y máximo. No localiza filas: **descarta bloques**.

```text
Tabla de 100 GB con 13 millones de páginas
B-Tree sobre una columna:   ~3 GB
BRIN con pages_per_range=128: ~100 000 rangos × ~32 B ≈ 3 MB
```

**Mil veces más pequeño.** Funciona solo si los datos están **físicamente correlacionados** con la columna: típicamente una marca de tiempo en una tabla donde se inserta en orden cronológico.

```sql
CREATE INDEX eventos_brin ON eventos USING brin (ocurrido_en);
SELECT attname, correlation FROM pg_stats WHERE tablename = 'eventos';
-- correlación cercana a 1 o -1 → BRIN es viable
```

Con correlación 0,99, BRIN descarta casi todos los bloques. Con correlación 0,1 —por ejemplo tras muchas actualizaciones que reubican filas— es inútil.

### Índice parcial

Indexa solo las filas que cumplen un predicado.

```sql
CREATE INDEX enr_pendientes ON enrollments (course_id, registrada_en)
WHERE estado = 'pendiente';
```

Dos condiciones para que se use: la consulta debe incluir un predicado que **implique** el del índice, y el planificador debe poder demostrarlo. `WHERE estado = 'pendiente'` sirve; `WHERE estado <> 'activa'` no, aunque lógicamente lo incluya.

Uso frecuente y elegante: excluir los nulos.

```sql
CREATE INDEX t_ref ON t (referencia) WHERE referencia IS NOT NULL;
```

### Índice de expresión

```sql
-- NO usa un índice sobre email:
SELECT * FROM students WHERE lower(email) = 'ana@ejemplo.cl';

CREATE INDEX students_email_lower ON students (lower(email));   -- ahora sí
```

Regla general: **cualquier función aplicada a la columna en el `WHERE` inutiliza el índice ordinario**. Incluye `date(created_at)`, `substr(codigo, 1, 3)` y las conversiones implícitas de tipo, que son las más difíciles de ver.

### Exclusión

Restricción declarativa que impide solapamientos, imposible con `UNIQUE`:

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE reservas ADD CONSTRAINT sin_solape
  EXCLUDE USING gist (sala_id WITH =, durante WITH &&);
```

`durante` es un `tstzrange`. El motor rechaza cualquier reserva que solape en la misma sala. Es la solución declarativa a un problema que casi siempre se resuelve —mal— en la aplicación.

```mermaid
flowchart TD
    O["¿Qué operador usa<br/>la consulta?"] --> E{"="}
    E -- "columna corta" --> BT["B-Tree"]
    E -- "columna larga, solo igualdad" --> H["Hash"]
    O --> R{"< > BETWEEN"}
    R -- "tabla mediana" --> BT
    R -- "tabla enorme correlacionada" --> BR["BRIN"]
    O --> C{"@> ? @@<br/>arreglos, jsonb, texto"} --> G["GIN"]
    O --> S{"&& <@ <-><br/>rangos, geometría"} --> GI["GiST"]
    BT --> P{"¿Solo interesa un<br/>subconjunto de filas?"}
    P -- "Sí" --> PA["+ índice parcial"]
    O --> F{"¿Función sobre<br/>la columna?"} --> EX["Índice de expresión<br/>(obligatorio)"]
```

## Ejemplo trabajado

Tabla `eventos`: 500 millones de filas, 180 GB, insertada en orden cronológico.

```sql
CREATE TABLE eventos (
  id          BIGSERIAL PRIMARY KEY,
  ocurrido_en TIMESTAMPTZ NOT NULL,
  tipo        TEXT NOT NULL,
  etiquetas   TEXT[] NOT NULL DEFAULT '{}',
  carga       JSONB NOT NULL,
  procesado   BOOLEAN NOT NULL DEFAULT false
);
```

**Consulta A — rango temporal:**

```sql
SELECT * FROM eventos WHERE ocurrido_en BETWEEN '2026-08-01' AND '2026-08-02';
```

| Índice | Tamaño | Bloques leídos |
|---|---:|---|
| B-Tree sobre `ocurrido_en` | ~11 GB | Precisos, pero el índice no cabe en memoria |
| BRIN sobre `ocurrido_en` | **~15 MB** | Los del rango + algunos de más |

Con correlación 0,999, BRIN descarta el 99,7 % de los bloques leyendo un índice que cabe entero en caché. **Mil veces menos espacio y prácticamente el mismo resultado.**

**Consulta B — etiquetas:**

```sql
SELECT * FROM eventos WHERE etiquetas @> ARRAY['error','pago'];
CREATE INDEX eventos_etiquetas ON eventos USING gin (etiquetas);
```

Ningún B-Tree sirve aquí: el operador de contención no es de orden.

**Consulta C — pendientes de procesar:**

```sql
SELECT * FROM eventos WHERE procesado = false ORDER BY ocurrido_en LIMIT 100;
```

`procesado` es booleana: un B-Tree sobre ella no se usaría. Pero solo el 0,01 % está pendiente:

```sql
CREATE INDEX eventos_pendientes ON eventos (ocurrido_en) WHERE procesado = false;
```

```text
índice completo sobre (procesado, ocurrido_en): 500 000 000 entradas ≈ 15 GB
índice parcial:                                      50 000 entradas ≈  1,5 MB
```

Cuatro órdenes de magnitud. Y además: cuando un evento se marca como procesado, **sale** del índice, que se mantiene pequeño para siempre. Es el patrón canónico de la cola de trabajo.

**Consulta D — dentro del `jsonb`:**

```sql
SELECT * FROM eventos WHERE carga @> '{"cliente_id": 42}';
CREATE INDEX eventos_carga ON eventos USING gin (carga jsonb_path_ops);
```

`jsonb_path_ops` indexa solo el operador de contención: índice más pequeño y rápido que el GIN por defecto, a cambio de soportar menos operadores.

**El costo total, que hay que sumar:**

| Índice | Tamaño | Coste por inserción |
|---|---:|---|
| Clave primaria B-Tree | 11 GB | Bajo (clave creciente) |
| BRIN `ocurrido_en` | 15 MB | Casi nulo |
| GIN `etiquetas` | 8 GB | **Alto**: una entrada por elemento |
| Parcial `pendientes` | 1,5 MB | Solo si `procesado = false` |
| GIN `carga` | 22 GB | **Muy alto** |

Los índices GIN son los que más encarecen la escritura. PostgreSQL mitiga con `fastupdate`, que acumula en una lista pendiente y la fusiona después; el efecto secundario es que una consulta puede tener que recorrer esa lista.

## Comparación

| Consulta | Índice correcto |
|---|---|
| `WHERE a = 1 AND b > 2` | B-Tree `(a, b)` |
| `WHERE etiquetas @> ARRAY[...]` | GIN |
| `WHERE rango && '[...]'` | GiST |
| `WHERE ts BETWEEN ...` en tabla enorme ordenada | BRIN |
| `WHERE lower(x) = ...` | Expresión |
| `WHERE estado = 'raro'` | Parcial |
| `WHERE doc @> '{...}'` | GIN `jsonb_path_ops` |
| Sin solapamiento | `EXCLUDE USING gist` |

## Errores frecuentes

1. **B-Tree por defecto para todo.** No sirve para contención ni para solapamiento.
2. **BRIN sin comprobar la correlación.** Sin ella no descarta nada.
3. **Función sobre la columna sin índice de expresión.** El índice existente no se usa.
4. **Índice parcial con un predicado que la consulta no implica.** No se usará.
5. **GIN sobre columnas de escritura intensa.** Encarece mucho la inserción.
6. **No revisar el uso.** `idx_scan = 0` significa costo sin beneficio.

## De la clase a la operación

Cambiar un B-Tree de 15 GB por un índice parcial de 1,5 MB no es una micro-optimización: cambia qué cabe en memoria, y con ello el comportamiento de todo el sistema. Es de las intervenciones con mejor relación entre esfuerzo y efecto.

## Reto de transferencia

1. Inventaría los índices de tu base con su tamaño y su número de barridos.
2. Busca una consulta con función sobre la columna y crea el índice de expresión.
3. Identifica una tabla con columna correlacionada y compara B-Tree con BRIN.
4. Convierte un índice completo en parcial y mide el ahorro.

## Preguntas de evaluación

1. ¿Qué condición debe cumplir la tabla para que BRIN sea útil, y cómo se comprueba?
2. Explica por qué `WHERE date(creado) = '2026-08-01'` no usa el índice sobre `creado`.
3. Da una consulta de tu dominio que solo un GIN pueda acelerar.
4. Calcula el ahorro de convertir en parcial uno de tus índices, con cifras reales.

---

## 🌐 El mismo problema en cada motor

**Caso:** Indexar solo lo que se consulta: los dos pedidos pendientes de seis

El índice B-Tree completo no siempre es la respuesta. Cuando la consulta
caliente mira **una fracción pequeña** de la tabla —los pedidos pendientes,
las filas no borradas, los usuarios activos—, un índice parcial indexa solo
esas filas: ocupa una fracción, se mantiene en una fracción de las
escrituras y cabe entero en memoria.

El caso tiene seis pedidos de los que dos están pendientes, y pide esos dos
ordenados por fecha. El resultado es trivial; lo que se compara es qué
índice puede construir cada motor para responderlo sin tocar los otros
cuatro, y qué hacen los que no tienen índices parciales.

Salida esperada, idéntica en todos los motores que lo resuelven:

| pedido | fecha |
|---|---|
| `P-2` | `2026-08-02` |
| `P-5` | `2026-08-05` |

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase 051`: 5 de
las 5 implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| PostgreSQL | sí | servicio | [código](implementaciones/postgresql/consulta.sql) | [doc oficial](https://www.postgresql.org/docs/current/indexes-types.html) |
| SQLite | sí | núcleo | [código](implementaciones/sqlite/consulta.sql) | [doc oficial](https://sqlite.org/partialindex.html) |
| MySQL | sí | servicio | [código](implementaciones/mysql/consulta.sql) | [doc oficial](https://dev.mysql.com/doc/refman/8.4/en/create-index.html) |
| MongoDB | sí | servicio | [código](implementaciones/mongodb/consulta.js) | [doc oficial](https://www.mongodb.com/docs/manual/core/index-partial/) |
| DuckDB | sí | núcleo | [código](implementaciones/duckdb/consulta.sql) | [doc oficial](https://duckdb.org/docs/stable/sql/indexes.html) |
| Apache Cassandra | **no** | — | — | [doc oficial](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/indexing/2i/2i-usage.html) |
| Redis | **no** | — | — | [doc oficial](https://redis.io/docs/latest/commands/zadd/) |

### Los que resuelven el caso

#### PostgreSQL · [`implementaciones/postgresql/consulta.sql`](implementaciones/postgresql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/indexes-types.html
-- nota: el indice de abajo es PARCIAL y ademas CUBRIENTE: con INCLUDE (id), el
--       plan pasa a «Index Only Scan» y no toca la tabla en ningun momento.
--       El resto del catalogo, para tenerlo a la vista:
--         GIN   arreglos, jsonb, busqueda de texto
--         GiST  geometria, rangos, vecino mas cercano
--         BRIN  tablas enormes ya ordenadas por la columna (fechas, series)
--         HASH  solo igualdad, sin orden ni rangos

-- === preparacion ===
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id     text PRIMARY KEY,
    estado text NOT NULL,
    fecha  text NOT NULL
);
INSERT INTO pedidos (id, estado, fecha) VALUES
    ('P-1', 'entregado', '2026-08-01'),
    ('P-2', 'pendiente', '2026-08-02'),
    ('P-3', 'entregado', '2026-08-03'),
    ('P-4', 'entregado', '2026-08-04'),
    ('P-5', 'pendiente', '2026-08-05'),
    ('P-6', 'entregado', '2026-08-06');

CREATE INDEX pedidos_pendientes ON pedidos (fecha) INCLUDE (id)
    WHERE estado = 'pendiente';

-- === consulta ===
SELECT id AS pedido, fecha
FROM pedidos
WHERE estado = 'pendiente'
ORDER BY fecha;
```

- **Por qué sí:** Tiene el catálogo más completo y cada tipo resuelve un problema distinto: **parcial** para subconjuntos, `INCLUDE` para cubrir la consulta sin ir a la tabla, **GIN** para arreglos y texto, **GiST** para geometría y rangos, **BRIN** para tablas enormes y ordenadas por naturaleza, y **hash** para igualdad pura.
- **Por qué no:** Elegir mal es fácil y sale caro: BRIN sobre datos desordenados no descarta nada, hash no sirve para rangos ni para ordenar, y cada índice de más se paga en cada escritura. Y un índice parcial solo se usa si el planificador puede **demostrar** que la consulta implica su predicado.
- 📄 Documentación oficial: <https://www.postgresql.org/docs/current/indexes-types.html>

#### SQLite · [`implementaciones/sqlite/consulta.sql`](implementaciones/sqlite/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: sqlite
-- doc: https://sqlite.org/partialindex.html
-- nota: el indice tiene DOS entradas, no seis. En una tabla de diez millones de
--       pedidos con mil pendientes, la diferencia entre el indice completo y el
--       parcial es de cuatro ordenes de magnitud, y el parcial cabe en memoria.
--       Para comprobar que se usa: EXPLAIN QUERY PLAN delante de la consulta.

-- === preparacion ===
CREATE TABLE pedidos (
    id     TEXT PRIMARY KEY,
    estado TEXT NOT NULL,
    fecha  TEXT NOT NULL
);
INSERT INTO pedidos (id, estado, fecha) VALUES
    ('P-1', 'entregado', '2026-08-01'),
    ('P-2', 'pendiente', '2026-08-02'),
    ('P-3', 'entregado', '2026-08-03'),
    ('P-4', 'entregado', '2026-08-04'),
    ('P-5', 'pendiente', '2026-08-05'),
    ('P-6', 'entregado', '2026-08-06');

CREATE INDEX pedidos_pendientes ON pedidos (fecha) WHERE estado = 'pendiente';

-- === consulta ===
SELECT id AS pedido, fecha
FROM pedidos
WHERE estado = 'pendiente'
ORDER BY fecha;
```

- **Por qué sí:** Tiene índices parciales y por expresión, que es casi todo lo que hace falta: el índice de los pendientes ocupa dos entradas en vez de seis, y en una tabla real la diferencia es de órdenes de magnitud.
- **Por qué no:** No hay GIN, ni GiST, ni BRIN, ni cubrientes explícitos: para buscar dentro de un JSON o por geometría hay que extraer a una columna e indexar esa, o recurrir a extensiones como R-Tree.
- 📄 Documentación oficial: <https://sqlite.org/partialindex.html>

#### MySQL · [`implementaciones/mysql/consulta.sql`](implementaciones/mysql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/create-index.html
-- nota: MySQL NO tiene indices parciales. El rodeo estandar es una columna
--       generada que vale NULL en las filas que no interesan —los NULL no
--       ocupan entrada util en el arbol— e indexarla junto a la fecha. Funciona,
--       y hay que explicarlo cada vez que alguien lee el esquema.

-- === preparacion ===
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id     VARCHAR(10) PRIMARY KEY,
    estado VARCHAR(20) NOT NULL,
    fecha  VARCHAR(10) NOT NULL,
    fecha_pendiente VARCHAR(10)
        AS (IF(estado = 'pendiente', fecha, NULL)) STORED,
    KEY pedidos_pendientes (fecha_pendiente)
) ENGINE=InnoDB;

INSERT INTO pedidos (id, estado, fecha) VALUES
    ('P-1', 'entregado', '2026-08-01'),
    ('P-2', 'pendiente', '2026-08-02'),
    ('P-3', 'entregado', '2026-08-03'),
    ('P-4', 'entregado', '2026-08-04'),
    ('P-5', 'pendiente', '2026-08-05'),
    ('P-6', 'entregado', '2026-08-06');

-- === consulta ===
SELECT id AS pedido, fecha
FROM pedidos
WHERE estado = 'pendiente'
ORDER BY fecha;
```

- **Por qué sí:** Tiene índices por prefijo —útiles en columnas de texto largas—, multivaluados sobre JSON y espaciales con R-Tree, y su optimizador aplica «índice cubriente» cuando el índice contiene todas las columnas pedidas.
- **Por qué no:** **No tiene índices parciales**. La única forma de acercarse es una columna generada que valga `NULL` para las filas que no interesan e indexarla, un rodeo que hay que explicar cada vez que alguien lo lee.
- 📄 Documentación oficial: <https://dev.mysql.com/doc/refman/8.4/en/create-index.html>

#### MongoDB · [`implementaciones/mongodb/consulta.js`](implementaciones/mongodb/consulta.js)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```javascript
// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/index-partial/
// nota: el indice parcial solo se usa si la consulta INCLUYE su predicado. Si
//       la consulta pidiera { estado: { $in: ["pendiente", "enviado"] } }, el
//       motor no puede demostrar que implica el filtro del indice y lo ignora
//       en silencio: no hay aviso, solo una consulta mas lenta.

// === preparacion ===
db.pedidos.drop();
db.pedidos.insertMany([
  { _id: "P-1", estado: "entregado", fecha: "2026-08-01" },
  { _id: "P-2", estado: "pendiente", fecha: "2026-08-02" },
  { _id: "P-3", estado: "entregado", fecha: "2026-08-03" },
  { _id: "P-4", estado: "entregado", fecha: "2026-08-04" },
  { _id: "P-5", estado: "pendiente", fecha: "2026-08-05" },
  { _id: "P-6", estado: "entregado", fecha: "2026-08-06" },
]);
db.pedidos.createIndex(
  { fecha: 1 },
  { partialFilterExpression: { estado: "pendiente" } },
);

// === consulta ===
db.pedidos
  .find({ estado: "pendiente" }, { _id: 1, fecha: 1 })
  .sort({ fecha: 1 })
  .forEach((d) => print(d._id + "|" + d.fecha));
```

- **Por qué sí:** `partialFilterExpression` es el índice parcial con otro nombre, y además tiene índices dispersos, TTL, geoespaciales, de texto y hasta con recolección diferida (`hidden`) para probar si un índice hace falta antes de borrarlo.
- **Por qué no:** Un índice parcial solo se usa si la consulta **incluye** su predicado: si la consulta pide `estado: "pendiente"` y el índice se creó sobre `estado: {$eq: "pendiente"}`, la coincidencia tiene que ser exacta o el índice se ignora en silencio.
- 📄 Documentación oficial: <https://www.mongodb.com/docs/manual/core/index-partial/>

#### DuckDB · [`implementaciones/duckdb/consulta.sql`](implementaciones/duckdb/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/indexes.html
-- nota: aqui no se crea ningun indice, y es a proposito. Cada grupo de filas
--       guarda el minimo y el maximo de cada columna, asi que descartar bloques
--       enteros es gratis: es la idea de BRIN aplicada por omision a todo.
--       Con una condicion: los datos tienen que estar ORDENADOS por la columna
--       que se filtra. Si no, no se descarta nada.

-- === preparacion ===
CREATE TABLE pedidos (
    id     VARCHAR PRIMARY KEY,
    estado VARCHAR NOT NULL,
    fecha  VARCHAR NOT NULL
);
INSERT INTO pedidos (id, estado, fecha) VALUES
    ('P-1', 'entregado', '2026-08-01'),
    ('P-2', 'pendiente', '2026-08-02'),
    ('P-3', 'entregado', '2026-08-03'),
    ('P-4', 'entregado', '2026-08-04'),
    ('P-5', 'pendiente', '2026-08-05'),
    ('P-6', 'entregado', '2026-08-06');

-- === consulta ===
SELECT id AS pedido, fecha
FROM pedidos
WHERE estado = 'pendiente'
ORDER BY fecha;
```

- **Por qué sí:** Está aquí para mostrar la alternativa a los índices: no los necesita porque cada grupo de filas guarda los valores mínimo y máximo de cada columna, así que descartar bloques enteros es gratis. Es la misma idea que BRIN, aplicada por omisión a todo.
- **Por qué no:** Esa técnica solo funciona si los datos están **ordenados** por la columna que se filtra: sobre datos desordenados no descarta nada, exactamente igual que un BRIN mal usado.
- 📄 Documentación oficial: <https://duckdb.org/docs/stable/sql/indexes.html>

### Los que no resuelven este caso — y qué se hace en su lugar

Descartar un motor con un argumento es tan formativo como usarlo. Ninguna de estas filas dice que el motor sea peor: dice que este problema no es el suyo.

| Motor | Por qué no | Qué se hace en su lugar | Fuente |
|---|---|---|---|
| Apache Cassandra | Su índice secundario es local a cada nodo, así que una consulta por él pregunta a todo el anillo. Y sobre una columna de baja cardinalidad como `estado`, cada nodo devolvería muchísimas filas: es el antipatrón documentado. | Una tabla `pedidos_pendientes` con `estado` como clave de partición y la fecha como agrupamiento, alimentada por la aplicación y vaciada al entregar: el índice parcial construido a mano. | [doc](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/indexing/2i/2i-usage.html) |
| Redis | No hay índices que crear sobre datos ya escritos: la estructura de acceso se decide al escribir y no hay forma de añadir otra después sin recorrer todo el espacio de claves. | Un conjunto ordenado `pedidos:pendientes` con la fecha como puntuación, del que se saca el pedido al entregarlo. Es literalmente un índice parcial mantenido a mano, con la ventaja de que se lee en microsegundos y el inconveniente de que hay que acordarse de mantenerlo. | [doc](https://redis.io/docs/latest/commands/zadd/) |

---

## Laboratorio

```bash
python scripts/validate_repository.py
python labs/04-indexing/run_indexing_lab.py
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

- **PostgreSQL Global Development Group** (2026). [PostgreSQL: Indexes](https://www.postgresql.org/docs/current/indexes.html).  
  B-tree, hash, GiST, SP-GiST, GIN y BRIN con sus casos de uso.
- **Markus Winand** (2012). [SQL Performance Explained](https://use-the-index-luke.com/). Markus Winand. ISBN 978-3-9503078-2-5.  
  Versión web gratuita. Índices B-Tree y su relación con el orden de las columnas.
- **Egor Rogov** (2022). [PostgreSQL 14 Internals](https://postgrespro.com/community/books/internals). Postgres Professional. ISBN 978-5-6041193-2-8.  
  PDF gratuito. MVCC, vacuum, buffers, índices y planificador sobre el código real.

---

> [Programa](../../../README.md) · [Parte 09](../README.md) · [← Anterior](../../part-09-almacenamiento-indices-y-planes/050-lsm-tree-compactacion-y-amplificacion/README.md) · [Siguiente →](../../part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md)
