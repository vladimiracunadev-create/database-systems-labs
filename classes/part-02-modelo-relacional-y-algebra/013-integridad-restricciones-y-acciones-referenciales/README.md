# 013 — Integridad: restricciones, claves foraneas y acciones referenciales

> [Programa](../../../README.md) · [Parte 02](../README.md) · [← Anterior](../../part-02-modelo-relacional-y-algebra/012-calculo-relacional-y-equivalencia/README.md) · [Siguiente →](../../part-03-sql-en-profundidad/014-ddl-el-esquema-como-contrato/README.md)

Parte 02 — Modelo relacional y álgebra · Intermedio ·
3 horas estimadas · motores `postgresql`, `sqlite`, `mysql` · laboratorio
[`labs/01-sql-foundations`](../../../labs/01-sql-foundations/README.md) · 4 fuentes.

**Conceptos centrales:** `integridad de entidad` · `integridad referencial` · `CHECK` · `ON DELETE` · `aplazamiento`

**En este caso se comparan 6 motores**: 3 lo resuelven (3 con el resultado comprobado por máquina) y 3 no, con el motivo escrito.

---

## Propósito

Convertir las reglas del dominio en restricciones que el motor haga cumplir para todos los clientes. Una regla que vive solo en la aplicación es una regla que algún día alguien saltará.

## Resultados de aprendizaje

Al terminar podrás:

1. Distinguir integridad de entidad, referencial, de dominio y definida por el usuario.
2. Elegir la acción referencial correcta y justificar su efecto sobre los datos.
3. Usar restricciones diferidas y saber qué motores las soportan.
4. Reconocer qué reglas **no** puede expresar una restricción declarativa.
5. Escribir la invariante que audita lo que el motor no puede garantizar.

## Fundamentos

### Los cuatro tipos

| Tipo | Qué garantiza | Mecanismo |
|---|---|---|
| **De entidad** | Toda fila es identificable; la clave no es nula | `PRIMARY KEY` |
| **Referencial** | Toda referencia apunta a algo existente | `FOREIGN KEY` |
| **De dominio** | Cada valor pertenece a su dominio | Tipo + `CHECK` + `NOT NULL` |
| **Definida por el usuario** | Reglas de negocio arbitrarias | `CHECK`, restricciones diferidas, disparadores |

Codd (1979) añadió al modelo original la discusión de los nulos y la integridad de entidad. La regla que de ahí se deriva es tajante: **ningún componente de una clave primaria puede ser nulo**, porque un identificador desconocido no identifica.

### Acciones referenciales

Al borrar o actualizar la fila referenciada, el motor puede hacer cinco cosas:

| Acción | Efecto | Cuándo es correcta |
|---|---|---|
| `NO ACTION` / `RESTRICT` | Impide la operación | Por defecto sensato: obliga a decidir explícitamente |
| `CASCADE` | Propaga el borrado o el cambio | Composición real: líneas de una factura, tabla puente |
| `SET NULL` | Deja la referencia en nulo | La relación es opcional y su ausencia tiene sentido |
| `SET DEFAULT` | Apunta a un valor por defecto | Existe un «sin asignar» legítimo |

La diferencia entre `NO ACTION` y `RESTRICT` es sutil y real: `RESTRICT` comprueba de inmediato; `NO ACTION` puede diferirse al final de la sentencia o de la transacción, lo que permite reasignar filas dentro de la misma operación.

**Regla de criterio:** `CASCADE` en datos históricos o contables es casi siempre un error. Borrar un curso no debería borrar el registro de que alguien lo cursó y obtuvo una nota; eso destruye evidencia. La alternativa es el borrado lógico con una marca y una restricción parcial.

### Restricciones diferidas

Algunas reglas son imposibles de satisfacer fila a fila. Un ciclo obligatorio —«todo departamento tiene un jefe, y todo jefe pertenece a un departamento»— no admite una primera inserción válida si las restricciones se comprueban de inmediato.

