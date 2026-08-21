# 064 — OLTP frente a OLAP: por qué se separan

> [Programa](../../../README.md) · [Parte 12](../README.md) · [← Anterior](../../part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) · [Siguiente →](../../part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md)

Parte 12 — Analítica, integración y streaming · Intermedio ·
3 horas estimadas · motores `postgresql`, `duckdb`, `clickhouse` · laboratorio
[`labs/04-indexing`](../../../labs/04-indexing/README.md) · 3 fuentes.

**Conceptos centrales:** `carga transaccional` · `carga analítica` · `contención` · `formato de almacenamiento`

**En este caso se comparan 7 motores**: 5 lo resuelven (3 con el resultado comprobado por máquina) y 2 no, con el motivo escrito.

---

## Propósito

Explicar por qué las cargas transaccionales y analíticas se separan, qué pasa cuando no se separan y cuándo esa separación es innecesaria.

## Resultados de aprendizaje

Al terminar podrás:

1. Caracterizar ambas cargas por su patrón de acceso, no por su nombre.
2. Explicar los tres conflictos concretos de ejecutarlas en el mismo motor.
3. Ordenar las opciones de separación por costo creciente.
4. Reconocer cuándo la separación no compensa.
5. Situar HTAP y el enfoque de tabla externa.

## Fundamentos

### Dos cargas, dos formas

| Dimensión | OLTP | OLAP |
|---|---|---|
| Unidad de trabajo | Transacción de pocas filas | Consulta que barre millones |
| Columnas por consulta | Casi todas de pocas filas | Pocas de casi todas las filas |
| Concurrencia | Miles de sesiones | Decenas |
| Latencia objetivo | Milisegundos | Segundos a minutos |
| Escrituras | Continuas, pequeñas | Por lotes |
| Datos | Actuales | Históricos |
| Consistencia | Estricta | Tolera desfase |
| Formato óptimo | Filas | **Columnas** (clase 032) |
| Índices | Muchos, selectivos | Pocos, dispersos |

La incompatibilidad es física, no organizativa: **el mismo dato no puede estar simultáneamente ordenado por filas y por columnas** sin duplicarse.

### Los tres conflictos

**1. Contención de recursos.** Una consulta analítica lee millones de páginas y desaloja el conjunto de trabajo transaccional del buffer. Las consultas OLTP que iban a 2 ms pasan a 20 ms hasta que el caché se recalienta.

**2. Bloqueos y versiones.** En un motor MVCC, una consulta analítica de 40 minutos mantiene una instantánea abierta y **bloquea la recolección de versiones muertas** durante ese tiempo (clase 033). Con 2 000 escrituras/s, son 4,8 millones de versiones acumuladas.

**3. Modelos de datos opuestos.** El esquema normalizado que hace correcto el OLTP obliga a reuniones múltiples en el OLAP. El modelo dimensional que hace rápido el OLAP introduce redundancia inaceptable en el OLTP.

Stonebraker et al. midieron además que un motor OLTP tradicional gasta la mayor parte de sus ciclos en gestión de bloqueos, registro y buffer —trabajo que la carga analítica no necesita en absoluto—.

### Las opciones, de menor a mayor costo

```mermaid
flowchart TD
    A["Consultas analíticas<br/>sobre el OLTP"] --> B{"¿Molestan al<br/>transaccional?"}
    B -- "No" --> OK["No separar.<br/>Es la opción correcta"]
    B -- "Sí" --> C["1. Réplica de solo lectura<br/>mismo motor, mismo esquema"]
    C --> D{"¿Suficiente?"}
    D -- "Sí" --> OK2["Coste: una réplica"]
    D -- "No" --> E["2. Exportar a Parquet<br/>+ DuckDB"]
    E --> F{"¿Suficiente?"}
    F -- "Sí" --> OK3["Coste: un proceso de exportación"]
    F -- "No" --> G["3. Almacén columnar<br/>+ modelo dimensional (clase 055)"]
    G --> H["Coste: sistema, canal,<br/>modelo y equipo"]
```

**La opción 1 resuelve el conflicto 1 y parcialmente el 2**, y no el 3: el esquema sigue siendo el transaccional. Aun así, resuelve la mayoría de los casos reales y cuesta muy poco.

