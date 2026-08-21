## Propósito

Dar el paso que separa «guardar datos» de «modelar»: **partir una tabla en dos y
relacionarlas**. Es el momento en que aparecen las claves foráneas, y con ellas
la posibilidad de que el sistema impida por sí solo que un dato apunte a algo que
no existe.

## Resultados de aprendizaje

Al terminar podrás:

1. Reconocer cuándo una tabla está guardando dos cosas distintas.
2. Partirla en dos y relacionarlas con una clave foránea.
3. Consultar las dos tablas juntas con una reunión.
4. Explicar qué impide exactamente una clave foránea y qué no.
5. Nombrar la fuente de cada afirmación anterior.

## Fundamentos

### La señal: el dato que se repite

Cuando una tabla repite el mismo valor en muchas filas, casi siempre está
guardando dos cosas a la vez:

| estudiante | correo | curso | profesor |
|---|---|---|---|
| Ada | ada@example.org | DB-101 | A. Lovelace |
| Ada | ada@example.org | SE-201 | G. Hopper |
| Linus | linus@example.org | DB-101 | A. Lovelace |

El correo de Ada está dos veces. El profesor de DB-101, también. Eso produce tres
problemas con nombre propio, que se estudiarán en detalle en la parte de
normalización:

- **Anomalía de actualización.** Corregir el correo de Ada exige tocar dos filas,
  y basta olvidar una para que Ada tenga dos correos distintos.
- **Anomalía de inserción.** No se puede registrar un curso que todavía no tiene
  estudiantes: no habría fila donde ponerlo.
- **Anomalía de borrado.** Si Linus abandona y era el único de DB-101, al borrar
  su fila desaparece también el curso y su profesor.

### La solución: una tabla por cosa

```sql
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE
);

CREATE TABLE cursos (
    id       INTEGER PRIMARY KEY,
    codigo   TEXT NOT NULL UNIQUE,
    profesor TEXT NOT NULL
);

CREATE TABLE inscripciones (
    estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id),
    curso_id      INTEGER NOT NULL REFERENCES cursos(id),
    PRIMARY KEY (estudiante_id, curso_id)
);
```

Cada hecho vive **una sola vez**. El correo de Ada está en una fila; el profesor
de DB-101, en otra. Y la tercera tabla —la de inscripciones— guarda la relación:
una fila por pareja.

### Qué es una clave foránea

`REFERENCES estudiantes(id)` declara que ese campo **tiene que existir** en la
otra tabla. A partir de ahí, el motor impide dos cosas:

1. **Insertar una inscripción de un estudiante que no existe.**
2. **Borrar un estudiante que todavía tiene inscripciones** —salvo que se declare
   qué hacer en ese caso, que es una decisión de diseño con su propia clase.

Eso es todo lo que impide, y conviene saberlo: **no** obliga a que un estudiante
tenga al menos una inscripción, y **no** comprueba nada sobre el contenido de los
demás campos.

### Un aviso importante en SQLite

SQLite **solo comprueba las claves foráneas si se activan en la conexión**:

```sql
PRAGMA foreign_keys = ON;
```

Por compatibilidad con versiones antiguas viene desactivado. Hay muchísimas bases
SQLite en producción con claves foráneas declaradas que nunca se han comprobado.

### Volver a juntarlas: la reunión

Partir en tres tablas no significa perder la vista completa. `JOIN` las vuelve a
unir en el momento de consultar:

```sql
SELECT e.nombre, c.codigo, c.profesor
FROM inscripciones i
JOIN estudiantes e ON e.id = i.estudiante_id
JOIN cursos      c ON c.id = i.curso_id
ORDER BY e.nombre, c.codigo;
```

La condición `ON` dice **cómo se emparejan** las filas. Sin ella, el motor
combinaría cada fila con todas las de la otra tabla, que casi nunca es lo que se
quiere.

```mermaid
flowchart LR
    E["estudiantes<br/>id, nombre, correo"] --- I["inscripciones<br/>estudiante_id, curso_id"]
    I --- C["cursos<br/>id, codigo, profesor"]
```

