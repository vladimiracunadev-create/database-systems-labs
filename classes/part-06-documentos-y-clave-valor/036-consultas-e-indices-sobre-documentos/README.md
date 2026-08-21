# 036 — Consultas, índices y agregación sobre documentos

> [Programa](../../../README.md) · [Parte 06](../README.md) · [← Anterior](../../part-06-documentos-y-clave-valor/035-modelado-documental-incrustar-o-referenciar/README.md) · [Siguiente →](../../part-06-documentos-y-clave-valor/037-clave-valor-cache-y-expiracion/README.md)

Parte 06 — Documentos y clave-valor · Intermedio ·
3 horas estimadas · motores `mongodb` · laboratorio
[`labs/05-nosql-workloads`](../../../labs/05-nosql-workloads/README.md) · 3 fuentes.

**Conceptos centrales:** `índice compuesto` · `canalización de agregación` · `índice multiclave` · `cobertura`

**En este caso se comparan 7 motores**: 6 lo resuelven (4 con el resultado comprobado por máquina) y 1 no, con el motivo escrito.

---

## Propósito

Consultar documentos con la misma disciplina que se consulta SQL: sabiendo qué índice se usa, cuántos documentos se examinan y por qué una etapa de la canalización es cara.

## Resultados de aprendizaje

Al terminar podrás:

1. Leer un plan de MongoDB y distinguir `COLLSCAN` de `IXSCAN`.
2. Aplicar la regla ESR para ordenar las claves de un índice compuesto.
3. Reconocer una consulta cubierta y qué la habilita.
4. Ordenar las etapas de una canalización de agregación para reducir el trabajo.
5. Prever el efecto de los índices multiclave y parciales.

## Fundamentos

### Leer el plan

```javascript
db.enrollments.find({course_id: "curso-bd", estado: "activa"})
              .explain("executionStats")
```

Los tres números que importan:

| Campo | Significa | Objetivo |
|---|---|---|
| `nReturned` | Documentos devueltos | — |
| `totalKeysExamined` | Entradas de índice leídas | Cercano a `nReturned` |
| `totalDocsExamined` | Documentos leídos | Cercano a `nReturned`; **0** si la consulta está cubierta |

Diagnóstico rápido: si `totalDocsExamined` es mucho mayor que `nReturned`, falta índice o el que hay no sirve. Es el mismo razonamiento de selectividad de la clase 039, con otro vocabulario.

### La regla ESR

Para un índice compuesto, el orden de las claves debe ser:

1. **E**quality — campos comparados por igualdad.
2. **S**ort — campos por los que se ordena.
3. **R**ange — campos comparados por rango.

```javascript
db.enrollments.find({course_id: "curso-bd", nota: {$gte: 4.0}}).sort({registrada_en: -1})
db.enrollments.createIndex({course_id: 1, registrada_en: -1, nota: 1})
//                          E              S                  R
```

Poner el rango antes que el orden obliga al motor a ordenar en memoria el resultado del rango. Es la misma razón por la que en un B-Tree relacional el rango «rompe» el uso de las columnas siguientes (clase 039): una vez que se recorre un intervalo, las claves posteriores ya no están ordenadas globalmente.

### Consulta cubierta

Si todos los campos que la consulta necesita —filtro, orden y proyección— están en el índice, el motor no toca los documentos:

```javascript
db.enrollments.find({course_id: "curso-bd"}, {_id: 0, student_id: 1, nota: 1})
db.enrollments.createIndex({course_id: 1, student_id: 1, nota: 1})
// totalDocsExamined: 0
```

Hay que excluir `_id` explícitamente si no está en el índice, porque se devuelve por omisión.

### Tipos de índice

| Tipo | Para qué | Cuidado |
|---|---|---|
| Simple / compuesto | Lo habitual | Orden ESR |
| **Multiclave** | Campo que es un arreglo | Una entrada por elemento; solo un campo de arreglo por índice |
| **Parcial** | Subconjunto de documentos | Solo se usa si la consulta implica el filtro del índice |
| **TTL** | Expiración automática | Borra en segundo plano, con retraso |
| Texto | Búsqueda léxica básica | Uno por colección; para búsqueda seria, parte 06 |