**La opción 2** es la más infravalorada. Una exportación nocturna a Parquet consultada con DuckDB (clase 023) da rendimiento columnar sin ningún servidor nuevo:

```sql
-- Sobre archivos Parquet, sin base de datos analítica
SELECT periodo, count(*), avg(nota)
FROM read_parquet('exportacion/enrollments/*.parquet')
GROUP BY periodo;
```

**La opción 3** se justifica cuando hay varias fuentes que integrar, histórico que conservar más allá del OLTP, o volúmenes que no caben en una máquina.

### Cuándo no separar

Con menos de unos 100 GB y consultas analíticas fuera del horario punta, separar añade un canal que mantener, un desfase que explicar y un sistema que operar, a cambio de poco. La pregunta correcta es **si la carga analítica está degradando la transaccional**, medido, no supuesto.

## Ejemplo trabajado

Plataforma: 5 M de inscripciones, 300 consultas OLTP/s, y un panel de dirección que ejecuta 12 consultas analíticas cada mañana.

**Sin separar, medición:**

```sql
-- panel de dirección, 08:00
SELECT c.periodo, count(*), avg(e.nota),
       count(DISTINCT e.student_id)
FROM enrollments e JOIN courses c ON c.id = e.course_id
GROUP BY c.periodo;
```

```text
Duración:                       47 s
Páginas leídas:                 65 790 (barrido completo)
Efecto medido en el OLTP durante esos 47 s:
  p99 de lectura:  4 ms  →  38 ms
  aciertos de buffer:  99,2 %  →  71,4 %
  filas muertas no recuperables: +94 000
```

El panel funciona. Y durante 47 segundos, cada mañana, todos los usuarios notan la plataforma lenta. **Ese es el conflicto, cuantificado.**

**Opción 1 — réplica de solo lectura:**

```text
El panel consulta la réplica. El OLTP no se entera.
p99 durante el panel: 4 ms (sin cambio)
Coste: una instancia más
Nuevo problema: el retraso de réplica crece a 12 s durante el panel
                → aceptable para un panel; hay que declararlo
```

Para este caso, **aquí termina el problema**. Es la respuesta correcta y cuesta una instancia.

**Opción 2 — exportación a Parquet**, si la réplica no bastara:

```bash
# Exportación nocturna incremental
psql -c "\copy (SELECT * FROM enrollments WHERE registrada_en >= current_date - 1)
         TO PROGRAM 'zstd > exportacion/enrollments/$(date +%F).parquet.zst'"
```

```text
Consulta del panel sobre Parquet con DuckDB:  1,2 s   (frente a 47 s)
Bytes leídos:                                 0,4 GB  (frente a 20 GB)
Coste: un trabajo programado; ningún servidor nuevo
Desfase: hasta 24 h — hay que decidir si es aceptable
```

**Opción 3 — almacén columnar.** Se justificaría si hubiera que cruzar estas inscripciones con datos de facturación y de una plataforma externa, conservar diez años de histórico y servir a veinte analistas. Entonces el modelo dimensional (clase 055) y el canal de integración (clase 056) valen su costo.

**La regla de decisión, con los números de este caso:**

| Opción | Coste operativo | Latencia del panel | Desfase | ¿Resuelve? |
|---|---|---|---|---|
| No separar | 0 | 47 s | 0 | No: degrada el OLTP |
| Réplica | 1 instancia | 47 s | segundos | **Sí** |
| Parquet + DuckDB | 1 trabajo | 1,2 s | horas | Sí, y más rápido |
| Almacén | Sistema + equipo | < 1 s | horas | Sí, y desproporcionado aquí |

### HTAP

Algunos sistemas mantienen ambas representaciones a la vez: filas para el OLTP y un almacén columnar sincronizado para el OLAP (índices columnares de SQL Server, TiFlash de TiDB, `pg_analytics` y similares). Evita el canal de integración a cambio de más recursos y más complejidad interna. Es una opción real, no una promesa, pero no elimina el compromiso: sigue habiendo dos copias del dato en dos formatos.

## Comparación