```sql
ALTER TABLE departments
  ADD CONSTRAINT dept_jefe_fk FOREIGN KEY (jefe_id) REFERENCES employees(id)
  DEFERRABLE INITIALLY DEFERRED;
```

Con esto, la comprobación ocurre en el `COMMIT`: dentro de la transacción el estado puede ser transitoriamente inconsistente, y al confirmar debe ser válido. Es exactamente la «C» de ACID (clase 033).

Soporte real: PostgreSQL y Oracle lo ofrecen; MySQL no de esta forma; SQLite solo para claves foráneas declaradas como diferidas y con `PRAGMA foreign_keys = ON`.

### Lo que no se puede declarar

```mermaid
flowchart TD
    R["Regla del dominio"] --> A{"¿Afecta a una<br/>sola fila?"}
    A -- "Sí" --> C["CHECK"]
    A -- "No" --> B{"¿Es unicidad o<br/>referencia?"}
    B -- "Sí" --> U["UNIQUE / FOREIGN KEY<br/>(incluso parcial)"]
    B -- "No" --> D{"¿El motor tiene<br/>restricción de exclusión?"}
    D -- "Sí" --> E["EXCLUDE USING gist"]
    D -- "No" --> T{"¿Basta con detectar,<br/>o hay que impedir?"}
    T -- "Detectar" --> I["Invariante auditada<br/>+ alerta"]
    T -- "Impedir" --> G["Disparador o bloqueo<br/>explícito · documentar el costo"]
```

Ejemplos de reglas fuera del alcance de un `CHECK` estándar: «la suma de los porcentajes de un reparto es 100», «no hay dos reservas solapadas en la misma sala», «todo curso tiene al menos un profesor». La primera y la tercera exigen mirar varias filas; la segunda tiene solución declarativa solo en PostgreSQL, con restricciones de exclusión sobre rangos.

## Ejemplo trabajado

Reglas del dominio y su traducción:

```sql
CREATE TABLE courses (
  id         INTEGER PRIMARY KEY,
  nombre     TEXT    NOT NULL CHECK (length(trim(nombre)) > 0),
  periodo    TEXT    NOT NULL CHECK (periodo GLOB '[0-9][0-9][0-9][0-9]-[12]'),
  cupo       INTEGER NOT NULL CHECK (cupo BETWEEN 1 AND 500),
  UNIQUE (nombre, periodo)
);

CREATE TABLE enrollments (
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE RESTRICT,
  course_id  INTEGER NOT NULL REFERENCES courses(id)  ON DELETE RESTRICT,
  nota       NUMERIC(2,1) CHECK (nota IS NULL OR nota BETWEEN 1.0 AND 7.0),
  estado     TEXT NOT NULL DEFAULT 'activa'
             CHECK (estado IN ('activa','retirada','anulada')),
  PRIMARY KEY (student_id, course_id)
);
```

Qué garantiza cada línea, sin excepciones y para todo cliente:

- `NOT NULL` en `nombre`: no hay cursos anónimos. El `CHECK` con `trim` impide además el nombre de solo espacios, que `NOT NULL` sí permite.
- `UNIQUE (nombre, periodo)`: no hay dos «Bases de datos» en 2026-1. La regla de negocio queda escrita una vez.
- `nota BETWEEN 1.0 AND 7.0` **o nula**: una inscripción sin calificar es válida; una nota de 9,5 no lo es. Sin el `OR nota IS NULL`, la restricción se evaluaría como `UNKNOWN` para nulos y **los aceptaría igual** — conviene escribirlo explícito para que el lector no dude.
- `ON DELETE RESTRICT` en ambas: borrar un estudiante con inscripciones falla. Correcto: el historial académico es evidencia.

**Lo que este esquema no garantiza:** el cupo. La regla «no se puede inscribir más gente que el cupo» compara un conteo con un valor de otra tabla, y ningún `CHECK` estándar lo permite.

