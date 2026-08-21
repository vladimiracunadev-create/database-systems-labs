# 020 — La relación como conjunto: tuplas, dominios y acceso por valor

> [Programa](../../../README.md) · [Parte 03](../README.md) · [← Anterior](../../part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md) · [Siguiente →](../../part-03-modelo-relacional-y-algebra/021-algebra-relacional-operadores/README.md)

Parte 03 — Modelo relacional y álgebra · Fundamentos ·
3 horas estimadas · motores `postgresql`, `sqlite` · laboratorio
[`labs/01-sql-foundations`](../../../labs/01-sql-foundations/README.md) · 3 fuentes.

**Conceptos centrales:** `relación` · `tupla` · `dominio` · `acceso por valor` · `cierre`

**En este caso se comparan 5 motores**: 5 lo resuelven (5 con el resultado comprobado por máquina) y 0 no, con el motivo escrito.

---

## Propósito

Precisar qué es una relación en el sentido de Codd y en qué se aparta SQL de esa definición. Muchos comportamientos «raros» de SQL —duplicados, orden, nulos— se explican exactamente por ahí.

## Resultados de aprendizaje

Al terminar podrás:

1. Definir relación, tupla, atributo y dominio sin recurrir a «tabla», «fila» y «columna».
2. Enumerar las cuatro propiedades de una relación que SQL no respeta.
3. Explicar el acceso por valor y por qué excluye punteros y posiciones.
4. Justificar la propiedad de cierre y qué habilita.
5. Detectar en código propio dependencias del orden físico.

## Fundamentos

### La definición

Dada una lista de dominios `D1, …, Dn`, una **relación** es un subconjunto del producto cartesiano `D1 × … × Dn`. De ahí, por ser un conjunto matemático, se siguen cuatro propiedades:

| Propiedad | Significado | ¿SQL la respeta? |
|---|---|---|
| Sin tuplas duplicadas | Un conjunto no repite elementos | **No.** Una tabla sin clave admite filas idénticas |
| Sin orden entre tuplas | Un conjunto no está ordenado | **No del todo:** `ORDER BY` produce una lista, no una relación |
| Sin orden entre atributos | Se accede por nombre | **No.** `SELECT *` y `INSERT` sin lista de columnas dependen de la posición |
| Valores atómicos del dominio | Cada celda es un valor del dominio | **Parcialmente.** Admite nulos, que no pertenecen a ningún dominio |

Date insiste en que SQL implementa «tablas», no relaciones: una tabla es un multiconjunto (*bag*) con orden de columnas. Todas las sorpresas de la parte 03 —`UNION` frente a `UNION ALL`, `COUNT(*)` frente a `COUNT(col)`, el resultado de `NOT IN` con nulos— derivan de esa distancia.

### Acceso por valor

Codd exige que todo dato sea localizable por la terna **(nombre de relación, valor de clave, nombre de atributo)**. Nunca por posición física ni por puntero.

Consecuencias que se usan a diario:

- Se puede reorganizar el almacenamiento sin tocar consultas (independencia física, clase 003).
- Se puede replicar y particionar sin cambiar la semántica.
- No existe «la tercera fila»: sin `ORDER BY` no hay tercera fila, y con `ORDER BY` sobre una columna no única tampoco está determinada.

### Cierre

Todo operador relacional recibe relaciones y devuelve una relación. Eso permite componer sin límite: el resultado de una consulta puede ser la entrada de otra. En SQL se manifiesta en las subconsultas, las CTE y las vistas. Es lo que hace que el lenguaje sea composicional en lugar de un catálogo de comandos.

```mermaid
flowchart LR
    subgraph M["Modelo relacional (Codd)"]
        R1["Relación: conjunto"] --> P1["sin duplicados"]
        R1 --> P2["sin orden"]
        R1 --> P3["acceso por valor"]
        R1 --> P4["cierre"]
    end
    subgraph S["SQL (implementación)"]
        T1["Tabla: multiconjunto"] --> Q1["admite duplicados"]
        T1 --> Q2["orden observable"]
        T1 --> Q3["posición de columnas"]
        T1 --> Q4["cierre conservado"]
    end
    M -- "se aparta en 3 de 4" --> S
```

