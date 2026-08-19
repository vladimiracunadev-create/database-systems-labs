# Laboratorio 04 — Índices y planes

## Hipótesis

Un índice compuesto por `(course_id, student_id)` reducirá trabajo para consultas que filtran por curso y localizan un estudiante, pero tendrá costo de escritura y no necesariamente ayudará a filtros por `student_id` solamente.

## Protocolo

1. Genera un dataset determinista y registra su tamaño.
2. Ejecuta calentamiento separado.
3. Captura `EXPLAIN` o equivalente sin índice.
4. Ejecuta al menos 15 repeticiones y conserva tiempos.
5. Crea el índice.
6. Actualiza estadísticas si el motor lo requiere.
7. Repite exactamente la misma consulta.
8. Mide también una inserción por lote.

## Informe

Incluye plan, filas estimadas y reales cuando estén disponibles, mediana, dispersión, tamaño del índice, costo de escritura y conclusión limitada a la carga probada.