Las tres soluciones, con su precio:

```sql
-- 1. Detección: barata, honesta, deja ventana de incumplimiento
SELECT c.id, c.cupo, COUNT(e.student_id) AS inscritos
FROM courses c JOIN enrollments e ON e.course_id = c.id AND e.estado = 'activa'
GROUP BY c.id, c.cupo
HAVING COUNT(e.student_id) > c.cupo;
```

```sql
-- 2. Prevención con bloqueo explícito, dentro de la transacción
BEGIN;
SELECT cupo FROM courses WHERE id = :curso FOR UPDATE;      -- serializa los inscritos de ESE curso
INSERT INTO enrollments (student_id, course_id) VALUES (:est, :curso);
-- comprobar el conteo y abortar si excede
COMMIT;
```

```sql
-- 3. Contador desnormalizado con disparador (clase 009), con su invariante
```

La opción 2 es correcta y tiene un costo declarado: todas las inscripciones al mismo curso se serializan. Con un curso muy demandado, eso es una cola. La opción 1 no impide nada pero cuesta cero en el camino de escritura. La decisión depende de si un cupo excedido es un incidente grave o algo que se corrige a mano.

**Nota sobre SQLite:** las claves foráneas no se aplican salvo que se active `PRAGMA foreign_keys = ON` en **cada conexión**. Es la causa más común de referencias colgantes en proyectos que usan SQLite; el laboratorio del repositorio lo activa explícitamente y comprueba con `PRAGMA foreign_key_check`.

## Comparación

| Regla | Declarativa | Motor | Costo |
|---|---|---|---|
| Valor en un rango | `CHECK` | Todos | Nulo |
| Unicidad condicional | Índice único parcial | PostgreSQL, SQLite | Nulo |
| Referencia válida | `FOREIGN KEY` | Todos (SQLite con pragma) | Índice en el hijo |
| Sin solapamiento de rangos | `EXCLUDE USING gist` | Solo PostgreSQL | Índice GiST |
| Ciclo obligatorio | `DEFERRABLE` | PostgreSQL, Oracle | Nulo |
| Suma de un grupo | — | Ninguno | Disparador o invariante |

## Errores frecuentes

1. **Dejar la validación solo en la aplicación.** El script de migración, la consola y el próximo microservicio no la ejecutarán.
2. **`ON DELETE CASCADE` por comodidad.** Sobre datos históricos destruye evidencia sin dejar rastro.
3. **Olvidar `PRAGMA foreign_keys = ON` en SQLite.** Las claves foráneas quedan como documentación decorativa.
4. **`CHECK` que ignora los nulos.** Un `CHECK (nota BETWEEN 1 AND 7)` acepta nulos porque `UNKNOWN` no es falso.
5. **No indexar la columna hija de una clave foránea.** Cada borrado en el padre provoca un barrido completo del hijo.

## De la clase a la operación

Los datos sucios llegan por el camino que nadie vigilaba: una carga masiva, un arreglo manual, un servicio nuevo. Las restricciones declaradas son el único control que se aplica a todos los caminos, incluidos los que aún no existen.

## Reto de transferencia

1. Elige tres reglas de negocio reales y decláralas como restricciones.
2. Identifica una que el motor no pueda expresar y escribe su invariante.
3. Implementa la prevención con bloqueo explícito y mide su efecto en concurrencia.
4. Documenta qué acción referencial elegiste en cada clave foránea y por qué.

## Preguntas de evaluación

1. ¿Por qué un `CHECK` no rechaza los nulos y qué hay que escribir para que lo haga?
2. Da un caso de tu dominio donde `CASCADE` destruiría información que debe conservarse.
3. Explica con una traza por qué el ciclo obligatorio necesita restricciones diferidas.
4. Elige entre detectar y prevenir para la regla del cupo, y defiende la elección con el costo de cada una.