## Ejemplo trabajado

Creemos una tabla sin clave y observemos las tres desviaciones.

```sql
CREATE TABLE t (a INTEGER, b TEXT);
INSERT INTO t VALUES (1,'x'), (1,'x'), (2,'y');
SELECT COUNT(*) FROM t;              -- 3
SELECT COUNT(*) FROM (SELECT DISTINCT a, b FROM t);  -- 2
```

Si `t` fuese una relación, ambas consultas darían **2**. Dan 3 y 2: `t` es un multiconjunto. La consecuencia inmediata:

```sql
SELECT a, b FROM t
EXCEPT
SELECT 1, 'x';
```

En SQL estándar `EXCEPT` elimina duplicados, así que el resultado es `(2,'y')`: se han borrado **las dos** filas `(1,'x')` con una sola tupla. Con `EXCEPT ALL` el resultado incluiría una `(1,'x')` superviviente. Dos operadores distintos porque el modelo subyacente no es un conjunto.

**Desviación de orden.** Sobre el dominio del repositorio:

```sql
SELECT nombre FROM students;
```

El orden que devuelve depende del plan. Si el motor decide un barrido secuencial, sale el orden de inserción; si decide recorrer un índice, sale el orden del índice. Añadir un índice puede cambiar el resultado observado sin cambiar ningún dato. Todo código que dependa de ese orden es un fallo latente que se activa el día que alguien optimiza.

**Desviación de posición.**

```sql
INSERT INTO students VALUES (5, 'Ana');    -- depende del orden de columnas
INSERT INTO students (id, nombre) VALUES (5, 'Ana');  -- acceso por nombre
```

La primera forma se rompe en silencio si alguien añade una columna en medio. La segunda es la que respeta el acceso por valor.

**Traza del riesgo.** Un `INSERT` posicional sobre una tabla de 6 columnas, tras insertar una columna nueva en la posición 3, no falla: desplaza los valores y guarda datos incorrectos con tipos compatibles. El error se descubre en un informe semanas después.

## Comparación

| Operación | Semántica de conjunto | Semántica de multiconjunto (SQL) |
|---|---|---|
| `UNION` | Sin duplicados | `UNION` sin, `UNION ALL` con |
| `INTERSECT` | Sin duplicados | `INTERSECT` / `INTERSECT ALL` |
| `EXCEPT` | Sin duplicados | `EXCEPT` / `EXCEPT ALL` |
| Proyección | Elimina duplicados | Los conserva salvo `DISTINCT` |
| Conteo | Cardinalidad del conjunto | `COUNT(*)` cuenta repeticiones |

## Errores frecuentes

1. **Suponer que el motor devuelve las filas «en orden».** No hay orden sin `ORDER BY`, y con `ORDER BY` sobre columna no única el desempate tampoco está definido.
2. **Usar `SELECT *` en código de producción.** Ata el cliente a la posición y al número de columnas.
3. **Proyectar sin pensar en duplicados.** `SELECT ciudad FROM clientes` devuelve la ciudad repetida por cada cliente; casi nunca es lo que se quería.
4. **Confundir `NULL` con un valor.** No pertenece a ningún dominio: es una marca de información ausente (clase 019).
5. **Crear tablas sin clave primaria.** Sin ella no hay forma de referirse a una fila concreta ni de borrar un duplicado sin borrar el otro.

## De la clase a la operación

Los tres apartamientos de SQL respecto del modelo son la causa de una familia entera de fallos de producción: informes con totales inflados por duplicados, procesos que dependen del orden, migraciones que desplazan columnas. Reconocer la causa común los convierte en un solo problema con una sola disciplina.