### Canalización de agregación

El orden de las etapas determina cuánto trabajo se hace:

```javascript
// MAL: agrupa 5 millones y luego descarta
db.enrollments.aggregate([
  {$group: {_id: "$course_id", promedio: {$avg: "$nota"}}},
  {$match: {_id: "curso-bd"}}
])

// BIEN: filtra primero, con índice
db.enrollments.aggregate([
  {$match: {course_id: "curso-bd", estado: "activa"}},
  {$group: {_id: "$course_id", promedio: {$avg: "$nota"}}}
])
```

Es la equivalencia E2 de la clase 011 —empujar el filtro— aplicada a mano. El optimizador de MongoDB reordena algunos casos, pero no todos: cualquier etapa que calcule campos nuevos (`$addFields`, `$project`) bloquea el movimiento de las etapas posteriores.

Regla: **`$match` y `$limit` lo antes posible; `$lookup` y `$unwind` lo más tarde posible.**

```mermaid
flowchart LR
    M["$match<br/>usa índice"] --> S["$sort<br/>usa índice si sigue al match"]
    S --> L["$limit"]
    L --> P["$project<br/>reduce el tamaño"]
    P --> G["$group<br/>en memoria"]
    G --> LK["$lookup<br/>lo más tarde posible"]
```

## Ejemplo trabajado

Consulta: *«las 20 inscripciones activas más recientes del curso, con nota, ordenadas por fecha»*, sobre 5 millones de documentos.

**Sin índice adecuado:**

```javascript
db.enrollments.find({course_id: "curso-bd", estado: "activa"})
              .sort({registrada_en: -1}).limit(20).explain("executionStats")
```

```text
stage:                COLLSCAN
totalDocsExamined:    5 000 000
totalKeysExamined:    0
nReturned:            20
executionTimeMillis:  4 210
SORT: in-memory, 38 MB    ← cerca del límite de 100 MB
```

Cinco millones de documentos leídos para devolver 20. Además el ordenamiento se hace en memoria; superados los 100 MB, MongoDB aborta la consulta salvo que se permita el uso de disco.

**Con índice ESR:**

```javascript
db.enrollments.createIndex({course_id: 1, estado: 1, registrada_en: -1})
```

```text
stage:                IXSCAN → FETCH → LIMIT
totalKeysExamined:    20
totalDocsExamined:    20
nReturned:            20
executionTimeMillis:  1
SORT: ninguno    ← el índice ya entrega el orden
```

De 5 000 000 a 20 documentos examinados. La desaparición de la etapa `SORT` es tan importante como la reducción de lecturas: el índice ya está ordenado por `registrada_en` dentro de cada `(course_id, estado)`.

**Hacerla cubierta.** Si la interfaz solo necesita `student_id` y `nota`:

```javascript
db.enrollments.createIndex({course_id: 1, estado: 1, registrada_en: -1, student_id: 1, nota: 1})
db.enrollments.find({course_id: "curso-bd", estado: "activa"},
                    {_id: 0, student_id: 1, nota: 1, registrada_en: 1})
              .sort({registrada_en: -1}).limit(20)
// totalDocsExamined: 0
```

El índice es más ancho —más espacio y más costo por escritura— y a cambio la consulta no toca la colección. Compensa cuando esa consulta domina el tráfico; no compensa si es una de veinte.

**Índice parcial.** Si el 90 % de las inscripciones están activas, un índice parcial no aporta mucho. Si solo el 5 % está en estado `pendiente` y esa es la consulta caliente:

```javascript
db.enrollments.createIndex({course_id: 1, registrada_en: -1},
                           {partialFilterExpression: {estado: "pendiente"}})
```

El índice pasa de 5 millones de entradas a 250 000: cabe en memoria y se mantiene más barato. Requisito: la consulta debe incluir `estado: "pendiente"` explícitamente, o el motor no puede usarlo.

## Comparación

