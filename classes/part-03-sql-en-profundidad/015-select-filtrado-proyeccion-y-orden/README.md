# 015 — SELECT: filtrado, proyección y orden con semántica precisa

> [Programa](../../../README.md) · [Parte 03](../README.md) · [← Anterior](../../part-03-sql-en-profundidad/014-ddl-el-esquema-como-contrato/README.md) · [Siguiente →](../../part-03-sql-en-profundidad/016-reuniones-inner-outer-semi-y-anti/README.md)

| | |
|---|---|
| **Parte** | 03 — SQL en profundidad |
| **Nivel** | Fundamentos |
| **Horas estimadas** | 3 |
| **Motores** | `postgresql`, `sqlite` |
| **Laboratorio** | [`labs/01-sql-foundations`](../../../labs/01-sql-foundations/README.md) |
| **Fuentes** | 3 |

**Conceptos centrales:** `predicado` · `orden de evaluación` · `colación` · `determinismo de orden`

---

## Propósito

Escribir `SELECT` sabiendo exactamente qué devuelve. La mayoría de los errores de consulta no son de sintaxis: son de semántica, y aparecen cuando los datos cambian.

## Resultados de aprendizaje

Al terminar podrás:

1. Enunciar el orden lógico de evaluación de una consulta y usarlo para explicar errores.
2. Distinguir orden lógico de orden físico de ejecución.
3. Escribir un `ORDER BY` determinista y explicar por qué hace falta.
4. Prever el efecto de la colación en comparaciones y ordenaciones.
5. Paginar sin saltarse ni repetir filas.

## Fundamentos

### El orden lógico

SQL se escribe en un orden y se evalúa en otro. El orden lógico definido por la norma es:

```text
1. FROM      (y los JOIN)
2. WHERE
3. GROUP BY
4. HAVING
5. SELECT    (incluidas las funciones de ventana)
6. DISTINCT
7. ORDER BY
8. LIMIT / OFFSET
```

De aquí salen, sin más teoría, tres reglas que suelen memorizarse mal:

- **No se puede usar un alias de `SELECT` en `WHERE`.** En el paso 2 ese alias todavía no existe. Sí se puede en `ORDER BY`, porque es posterior.
- **`WHERE` filtra filas; `HAVING` filtra grupos.** Poner una condición de fila en `HAVING` funciona pero agrupa de más y es más lento.
- **Las funciones de ventana no se pueden filtrar en `WHERE`.** Se calculan en el paso 5. Para filtrarlas hace falta una subconsulta o una CTE (clase 018).

El orden **físico** es otro: el motor aplica las equivalencias de la clase 011 y puede filtrar antes de reunir. Ambas cosas conviven porque el resultado es el mismo.

### El orden de las filas no existe

Sin `ORDER BY`, el orden de salida es un accidente del plan. Con `ORDER BY` sobre una columna con valores repetidos, el orden entre las filas empatadas **tampoco** está definido.

Esto rompe la paginación por desplazamiento:

```sql
SELECT * FROM students ORDER BY nombre LIMIT 20 OFFSET 0;   -- página 1
SELECT * FROM students ORDER BY nombre LIMIT 20 OFFSET 20;  -- página 2
```

Con dos estudiantes llamados «Ana Pérez», su orden relativo puede cambiar entre las dos consultas: uno aparece en ambas páginas y otro en ninguna. La solución es un **orden total**, añadiendo una columna única como desempate:

```sql
SELECT * FROM students ORDER BY nombre, id LIMIT 20 OFFSET 20;
```

### Paginación por clave

`OFFSET` tiene además un problema de costo: para saltar 100 000 filas, el motor las produce y las descarta. El costo crece con el número de página. La alternativa es la paginación por clave (*keyset*), que recuerda dónde se quedó:

```sql
-- primera página
SELECT id, nombre FROM students ORDER BY nombre, id LIMIT 20;
-- siguiente, con el último par visto
SELECT id, nombre FROM students
WHERE (nombre, id) > ('Ana Pérez', 412)
ORDER BY nombre, id LIMIT 20;
```

La comparación de tuplas `(a, b) > (x, y)` es la forma correcta y está en la norma. Con un índice sobre `(nombre, id)`, el costo es constante por página, no creciente. Winand desarrolla este punto como uno de los usos canónicos del índice compuesto.

### Colación

La colación decide cómo se comparan y ordenan los textos: si `'a' = 'A'`, dónde va la «ñ», si los acentos importan.

| Motor | Comportamiento por defecto |
|---|---|
| PostgreSQL | Sensible a mayúsculas; colación del `initdb` (a menudo del sistema) |
| MySQL | Históricamente **insensible** a mayúsculas (`utf8mb4_0900_ai_ci`) |
| SQLite | `BINARY`: sensible a mayúsculas y solo ASCII en `NOCASE` |
| SQL Server | Depende de la instalación; suele ser insensible |

Esa diferencia hace que `WHERE email = 'ANA@X.CL'` encuentre la fila en MySQL y no en PostgreSQL. Es la causa de portabilidad más subestimada (clase 022). La defensa es normalizar explícitamente al escribir —guardar el correo en minúsculas— en vez de depender de la colación.

## Ejemplo trabajado

```sql
SELECT s.nombre,
       AVG(e.nota) AS promedio
FROM students s
JOIN enrollments e ON e.student_id = s.id
WHERE promedio > 5.0            -- ERROR
GROUP BY s.nombre;
```