## Reto de transferencia

1. Encuentra en un esquema real una tabla sin clave primaria y demuestra con una consulta que contiene duplicados lógicos.
2. Muestra una consulta de tu código que dependa del orden sin `ORDER BY`.
3. Reproduce el efecto de `EXCEPT` frente a `EXCEPT ALL` con tus propios datos.
4. Convierte un `INSERT` posicional en uno por nombre y explica qué fallo evitaste.

## Preguntas de evaluación

1. Da una consulta cuyo resultado cambie al crear un índice, sin que cambien los datos, y explica por qué.
2. ¿Por qué `COUNT(*)` y `COUNT(DISTINCT ...)` difieren, y qué dice eso del modelo subyacente?
3. Explica el acceso por valor y por qué prohíbe exponer identificadores de fila físicos.
4. La propiedad de cierre habilita las CTE. Da una consulta tuya que sería imposible sin ella.

---

## 🌐 El mismo problema en cada motor

**Caso:** Convertir una bolsa de registros en una relación

En el modelo relacional una relación es un **conjunto**: no tiene filas
repetidas y no tiene orden. Lo que las tablas guardan de verdad son bolsas
(`multisets`): admiten repetidos y llegan en el orden que sea.

El caso parte de un registro de accesos con repeticiones —Ada entró dos
veces a DB-101, Linus dos veces también— y devuelve el conjunto de pares
distintos, ordenado. El `DISTINCT` es lo que convierte la bolsa en conjunto;
el `ORDER BY` es una decisión de presentación, y por eso hay que escribirlo
siempre: sin él, ningún motor está obligado a devolver nada en un orden
concreto.

Salida esperada, idéntica en todos los motores que lo resuelven:

| estudiante | curso |
|---|---|
| `Ada` | `DB-101` |
| `Ada` | `SE-201` |
| `Linus` | `DB-101` |

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase 020`: 5 de
las 5 implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| SQLite | sí | núcleo | [código](implementaciones/sqlite/consulta.sql) | [doc oficial](https://sqlite.org/lang_select.html) |
| DuckDB | sí | núcleo | [código](implementaciones/duckdb/consulta.sql) | [doc oficial](https://duckdb.org/docs/stable/sql/query_syntax/orderby.html) |
| PostgreSQL | sí | servicio | [código](implementaciones/postgresql/consulta.sql) | [doc oficial](https://www.postgresql.org/docs/current/sql-select.html) |
| Redis | sí | servicio | [código](implementaciones/redis/consulta.txt) | [doc oficial](https://redis.io/docs/latest/develop/data-types/sets/) |
| MongoDB | sí | servicio | [código](implementaciones/mongodb/consulta.js) | [doc oficial](https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/) |

### Los que resuelven el caso

#### SQLite · [`implementaciones/sqlite/consulta.sql`](implementaciones/sqlite/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: sqlite
-- doc: https://sqlite.org/lang_select.html
-- nota: quitar el ORDER BY no rompe la consulta, y ese es el peligro: devuelve
--       un orden que parece estable hasta que un indice nuevo cambia el plan.

-- === preparacion ===
-- El registro de accesos es una BOLSA: admite repetidos y tiene orden de
-- llegada. Una relacion no es eso.
CREATE TABLE accesos (
    id         INTEGER PRIMARY KEY,
    estudiante TEXT NOT NULL,
    curso      TEXT NOT NULL
);
INSERT INTO accesos (id, estudiante, curso) VALUES
    (1, 'Linus', 'DB-101'),
    (2, 'Ada',   'DB-101'),
    (3, 'Ada',   'DB-101'),
    (4, 'Ada',   'SE-201'),
    (5, 'Linus', 'DB-101');

-- === consulta ===
-- DISTINCT convierte la bolsa en conjunto; ORDER BY impone un orden que la
-- relacion NO tiene: es una decision de presentacion, no del modelo.
SELECT DISTINCT estudiante, curso
FROM accesos
ORDER BY estudiante, curso;
```

