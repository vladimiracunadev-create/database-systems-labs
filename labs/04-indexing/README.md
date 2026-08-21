# Laboratorio 04 — Planes de ejecución y costo real de un índice

> Las aserciones son sobre el **plan** y sobre el **trabajo**, nunca sobre el tiempo. Un
> milisegundo depende de tu portátil; un recorrido de tabla, no.

**Duración:** 90 minutos · **Dependencias:** Python 3.11+ (SQLite). PostgreSQL, opcional
· **Marca de éxito:** `INDEXING_LAB_OK`
· **Parte:** [08 — Almacenamiento, índices y planes](../../classes/part-09-almacenamiento-indices-y-planes/README.md)

## 🎯 Qué demuestra

Que un índice no es «más rápido» en abstracto: cambia el plan que el motor puede elegir, y ese
cambio se paga en cada escritura. El laboratorio mide las dos caras sobre 20 000 filas
deterministas.

## 🔬 Hipótesis

1. Sin índices, las tres consultas recorrerán la tabla entera.
2. Un índice compuesto `(course_id, student_id)` servirá para filtrar por ambas columnas y
   también por el **prefijo izquierdo** `course_id` solo.
3. Filtrar solo por `student_id` —la segunda columna— no se resolverá igual de bien.
4. Mantener dos índices encarecerá una carga de 5000 inserciones, en trabajo y en páginas.

## ▶️ Ejecutar

```bash
python labs/04-indexing/run_indexing_lab.py
```

## 📊 Lo que verás

| Consulta | Sin índices | Con índice compuesto | Con ambos índices |
| --- | ---: | ---: | ---: |
| `course_id` + `student_id` | 60 810 pasos · `SCAN` | 20 pasos · `SEARCH … (course_id=? AND student_id=?)` | 10 pasos |
| `course_id` (prefijo) | 61 610 pasos · `SCAN` | 2 810 pasos · `SEARCH … (course_id=?)` | 2 820 pasos |
| `student_id` (no prefijo) | 60 210 pasos · `SCAN` | 760 pasos · `SEARCH … (ANY(course_id) AND student_id=?)` | 370 pasos · índice dedicado |

Costo de escritura de 5000 inserciones: **100 000 pasos y 29 páginas** sin índices secundarios,
frente a **160 000 pasos y 59 páginas** con dos. El índice no es gratis; es una apuesta a que
lees más de lo que escribes.

## 🧠 Por qué está hecho así

- **El trabajo se cuenta en instrucciones de la máquina virtual** con `set_progress_handler`, no
  con un cronómetro. Es determinista para un plan dado y comparable entre ejecuciones.
- **Los datos se generan con un primo** (7919) que no divide al número de cursos ni al de
  estudiantes: así no hay correlación artificial entre columnas que falsee la selectividad.
- **La tercera consulta es la interesante.** Con estadísticas y una primera columna de baja
  cardinalidad, SQLite puede recorrer el índice **por saltos** (*skip-scan*, visible como
  `ANY(course_id)` en el plan) en vez de descartarlo. Sigue costando el doble que un índice
  dedicado, y que aparezca depende de la versión y de `ANALYZE`. Por eso el laboratorio compara
  trabajo en lugar de dar por buena una forma concreta de plan: una aserción sobre el texto del
  plan se rompería con la próxima versión del motor sin que nada estuviera mal.

## ⚠️ Lo que este laboratorio no demuestra

- No mide latencia ni rendimiento bajo carga concurrente.
- No cubre índices parciales, cubrientes, GIN, GiST ni BRIN: eso es la
  [clase 041](../../classes/part-09-almacenamiento-indices-y-planes/051-indices-especializados/README.md).
- El planificador de SQLite es más simple que el de PostgreSQL u Oracle; las **formas** se
  transfieren, los costes concretos no.
- No modela fragmentación ni mantenimiento del índice a lo largo del tiempo.

## 🧪 Extensiones

1. Invierte el orden del índice a `(student_id, course_id)` y repite: cambia qué consulta gana.
   El orden de las columnas **es** la decisión de diseño.
2. Ejecuta sin `ANALYZE` y observa si el skip-scan desaparece: las estadísticas cambian los
   planes, y por eso se mantienen.
3. Sube a 200 000 filas y comprueba que las proporciones se mantienen aunque los números crezcan.
4. Añade un tercer índice y vuelve a medir la carga: la penalización de escritura es acumulativa.

## 🏭 Llevarlo a un motor real

```bash
docker compose --profile relational up -d
```

En PostgreSQL usa `EXPLAIN (ANALYZE, BUFFERS)` para ver filas estimadas frente a reales y páginas
tocadas; en MySQL, `EXPLAIN ANALYZE`. Protocolo honesto para medir tiempos: calentamiento
aparte, al menos quince repeticiones, mediana y dispersión, y declarar la máquina.

## 🎓 Dónde encaja

- **Clases:** [038–042](../../classes/part-09-almacenamiento-indices-y-planes/README.md), en
  especial [039 — B-tree, orden de columnas y selectividad](../../classes/part-09-almacenamiento-indices-y-planes/049-b-tree-orden-de-columnas-y-selectividad/README.md)
  y [042 — Planes de ejecución y refutación](../../classes/part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md).
- **Rutas:** [Desarrollador de aplicaciones](../../rutas/desarrollo-de-aplicaciones.md),
  [DBA / SRE de datos](../../rutas/fiabilidad-y-operacion.md),
  [Analytics engineer / BI](../../rutas/analitica-y-bi.md).
- **Certificaciones:** cubre el dominio de monitorización y optimización de recursos del
  [DP-300](../../certificaciones/dp-300.md) —revisar planes, índices y estadísticas—.

## 📖 Fuentes

- **Markus Winand**, *SQL Performance Explained* — el índice explicado desde la consulta, que es
  como hay que leerlo.
- **SQLite: Query Optimizer Overview** — incluido el recorrido por saltos que aparece en la
  salida.
- **PostgreSQL: Using EXPLAIN** — cómo se lee un plan en un motor serio.
- **Rudolf Bayer, Edward McCreight** (1972) — el artículo del B-tree, que sigue siendo la
  estructura por debajo de casi todo esto.

Fichas completas en el [registro de fuentes](../../catalog/sources.json).

## 🧹 Limpieza

No hace falta: todo ocurre en memoria.