## Ejemplo trabajado

Partiendo de la tabla única del principio, con los mismos datos:

```sql
INSERT INTO estudiantes (id, nombre, correo) VALUES
    (1, 'Ada', 'ada@example.org'),
    (2, 'Linus', 'linus@example.org');

INSERT INTO cursos (id, codigo, profesor) VALUES
    (10, 'DB-101', 'A. Lovelace'),
    (20, 'SE-201', 'G. Hopper');

INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (1, 10), (1, 20), (2, 10);
```

**Prueba 1: corregir el correo de Ada.**

```sql
UPDATE estudiantes SET correo = 'ada@nuevo.org' WHERE id = 1;
```

Una fila. En la tabla única habrían sido dos, y en un sistema real, cientos.

**Prueba 2: registrar un curso sin estudiantes.**

```sql
INSERT INTO cursos (id, codigo, profesor) VALUES (30, 'AR-301', 'M. Hamilton');
```

Se puede. En la tabla única, no había dónde ponerlo.

**Prueba 3: intentar inscribir a alguien que no existe.**

```sql
INSERT INTO inscripciones (estudiante_id, curso_id) VALUES (99, 10);
```

El motor lo rechaza: `FOREIGN KEY constraint failed`. Sin la clave foránea, esa
fila entraría y quedaría un huérfano que ninguna consulta encontraría.

**Prueba 4: la vista completa, cuando hace falta.**

```sql
SELECT e.nombre, c.codigo, c.profesor
FROM inscripciones i
JOIN estudiantes e ON e.id = i.estudiante_id
JOIN cursos      c ON c.id = i.curso_id
ORDER BY e.nombre, c.codigo;
```

| nombre | codigo | profesor |
|---|---|---|
| Ada | DB-101 | A. Lovelace |
| Ada | SE-201 | G. Hopper |
| Linus | DB-101 | A. Lovelace |

Los mismos datos del principio, sin ninguna repetición guardada.

## Errores frecuentes

1. **No activar `PRAGMA foreign_keys = ON` en SQLite.** Las restricciones están
   declaradas y no comprueban nada.
2. **Declarar la clave foránea y no indexarla.** El campo referenciado ya tiene
   índice por ser clave primaria; el que **referencia**, no, y las consultas y
   los borrados en cascada lo pagan.
3. **Reunir sin condición `ON`.** Devuelve el producto de las dos tablas: con
   1000 y 1000 filas, un millón.
4. **Copiar el nombre además del identificador «para no tener que reunir».** El
   día que el nombre cambie, la copia queda desactualizada; eso es
   desnormalización, y se hace a propósito o no se hace.
5. **Partir en tablas por costumbre.** Si un dato pertenece a una sola cosa y no
   se comparte, no hace falta otra tabla.

## Ejemplo de transferencia

La misma decisión existe fuera del modelo relacional, con otro nombre: en
MongoDB se llama «incrustar o referenciar», y la regla se parece —se incrusta lo
que solo tiene sentido dentro de su padre, se referencia lo que se comparte—. La
diferencia grande es que allí **no hay clave foránea**: si se borra el curso, las
inscripciones siguen apuntando al vacío y ninguna consulta avisa.

## Reto de transferencia

1. Busca una tabla real con un dato repetido en muchas filas.
2. Escribe las tablas en que la partirías y la clave foránea que las une.
3. Ejecuta el `UPDATE` que corrige ese dato repetido en la versión original y
   cuenta cuántas filas cambia; hazlo después en la versión partida.
4. Intenta insertar una referencia a algo que no existe y guarda el mensaje de
   error.

## Preguntas de evaluación

1. Nombra las tres anomalías que produce guardar dos cosas en una tabla.
2. ¿Qué impide exactamente una clave foránea, y qué **no** impide?
3. ¿Por qué en SQLite una clave foránea puede no estar comprobando nada?
4. ¿Qué devuelve una reunión escrita sin condición `ON`, y por qué casi nunca es
   lo que se quería?