- **Por qué sí:** Muestra la diferencia entre bolsa y conjunto en tres líneas, y permite comprobar a mano que sin `ORDER BY` el orden depende del plan que el motor elija, no de cómo se insertaron las filas.
- **Por qué no:** Al ser un archivo pequeño y con planes simples, el orden «casual» suele coincidir con el de inserción: es justo el motor donde más fácil resulta creerse que el orden está garantizado cuando no lo está.
- 📄 Documentación oficial: <https://sqlite.org/lang_select.html>

#### DuckDB · [`implementaciones/duckdb/consulta.sql`](implementaciones/duckdb/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/query_syntax/orderby.html
-- nota: al ejecutar en paralelo por trozos, sin ORDER BY el orden cambia entre
--       ejecuciones de verdad. Es el motor que mejor demuestra que una relacion
--       no tiene orden.

-- === preparacion ===
-- El registro de accesos es una BOLSA: admite repetidos y tiene orden de
-- llegada. Una relacion no es eso.
CREATE TABLE accesos (
    id         INTEGER PRIMARY KEY,
    estudiante VARCHAR NOT NULL,
    curso      VARCHAR NOT NULL
);
INSERT INTO accesos (id, estudiante, curso) VALUES
    (1, 'Linus', 'DB-101'),
    (2, 'Ada',   'DB-101'),
    (3, 'Ada',   'DB-101'),
    (4, 'Ada',   'SE-201'),
    (5, 'Linus', 'DB-101');

-- === consulta ===
-- DISTINCT convierte la bolsa en conjunto; ORDER BY impone un orden que la
-- relacion NO tiene: es una decision de presentacion, no del modelo.
SELECT DISTINCT estudiante, curso
FROM accesos
ORDER BY estudiante, curso;
```

- **Por qué sí:** Al ejecutar en paralelo por trozos, el orden sin `ORDER BY` cambia de verdad entre ejecuciones: es el motor que mejor demuestra que una relación no tiene orden.
- **Por qué no:** `DISTINCT` sobre columnas de alta cardinalidad obliga a una tabla hash completa en memoria; barato en el ejemplo, caro en un conjunto real.
- 📄 Documentación oficial: <https://duckdb.org/docs/stable/sql/query_syntax/orderby.html>

#### PostgreSQL · [`implementaciones/postgresql/consulta.sql`](implementaciones/postgresql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/sql-select.html
-- nota: la documentacion lo dice sin rodeos: sin ORDER BY el orden de las filas
--       es indeterminado. No es un descuido del motor; es el modelo.

DROP TABLE IF EXISTS accesos;

-- === preparacion ===
-- El registro de accesos es una BOLSA: admite repetidos y tiene orden de
-- llegada. Una relacion no es eso.
CREATE TABLE accesos (
    id         integer PRIMARY KEY,
    estudiante text NOT NULL,
    curso      text NOT NULL
);
INSERT INTO accesos (id, estudiante, curso) VALUES
    (1, 'Linus', 'DB-101'),
    (2, 'Ada',   'DB-101'),
    (3, 'Ada',   'DB-101'),
    (4, 'Ada',   'SE-201'),
    (5, 'Linus', 'DB-101');

-- === consulta ===
-- DISTINCT convierte la bolsa en conjunto; ORDER BY impone un orden que la
-- relacion NO tiene: es una decision de presentacion, no del modelo.
SELECT DISTINCT estudiante, curso
FROM accesos
ORDER BY estudiante, curso;
```

- **Por qué sí:** Además de `DISTINCT` tiene `DISTINCT ON`, que resuelve «una fila por grupo» sin ventana ni subconsulta, y su documentación explica que sin `ORDER BY` el orden es indeterminado por diseño.
- **Por qué no:** `DISTINCT ON` es una extensión propia: usarla ata la consulta a PostgreSQL, y el equivalente portable —una función de ventana— hay que escribirlo desde cero al migrar.
- 📄 Documentación oficial: <https://www.postgresql.org/docs/current/sql-select.html>

