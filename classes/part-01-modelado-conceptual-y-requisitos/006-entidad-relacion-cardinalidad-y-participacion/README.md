# 006 — Entidad-relación, cardinalidad y participación

> [Programa](../../../README.md) · [Parte 01](../README.md) · [← Anterior](../../part-01-modelado-conceptual-y-requisitos/005-de-requisitos-a-entidades/README.md) · [Siguiente →](../../part-01-modelado-conceptual-y-requisitos/007-claves-identidad-natural-y-sustituta/README.md)

Parte 01 — Modelado conceptual y requisitos · Fundamentos ·
3 horas estimadas · motores `postgresql`, `sqlite` · laboratorio
[`labs/01-sql-foundations`](../../../labs/01-sql-foundations/README.md) · 3 fuentes.

**Conceptos centrales:** `entidad débil` · `cardinalidad` · `participación total` · `atributo de relación`

**En este caso se comparan 6 motores**: 5 lo resuelven (5 con el resultado comprobado por máquina) y 1 no, con el motivo escrito.

---

## Propósito

Representar el dominio con el modelo entidad-relación de Chen y, sobre todo, leer un diagrama con precisión: qué dice exactamente una cardinalidad y qué obliga una participación total.

## Resultados de aprendizaje

Al terminar podrás:

1. Distinguir entidad, relación, atributo y entidad débil.
2. Leer y escribir cardinalidades sin ambigüedad (mínimo y máximo, en ambos sentidos).
3. Traducir participación total en una restricción concreta del esquema.
4. Convertir cualquier relación N:M en tablas, sabiendo qué se gana y qué se pierde.
5. Detectar las relaciones ternarias falsas.

## Fundamentos

### El vocabulario de Chen

Chen (1976) propuso el modelo entidad-relación para unificar las vistas de red, jerárquica y relacional. Sus piezas:

- **Entidad:** cosa distinguible del dominio (un estudiante, un curso).
- **Conjunto de entidades:** todas las del mismo tipo. Es lo que suele acabar siendo una tabla.
- **Relación:** asociación entre entidades (un estudiante *inscribe* un curso).
- **Atributo:** propiedad de una entidad o de una relación. La nota es atributo de la **relación** inscripción, no del estudiante ni del curso, y esto se olvida constantemente.
- **Entidad débil:** no tiene identidad propia; se identifica por la entidad fuerte de la que depende (una línea de factura respecto de la factura).

### Cardinalidad: cuatro números, no dos

Una cardinalidad completa declara **cuatro** valores: mínimo y máximo en cada sentido. La notación abreviada «1:N» solo declara dos y por eso genera discusiones.

Para «estudiante inscribe curso»:

| Sentido | Mínimo | Máximo | Lectura |
|---|---:|---:|---|
| estudiante → curso | 0 | N | Un estudiante puede no tener cursos, o tener muchos |
| curso → estudiante | 0 | N | Un curso puede no tener inscritos, o tener muchos |

Cambiar el mínimo de 0 a 1 en el segundo sentido significa «no existen cursos sin inscritos», y eso **no** se puede expresar con una clave foránea: exige una restricción diferida o una comprobación en la aplicación. Esa es la diferencia práctica entre participación parcial y total.

| Concepto | Notación | Cómo se implementa |
|---|---|---|
| Participación parcial (mín. 0) | línea simple | Clave foránea que admite nulo, o simple ausencia de filas |
| Participación total (mín. 1) | línea doble | `NOT NULL` en el lado N, o restricción diferida si el lado 1 la exige |
| Máximo 1 | flecha / `1` | Clave única |
| Máximo N | `N` | Sin restricción de unicidad |

### La regla de traducción

```mermaid
erDiagram
    STUDENT ||--o{ ENROLLMENT : "inscribe"
    COURSE  ||--o{ ENROLLMENT : "recibe"
    TEACHER ||--o{ TEACHING   : "dicta"
    COURSE  ||--o{ TEACHING   : "es dictado por"
    STUDENT {
        int  id PK
        text nombre
    }
    COURSE {
        int  id PK
        text nombre
        text periodo
    }
    ENROLLMENT {
        int     student_id PK,FK
        int     course_id  PK,FK
        numeric nota
        text    registrada_en
    }
    TEACHING {
        int teacher_id PK,FK
        int course_id  PK,FK
    }
```

Reglas, en orden:

1. **1:N** → clave foránea en el lado N. No hace falta tabla nueva.
2. **N:M** → tabla puente cuya clave primaria es la pareja de claves foráneas. Los atributos de la relación viven ahí.
3. **1:1** → clave foránea con restricción `UNIQUE` en el lado con participación total.
4. **Entidad débil** → clave primaria compuesta por la clave de la entidad fuerte más un discriminador, con `ON DELETE CASCADE`.

### Relaciones ternarias: casi siempre son falsas

Una relación ternaria genuina es aquella cuya semántica **no** se recupera con tres binarias. El ejemplo clásico: «el proveedor P suministra la pieza Z para el proyecto Y». Saber que P suministra Z, que P trabaja en Y y que Z se usa en Y **no** implica el hecho ternario.

En la mayoría de los modelos de gestión, sin embargo, lo que parece ternario es una entidad que aún no se ha nombrado. «Profesor dicta curso en aula» no es ternario: es la entidad `sesión`, con su horario y su capacidad. Antes de dibujar un rombo con tres patas, busca el sustantivo que falta.

## Ejemplo trabajado

Requisito: *«Un curso lo puede dictar más de un profesor, y un profesor dicta varios cursos. Todo curso debe tener al menos un profesor asignado.»*

**Cardinalidades completas:**

| Sentido | Mín | Máx |
|---|---:|---:|
| curso → profesor | **1** | N |
| profesor → curso | 0 | N |

El mínimo 1 del primer sentido es participación total del lado `course`. Traducción:

```sql
CREATE TABLE teaching (
  course_id  INTEGER NOT NULL REFERENCES courses(id)  ON DELETE CASCADE,
  teacher_id INTEGER NOT NULL REFERENCES teachers(id) ON DELETE RESTRICT,
  PRIMARY KEY (course_id, teacher_id)
);
```

Esto garantiza N:M y evita duplicados. **No** garantiza «todo curso tiene al menos un profesor»: se puede insertar un curso y no insertar nunca su fila en `teaching`.

Las tres formas honestas de cerrar ese hueco, con su costo:

| Mecanismo | Garantía | Costo |
|---|---|---|
| Restricción diferida al final de la transacción | Total, en el motor | Solo en motores que la soportan (PostgreSQL sí; SQLite y MySQL, no de esta forma) |
| Comprobación en la aplicación al crear el curso | Depende del cliente | Cualquier otro cliente la salta |
| Invariante auditada periódicamente | Detecta, no impide | Barata y honesta; deja ventana de inconsistencia |

Consulta de la invariante, útil en cualquier motor:

```sql
SELECT c.id, c.nombre
FROM courses c
LEFT JOIN teaching t ON t.course_id = c.id
WHERE t.course_id IS NULL;
```

Cero filas significa que la participación total se cumple ahora mismo. Es exactamente el tipo de comprobación que el laboratorio ejecuta como invariante.

## Comparación

| Construcción | Tablas resultantes | ¿Puede el motor garantizar el mínimo 1? |
|---|---:|---|
| 1:N con participación parcial | 2 | Sí (`NULL` permitido) |
| 1:N con participación total en N | 2 | Sí (`NOT NULL`) |
| 1:N con participación total en 1 | 2 | Solo con restricción diferida |
| N:M | 3 | No, sin restricción diferida |
| 1:1 | 2 | Sí, con `UNIQUE` + `NOT NULL` en un lado |
| Entidad débil | 2 | Sí (clave compuesta + cascada) |

## Errores frecuentes

1. **Poner los atributos de la relación en una de las entidades.** La nota en `students` obliga a un estudiante a tener una sola nota en toda su vida académica.
2. **Leer «1:N» sin preguntar por los mínimos.** La mitad de la información de la cardinalidad está en el mínimo, y es la mitad que genera reglas de negocio.
3. **Creer que la clave foránea garantiza la participación total.** Garantiza que si hay referencia, existe; no que haya referencia.
4. **Inventar relaciones ternarias.** Busca primero el sustantivo que falta.
5. **Usar `ON DELETE CASCADE` por comodidad.** En una tabla puente es razonable; sobre datos históricos borra evidencia que quizá deba conservarse.

## De la clase a la operación

Las cardinalidades mal declaradas se manifiestan meses después como filas huérfanas, informes que no cuadran y consultas que devuelven duplicados. Una cardinalidad es una promesa: si el motor no puede hacerla cumplir, hay que decir explícitamente quién la vigila.

## Reto de transferencia

Sobre el dominio del repositorio:

1. Dibuja el diagrama con las cuatro cardinalidades completas de cada relación.
2. Identifica una participación total que el esquema actual **no** garantiza.
3. Escribe la consulta de invariante que la audita y ejecútala.
4. Propón el mecanismo que la haría cumplir y declara su costo.

## Preguntas de evaluación

1. Explica con un ejemplo del dominio por qué la nota es atributo de la relación y no de la entidad.
2. Da una relación ternaria genuina de tu experiencia y demuestra que no se descompone en tres binarias.
3. ¿Qué diferencia práctica hay entre `ON DELETE CASCADE` y `ON DELETE RESTRICT` en la tabla `teaching`?
4. Un modelo declara participación total en ambos lados de una relación 1:1. ¿Cómo se inserta la primera fila?

---

## 🌐 El mismo problema en cada motor

**Caso:** Una relación de muchos a muchos y las dos cardinalidades que hay que poder contar

Estudiantes y cursos se relacionan de muchos a muchos: un estudiante toma
varios cursos y un curso tiene varios estudiantes. Ada toma dos cursos,
Linus uno, Grace ninguno; DB-101 tiene dos estudiantes, SE-201 uno y AR-301
ninguno.

La consulta devuelve, para cada curso ordenado por código, cuántos
estudiantes tiene. Que AR-301 aparezca con 0 es la mitad del ejercicio: la
**participación parcial** —un curso puede existir sin estudiantes— solo se
ve si el modelo conserva a los que no participan.

Salida esperada, idéntica en todos los motores que lo resuelven:

| curso | estudiantes |
|---|---|
| `AR-301` | `0` |
| `DB-101` | `2` |
| `SE-201` | `1` |

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase 006`: 5 de
las 5 implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| SQLite | sí | núcleo | [código](implementaciones/sqlite/consulta.sql) | [doc oficial](https://sqlite.org/foreignkeys.html) |
| DuckDB | sí | núcleo | [código](implementaciones/duckdb/consulta.sql) | [doc oficial](https://duckdb.org/docs/stable/sql/statements/create_table.html) |
| PostgreSQL | sí | servicio | [código](implementaciones/postgresql/consulta.sql) | [doc oficial](https://www.postgresql.org/docs/current/ddl-constraints.html) |
| Neo4j | sí | servicio | [código](implementaciones/neo4j/consulta.cypher) | [doc oficial](https://neo4j.com/docs/cypher-manual/current/patterns/) |
| MongoDB | sí | servicio | [código](implementaciones/mongodb/consulta.js) | [doc oficial](https://www.mongodb.com/docs/manual/data-modeling/) |
| Apache Cassandra | **no** | — | — | [doc oficial](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/intro.html) |

### Los que resuelven el caso

#### SQLite · [`implementaciones/sqlite/consulta.sql`](implementaciones/sqlite/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: sqlite
-- doc: https://sqlite.org/foreignkeys.html
-- nota: SQLite solo comprueba las claves foraneas si PRAGMA foreign_keys esta
--       activo; el verificador lo activa, y en una aplicacion real hay que
--       hacerlo en cada conexion.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);
CREATE TABLE cursos (
    id     INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL
);
-- La tabla intermedia ES la relacion. La clave compuesta impone «una fila por
-- par»: sin ella, el mismo estudiante podria inscribirse dos veces al mismo
-- curso y todos los recuentos quedarian inflados.
CREATE TABLE inscripciones (
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id),
    curso_id      INTEGER NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201'), (30, 'AR-301');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
-- El LEFT JOIN es lo que conserva AR-301 con cero: la participacion parcial
-- solo se ve si el modelo no descarta a quien no participa.
SELECT c.codigo AS curso,
       COUNT(i.estudiante_id) AS estudiantes
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
```

- **Por qué sí:** La tabla intermedia con clave primaria compuesta es la traducción directa del diagrama entidad-relación: una fila por par, ni más ni menos, y la cardinalidad máxima queda impuesta por la clave.
- **Por qué no:** El diagrama distingue participación total de parcial; la tabla no. Que un curso deba tener al menos un estudiante no se puede declarar y hay que comprobarlo aparte.
- 📄 Documentación oficial: <https://sqlite.org/foreignkeys.html>

#### DuckDB · [`implementaciones/duckdb/consulta.sql`](implementaciones/duckdb/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/create_table.html
-- nota: la misma consulta sirve para auditar datos existentes: si algun curso
--       aparece con mas estudiantes que inscripciones unicas, la clave
--       compuesta no estaba y hay duplicados.