| Situación | Decisión |
|---|---|
| Consultas analíticas ocasionales, < 100 GB | No separar |
| Panel diario que degrada el OLTP | Réplica de solo lectura |
| Analítica pesada, una sola fuente | Exportar a Parquet + DuckDB |
| Varias fuentes, histórico largo, muchos analistas | Almacén + modelo dimensional |
| Necesidad de analítica sobre datos del segundo | HTAP, con su costo |

## Errores frecuentes

1. **Montar un almacén sin haber medido la degradación.** Coste alto para un problema que quizá no existe.
2. **Consultas analíticas contra el primario.** Contención y bloqueo de la recolección.
3. **Ignorar el retraso de réplica durante el panel.** El panel muestra datos más viejos de lo que cree.
4. **Copiar el esquema OLTP al almacén.** Se hereda la normalización y las reuniones.
5. **Separar y no declarar el desfase.** Dos cifras distintas y nadie sabe cuál es la buena.
6. **Suponer que HTAP elimina el compromiso.** Lo esconde, no lo elimina.

## De la clase a la operación

La conversación productiva no es «¿necesitamos un almacén de datos?», sino «¿cuánto degrada el OLTP nuestra carga analítica, y cuál es la opción más barata que lo resuelve?». Medir primero convierte una decisión de arquitectura en una decisión con evidencia.

## Reto de transferencia

1. Mide el p99 del OLTP con y sin la carga analítica en ejecución.
2. Cuantifica el efecto sobre el buffer y sobre las versiones no recuperables.
3. Prueba la opción 2 exportando a Parquet y consultando con DuckDB.
4. Justifica con cifras qué opción elegirías y qué desfase declararías.

## Preguntas de evaluación

1. Explica los tres conflictos con datos de tu propio sistema.
2. ¿Por qué una consulta analítica larga impide recuperar versiones muertas?
3. ¿En qué caso la exportación a Parquet supera a una réplica de solo lectura?
4. Da una situación donde no separar sea la decisión correcta, y defiéndela.

---

## 🌐 El mismo problema en cada motor

**Caso:** Cuatro números que resumen doce meses, y la consulta contraria que ningún motor sirve igual de bien

Las dos cargas piden cosas opuestas. La **transaccional** toca una fila con
todas sus columnas, muchas veces por segundo, y necesita que la escritura sea
inmediata y duradera. La **analítica** toca todas las filas de pocas
columnas, unas cuantas veces al día, y necesita leer mucho y rápido.

Un mismo almacenamiento no puede estar optimizado para las dos, y de ahí
salen las dos consecuencias que organizan esta parte del programa: que
existan dos sistemas, y que haga falta un proceso que copie del primero al
segundo.

El caso es la consulta analítica en su forma mínima: doce meses de ventas
resumidos en cuatro trimestres. Todos los motores la responden; el «por qué
no» de cada uno dice qué se rompe cuando se le pide además la otra.

Salida esperada, idéntica en todos los motores que lo resuelven:

| trimestre | importe |
|---|---|
| `T1` | `600` |
| `T2` | `1500` |
| `T3` | `2400` |
| `T4` | `3300` |

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase 064`: 3 de
las 5 implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| DuckDB | sí | núcleo | [código](implementaciones/duckdb/consulta.sql) | [doc oficial](https://duckdb.org/docs/stable/why_duckdb) |
| ClickHouse | sí | declarado | [código](implementaciones/clickhouse/consulta.sql) | [doc oficial](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree) |
| PostgreSQL | sí | servicio | [código](implementaciones/postgresql/consulta.sql) | [doc oficial](https://www.postgresql.org/docs/current/rules-materializedviews.html) |
| SQLite | sí | núcleo | [código](implementaciones/sqlite/consulta.sql) | [doc oficial](https://sqlite.org/whentouse.html) |
| Google BigQuery | sí | declarado | [código](implementaciones/bigquery/consulta.sql) | [doc oficial](https://cloud.google.com/bigquery/docs/introduction) |
| MongoDB | **no** | — | — | [doc oficial](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/) |
| Redis | **no** | — | — | [doc oficial](https://redis.io/docs/latest/commands/hincrby/) |

### Los que resuelven el caso

#### DuckDB · [`implementaciones/duckdb/consulta.sql`](implementaciones/duckdb/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/why_duckdb
-- nota: el lado ANALITICO. Lee dos columnas y ninguna mas, vectorizadas. Y la
--       misma consulta funciona sobre el fichero exportado por el sistema
--       transaccional, sin cargarlo:
--         SELECT ... FROM 'ventas.parquet' GROUP BY ...

-- === preparacion ===
CREATE TABLE ventas (
    id      INTEGER PRIMARY KEY,
    mes     INTEGER NOT NULL,
    importe INTEGER NOT NULL
);
INSERT INTO ventas (id, mes, importe) VALUES
    (1, 1, 100), (2, 2, 200), (3, 3, 300),
    (4, 4, 400), (5, 5, 500), (6, 6, 600),
    (7, 7, 700), (8, 8, 800), (9, 9, 900),
    (10, 10, 1000), (11, 11, 1100), (12, 12, 1200);

-- === consulta ===
-- Una consulta ANALITICA: toca TODAS las filas, POCAS columnas, y devuelve
-- cuatro numeros. La transaccional seria la contraria —«dame la venta 7»— y
-- toca UNA fila con TODAS sus columnas.
-- El mismo motor no puede estar optimizado para las dos cosas, y esa es la
-- razon de que existan dos sistemas y un proceso que copia de uno a otro.
SELECT CASE WHEN mes <= 3 THEN 'T1'
            WHEN mes <= 6 THEN 'T2'
            WHEN mes <= 9 THEN 'T3'
            ELSE 'T4'
       END AS trimestre,
       SUM(importe) AS importe
FROM ventas
GROUP BY trimestre
ORDER BY trimestre;
```

- **Por qué sí:** Es analítico puro y embebido: lee solo las columnas `mes` e `importe`, las procesa vectorizadas y no necesita servidor. Para el análisis local sobre una copia de los datos, no hay nada más directo.
- **Por qué no:** Un solo escritor y sin concurrencia entre procesos: no puede ser el sistema donde se registran las ventas, solo donde se analizan.
- 📄 Documentación oficial: <https://duckdb.org/docs/stable/why_duckdb>

#### ClickHouse · [`implementaciones/clickhouse/consulta.sql`](implementaciones/clickhouse/consulta.sql)

⚪ **declarado** — se revisa a mano contra la documentación citada; la máquina no lo ejecuta

```sql
-- motor: clickhouse
-- doc: https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree
-- nota: implementacion declarada. Aqui el informe trimestral no se calcula: se
--       lee ya calculado, porque la vista materializada agrega AL INSERTAR.
--       El precio: no es transaccional, y corregir una venta mal registrada no
--       es un UPDATE sino una mutacion asincrona que reescribe partes.

-- === preparacion ===
CREATE TABLE ventas (
    id      UInt32,
    mes     UInt8,
    importe UInt32
) ENGINE = MergeTree ORDER BY (mes, id);

CREATE MATERIALIZED VIEW ventas_por_trimestre
ENGINE = SummingMergeTree ORDER BY trimestre
AS SELECT concat('T', toString(intDiv(mes - 1, 3) + 1)) AS trimestre,
          SUM(importe) AS importe
FROM ventas GROUP BY trimestre;

INSERT INTO ventas VALUES
    (1, 1, 100), (2, 2, 200), (3, 3, 300), (4, 4, 400), (5, 5, 500), (6, 6, 600),
    (7, 7, 700), (8, 8, 800), (9, 9, 900), (10, 10, 1000), (11, 11, 1100), (12, 12, 1200);

-- === consulta ===
SELECT trimestre, SUM(importe) AS importe
FROM ventas_por_trimestre
GROUP BY trimestre
ORDER BY trimestre;
```

- **Por qué sí:** La misma arquitectura columnar a escala distribuida, con vistas materializadas que agregan **al insertar**: el informe trimestral no se calcula, se lee ya calculado.
- **Por qué no:** No es transaccional y las modificaciones fila a fila son mutaciones asíncronas: corregir una venta mal registrada no es un `UPDATE`, es una operación de mantenimiento.
- 📄 Documentación oficial: <https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree>

