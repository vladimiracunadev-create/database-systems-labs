# Laboratorio 04 — Índices y planes

Duración: 90 minutos. Dependencia: Python 3.11+ (SQLite en la biblioteca estándar). PostgreSQL, opcional.

## Hipótesis

Un índice compuesto por `(course_id, student_id)` reducirá trabajo para consultas que filtran por curso y localizan un estudiante, pero tendrá costo de escritura y no ayudará igual a los filtros que no empiezan por `course_id`.

## Ejecución

```bash
python labs/04-indexing/run_indexing_lab.py
```

Genera 20 000 filas deterministas y mide tres consultas antes y después de cada índice. Debe terminar con `INDEXING_LAB_OK`.

**Las aserciones son sobre el plan y sobre el trabajo, nunca sobre el tiempo.** El plan se obtiene con `EXPLAIN QUERY PLAN`; el trabajo se cuenta en instrucciones de la máquina virtual de SQLite con `set_progress_handler`. Un laboratorio que afirmara «baja de 40 ms a 3 ms» no sería repetible en otra máquina; «pasa de recorrer la tabla a buscar por índice» se sostiene en todas.

## Lo que aparece en la salida

- la consulta por `(course_id, student_id)` pasa de recorrer la tabla a una búsqueda por índice, con tres órdenes de magnitud menos de trabajo;
- el prefijo izquierdo (`course_id` solo) usa el mismo índice;
- filtrar solo por `student_id` es el caso interesante: con estadísticas y una primera columna de baja cardinalidad, el planificador puede recorrer el índice **por saltos** (`ANY(course_id)` en el plan, *skip-scan*) en vez de descartarlo. Sigue costando más que un índice dedicado, y que aparezca depende de la versión y de `ANALYZE`; por eso el laboratorio compara trabajo y no da por buena la forma del plan;
- insertar 5000 filas con dos índices cuesta más trabajo y más páginas que sin ellos.

## Protocolo para tu propio motor

1. Genera un dataset determinista y registra su tamaño.
2. Ejecuta calentamiento separado.
3. Captura `EXPLAIN` o equivalente sin índice.
4. Ejecuta al menos 15 repeticiones y conserva tiempos.
5. Crea el índice.
6. Actualiza estadísticas si el motor lo requiere (`ANALYZE`).
7. Repite exactamente la misma consulta.
8. Mide también una inserción por lote.

## Informe

Incluye plan, filas estimadas y reales cuando estén disponibles, mediana, dispersión, tamaño del índice, costo de escritura y conclusión limitada a la carga probada.