-- === preparacion ===
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL
);
CREATE TABLE cursos (
    id     INTEGER PRIMARY KEY,
    codigo VARCHAR NOT NULL
);
-- La tabla intermedia ES la relacion. La clave compuesta impone «una fila por
-- par»: sin ella, el mismo estudiante podria inscribirse dos veces al mismo
-- curso y todos los recuentos quedarian inflados.
CREATE TABLE inscripciones (
    estudiante_id INTEGER NOT NULL,
    curso_id      INTEGER NOT NULL,
    PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201'), (30, 'AR-301');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
-- El LEFT JOIN es lo que conserva AR-301 con cero: la participacion parcial
-- solo se ve si el modelo no descarta a quien no participa.
SELECT c.codigo AS curso,
       COUNT(i.estudiante_id) AS estudiantes
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
```

- **Por qué sí:** Sirve para lo que esta clase realmente entrena: contar cardinalidades sobre datos ya existentes para descubrir cuál era el modelo de verdad, en vez del que estaba en el documento.
- **Por qué no:** Sus claves foráneas no impiden borrar la fila referenciada con la misma firmeza que un motor transaccional: es un almacén para analizar, no para sostener la integridad de un sistema en producción.
- 📄 Documentación oficial: <https://duckdb.org/docs/stable/sql/statements/create_table.html>

#### PostgreSQL · [`implementaciones/postgresql/consulta.sql`](implementaciones/postgresql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-constraints.html
-- nota: para una participacion TOTAL («todo curso tiene al menos un
--       estudiante») la clave foranea no basta: se declara DEFERRABLE
--       INITIALLY DEFERRED y se comprueba al cerrar la transaccion.

DROP TABLE IF EXISTS inscripciones, cursos, estudiantes;

-- === preparacion ===
CREATE TABLE estudiantes (
    id     integer PRIMARY KEY,
    nombre text NOT NULL
);
CREATE TABLE cursos (
    id     integer PRIMARY KEY,
    codigo text NOT NULL
);
-- La tabla intermedia ES la relacion. La clave compuesta impone «una fila por
-- par»: sin ella, el mismo estudiante podria inscribirse dos veces al mismo
-- curso y todos los recuentos quedarian inflados.
CREATE TABLE inscripciones (
    estudiante_id integer NOT NULL REFERENCES estudiantes(id),
    curso_id      integer NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante_id, curso_id)
);

INSERT INTO estudiantes (id, nombre) VALUES (1, 'Ada'), (2, 'Linus'), (3, 'Grace');
INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201'), (30, 'AR-301');
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);

-- === consulta ===
-- El LEFT JOIN es lo que conserva AR-301 con cero: la participacion parcial
-- solo se ve si el modelo no descarta a quien no participa.
SELECT c.codigo AS curso,
       COUNT(i.estudiante_id) AS estudiantes
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
```

- **Por qué sí:** Impone las dos claves foráneas y la clave compuesta, y permite además diferir la comprobación al final de la transacción (`DEFERRABLE INITIALLY DEFERRED`), que es como se modela una participación total sin bloquearse al insertar la primera fila.
- **Por qué no:** Cada clave foránea añade una comprobación por inserción y un bloqueo sobre la fila referenciada: en tablas de relación muy escritas, ese costo es real y hay que medirlo.
- 📄 Documentación oficial: <https://www.postgresql.org/docs/current/ddl-constraints.html>

#### Neo4j · [`implementaciones/neo4j/consulta.cypher`](implementaciones/neo4j/consulta.cypher)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```cypher
// motor: neo4j
// doc: https://neo4j.com/docs/cypher-manual/current/patterns/
// nota: no hay tabla intermedia. La relacion de muchos a muchos es la arista
//       misma, y el diagrama entidad-relacion se parece tanto al modelo fisico
//       que el paso de uno a otro deja de ser una traduccion.

// === preparacion ===
MATCH (n) DETACH DELETE n;
CREATE (a:Estudiante {nombre: 'Ada'}),
       (l:Estudiante {nombre: 'Linus'}),
       (:Estudiante {nombre: 'Grace'}),
       (db:Curso {codigo: 'DB-101'}),
       (se:Curso {codigo: 'SE-201'}),
       (:Curso {codigo: 'AR-301'}),
       (a)-[:INSCRITO_EN]->(db),
       (a)-[:INSCRITO_EN]->(se),
       (l)-[:INSCRITO_EN]->(db);

// === consulta ===
MATCH (c:Curso)
OPTIONAL MATCH (e:Estudiante)-[:INSCRITO_EN]->(c)
RETURN c.codigo AS curso, count(e) AS estudiantes
ORDER BY curso;
```

- **Por qué sí:** La relación de muchos a muchos no necesita tabla intermedia: es una arista. El diagrama entidad-relación y el modelo físico se parecen tanto que el paso de uno a otro deja de ser una traducción.
- **Por qué no:** Contar por etiqueta obliga a recorrer todos los nodos de esa etiqueta, que es exactamente lo que una tabla con índice hace mejor: el grafo gana en recorridos, no en recuentos globales.
- 📄 Documentación oficial: <https://neo4j.com/docs/cypher-manual/current/patterns/>

#### MongoDB · [`implementaciones/mongodb/consulta.js`](implementaciones/mongodb/consulta.js)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```javascript
// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/data-modeling/
// nota: aqui la relacion vive como un arreglo de referencias dentro del curso.
//       Es el modelo natural cuando la pregunta frecuente es «quienes estan en
//       este curso»; la pregunta inversa exige un indice multiclave.

// === preparacion ===
db.cursos.drop();
db.estudiantes.drop();

db.estudiantes.insertMany([
  { _id: 1, nombre: "Ada" },
  { _id: 2, nombre: "Linus" },
  { _id: 3, nombre: "Grace" },
]);
db.cursos.insertMany([
  { _id: 10, codigo: "DB-101", inscritos: [1, 2] },
  { _id: 20, codigo: "SE-201", inscritos: [1] },
  // Participacion parcial: el curso existe con el arreglo vacio.
  { _id: 30, codigo: "AR-301", inscritos: [] },
]);

// === consulta ===
db.cursos
  .aggregate([
    { $project: { _id: 0, curso: "$codigo", estudiantes: { $size: "$inscritos" } } },
    { $sort: { curso: 1 } },
  ])
  .forEach((d) => print(d.curso + "|" + d.estudiantes));
```

- **Por qué sí:** Permite modelar la relación como un arreglo de referencias dentro del curso, que es el modelo natural cuando la pregunta frecuente es «quiénes están en este curso».
- **Por qué no:** El arreglo tiene el límite de 16 MB del documento y hace cara la pregunta inversa —«en qué cursos está este estudiante»— salvo que se añada un índice multiclave y se acepte mantener las dos direcciones.
- 📄 Documentación oficial: <https://www.mongodb.com/docs/manual/data-modeling/>

### Los que no resuelven este caso — y qué se hace en su lugar

Descartar un motor con un argumento es tan formativo como usarlo. Ninguna de estas filas dice que el motor sea peor: dice que este problema no es el suyo.

| Motor | Por qué no | Qué se hace en su lugar | Fuente |
|---|---|---|---|
| Apache Cassandra | Una relación de muchos a muchos consultable en las dos direcciones no cabe en una sola tabla: haría falta una tabla por dirección de consulta y escribir en las dos, sin transacción que las mantenga de acuerdo. | `estudiantes_por_curso` y `cursos_por_estudiante` como dos tablas independientes, escritas ambas en cada inscripción, asumiendo la posibilidad de que una quede desincronizada tras un fallo. | [doc](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/intro.html) |

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

- **Peter Pin-Shan Chen** (1976). [The Entity-Relationship Model - Toward a Unified View of Data](https://dl.acm.org/doi/10.1145/320434.320440). ACM TODS 1(1). DOI [10.1145/320434.320440](https://doi.org/10.1145/320434.320440).  
  Origen del diagrama entidad-relación.
- **Ramez Elmasri, Shamkant B. Navathe** (2015). [Fundamentals of Database Systems](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003546). 7.a ed. Pearson. ISBN 978-0-13-397077-7.  
  Modelado entidad-relación tratado con más detalle que en otros manuales.
- **Abraham Silberschatz, Henry F. Korth, S. Sudarshan** (2019). [Database System Concepts](https://db-book.com/). 7.a ed. McGraw-Hill. ISBN 978-0-07-802215-9.  
  Texto de referencia universitario. El sitio oficial publica diapositivas y capítulos de muestra.

---

> [Programa](../../../README.md) · [Parte 01](../README.md) · [← Anterior](../../part-01-modelado-conceptual-y-requisitos/005-de-requisitos-a-entidades/README.md) · [Siguiente →](../../part-01-modelado-conceptual-y-requisitos/007-claves-identidad-natural-y-sustituta/README.md)