---

## 🌐 El mismo problema en cada motor

**Caso:** Qué le pasa a lo que cuelga de una fila cuando esa fila se borra

Una clave foránea no solo prohíbe apuntar a lo que no existe: también
decide qué ocurre cuando lo apuntado desaparece. Y esa decisión —`CASCADE`,
`RESTRICT`, `SET NULL`— es de diseño, no de implementación: dice si el hijo
tiene sentido sin el padre.

El caso lo pone a prueba. Las inscripciones cuelgan del curso con `ON DELETE
CASCADE` (una inscripción a un curso que ya no existe no significa nada),
pero las evaluaciones lo hacen con `ON DELETE RESTRICT` (son evidencia
académica y no pueden evaporarse). Se borra SE-201, que solo tiene
inscripciones: desaparece con ellas. Se intenta borrar DB-101, que tiene
evaluaciones: el motor lo impide. La consulta devuelve los cursos que
quedan con sus inscripciones.

Salida esperada, idéntica en todos los motores que lo resuelven:

| curso | inscripciones |
|---|---|
| `DB-101` | `2` |

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase 013`: 3 de
las 3 implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| SQLite | sí | núcleo | [código](implementaciones/sqlite/consulta.sql) | [doc oficial](https://sqlite.org/foreignkeys.html) |
| PostgreSQL | sí | servicio | [código](implementaciones/postgresql/consulta.sql) | [doc oficial](https://www.postgresql.org/docs/current/ddl-constraints.html) |
| MySQL | sí | servicio | [código](implementaciones/mysql/consulta.sql) | [doc oficial](https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html) |
| DuckDB | **no** | — | — | [doc oficial](https://duckdb.org/docs/stable/sql/statements/create_table.html) |
| MongoDB | **no** | — | — | [doc oficial](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/) |
| Apache Cassandra | **no** | — | — | [doc oficial](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html) |

### Los que resuelven el caso

#### SQLite · [`implementaciones/sqlite/consulta.sql`](implementaciones/sqlite/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: sqlite
-- doc: https://sqlite.org/foreignkeys.html
-- nota: sin PRAGMA foreign_keys = ON, todo lo de abajo se declara y NADA se
--       comprueba: el borrado de SE-201 dejaria inscripciones huerfanas y el
--       de DB-101 no fallaria. El verificador activa el pragma en cada
--       conexion; una aplicacion real tiene que hacer lo mismo.

-- === preparacion ===
PRAGMA foreign_keys = ON;

CREATE TABLE cursos (
    id     INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL
);
-- Una inscripcion a un curso que ya no existe no significa nada: se va con el.
CREATE TABLE inscripciones (
    estudiante TEXT NOT NULL,
    curso_id   INTEGER NOT NULL REFERENCES cursos(id) ON DELETE CASCADE,
    PRIMARY KEY (estudiante, curso_id)
);
-- Una evaluacion es evidencia academica: NO puede evaporarse por un borrado.
CREATE TABLE evaluaciones (
    id       INTEGER PRIMARY KEY,
    curso_id INTEGER NOT NULL REFERENCES cursos(id) ON DELETE RESTRICT,
    titulo   TEXT NOT NULL
);

INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20);
INSERT INTO evaluaciones (id, curso_id, titulo) VALUES (1, 10, 'Examen final');

-- Cae con sus inscripciones.
DELETE FROM cursos WHERE codigo = 'SE-201';

-- Este borrado lo IMPIDE el motor: DB-101 tiene evaluaciones.
-- Descomentar la linea siguiente hace fallar el guion, que es la prueba:
-- DELETE FROM cursos WHERE codigo = 'DB-101';

-- === consulta ===
SELECT c.codigo AS curso,
       COUNT(i.estudiante) AS inscripciones
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
```

