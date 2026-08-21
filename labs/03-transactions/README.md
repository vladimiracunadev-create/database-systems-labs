# Laboratorio 03 — Actualización perdida y sus tres correcciones

> Dos hilos reales compiten por la última plaza. El fallo se reproduce siempre, no «a veces»:
> por eso sirve como evidencia.

**Duración:** 90 minutos · **Dependencias:** Python 3.11+ (SQLite). PostgreSQL, opcional
· **Marca de éxito:** `TRANSACTIONS_LAB_OK`
· **Parte:** [07 — Transacciones, concurrencia y recuperación](../../classes/part-08-transacciones-concurrencia-y-recuperacion/README.md)

## 🎯 Qué demuestra

Que el patrón «leer, comprobar en la aplicación, escribir» está roto en cuanto hay dos procesos,
y que hay exactamente tres formas de arreglarlo, cada una con su costo. No es un problema de
lenguaje ni de framework: es de dónde se evalúa la condición.

## 🔬 Hipótesis

1. Con dos clientes que leen el mismo valor antes de escribir, **ambos** aceptarán la reserva y
   el contador registrará solo una: dos personas con la misma plaza.
2. Mover la condición dentro del `UPDATE` la evalúa el motor sobre la fila viva, y solo uno gana.
3. El control optimista detecta el conflicto por versión y **reintenta**; el segundo cliente
   descubre entonces que ya no hay plaza.
4. El bloqueo pesimista serializa a los clientes antes de leer, a costa de que el segundo espere.

## ▶️ Ejecutar

```bash
python labs/03-transactions/run_transactions_lab.py
```

El guion lanza dos hilos contra la misma base y los sincroniza en una barrera para forzar el
entrelazado peligroso. Sin esa barrera el fallo aparecería de vez en cuando; con ella, siempre.

## 📊 Lo que verás

| Cliente | Mecanismo | Reservas aceptadas | `occupied` |
| --- | --- | ---: | ---: |
| leer-modificar-escribir | ninguno | **2** | 1 |
| actualización atómica | condición dentro del `UPDATE` | 1 | 1 |
| control optimista | `WHERE version = ?` y reintento | 1 | 1 |
| bloqueo pesimista | `BEGIN IMMEDIATE` | 1 | 1 |

La primera fila es el fallo, con su firma característica: **dos aceptadas y un contador en uno**.
Una de las dos escrituras se perdió, y el sistema no se enteró.

## 🧠 Por qué está hecho así

- **Hilos reales, no simulación.** Dos conexiones distintas contra el mismo archivo, con el
  bloqueo de escritura del motor haciendo su trabajo.
- **Barrera de sincronización.** Convierte una carrera intermitente en un experimento
  reproducible. Reproducible es lo que hace que sirva como evidencia en una revisión de código.
- **La evidencia es el invariante, no el tiempo.** «Dos reservas para una plaza» es un error en
  cualquier máquina; «tardó 40 ms» no dice nada.
- **`isolation_level=None`.** Las transacciones se abren a mano; con el valor por defecto sería
  el driver quien decidiera, y el laboratorio mediría al driver.

## ⚠️ Lo que este laboratorio no demuestra

- SQLite serializa las escrituras: no reproduce anomalías que necesitan concurrencia real de
  escritura, como la desviación de escritura (*write skew*) bajo instantánea.
- No cubre `SERIALIZABLE` ni la detección de conflictos de PostgreSQL, que aborta transacciones
  con un error que tu cliente debe saber reintentar.
- No mide contención ni rendimiento bajo carga.

Para eso, la extensión con contenedores de abajo, y el método de Hermitage citado en las fuentes.

## 🧪 Extensiones

1. Sube `CAPACIDAD` a 3 y `CLIENTES` a 10: el invariante debe sostenerse en las tres
   correcciones. Predice cuántas se aceptan **antes** de ejecutar.
2. Quita la barrera y ejecuta cien veces: cuenta en cuántas aparece el fallo. Así se ve por qué
   estos errores llegan a producción sin que nadie los reproduzca.
3. Añade un retraso entre la lectura y la escritura del cliente roto: la ventana se agranda y el
   fallo se vuelve permanente.
4. Reescribe la corrección optimista sin reintento y observa qué recibe el usuario: un error
   crudo. La política de reintento es parte del diseño, no un detalle.

## 🏭 Llevarlo a un motor real

```bash
docker compose --profile relational up -d
```

Repite el escenario contra PostgreSQL con `READ COMMITTED` y con `SERIALIZABLE`, y anota qué
cambia: en el segundo, el motor puede abortar una transacción con un error de serialización, y
tu cliente **tiene** que reintentarlo. Guarda el mensaje de error exacto como evidencia.

Actualización atómica orientativa:

```sql
UPDATE course_capacity
SET occupied = occupied + 1
WHERE course_id = :course_id AND occupied < capacity;
```

El cliente debe comprobar las filas afectadas. El marcador `:course_id` representa un parámetro
del driver, no concatenación.

## 🎓 Dónde encaja

- **Clases:** [033–037](../../classes/part-08-transacciones-concurrencia-y-recuperacion/README.md),
  en especial [034 — Anomalías de aislamiento](../../classes/part-08-transacciones-concurrencia-y-recuperacion/044-anomalias-de-aislamiento-y-la-critica-ansi/README.md)
  y [037 — Concurrencia en la aplicación](../../classes/part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md).
- **Rutas:** [Desarrollador de aplicaciones](../../rutas/desarrollo-de-aplicaciones.md),
  [DBA / SRE de datos](../../rutas/fiabilidad-y-operacion.md),
  [Gobierno y privacidad del dato](../../rutas/gobierno-y-privacidad.md).
- **Certificaciones:** apoya el dominio de monitorización y optimización del
  [DP-300](../../certificaciones/dp-300.md), donde entra el bloqueo de sesiones.

## 📖 Fuentes

- **Hal Berenson y otros**, *A Critique of ANSI SQL Isolation Levels* — por qué los nombres de
  los niveles no bastan para saber qué anomalías quedan permitidas.
- **Jim Gray, Andreas Reuter**, *Transaction Processing* — el tratado de referencia del que
  salen los tres mecanismos.
- **SQLite: Isolation** y **PostgreSQL: Concurrency Control** — lo que cada motor garantiza de
  verdad.
- **Martin Kleppmann**, *Hermitage* — el método para comprobar empíricamente qué anomalías
  permite cada nivel en cada motor.

Fichas completas en el [registro de fuentes](../../catalog/sources.json).

## 🧹 Limpieza

No hace falta: el guion trabaja sobre un archivo temporal que borra al terminar. Si levantaste
contenedores: `docker compose --profile relational down -v`.
