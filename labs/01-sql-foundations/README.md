# Laboratorio 01 — Fundamentos de SQL sobre el dominio educativo

> El laboratorio que se da por supuesto en toda entrevista y que casi nadie hace bien:
> predecir el resultado **antes** de ejecutar la consulta.

**Duración:** 90 minutos · **Dependencias:** Python 3.11+ (SQLite en memoria)
· **Marca de éxito:** `LAB_OK`
· **Partes:** [00](../../classes/part-00-fundamentos-datos-sistemas-y-metodo/README.md) ·
[01](../../classes/part-01-modelado-conceptual-y-requisitos/README.md) ·
[02](../../classes/part-02-modelo-relacional-y-algebra/README.md) ·
[03](../../classes/part-03-sql-en-profundidad/README.md)

## 🎯 Qué demuestra

Que una consulta no se valida mirándola, sino comparándola con lo que devuelve sobre datos
conocidos. El guion carga el esquema y los datos canónicos del programa, ejecuta tres consultas
—matriculados activos por curso, promedios con calificaciones ausentes y entregas pendientes— y
**afirma** el resultado exacto de cada una.

Esa afirmación es el laboratorio: si alguien cambia el esquema, los datos o la consulta y el
resultado deja de cuadrar, falla en integración continua antes de llegar a nadie.

## 🔬 Hipótesis

1. El conteo de matriculados activos depende de la reunión y del filtro: cambiar el orden de
   `WHERE` y `JOIN` en una reunión externa cambia el resultado, no solo el estilo.
2. El promedio de un estudiante con una entrega ausente **no** es el mismo si la ausencia se
   modela con `NULL` que si se modela con cero.
3. Las entregas pendientes no se obtienen con `NOT IN` sobre una subconsulta que puede devolver
   nulos: ahí está el error silencioso más frecuente del oficio.

## ▶️ Ejecutar

```bash
python labs/01-sql-foundations/run_lab.py
```

El guion no crea archivos: SQLite trabaja en memoria y el proceso descarta los datos al salir.

## 📊 Lo que verás

```text
Active students: [('DB-101', 3), ('SE-201', 2)]
DB-101 averages: [('Estudiante Ada', 90.0), ('Estudiante Linus', 58.0), ('Estudiante Grace', 78.5)]
Pending submissions: [('Estudiante Linus', 'Consultas SQL'), ('Estudiante Grace', 'ADR inicial')]
LAB_OK
```

Fíjate en el promedio de Grace: 78,5 y no 52,3. Tiene dos evaluaciones y una entrega ausente;
`AVG` ignora el nulo en vez de contarlo como cero. Ese detalle decide si un informe académico es
correcto o injusto.

## 🧠 Por qué está hecho así

- **Datos canónicos y minúsculos.** Cuatro estudiantes y dos cursos caben en la cabeza: puedes
  predecir cada resultado a mano, que es justo el ejercicio.
- **Aserciones, no impresiones.** El guion no imprime «parece correcto»: compara con la lista
  exacta esperada. Un laboratorio que no puede fallar no prueba nada.
- **En memoria y sin dependencias.** Se ejecuta en cualquier máquina con Python, y la
  integración continua lo corre en 3.11, 3.12 y 3.13 para que no dependa de una versión.

## ⚠️ Lo que este laboratorio no demuestra

- No mide rendimiento: con veinte filas, cualquier plan es rápido. Eso se trabaja en el
  [laboratorio 04](../04-indexing/README.md).
- No cubre concurrencia: aquí hay un solo proceso. Eso es el [laboratorio 03](../03-transactions/README.md).
- SQLite es permisivo con los tipos; PostgreSQL o SQL Server rechazarían cosas que aquí pasan.
  Repite las consultas contra un motor estricto antes de sacar conclusiones de portabilidad.

## 🧪 Extensiones

1. Completa [`exercises.md`](exercises.md) **sin mirar** [`solution.sql`](solution.sql).
2. Añade un estudiante con dos matrículas y una entrega duplicada, y comprueba qué consulta
   empieza a contar de más. Ese es el mecanismo del doble conteo por reunión.
3. Cambia `LEFT JOIN` por `INNER JOIN` en la consulta de pendientes y explica por qué el
   resultado se vacía.
4. Sustituye el `NULL` de una calificación ausente por un cero y observa el promedio: decide
   cuál de las dos representaciones quiere el reglamento académico, y escríbelo.
5. Añade la restricción que impide que un estudiante entregue una evaluación de un curso en el
   que no está matriculado. Es una restricción, no una comprobación en la aplicación.

## 🎓 Dónde encaja

- **Clases:** de la [001](../../classes/part-00-fundamentos-datos-sistemas-y-metodo/001-que-resuelve-un-sistema-de-bases-de-datos/README.md)
  a la [019](../../classes/part-03-sql-en-profundidad/019-nulos-y-logica-de-tres-valores/README.md), y
  [051 — Inyección SQL](../../classes/part-10-operacion-seguridad-y-gobierno/051-inyeccion-sql-y-parametrizacion/README.md).
- **Rutas:** todas. Es el único laboratorio que aparece en las siete.
- **Certificaciones:** el dominio de conceptos relacionales del
  [DP-900](../../certificaciones/dp-900.md) se cubre entero aquí.

## 📖 Fuentes

- **SQLite Documentation** — el motor que ejecuta el laboratorio y sus particularidades de tipo.
- **Python: sqlite3** — la interfaz DB-API 2.0 que usa el guion.
- **ISO/IEC 9075** — la norma que define qué es SQL, y frente a la que se miden los dialectos.

Fichas completas en el [registro de fuentes](../../catalog/sources.json).

## 🧹 Limpieza

No es necesaria: SQLite se ejecuta en memoria y el proceso descarta los datos.