- **Por qué sí:** Implementa las acciones referenciales del estándar, incluidas `CASCADE` y `RESTRICT`, con la misma sintaxis que los motores grandes.
- **Por qué no:** Las comprueba **solo si** `PRAGMA foreign_keys = ON` está activo en esa conexión, y por compatibilidad viene desactivado. Miles de bases SQLite en producción tienen claves foráneas declaradas que nunca se han comprobado.
- 📄 Documentación oficial: <https://sqlite.org/foreignkeys.html>

#### PostgreSQL · [`implementaciones/postgresql/consulta.sql`](implementaciones/postgresql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/ddl-constraints.html
-- nota: aqui el intento prohibido SI se ejecuta, dentro de un bloque que
--       captura el error: la prueba de que la restriccion actua queda en el
--       propio guion en vez de en un comentario.

-- === preparacion ===
DROP TABLE IF EXISTS evaluaciones, inscripciones, cursos;

CREATE TABLE cursos (
    id     integer PRIMARY KEY,
    codigo text NOT NULL
);
CREATE TABLE inscripciones (
    estudiante text NOT NULL,
    curso_id   integer NOT NULL REFERENCES cursos(id) ON DELETE CASCADE,
    PRIMARY KEY (estudiante, curso_id)
);
CREATE TABLE evaluaciones (
    id       integer PRIMARY KEY,
    curso_id integer NOT NULL REFERENCES cursos(id) ON DELETE RESTRICT,
    titulo   text NOT NULL
);

INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20);
INSERT INTO evaluaciones (id, curso_id, titulo) VALUES (1, 10, 'Examen final');

DELETE FROM cursos WHERE codigo = 'SE-201';

DO $$
BEGIN
    DELETE FROM cursos WHERE codigo = 'DB-101';
    RAISE EXCEPTION 'la restriccion no actuo: DB-101 no deberia poder borrarse';
EXCEPTION
    -- RESTRICT levanta restrict_violation (23001), no foreign_key_violation
    -- (23503): son dos codigos distintos y conviene no confundirlos.
    WHEN restrict_violation OR foreign_key_violation THEN
        RAISE NOTICE 'RESTRICT impidio el borrado, como debia';
END;
$$;

-- === consulta ===
SELECT c.codigo AS curso,
       COUNT(i.estudiante) AS inscripciones
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
```

- **Por qué sí:** Tiene todas las acciones del estándar y distingue `RESTRICT` de `NO ACTION`: la primera comprueba de inmediato, la segunda al final de la transacción si es diferible. Esa diferencia es la que permite reordenar datos dentro de una transacción sin desactivar nada.
- **Por qué no:** Un `DELETE` en cascada sobre una jerarquía profunda puede tocar millones de filas en una sola transacción sin que nadie lo haya pedido explícitamente: la cascada es cómoda y silenciosa a la vez.
- 📄 Documentación oficial: <https://www.postgresql.org/docs/current/ddl-constraints.html>

#### MySQL · [`implementaciones/mysql/consulta.sql`](implementaciones/mysql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html
-- nota: InnoDB comprueba las claves foraneas siempre, sin activar nada. Lo que
--       NO hace es disparar los triggers de las tablas hijas al cascadear: un
--       contador mantenido por trigger se desfasa justo ahi.

-- === preparacion ===
DROP TABLE IF EXISTS evaluaciones;
DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS cursos;

CREATE TABLE cursos (
    id     INT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE inscripciones (
    estudiante VARCHAR(50) NOT NULL,
    curso_id   INT NOT NULL,
    PRIMARY KEY (estudiante, curso_id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
) ENGINE=InnoDB;
CREATE TABLE evaluaciones (
    id       INT PRIMARY KEY,
    curso_id INT NOT NULL,
    titulo   VARCHAR(50) NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

INSERT INTO cursos (id, codigo) VALUES (10, 'DB-101'), (20, 'SE-201');
INSERT INTO inscripciones (estudiante, curso_id) VALUES
    ('Ada', 10), ('Linus', 10), ('Grace', 20);
INSERT INTO evaluaciones (id, curso_id, titulo) VALUES (1, 10, 'Examen final');

DELETE FROM cursos WHERE codigo = 'SE-201';

-- El borrado de DB-101 fallaria con el error 1451. Se deja fuera del guion
-- para que el resto se ejecute; probarlo a mano es parte del laboratorio.

-- === consulta ===
SELECT c.codigo AS curso,
       COUNT(i.estudiante) AS inscripciones
FROM cursos c
LEFT JOIN inscripciones i ON i.curso_id = c.id
GROUP BY c.id, c.codigo
ORDER BY c.codigo;
```