| Situación | Señal en el plan | Corrección |
|---|---|---|
| Sin índice útil | `COLLSCAN` | Crear índice siguiendo ESR |
| Índice mal ordenado | `IXSCAN` + `SORT` en memoria | Reordenar claves |
| Muchos documentos por resultado | `totalDocsExamined ≫ nReturned` | Añadir campos del filtro al índice |
| Proyección pequeña y repetida | `totalDocsExamined > 0` | Índice cubriente |
| Filtro muy selectivo y raro | Índice enorme | Índice parcial |

## Errores frecuentes

1. **Un índice por campo.** Los índices compuestos sirven a más consultas; el motor rara vez combina dos índices con eficacia.
2. **Ignorar el orden ESR.** Provoca ordenamientos en memoria y el límite de 100 MB.
3. **`$lookup` al principio de la canalización.** Multiplica el trabajo de todas las etapas siguientes.
4. **Índices que nadie usa.** Revisa `$indexStats`; cada índice se mantiene en cada escritura.
5. **Índice multiclave sobre arreglos largos.** Multiplica las entradas por la longitud del arreglo.
6. **Olvidar `_id: 0` en una consulta que se quiere cubierta.** Basta para que deje de serlo.

## De la clase a la operación

El síntoma habitual —«MongoDB se puso lento al crecer»— casi siempre significa que los índices dejaron de caber en memoria. Vigilar el tamaño total de los índices frente a la RAM disponible es más predictivo que cualquier métrica de CPU.

## Reto de transferencia

1. Toma la consulta más frecuente de tu dominio y captura su `explain` sin índice.
2. Diseña el índice con la regla ESR y vuelve a capturar.
3. Conviértela en consulta cubierta y compara los tres números del plan.
4. Mide el tamaño de los índices con `$indexStats` y elimina los que no se usan.

## Preguntas de evaluación

1. ¿Por qué el rango va al final en la regla ESR?
2. ¿Qué condiciones exactas debe cumplir una consulta cubierta?
3. Explica el efecto de un `$lookup` colocado antes de un `$match` selectivo.
4. Da un caso de tu dominio donde un índice parcial reduzca el tamaño más de un 80 %.

---

## 🌐 El mismo problema en cada motor

**Caso:** Cuánto se vendió por categoría, con las líneas dentro de los documentos

Agregar sobre documentos obliga a hacer algo que en una tabla no hace falta:
**desanidar** antes de agrupar. Las líneas viven dentro del pedido, así que
primero hay que abrirlas en filas y después sumarlas por categoría.

El caso parte de dos pedidos con sus líneas incrustadas y pide el importe
total por categoría, ordenado alfabéticamente. La comparación deja a la
vista dos cosas: que la tubería de agregación de MongoDB y una consulta SQL
sobre `jsonb` son la misma idea con distinta sintaxis, y que el índice que
hace rápida esta consulta no es el mismo en los dos.

Salida esperada, idéntica en todos los motores que lo resuelven:

| categoria | importe |
|---|---|
| `accesorios` | `180` |
| `perifericos` | `120` |

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase 036`: 4 de
las 6 implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| MongoDB | sí | servicio | [código](implementaciones/mongodb/consulta.js) | [doc oficial](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/) |
| PostgreSQL | sí | servicio | [código](implementaciones/postgresql/consulta.sql) | [doc oficial](https://www.postgresql.org/docs/current/functions-json.html) |
| SQLite | sí | núcleo | [código](implementaciones/sqlite/consulta.sql) | [doc oficial](https://sqlite.org/json1.html) |
| DuckDB | sí | núcleo | [código](implementaciones/duckdb/consulta.sql) | [doc oficial](https://duckdb.org/docs/stable/sql/query_syntax/unnest.html) |
| OpenSearch | sí | declarado | [código](implementaciones/opensearch/consulta.json) | [doc oficial](https://docs.opensearch.org/latest/aggregations/bucket/terms/) |
| Apache CouchDB | sí | declarado | [código](implementaciones/couchdb/consulta.json) | [doc oficial](https://docs.couchdb.org/en/stable/ddocs/views/intro.html) |
| Redis | **no** | — | — | [doc oficial](https://redis.io/docs/latest/commands/hincrby/) |

### Los que resuelven el caso

#### MongoDB · [`implementaciones/mongodb/consulta.js`](implementaciones/mongodb/consulta.js)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```javascript
// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
// nota: el indice multiclave sobre lineas.categoria acelera el FILTRO, no el
//       $group: agrupar siempre recorre los documentos que pasen el filtro, con
//       un limite de 100 MB por etapa salvo que se permita usar disco.

