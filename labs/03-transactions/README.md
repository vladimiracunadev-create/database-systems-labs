# Laboratorio 03 — Transacciones y concurrencia

## Escenario

Dos procesos intentan reservar el último cupo de un curso. Una secuencia “leer cupos, comprobar, actualizar” puede aceptar ambos si no existe protección concurrente.

## Experimento

1. Crea `course_capacity(course_id, capacity, occupied, version)`.
2. Abre dos sesiones.
3. Lee `occupied` en ambas antes de actualizar.
4. Ejecuta las actualizaciones y registra el resultado.
5. Repite con:
   - actualización atómica condicionada;
   - bloqueo de fila;
   - control optimista por versión.

Actualización atómica orientativa:

```sql
UPDATE course_capacity
SET occupied = occupied + 1
WHERE course_id = :course_id AND occupied < capacity;
```

El cliente debe comprobar filas afectadas. El marcador `:course_id` representa un parámetro del driver, no concatenación.

## Evidencia

Cronología de ambas sesiones, nivel de aislamiento, filas afectadas y prueba de que `occupied <= capacity` siempre se mantiene.
