# Laboratorio 03 — Transacciones y concurrencia

Duración: 90 minutos. Dependencia: Python 3.11+ (SQLite en la biblioteca estándar). PostgreSQL, opcional.

## Escenario

Dos procesos intentan reservar el último cupo de un curso. Una secuencia “leer cupos, comprobar, actualizar” puede aceptar ambos si no existe protección concurrente.

## Ejecución

```bash
python labs/03-transactions/run_transactions_lab.py
```

El script lanza dos hilos reales contra la misma base y los sincroniza en una barrera para forzar el entrelazado peligroso. Debe terminar con `TRANSACTIONS_LAB_OK`.

Compara cuatro clientes sobre el mismo escenario:

| Cliente | Mecanismo | Reservas aceptadas para una plaza |
| --- | --- | ---: |
| leer-modificar-escribir | ninguno | 2 |
| actualización atómica | condición dentro del `UPDATE` | 1 |
| control optimista | `WHERE version = ?` y reintento | 1 |
| bloqueo pesimista | `BEGIN IMMEDIATE` | 1 |

La primera fila es el fallo, reproducido de forma repetible: dos clientes se llevan la misma plaza y el contador solo registra una de las dos escrituras. La actualización perdida no es una anécdota, es el resultado esperado de decidir con un valor caducado.

## Experimento

1. Ejecuta el script y anota la salida.
2. Sube `CAPACIDAD` y `CLIENTES`: comprueba que el invariante se mantiene.
3. Quita la barrera y observa cuántas ejecuciones hacen falta para ver el fallo sin sincronización.
4. Repite el escenario contra PostgreSQL en contenedor y anota qué cambia con `READ COMMITTED` y con `SERIALIZABLE`:

   ```bash
   docker compose --profile relational up -d
   ```

Actualización atómica orientativa:

```sql
UPDATE course_capacity
SET occupied = occupied + 1
WHERE course_id = :course_id AND occupied < capacity;
```

El cliente debe comprobar filas afectadas. El marcador `:course_id` representa un parámetro del driver, no concatenación.

## Evidencia

Cronología de ambas sesiones, nivel de aislamiento, filas afectadas y prueba de que `occupied <= capacity` siempre se mantiene. Para la parte con PostgreSQL, añade el error que devuelve el motor cuando aborta una transacción serializable y qué hace tu cliente con él.

## Limpieza

No es necesaria: el script trabaja sobre un archivo temporal que borra al terminar.