// === preparacion ===
db.pedidos.drop();
db.pedidos.insertMany([
  { _id: "P-1", lineas: [
    { producto: "teclado", categoria: "perifericos", importe: 120 },
    { producto: "raton", categoria: "accesorios", importe: 80 },
  ] },
  { _id: "P-2", lineas: [
    { producto: "cable", categoria: "accesorios", importe: 100 },
  ] },
]);
db.pedidos.createIndex({ "lineas.categoria": 1 });

// === consulta ===
db.pedidos
  .aggregate([
    { $unwind: "$lineas" },
    { $group: { _id: "$lineas.categoria", importe: { $sum: "$lineas.importe" } } },
    { $sort: { _id: 1 } },
  ])
  .forEach((d) => print(d._id + "|" + d.importe));
```

- **Por qué sí:** `$unwind` seguido de `$group` es la forma canónica, y `explain("executionStats")` dice si la etapa inicial usó índice o recorrió la colección. Con un índice multiclave sobre `lineas.categoria`, el filtro previo se resuelve sin abrir los documentos que no interesan.
- **Por qué no:** El índice ayuda a **filtrar**, no a agrupar: el `$group` siempre procesa documento a documento en memoria, con el límite de 100 MB por etapa. Para agregaciones grandes hay que permitir disco o precalcular.
- 📄 Documentación oficial: <https://www.mongodb.com/docs/manual/core/aggregation-pipeline/>

#### PostgreSQL · [`implementaciones/postgresql/consulta.sql`](implementaciones/postgresql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/functions-json.html
-- nota: lo que aqui se puede hacer y en un almacen documental puro no: esta
--       misma consulta podria reunir los documentos con tablas normales del
--       mismo esquema, en la misma transaccion.

-- === preparacion ===
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id     text PRIMARY KEY,
    lineas jsonb NOT NULL
);
CREATE INDEX pedidos_lineas ON pedidos USING GIN (lineas);

INSERT INTO pedidos (id, lineas) VALUES
    ('P-1', '[{"producto":"teclado","categoria":"perifericos","importe":120},
              {"producto":"raton","categoria":"accesorios","importe":80}]'::jsonb),
    ('P-2', '[{"producto":"cable","categoria":"accesorios","importe":100}]'::jsonb);

-- === consulta ===
SELECT l->>'categoria' AS categoria,
       SUM((l->>'importe')::int) AS importe
FROM pedidos p
CROSS JOIN LATERAL jsonb_array_elements(p.lineas) AS l
GROUP BY l->>'categoria'
ORDER BY categoria;
```

- **Por qué sí:** `jsonb_array_elements` desanida y el `GROUP BY` de siempre agrupa: la misma consulta puede reunir documentos con tablas normales, que es justamente lo que un almacén documental puro no puede hacer.
- **Por qué no:** El índice GIN acelera la búsqueda dentro del `jsonb`, pero no evita desanidar en la agregación; y cada elemento extraído se convierte de texto a número en tiempo de consulta, lo que en volúmenes grandes se nota.
- 📄 Documentación oficial: <https://www.postgresql.org/docs/current/functions-json.html>

#### SQLite · [`implementaciones/sqlite/consulta.sql`](implementaciones/sqlite/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: sqlite
-- doc: https://sqlite.org/json1.html
-- nota: json_each se comporta como una tabla virtual, asi que desanidar y
--       agrupar se escribe como cualquier otra consulta. Lo que no hay es
--       indice: esto recorre la tabla entera siempre.

-- === preparacion ===
CREATE TABLE pedidos (
    id     TEXT PRIMARY KEY,
    lineas TEXT NOT NULL
);