#### PostgreSQL · [`implementaciones/postgresql/consulta.sql`](implementaciones/postgresql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/rules-materializedviews.html
-- nota: el punto intermedio, y el que muchas arquitecturas no necesitan
--       abandonar. Con una vista materializada, el informe deja de recalcularse:
--         CREATE MATERIALIZED VIEW ventas_por_trimestre AS SELECT ...;
--         REFRESH MATERIALIZED VIEW CONCURRENTLY ventas_por_trimestre;
--       A cambio de que el dato vaya con el retraso del ultimo refresco.

-- === preparacion ===
DROP TABLE IF EXISTS ventas;

CREATE TABLE ventas (
    id      integer PRIMARY KEY,
    mes     integer NOT NULL,
    importe integer NOT NULL
);
INSERT INTO ventas (id, mes, importe) VALUES
    (1, 1, 100), (2, 2, 200), (3, 3, 300),
    (4, 4, 400), (5, 5, 500), (6, 6, 600),
    (7, 7, 700), (8, 8, 800), (9, 9, 900),
    (10, 10, 1000), (11, 11, 1100), (12, 12, 1200);

-- === consulta ===
-- Una consulta ANALITICA: toca TODAS las filas, POCAS columnas, y devuelve
-- cuatro numeros. La transaccional seria la contraria —«dame la venta 7»— y
-- toca UNA fila con TODAS sus columnas.
-- El mismo motor no puede estar optimizado para las dos cosas, y esa es la
-- razon de que existan dos sistemas y un proceso que copia de uno a otro.
SELECT CASE WHEN mes <= 3 THEN 'T1'
            WHEN mes <= 6 THEN 'T2'
            WHEN mes <= 9 THEN 'T3'
            ELSE 'T4'
       END AS trimestre,
       SUM(importe) AS importe
FROM ventas
GROUP BY trimestre
ORDER BY trimestre;
```

- **Por qué sí:** Es el punto donde muchas arquitecturas empiezan y donde muchas deberían quedarse: con agregación paralela y vistas materializadas resuelve la analítica de tamaño medio **sobre los datos operativos**, sin proceso de copia, sin retraso y sin un sistema más.
- **Por qué no:** El informe compite por la misma caché y las mismas conexiones que las transacciones. Un análisis pesado a la hora punta degrada las ventas, y esa es exactamente la razón por la que se separan las dos cargas.
- 📄 Documentación oficial: <https://www.postgresql.org/docs/current/rules-materializedviews.html>

#### SQLite · [`implementaciones/sqlite/consulta.sql`](implementaciones/sqlite/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: sqlite
-- doc: https://sqlite.org/whentouse.html
-- nota: el lado TRANSACCIONAL de la comparacion. La consulta contraria —la que
--       este motor sirve mejor que ningun columnar— es esta:
--         SELECT * FROM ventas WHERE id = 7;
--       una fila, todas sus columnas, una sola pagina leida.

-- === preparacion ===
CREATE TABLE ventas (
    id      INTEGER PRIMARY KEY,
    mes     INTEGER NOT NULL,
    importe INTEGER NOT NULL
);
INSERT INTO ventas (id, mes, importe) VALUES
    (1, 1, 100), (2, 2, 200), (3, 3, 300),
    (4, 4, 400), (5, 5, 500), (6, 6, 600),
    (7, 7, 700), (8, 8, 800), (9, 9, 900),
    (10, 10, 1000), (11, 11, 1100), (12, 12, 1200);

-- === consulta ===
-- Una consulta ANALITICA: toca TODAS las filas, POCAS columnas, y devuelve
-- cuatro numeros. La transaccional seria la contraria —«dame la venta 7»— y
-- toca UNA fila con TODAS sus columnas.
-- El mismo motor no puede estar optimizado para las dos cosas, y esa es la
-- razon de que existan dos sistemas y un proceso que copia de uno a otro.
SELECT CASE WHEN mes <= 3 THEN 'T1'
            WHEN mes <= 6 THEN 'T2'
            WHEN mes <= 9 THEN 'T3'
            ELSE 'T4'
       END AS trimestre,
       SUM(importe) AS importe
FROM ventas
GROUP BY trimestre
ORDER BY trimestre;
```