- **Por qué sí:** InnoDB comprueba las claves foráneas siempre, sin activar nada, y admite `CASCADE`, `RESTRICT` y `SET NULL`.
- **Por qué no:** Las cascadas de InnoDB **no disparan** los disparadores de las tablas hijas: un contador mantenido por disparador se queda desfasado justo cuando una cascada borra sus filas. Y `NO ACTION` se trata como `RESTRICT`: no hay comprobación diferida.
- 📄 Documentación oficial: <https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html>

### Los que no resuelven este caso — y qué se hace en su lugar

Descartar un motor con un argumento es tan formativo como usarlo. Ninguna de estas filas dice que el motor sea peor: dice que este problema no es el suyo.

| Motor | Por qué no | Qué se hace en su lugar | Fuente |
|---|---|---|---|
| DuckDB | Admite declarar claves foráneas, pero no las acciones referenciales de borrado: no hay `ON DELETE CASCADE` ni `RESTRICT` que aplicar. Su papel es analizar datos que otro sistema ya validó. | Borrar padre e hijos con dos sentencias dentro de la misma transacción, o —lo habitual en analítica— reconstruir la tabla completa desde el origen. | [doc](https://duckdb.org/docs/stable/sql/statements/create_table.html) |
| MongoDB | No hay claves foráneas ni acciones referenciales entre colecciones: si se borra el curso, las inscripciones que lo referencian quedan apuntando al vacío y ninguna consulta avisa. | Incrustar lo que no tiene sentido sin el padre —las inscripciones dentro del curso— para que borrar el documento las borre con él, y usar referencias solo para lo que sí sobrevive por su cuenta. | [doc](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/) |
| Apache Cassandra | No hay integridad referencial de ningún tipo: ninguna escritura consulta otra tabla, porque hacerlo obligaría a coordinar nodos en cada operación y eso es justo lo que su diseño evita. | Borrar en la aplicación todas las tablas afectadas, aceptando que un fallo a mitad deja filas huérfanas, y prever un trabajo de reparación periódico. | [doc](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html) |

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

- **E. F. Codd** (1979). [Extending the Database Relational Model to Capture More Meaning](https://dl.acm.org/doi/10.1145/320107.320109). ACM TODS 4(4). DOI [10.1145/320107.320109](https://doi.org/10.1145/320107.320109).  
  Introduce los valores nulos y la semántica de información faltante.
- **C. J. Date** (2015). [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/). 3.a ed. O'Reilly. ISBN 978-1-4919-4117-1.  
  Separa el modelo relacional de lo que SQL realmente implementa, incluidos los nulos.
- **PostgreSQL Global Development Group** (2026). [PostgreSQL Documentation](https://www.postgresql.org/docs/current/).  
  Documentación de referencia del motor relacional principal del programa.
- **ISO/IEC JTC 1/SC 32** (2023). [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html).  
  Norma del lenguaje SQL. Ningún motor la implementa por completo.

---

> [Programa](../../../README.md) · [Parte 02](../README.md) · [← Anterior](../../part-02-modelo-relacional-y-algebra/012-calculo-relacional-y-equivalencia/README.md) · [Siguiente →](../../part-03-sql-en-profundidad/014-ddl-el-esquema-como-contrato/README.md)