#### Redis · [`implementaciones/redis/consulta.txt`](implementaciones/redis/consulta.txt)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```text
# motor: redis
# doc: https://redis.io/docs/latest/develop/data-types/sets/
# nota: el conjunto no es una operacion sobre los datos, es el tipo de dato.
#       El precio: el par estudiante-curso hay que serializarlo en una cadena.

# === preparacion ===
FLUSHDB
SADD accesos Linus|DB-101
SADD accesos Ada|DB-101
SADD accesos Ada|DB-101
SADD accesos Ada|SE-201
SADD accesos Linus|DB-101

# === consulta ===
SORT accesos ALPHA
```

- **Por qué sí:** Aquí el conjunto no es una operación sobre los datos: es el tipo de dato. `SADD` no admite repetidos y no promete orden, que es literalmente la definición de relación de esta clase.
- **Por qué no:** Un conjunto de Redis guarda cadenas sueltas, no tuplas con atributos: para representar el par estudiante-curso hay que serializarlo en una sola cadena y perder la estructura.
- 📄 Documentación oficial: <https://redis.io/docs/latest/develop/data-types/sets/>

#### MongoDB · [`implementaciones/mongodb/consulta.js`](implementaciones/mongodb/consulta.js)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```javascript
// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/
// nota: $group por la pareja de campos hace de DISTINCT. El $sort explicito
//       deja claro que el orden se pide; no se hereda del orden de insercion.

// === preparacion ===
db.accesos.drop();
db.accesos.insertMany([
  { estudiante: "Linus", curso: "DB-101" },
  { estudiante: "Ada", curso: "DB-101" },
  { estudiante: "Ada", curso: "DB-101" },
  { estudiante: "Ada", curso: "SE-201" },
  { estudiante: "Linus", curso: "DB-101" },
]);

// === consulta ===
db.accesos
  .aggregate([
    { $group: { _id: { estudiante: "$estudiante", curso: "$curso" } } },
    { $sort: { "_id.estudiante": 1, "_id.curso": 1 } },
  ])
  .forEach((d) => print(d._id.estudiante + "|" + d._id.curso));
```

- **Por qué sí:** `$group` por la pareja de campos elimina los repetidos igual que un `DISTINCT`, y la etapa `$sort` deja explícito que el orden se pide, no se hereda.
- **Por qué no:** Sin índice que cubra el `$sort`, la ordenación se hace en memoria con un límite de 100 MB por etapa, y la consulta falla en vez de ir lenta.
- 📄 Documentación oficial: <https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/>

---

## Laboratorio

```bash
python scripts/validate_repository.py
python labs/01-sql-foundations/run_lab.py
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

- **E. F. Codd** (1970). [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685). Communications of the ACM 13(6). DOI [10.1145/362384.362685](https://doi.org/10.1145/362384.362685).  
  Artículo fundacional del modelo relacional y de la independencia de datos.
- **C. J. Date** (2015). [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/). 3.a ed. O'Reilly. ISBN 978-1-4919-4117-1.  
  Separa el modelo relacional de lo que SQL realmente implementa, incluidos los nulos.
- **Raghu Ramakrishnan, Johannes Gehrke** (2002). [Database Management Systems](https://pages.cs.wisc.edu/~dbbook/). 3.a ed. McGraw-Hill. ISBN 978-0-07-246563-1.  
  Fuerte en álgebra relacional, evaluación de consultas y estructuras de almacenamiento.

---

> [Programa](../../../README.md) · [Parte 03](../README.md) · [← Anterior](../../part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md) · [Siguiente →](../../part-03-modelo-relacional-y-algebra/021-algebra-relacional-operadores/README.md)