INSERT INTO pedidos (id, lineas) VALUES
    ('P-1', '[{"producto":"teclado","categoria":"perifericos","importe":120},
              {"producto":"raton","categoria":"accesorios","importe":80}]'),
    ('P-2', '[{"producto":"cable","categoria":"accesorios","importe":100}]');

-- === consulta ===
SELECT json_extract(l.value, '$.categoria') AS categoria,
       SUM(json_extract(l.value, '$.importe')) AS importe
FROM pedidos p, json_each(p.lineas) l
GROUP BY categoria
ORDER BY categoria;
```

- **Por qué sí:** `json_each` se comporta como una tabla virtual, así que desanidar y agrupar se escribe como cualquier otra consulta: sirve para entender el mecanismo sin levantar nada.
- **Por qué no:** No hay ningún índice posible sobre el contenido del JSON salvo que se extraiga a una columna generada e indexada: toda agregación recorre la tabla completa.
- 📄 Documentación oficial: <https://sqlite.org/json1.html>

#### DuckDB · [`implementaciones/duckdb/consulta.sql`](implementaciones/duckdb/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/unnest.html
-- nota: la misma consulta funciona sobre un fichero anidado sin cargarlo:
--         SELECT ... FROM read_json_auto('pedidos.json'), UNNEST(lineas) ...

-- === preparacion ===
CREATE TABLE pedidos (
    id     VARCHAR PRIMARY KEY,
    lineas STRUCT(producto VARCHAR, categoria VARCHAR, importe INTEGER)[]
);

INSERT INTO pedidos VALUES
    ('P-1', [{'producto': 'teclado', 'categoria': 'perifericos', 'importe': 120},
             {'producto': 'raton',   'categoria': 'accesorios',  'importe': 80}]),
    ('P-2', [{'producto': 'cable',   'categoria': 'accesorios',  'importe': 100}]);

-- === consulta ===
SELECT l.categoria, SUM(l.importe) AS importe
FROM (SELECT UNNEST(lineas) AS l FROM pedidos)
GROUP BY l.categoria
ORDER BY l.categoria;
```

- **Por qué sí:** `UNNEST` sobre tipos anidados nativos y agregación vectorizada: es el motor donde esta forma de consulta escala mejor sin cambiar de sintaxis, y puede leer directamente un fichero JSON o Parquet anidado.
- **Por qué no:** No hay índices que valgan aquí: la velocidad viene de leer menos columnas, no de saltar filas. Si la consulta filtra por un valor muy selectivo, un motor con índice gana.
- 📄 Documentación oficial: <https://duckdb.org/docs/stable/sql/query_syntax/unnest.html>

#### OpenSearch · [`implementaciones/opensearch/consulta.json`](implementaciones/opensearch/consulta.json)

⚪ **declarado** — se revisa a mano contra la documentación citada; la máquina no lo ejecuta

```json
{
  "_comentario": [
    "motor: opensearch",
    "doc: https://docs.opensearch.org/latest/aggregations/bucket/terms/",
    "nota: implementacion declarada. Para que el desanidado sea CORRECTO, el",
    "arreglo `lineas` tiene que estar mapeado como `nested`; si no, OpenSearch",
    "aplana los campos y pierde la correlacion entre categoria e importe de la",
    "misma linea. Ese mapeo convierte cada linea en un documento oculto con su",
    "propio costo de indexacion.",
    "Se aplica con:  PUT /pedidos  con el bloque `mappings`",
    "y se consulta:  POST /pedidos/_search  con el bloque `busqueda`"
  ],

  "mappings": {
    "properties": {
      "lineas": {
        "type": "nested",
        "properties": {
          "producto": { "type": "keyword" },
          "categoria": { "type": "keyword" },
          "importe": { "type": "integer" }
        }
      }
    }
  },

  "busqueda": {
    "size": 0,
    "aggs": {
      "lineas": {
        "nested": { "path": "lineas" },
        "aggs": {
          "por_categoria": {
            "terms": { "field": "lineas.categoria", "order": { "_key": "asc" } },
            "aggs": { "importe": { "sum": { "field": "lineas.importe" } } }
          }
        }
      }
    }
  }
}
```