Falla porque en el paso 2 (`WHERE`) el alias `promedio` no existe y la agregación aún no se ha hecho. La forma correcta usa `HAVING`:

```sql
SELECT s.id, s.nombre, AVG(e.nota) AS promedio
FROM students s
JOIN enrollments e ON e.student_id = s.id
GROUP BY s.id, s.nombre
HAVING AVG(e.nota) > 5.0
ORDER BY promedio DESC, s.id;
```

Detalles que no son adorno:

- Se agrupa por `s.id` además de `s.nombre`: dos estudiantes homónimos se contarían como uno solo al agrupar solo por nombre. Un error de resultado, no de estilo.
- `ORDER BY promedio DESC, s.id` usa el alias (permitido en el paso 7) y desempata con la clave.

**Filtro de fila frente a filtro de grupo.** Comparemos:

```sql
-- A: filtra filas antes de agrupar
SELECT e.course_id, AVG(e.nota)
FROM enrollments e
WHERE e.estado = 'activa'
GROUP BY e.course_id;

-- B: filtra grupos después
SELECT e.course_id, AVG(e.nota)
FROM enrollments e
GROUP BY e.course_id
HAVING MIN(e.estado) = 'activa';
```

No son equivalentes ni en resultado ni en costo. A calcula el promedio **solo** de las activas; B calcula el promedio de todas y luego descarta grupos. Con 240 000 inscripciones de las que 200 000 están activas, A agrega 200 000 filas y B agrega 240 000 para descartar después. La regla: **filtrar lo antes posible**, que es la equivalencia E2 de la clase 011 aplicada a mano.

**Paginación, medición.** Sobre 5 millones de filas con índice en `(nombre, id)`:

```text
OFFSET 0        →  20 filas producidas
OFFSET 100 000  →  100 020 filas producidas, 100 000 descartadas
keyset          →  20 filas producidas, siempre
```

## Comparación

| Necesidad | Construcción correcta | Trampa habitual |
|---|---|---|
| Filtrar filas | `WHERE` | Hacerlo en `HAVING` |
| Filtrar agregados | `HAVING` | Intentarlo en `WHERE` |
| Filtrar ventanas | Subconsulta o CTE | Intentarlo en `WHERE` |
| Orden estable | `ORDER BY` con columna única final | Confiar en el orden natural |
| Paginar mucho | Paginación por clave | `OFFSET` creciente |
| Comparar texto | Normalizar al escribir | Depender de la colación |

## Errores frecuentes

1. **Paginar con `OFFSET` sobre un orden no total.** Filas repetidas y filas perdidas, sin ningún error visible.
2. **Agrupar por el nombre y no por la clave.** Fusiona homónimos en silencio.
3. **`SELECT *` con `JOIN`.** Trae columnas duplicadas y ata el cliente al esquema.
4. **Suponer que `WHERE` y `HAVING` son intercambiables.** Cambian el resultado cuando hay agregados.
5. **Confiar en la insensibilidad a mayúsculas.** Funciona en MySQL y falla al migrar a PostgreSQL.
6. **`LIMIT` sin `ORDER BY`.** Devuelve «20 filas cualesquiera», que pueden ser otras 20 en la siguiente ejecución.

## De la clase a la operación

Las listas paginadas con elementos que se repiten o desaparecen son un clásico de los informes de error de usuario, y casi siempre se atribuyen al *frontend*. Casi siempre son un `ORDER BY` sin desempate.

## Reto de transferencia

1. Encuentra una consulta paginada real y demuestra con datos que su orden no es total.
2. Conviértela a paginación por clave y mide el costo en la página 1 y en la 5 000.
3. Reescribe una consulta que use `HAVING` para filtrar filas y compara los planes.
4. Documenta la colación por defecto de tu motor y una consulta cuyo resultado cambiaría al migrar.

## Preguntas de evaluación

1. Explica con el orden lógico por qué un alias funciona en `ORDER BY` y no en `WHERE`.
2. Da un caso donde `WHERE` y `HAVING` produzcan resultados distintos, con datos.
3. ¿Por qué la paginación por clave necesita un índice sobre exactamente las columnas del `ORDER BY`?
4. Tu aplicación funciona en MySQL y falla en PostgreSQL al buscar correos. Diagnostica y propón la corrección definitiva.

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

- **C. J. Date** (2015). [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/). 3.a ed. O'Reilly. ISBN 978-1-4919-4117-1.  
  Separa el modelo relacional de lo que SQL realmente implementa, incluidos los nulos.
- **Anthony Molinaro, Robert de Graaf** (2020). [SQL Cookbook](https://www.oreilly.com/library/view/sql-cookbook-2nd/9781492077435/). 2.a ed. O'Reilly. ISBN 978-1-4920-7744-2.  
  Recetas comparadas entre dialectos, útil para la matriz de portabilidad.
- **SQLite Consortium** (2026). [SQLite Documentation](https://sqlite.org/docs.html).  
  Motor embebido usado por los laboratorios sin dependencias del programa.

---

> [Programa](../../../README.md) · [Parte 03](../README.md) · [← Anterior](../../part-03-sql-en-profundidad/014-ddl-el-esquema-como-contrato/README.md) · [Siguiente →](../../part-03-sql-en-profundidad/016-reuniones-inner-outer-semi-y-anti/README.md)
