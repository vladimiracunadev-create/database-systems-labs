# 035 — Modelado documental: incrustar o referenciar

![🗂️ parte](https://img.shields.io/badge/%F0%9F%97%82%EF%B8%8F%20parte-06-2e8b57?style=flat-square) ![🎚️ nivel](https://img.shields.io/badge/%F0%9F%8E%9A%EF%B8%8F%20nivel-Intermedio-1f6feb?style=flat-square) ![⏱️ duración](https://img.shields.io/badge/%E2%8F%B1%EF%B8%8F%20duraci%C3%B3n-4%20h-24292f?style=flat-square) ![📗 clase](https://img.shields.io/badge/%F0%9F%93%97%20clase-035%20%2F%2074-6e7781?style=flat-square)

> [Programa](../../../README.md) · [Parte 06](../README.md) · [← Anterior](../../part-06-documentos-y-clave-valor/034-el-agregado-como-unidad-de-consistencia/README.md) · [Siguiente →](../../part-06-documentos-y-clave-valor/036-consultas-e-indices-sobre-documentos/README.md)

Parte 06 — Documentos y clave-valor · Intermedio ·
4 horas estimadas · motores `mongodb` · laboratorio
[`labs/05-nosql-workloads`](../../../labs/05-nosql-workloads/README.md) · 3 fuentes.

**Conceptos centrales:** `incrustación` · `referencia` · `crecimiento no acotado` · `patrón de extensión`

**En este caso se comparan 6 motores**: 5 lo resuelven (4 con el resultado comprobado por máquina) y 1 no, con el motivo escrito.

```mermaid
flowchart LR
    C["🗄️ Clase 035"]
    C --> K1["incrustación"]
    C --> K2["referencia"]
    C --> K3["crecimiento no acotado"]
    C --> K4["patrón de extensión"]
    classDef raiz fill:#0b3d2e,stroke:#3fb950,color:#fff
    class C raiz
```

---

## Propósito

Tomar la decisión central del modelado documental —incrustar o referenciar— con criterios medibles, y conocer los patrones que resuelven los casos donde ninguna de las dos basta.

## Resultados de aprendizaje

Al terminar podrás:

1. Aplicar los cuatro criterios de decisión de la documentación de MongoDB.
2. Reconocer y aplicar los patrones de extensión, de subconjunto y de atributo.
3. Detectar el crecimiento no acotado antes de que llegue al límite de tamaño.
4. Modelar relaciones N:M en documentos sin duplicación descontrolada.
5. Justificar cuándo un modelo documental es peor que uno relacional.

## Fundamentos

### Los cuatro criterios

| Criterio | Favorece incrustar | Favorece referenciar |
|---|---|---|
| **Cómo se lee** | Siempre junto al padre | A veces solo, o desde otros padres |
| **Cardinalidad** | Pocos y acotados | Muchos o sin cota |
| **Frecuencia de cambio** | Cambian con el padre | El hijo cambia mucho más |
| **Duplicación** | El hijo pertenece a un solo padre | El hijo es compartido |

Regla resumida de la documentación oficial: *«los datos a los que se accede juntos deben almacenarse juntos»*. El matiz que se olvida: **junto ≠ siempre dentro**. Si se leen juntos pero uno se escribe cien veces más, incrustar obliga a reescribir el padre entero en cada cambio.

### El límite duro

MongoDB limita cada documento a **16 MB**. Con subdocumentos de ~200 bytes, eso son unos 80 000 elementos. Pero el problema práctico llega mucho antes:

- Un arreglo de 5 000 elementos hace que cada lectura del padre transfiera 1 MB aunque se quiera un solo campo.
- Cada actualización de un elemento reescribe el documento; si crece más allá del espacio reservado, se reubica.
- Los índices multiclave generan **una entrada por elemento del arreglo**: un arreglo de 5 000 elementos en 10 000 documentos produce 50 millones de entradas de índice.

Criterio operativo del repositorio: **si el arreglo puede superar unos cientos de elementos, no se incrusta**.

### Los tres patrones que resuelven el 80 % de los casos

**Patrón de extensión (*outlier*)** — la mayoría de los casos son pequeños y unos pocos son enormes:

```json
{"_id": "curso-bd", "inscritos": [ ...40 elementos... ], "tiene_extension": false}
{"_id": "curso-intro", "inscritos": [ ...primeros 100... ], "tiene_extension": true}
```

Los casos normales se resuelven con una lectura; los excepcionales llevan una marca y sus datos adicionales viven en otra colección. Se optimiza el caso común sin romperse en el raro.

**Patrón de subconjunto** — incrustar solo lo que se muestra:

```json
{"_id": "curso-bd", "nombre": "Bases de datos",
 "ultimas_inscripciones": [ {"student_id": 11, "nombre": "Ana"}, ... 5 elementos ... ],
 "total_inscritos": 3812}
```

La portada se sirve con una lectura; el detalle completo consulta la colección de inscripciones. Es la respuesta correcta cuando la interfaz muestra «los últimos N».

**Patrón de atributo** — muchos campos opcionales sobre los que se filtra:

```json
{"_id": "curso-bd",
 "atributos": [{"k": "sala", "v": "B-201"}, {"k": "modalidad", "v": "presencial"}]}
```

Con un único índice sobre `atributos.k` y `atributos.v` se filtra por cualquier atributo. Sin este patrón haría falta un índice por campo posible.

```mermaid
flowchart TD
    R["Relación padre-hijo"] --> C{"¿El hijo se consulta<br/>por sí solo?"}
    C -- "Sí" --> REF["Referenciar"]
    C -- "No" --> N{"¿La cardinalidad<br/>está acotada?"}
    N -- "No" --> SUB{"¿Basta con mostrar<br/>los últimos N?"}
    SUB -- "Sí" --> S["Patrón de subconjunto"]
    SUB -- "No" --> REF
    N -- "Sí" --> F{"¿El hijo cambia mucho<br/>más que el padre?"}
    F -- "Sí" --> REF
    F -- "No" --> O{"¿Hay casos atípicos<br/>enormes?"}
    O -- "Sí" --> EXT["Patrón de extensión"]
    O -- "No" --> EMB["Incrustar"]
```

## Ejemplo trabajado

Dominio: cursos, estudiantes e inscripciones, en MongoDB.

**Modelo 1 — todo incrustado en el curso.** Ya analizado en la clase 024: correcto para cursos pequeños, insostenible para uno con 20 000 inscritos.

**Modelo 2 — copiar el relacional.** Tres colecciones y `$lookup` para reunir. Funciona, pero el motor documental no está optimizado para reuniones: no hay optimizador de orden de reunión ni índices de hash de reunión. Si el modelo necesita `$lookup` en todas las consultas, la pregunta correcta es por qué no se usa un motor relacional.

**Modelo 3 — dirigido por las consultas reales.** Enumeramos primero qué se pregunta:

| Consulta | Frecuencia diaria |
|---|---:|
| Portada del curso: nombre, cupo, total inscritos, últimos 5 | 200 000 |
| Ficha del estudiante: sus cursos con nota | 40 000 |
| Listado completo de inscritos de un curso (paginado) | 3 000 |
| Inscribir | 400 |

Diseño resultante:

```json
// courses
{"_id": "curso-2026-1-bd", "nombre": "Bases de datos", "periodo": "2026-1", "cupo": 40,
 "total_inscritos": 38,
 "ultimas_inscripciones": [{"student_id": 11, "nombre": "Ana Pérez",
                            "en": "2026-03-11T12:00:00Z"}]}

// enrollments
{"_id": {"s": 11, "c": "curso-2026-1-bd"},
 "student_id": 11, "student_nombre": "Ana Pérez",
 "course_id": "curso-2026-1-bd", "course_nombre": "Bases de datos",
 "nota": 6.0, "estado": "activa", "registrada_en": "2026-03-11T12:00:00Z"}
```

Justificación de cada decisión:

- **`_id` compuesto en `enrollments`**: la clave natural garantiza que no haya inscripciones duplicadas. Es la misma clave natural compuesta de la clase 007, aquí como identificador del documento.
- **`student_nombre` y `course_nombre` duplicados**: evitan `$lookup` en la ficha del estudiante y en el listado. Son datos que cambian rarísimamente.
- **`ultimas_inscripciones` acotado a 5**: patrón de subconjunto, mantenido con `$push` + `$slice: -5`.
- **`total_inscritos`**: contador declarado, con su invariante (clase 024).

**El costo de duplicar el nombre.** Si una estudiante cambia de nombre, hay que actualizar sus N inscripciones:

```javascript
db.enrollments.updateMany({student_id: 11}, {$set: {student_nombre: "Ana Rojas"}})
```

Con 8 inscripciones de media, son 8 escrituras por cambio de nombre. Si los cambios de nombre son ~5 al mes y las lecturas que se ahorran el `$lookup` son 40 000 diarias, la aritmética es clara: **40 escrituras mensuales frente a 1,2 millones de reuniones evitadas**. Esa comparación —y no una preferencia estética— es lo que justifica la duplicación.

La misma aritmética con datos que cambian a diario daría el resultado opuesto.

**Índices necesarios:**

```javascript
db.enrollments.createIndex({student_id: 1, registrada_en: -1})
db.enrollments.createIndex({course_id: 1, estado: 1})
db.courses.createIndex({periodo: 1})
```

## Comparación

| Modelo | Lecturas de portada | Reuniones | Riesgo de divergencia | Escala en escritura |
|---|---|---|---|---|
| Todo incrustado | 1 | 0 | Ninguno | Mala |
| Copia del relacional | 1 + `$lookup` | Muchas | Ninguno | Buena |
| Dirigido por consultas | 1 | 0 | Real, acotado y medido | Buena |
| Relacional | 1 con reunión | Optimizadas por el motor | Ninguno | Buena hasta un nodo |

## Errores frecuentes

1. **Incrustar arreglos sin cota.** Se descubre al llegar a 16 MB, con datos ya en producción.
2. **Duplicar datos que cambian a menudo.** La aritmética se invierte y cada cambio propaga N escrituras.
3. **`$lookup` en el camino crítico.** Si es imprescindible, el motor relacional lo hace mejor.
4. **Un índice por campo posible.** Usa el patrón de atributo.
5. **Modelar antes de enumerar las consultas.** En documental, las consultas *son* el modelo.
6. **Olvidar el índice multiclave.** Un arreglo indexado multiplica las entradas por su longitud.

## De la clase a la operación

Cambiar la forma de los documentos con datos en producción exige una migración con lectura tolerante a las dos formas: los documentos antiguos y los nuevos conviven durante semanas. Diseñar previendo esa convivencia —con un campo de versión de esquema— es lo que evita una parada.

## Reto de transferencia

1. Enumera las cinco consultas más frecuentes de tu dominio con su frecuencia real.
2. Diseña el modelo documental que las sirve con una lectura cada una.
3. Calcula la aritmética de duplicación: escrituras añadidas frente a reuniones evitadas.
4. Identifica el arreglo con mayor riesgo de crecimiento y aplícale el patrón que corresponda.

## Preguntas de evaluación

1. ¿Por qué «se leen juntos» no implica «se guardan dentro»?
2. Calcula el punto de equilibrio de duplicar un campo en tu dominio, con cifras reales.
3. Explica el efecto de un arreglo de 5 000 elementos sobre un índice multiclave.
4. Da un caso de tu dominio donde el modelo documental sea peor que el relacional, y justifícalo.

---

## 🌐 El mismo problema en cada motor

**Caso:** Las líneas de un pedido, incrustadas o referenciadas

La decisión central del modelado documental cabe en una pregunta: ¿este dato
vive **dentro** del documento o **al lado**? Y la respuesta no sale del
dominio, sale del patrón de acceso: se incrusta lo que siempre se lee junto
y cambia junto; se referencia lo que se comparte, lo que crece sin límite y
lo que cambia por su cuenta.

El caso pide las líneas del pedido `P-1` con su importe, ordenadas por
producto. Los seis motores devuelven lo mismo; lo que cambia es dónde
estaban guardadas, y el bloque de cada uno muestra la forma que le es
natural. Compararlas es comparar el precio de cada decisión.

Salida esperada, idéntica en todos los motores que lo resuelven:

| producto | importe |
|---|---|
| `cable` | `100` |
| `raton` | `80` |
| `teclado` | `120` |

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase 035`: 4 de
las 5 implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| MongoDB | sí | servicio | [código](implementaciones/mongodb/consulta.js) | [doc oficial](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/) |
| SQLite | sí | núcleo | [código](implementaciones/sqlite/consulta.sql) | [doc oficial](https://sqlite.org/json1.html) |
| DuckDB | sí | núcleo | [código](implementaciones/duckdb/consulta.sql) | [doc oficial](https://duckdb.org/docs/stable/sql/data_types/struct.html) |
| PostgreSQL | sí | servicio | [código](implementaciones/postgresql/consulta.sql) | [doc oficial](https://www.postgresql.org/docs/current/datatype-json.html) |
| Apache CouchDB | sí | declarado | [código](implementaciones/couchdb/consulta.json) | [doc oficial](https://docs.couchdb.org/en/stable/ddocs/views/intro.html) |
| Amazon DynamoDB | **no** | — | — | [doc oficial](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-adjacency-graphs.html) |

### Los que resuelven el caso

#### MongoDB · [`implementaciones/mongodb/consulta.js`](implementaciones/mongodb/consulta.js)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```javascript
// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/
// nota: forma INCRUSTADA. Un documento, un viaje, sin reunion. La forma
//       referenciada seria una coleccion `lineas` con `pedido_id` y un $lookup:
//       correcta cuando las lineas crecen sin techo o se consultan solas.

// === preparacion ===
db.pedidos.drop();
db.pedidos.insertOne({
  _id: "P-1",
  lineas: [
    { producto: "teclado", importe: 120 },
    { producto: "raton", importe: 80 },
    { producto: "cable", importe: 100 },
  ],
});

// === consulta ===
db.pedidos
  .aggregate([
    { $match: { _id: "P-1" } },
    { $unwind: "$lineas" },
    { $project: { _id: 0, producto: "$lineas.producto", importe: "$lineas.importe" } },
    { $sort: { producto: 1 } },
  ])
  .forEach((d) => print(d.producto + "|" + d.importe));
```

- **Por qué sí:** Incrustar es una lectura: un documento, un viaje, sin reunión. Para datos que solo tienen sentido dentro de su padre —las líneas de un pedido— es la forma correcta y la que su propia guía de modelado recomienda.
- **Por qué no:** Deja de serlo en cuanto el arreglo crece sin techo: el documento tiene un límite de 16 MB, y cada actualización reescribe el documento entero aunque solo cambie un elemento del arreglo.
- 📄 Documentación oficial: <https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/>

#### SQLite · [`implementaciones/sqlite/consulta.sql`](implementaciones/sqlite/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: sqlite
-- doc: https://sqlite.org/json1.html
-- nota: forma INCRUSTADA con JSON. Para el motor eso es texto: no hay
--       restricciones sobre su contenido, ni claves foraneas, ni indice que lo
--       recorra. La forma referenciada seria una tabla `lineas` de toda la vida.

-- === preparacion ===
CREATE TABLE pedidos (
    id     TEXT PRIMARY KEY,
    lineas TEXT NOT NULL   -- arreglo JSON incrustado
);

INSERT INTO pedidos (id, lineas) VALUES (
    'P-1',
    '[{"producto":"teclado","importe":120},
      {"producto":"raton","importe":80},
      {"producto":"cable","importe":100}]'
);

-- === consulta ===
SELECT json_extract(l.value, '$.producto') AS producto,
       json_extract(l.value, '$.importe')  AS importe
FROM pedidos p, json_each(p.lineas) l
WHERE p.id = 'P-1'
ORDER BY producto;
```

- **Por qué sí:** Con las funciones JSON integradas se puede incrustar de verdad: el pedido es una fila y sus líneas un arreglo JSON dentro de una columna, que `json_each` desanida cuando hace falta.
- **Por qué no:** Ese arreglo es texto para el motor: no hay restricciones sobre su contenido, ni claves foráneas, ni índice que lo recorra. Se gana la forma documental y se pierde todo lo que hacía valioso al relacional.
- 📄 Documentación oficial: <https://sqlite.org/json1.html>

#### DuckDB · [`implementaciones/duckdb/consulta.sql`](implementaciones/duckdb/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/data_types/struct.html
-- nota: aqui lo anidado no es texto: STRUCT y LIST son tipos con tipo interno
--       declarado, asi que la columna sigue siendo columnar y UNNEST la abre
--       sin analizar ninguna cadena.

-- === preparacion ===
CREATE TABLE pedidos (
    id     VARCHAR PRIMARY KEY,
    lineas STRUCT(producto VARCHAR, importe INTEGER)[]
);

INSERT INTO pedidos VALUES ('P-1', [
    {'producto': 'teclado', 'importe': 120},
    {'producto': 'raton',   'importe': 80},
    {'producto': 'cable',   'importe': 100}
]);

-- === consulta ===
SELECT l.producto, l.importe
FROM (SELECT UNNEST(lineas) AS l FROM pedidos WHERE id = 'P-1')
ORDER BY l.producto;
```

- **Por qué sí:** Tiene tipos anidados de verdad —`STRUCT` y `LIST` con tipos declarados—, así que el documento incrustado sigue siendo columnar y `UNNEST` lo abre sin analizar texto.
- **Por qué no:** Está pensado para leer datos anidados que vienen de otro sitio (Parquet, JSON), no para ser el sistema donde esos documentos se editan a diario.
- 📄 Documentación oficial: <https://duckdb.org/docs/stable/sql/data_types/struct.html>

#### PostgreSQL · [`implementaciones/postgresql/consulta.sql`](implementaciones/postgresql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/datatype-json.html
-- nota: jsonb no guarda texto: guarda una representacion binaria indexable con
--       GIN. Por eso aqui se puede incrustar SIN renunciar al indice, a las
--       transacciones ni a las claves foraneas del resto del esquema.

-- === preparacion ===
DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id     text PRIMARY KEY,
    lineas jsonb NOT NULL
);
CREATE INDEX pedidos_lineas ON pedidos USING GIN (lineas);

INSERT INTO pedidos (id, lineas) VALUES (
    'P-1',
    '[{"producto":"teclado","importe":120},
      {"producto":"raton","importe":80},
      {"producto":"cable","importe":100}]'::jsonb
);

-- === consulta ===
SELECT l->>'producto' AS producto,
       (l->>'importe')::int AS importe
FROM pedidos p
CROSS JOIN LATERAL jsonb_array_elements(p.lineas) AS l
WHERE p.id = 'P-1'
ORDER BY producto;
```

- **Por qué sí:** `jsonb` no guarda texto: guarda una representación binaria indexable con GIN, así que se puede incrustar sin renunciar al índice ni a las transacciones ni a las claves foráneas del resto del esquema. Es la opción que permite decidir tabla por tabla.
- **Por qué no:** Un `UPDATE` sobre un campo del `jsonb` reescribe la fila entera y genera una versión nueva: con documentos grandes y cambios frecuentes, el almacenamiento y el autovacío se resienten.
- 📄 Documentación oficial: <https://www.postgresql.org/docs/current/datatype-json.html>

#### Apache CouchDB · [`implementaciones/couchdb/consulta.json`](implementaciones/couchdb/consulta.json)

⚪ **declarado** — se revisa a mano contra la documentación citada; la máquina no lo ejecuta

```json
{
  "_comentario": [
    "motor: couchdb",
    "doc: https://docs.couchdb.org/en/stable/ddocs/views/intro.html",
    "nota: implementacion declarada. En CouchDB el documento es la unidad de",
    "todo: de lectura, de escritura, de conflicto y de replica. Incrustar no es",
    "una opcion de diseno, es el modelo. Y cualquier consulta que no sea por",
    "identificador exige definir antes una vista con map/reduce.",
    "Se aplica con:  curl -X PUT $COUCH/pedidos/_design/lineas -d @consulta.json",
    "y se consulta:  curl $COUCH/pedidos/_design/lineas/_view/por_producto?key=\"P-1\""
  ],

  "_id": "_design/lineas",
  "language": "javascript",
  "views": {
    "por_producto": {
      "map": "function (doc) { if (doc.type === 'pedido') { doc.lineas.forEach(function (l) { emit([doc._id, l.producto], l.importe); }); } }"
    }
  },

  "_documento_de_ejemplo": {
    "_id": "P-1",
    "type": "pedido",
    "lineas": [
      { "producto": "teclado", "importe": 120 },
      { "producto": "raton", "importe": 80 },
      { "producto": "cable", "importe": 100 }
    ]
  }
}
```

- **Por qué sí:** Lleva la idea al extremo: el documento es la unidad de todo —de lectura, de escritura, de conflicto y de réplica—, así que incrustar no es una opción de diseño sino el modelo. Y su réplica multimaestro está construida sobre esa unidad.
- **Por qué no:** No hay reuniones ni consultas ad hoc eficientes: todo lo que no sea leer por identificador exige definir una vista con `map`/`reduce` de antemano. Referenciar es posible y es incómodo a propósito.
- 📄 Documentación oficial: <https://docs.couchdb.org/en/stable/ddocs/views/intro.html>

### Los que no resuelven este caso — y qué se hace en su lugar

Descartar un motor con un argumento es tan formativo como usarlo. Ninguna de estas filas dice que el motor sea peor: dice que este problema no es el suyo.

| Motor | Por qué no | Qué se hace en su lugar | Fuente |
|---|---|---|---|
| Amazon DynamoDB | Aquí la disyuntiva no se plantea igual: el límite duro de 400 KB por elemento hace que incrustar una lista sin techo sea inviable desde el primer día, y no hay consulta que sirva para descubrirlo tarde. | Diseño de tabla única: el pedido y sus líneas comparten clave de partición (`PEDIDO#P-1`) y se distinguen por la de ordenación (`META`, `LINEA#cable`), de modo que una sola `Query` devuelve el pedido entero sin incrustar nada. | [doc](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-adjacency-graphs.html) |

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

- **MongoDB, Inc.** (2026). [MongoDB: Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/).  
  Criterio para incrustar o referenciar según patrones de acceso.
- **Shannon Bradshaw, Eoin Brazil, Kristina Chodorow** (2019). [MongoDB: The Definitive Guide](https://www.oreilly.com/library/view/mongodb-the-definitive/9781491954454/). 3.a ed. O'Reilly. ISBN 978-1-4919-5446-1.  
  Modelado documental, índices y canalización de agregación.
- **Pramod J. Sadalage, Martin Fowler** (2012). [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html). Addison-Wesley. ISBN 978-0-321-82662-6.  
  Origen del término agregado y de la persistencia políglota que estructura este programa.

---

> [Programa](../../../README.md) · [Parte 06](../README.md) · [← Anterior](../../part-06-documentos-y-clave-valor/034-el-agregado-como-unidad-de-consistencia/README.md) · [Siguiente →](../../part-06-documentos-y-clave-valor/036-consultas-e-indices-sobre-documentos/README.md)