- **Por qué sí:** Las agregaciones por término son su especialidad: calcula el total por categoría sobre millones de documentos en milisegundos, porque el índice invertido y los `doc_values` columnares ya tienen los datos agrupados por valor.
- **Por qué no:** Para que el desanidado sea correcto hay que declarar `nested`, y eso convierte cada línea en un documento oculto con su propio costo de indexación; sin `nested`, los campos del arreglo se aplanan y las correlaciones entre ellos se pierden.
- 📄 Documentación oficial: <https://docs.opensearch.org/latest/aggregations/bucket/terms/>

#### Apache CouchDB · [`implementaciones/couchdb/consulta.json`](implementaciones/couchdb/consulta.json)

⚪ **declarado** — se revisa a mano contra la documentación citada; la máquina no lo ejecuta

```json
{
  "_comentario": [
    "motor: couchdb",
    "doc: https://docs.couchdb.org/en/stable/ddocs/views/intro.html",
    "nota: implementacion declarada. La vista se calcula de forma INCREMENTAL al",
    "escribir y se guarda en un arbol B, asi que la consulta solo lee el",
    "resultado ya agregado. El precio: hay que decidir la agregacion antes de",
    "necesitarla, y una pregunta nueva es una vista nueva sobre toda la base.",
    "Se consulta con: _view/por_categoria?group=true"
  ],

  "_id": "_design/ventas",
  "language": "javascript",
  "views": {
    "por_categoria": {
      "map": "function (doc) { if (doc.type === 'pedido') { doc.lineas.forEach(function (l) { emit(l.categoria, l.importe); }); } }",
      "reduce": "_sum"
    }
  }
}
```

- **Por qué sí:** Su modelo de vistas `map`/`reduce` está pensado exactamente para esto: el resultado se calcula de forma incremental al escribir, así que la consulta solo lee un árbol B ya agregado.
- **Por qué no:** Hay que decidir la agregación **antes** de necesitarla: una pregunta nueva es una vista nueva que hay que construir sobre toda la base. No existe la consulta ad hoc.
- 📄 Documentación oficial: <https://docs.couchdb.org/en/stable/ddocs/views/intro.html>

### Los que no resuelven este caso — y qué se hace en su lugar

Descartar un motor con un argumento es tan formativo como usarlo. Ninguna de estas filas dice que el motor sea peor: dice que este problema no es el suyo.

| Motor | Por qué no | Qué se hace en su lugar | Fuente |
|---|---|---|---|
| Redis | No hay desanidado ni agrupación: los documentos serían cadenas opacas y todo el cálculo tendría que hacerse en el cliente después de traérselos. | Mantener el total por categoría en un hash actualizado con `HINCRBY` en cada venta: el resultado está siempre listo, y a cambio solo responde la pregunta que se decidió de antemano. | [doc](https://redis.io/docs/latest/commands/hincrby/) |

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

- **MongoDB, Inc.** (2026). [MongoDB Manual](https://www.mongodb.com/docs/manual/).  
  Modelo documental, índices, agregación y transacciones multi-documento.
- **Shannon Bradshaw, Eoin Brazil, Kristina Chodorow** (2019). [MongoDB: The Definitive Guide](https://www.oreilly.com/library/view/mongodb-the-definitive/9781491954454/). 3.a ed. O'Reilly. ISBN 978-1-4919-5446-1.  
  Modelado documental, índices y canalización de agregación.
- **Markus Winand** (2012). [SQL Performance Explained](https://use-the-index-luke.com/). Markus Winand. ISBN 978-3-9503078-2-5.  
  Versión web gratuita. Índices B-Tree y su relación con el orden de las columnas.

---

> [Programa](../../../README.md) · [Parte 06](../README.md) · [← Anterior](../../part-06-documentos-y-clave-valor/035-modelado-documental-incrustar-o-referenciar/README.md) · [Siguiente →](../../part-06-documentos-y-clave-valor/037-clave-valor-cache-y-expiracion/README.md)
