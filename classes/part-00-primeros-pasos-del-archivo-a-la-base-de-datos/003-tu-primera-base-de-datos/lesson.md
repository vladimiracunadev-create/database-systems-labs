## Propósito

Crear una base de datos, una tabla y guardar datos dentro, con la menor cantidad
de ceremonia posible. Al terminar esta clase habrás ejecutado las tres órdenes
que sostienen todo lo demás —`CREATE TABLE`, `INSERT` y `SELECT`— y sabrás qué
hace cada una.

## Resultados de aprendizaje

Al terminar podrás:

1. Crear una tabla declarando sus campos y sus tipos.
2. Insertar filas y leerlas.
3. Explicar la diferencia entre **definir** el esquema y **modificar** los datos.
4. Reconocer el error de sintaxis más común y corregirlo sin buscarlo.
5. Nombrar la fuente de cada afirmación anterior.

## Fundamentos

### Tres órdenes y dos familias

Todo lo que se hace con SQL cae en dos familias, y conviene separarlas desde el
primer día:

| Familia | Qué hace | Órdenes |
|---|---|---|
| **Definición** (DDL) | Describe la **forma** de los datos | `CREATE`, `ALTER`, `DROP` |
| **Manipulación** (DML) | Trabaja con los **datos** | `INSERT`, `SELECT`, `UPDATE`, `DELETE` |

La distinción importa porque las dos familias se usan en momentos distintos: la
definición, pocas veces y con cuidado; la manipulación, todo el rato. Y porque
en la mayoría de los motores un cambio de definición **no se puede deshacer** con
la misma facilidad que un cambio de datos.

### `CREATE TABLE`: declarar la forma

```sql
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT
);
```

Se lee de arriba abajo: una tabla llamada `estudiantes`, con tres campos. `id` es
un número entero y es la clave primaria —el campo que distingue una fila de otra,
que se estudiará en su propia clase—. `nombre` es texto y **no puede quedar
vacío**. `correo` es texto y sí puede.

Eso es todo lo que hace `CREATE TABLE`: escribir en el catálogo del motor cómo
tienen que ser las filas de esa tabla. No guarda ningún dato.

### `INSERT`: añadir filas

```sql
INSERT INTO estudiantes (id, nombre, correo)
VALUES (1, 'Ada Lovelace', 'ada@example.org');
```

Se nombran los campos que se van a rellenar y se dan los valores en el mismo
orden. Nombrar los campos parece redundante y no lo es: el día que la tabla gane
una columna, el `INSERT` que no los nombraba deja de funcionar o, peor, empieza a
poner cada valor en el sitio equivocado.

**El texto va entre comillas simples. Los números, no.** Es el error de sintaxis
más frecuente de las primeras horas, y da un mensaje distinto en cada motor.

### `SELECT`: leer

```sql
SELECT nombre, correo FROM estudiantes;
```

«De la tabla `estudiantes`, dame los campos `nombre` y `correo` de todas las
filas.» El `*` sirve para pedir todos los campos, y conviene acostumbrarse a **no
usarlo** fuera de la exploración: una consulta con `SELECT *` cambia de resultado
cuando alguien añade una columna, y quien la escribió ya no está para explicarlo.

### Dónde ocurre todo esto

Para esta clase no hace falta instalar nada: SQLite viene incluido con Python, y
una base de datos es un archivo —o ni siquiera eso, si se pide en memoria—. El
laboratorio del repositorio funciona así, y por eso se puede ejecutar en
cualquier máquina.

```mermaid
flowchart LR
    A["CREATE TABLE<br/>declara la forma"] --> B["INSERT<br/>añade filas"]
    B --> C["SELECT<br/>lee filas"]
    C -->|"la forma no cambia"| B
```

## Ejemplo trabajado

Una academia quiere registrar sus tres primeros estudiantes.

```sql
CREATE TABLE estudiantes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT
);

INSERT INTO estudiantes (id, nombre, correo) VALUES (1, 'Ada Lovelace', 'ada@example.org');
INSERT INTO estudiantes (id, nombre, correo) VALUES (2, 'Linus Torvalds', 'linus@example.org');
INSERT INTO estudiantes (id, nombre, correo) VALUES (3, 'Grace Hopper', NULL);

SELECT id, nombre FROM estudiantes ORDER BY nombre;
```

Resultado:

| id | nombre |
|---|---|
| 1 | Ada Lovelace |
| 3 | Grace Hopper |
| 2 | Linus Torvalds |

**Tres cosas que merece la pena mirar.**

El orden del resultado **no** es el de inserción: es el que pidió `ORDER BY`. Sin
esa cláusula, ningún motor está obligado a devolver las filas en un orden
concreto, aunque en una tabla pequeña casi siempre lo parezca. Es una de las
confusiones más persistentes y tiene su propia clase más adelante.

`NULL` —sin comillas— no es la palabra «NULL»: es la marca de **ausencia de
valor**. Grace no tiene correo, y eso es distinto de tener un correo vacío.

Y si se intenta insertar un cuarto estudiante con `id` 1, el motor lo rechaza:
la clave primaria no admite repetidos. Esa negativa es exactamente lo que se
compró al elegir una base de datos.

## Errores frecuentes

1. **Olvidar las comillas en el texto o ponerlas en los números.** `VALUES (1,
   Ada)` falla; `VALUES ('1', 'Ada')` a veces funciona y guarda el número como
   texto, que es peor.
2. **Usar comillas dobles para el texto.** En SQL estándar, las comillas dobles
   son para los **nombres** de tabla y columna; el texto va en comillas simples.
   Algunos motores lo perdonan y otros no.
3. **`INSERT` sin nombrar los campos.** Funciona hasta que la tabla cambia.
4. **Confundir `NULL` con `'NULL'`.** El primero es ausencia de valor; el segundo
   es un texto de cuatro letras.
5. **Suponer que el orden de salida es el de entrada.** Sin `ORDER BY` no hay
   orden garantizado.
6. **Ejecutar `DROP TABLE` para «volver a empezar» en la base equivocada.** La
   definición no se deshace con `Ctrl+Z`.

## Ejemplo de transferencia

Estas tres órdenes son las mismas —con diferencias mínimas de sintaxis— en
PostgreSQL, MySQL, SQL Server, Oracle y DuckDB. Lo que se aprende aquí no es
SQLite: es el subconjunto de SQL que la norma ISO/IEC 9075 define y que todos
implementan. Cambiar de motor no obliga a reaprender esto.

## Reto de transferencia

1. Crea una tabla para algo que lleves de verdad: libros, gastos, plantas,
   partidas. Declara al menos cuatro campos y decide cuáles no pueden quedar
   vacíos.
2. Inserta cinco filas, y que una de ellas tenga un campo sin valor.
3. Escribe tres consultas distintas sobre esos datos.
4. Intenta insertar una fila que viole una de tus reglas, y **guarda el mensaje
   de error**: es la prueba de que la regla existe.

## Preguntas de evaluación

1. ¿Qué diferencia hay entre la familia de definición y la de manipulación?
2. ¿Por qué conviene nombrar los campos en un `INSERT`?
3. ¿Qué significa `NOT NULL` y qué ocurre exactamente al violarlo?
4. Explica por qué `SELECT *` es cómodo para explorar y mala idea en el código de
   una aplicación.