- **Por qué sí:** Sirve para ver el contraste desde el lado transaccional: el mismo SQL, el mismo resultado, y un almacenamiento por filas que tiene que leer los doce registros completos para sumar una columna.
- **Por qué no:** Con doce filas da igual; con doce millones, la diferencia es de órdenes de magnitud, y no hay índice que la arregle porque hay que leerlas todas.
- 📄 Documentación oficial: <https://sqlite.org/whentouse.html>

#### Google BigQuery · [`implementaciones/bigquery/consulta.sql`](implementaciones/bigquery/consulta.sql)

⚪ **declarado** — se revisa a mano contra la documentación citada; la máquina no lo ejecuta

```sql
-- motor: bigquery
-- doc: https://cloud.google.com/bigquery/docs/introduction
-- nota: implementacion declarada. No hay servidor, ni indices, ni ajuste: solo
--       consultas y una factura. Se paga por BYTES LEIDOS, asi que esta
--       consulta cuesta dos columnas; con SELECT * costaria la tabla entera y
--       devolveria lo mismo.
--         bq query --dry_run   dice cuantos bytes antes de cobrarlos.

-- === preparacion ===
CREATE OR REPLACE TABLE analitica.ventas AS
SELECT n AS id, n AS mes, n * 100 AS importe
FROM UNNEST(GENERATE_ARRAY(1, 12)) AS n;

-- === consulta ===
SELECT CONCAT('T', CAST(DIV(mes - 1, 3) + 1 AS STRING)) AS trimestre,
       SUM(importe) AS importe
FROM analitica.ventas
GROUP BY trimestre
ORDER BY trimestre;
```

- **Por qué sí:** Elimina la operación por completo: no hay servidor, ni índices, ni ajuste; solo consultas y una factura. Para un informe trimestral sobre volúmenes grandes y esporádicos, es la opción con menos trabajo humano.
- **Por qué no:** Es exclusivamente analítico: no admite escrituras fila a fila con latencia baja, y la inserción en flujo tiene su propio costo y sus propias reglas. Nunca es la otra mitad de la pareja.
- 📄 Documentación oficial: <https://cloud.google.com/bigquery/docs/introduction>

### Los que no resuelven este caso — y qué se hace en su lugar

Descartar un motor con un argumento es tan formativo como usarlo. Ninguna de estas filas dice que el motor sea peor: dice que este problema no es el suyo.

| Motor | Por qué no | Qué se hace en su lugar | Fuente |
|---|---|---|---|
| MongoDB | Puede resolver la consulta con `$group`, pero no aporta una fila distinta a esta comparación: su almacenamiento es orientado a documentos, así que agregar obliga a leer documentos completos, igual que SQLite lee filas completas. | Exportar a un almacén columnar para la analítica —o usar los servicios analíticos que su propio proveedor ofrece— y dejar la colección para lo transaccional, que es su terreno. | [doc](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/) |
| Redis | No hay agregación sobre un conjunto de registros: habría que traerse las doce ventas al cliente y sumarlas allí. Con doce da igual; con doce millones, no hay conversación. | Mantener los totales por trimestre como contadores actualizados en cada venta: el informe está siempre listo y solo responde la pregunta que se decidió de antemano. | [doc](https://redis.io/docs/latest/commands/hincrby/) |

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

- **Michael Stonebraker, Samuel Madden, Daniel J. Abadi, Stavros Harizopoulos, Nabil Hachem, Pat Helland** (2007). [The End of an Architectural Era (It's Time for a Complete Rewrite)](https://cs.brown.edu/courses/cs227/archives/2008/Papers/OLTP/hstore.pdf). VLDB.  
  Mide en qué gasta el tiempo realmente un motor OLTP tradicional.
- **Ralph Kimball, Margy Ross** (2013). [The Data Warehouse Toolkit](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/). 3.a ed. Wiley. ISBN 978-1-118-53080-1.  
  Modelado dimensional, tablas de hechos y dimensiones de cambio lento.
- **DuckDB Foundation** (2026). [DuckDB Documentation](https://duckdb.org/docs/).  
  Motor analítico embebido: OLAP columnar sin servidor.

---

> [Programa](../../../README.md) · [Parte 12](../README.md) · [← Anterior](../../part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) · [Siguiente →](../../part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md)
