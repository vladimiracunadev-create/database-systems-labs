# Laboratorio 07 — Réplica, retraso y garantías de sesión

> Leer de una réplica no es una optimización gratuita: es un cambio de garantía.
> Este laboratorio cuenta exactamente qué se rompe y qué cuesta arreglarlo.

**Duración:** 90 minutos · **Dependencias:** Python 3.11+ · **Marca de éxito:** `REPLICATION_LAB_OK`
· **Parte:** [09 — Distribución, réplica y consistencia](../../classes/part-10-distribucion-replica-y-consistencia/README.md)

## 🎯 Qué demuestra

Que la frase «movemos las lecturas a la réplica para aliviar el líder» tiene una letra pequeña
que casi nunca se declara: el cliente deja de ver lo que acaba de escribir, y si el balanceador
reparte entre réplicas con distinto retraso, además ve el tiempo ir hacia atrás.

El laboratorio reproduce las dos anomalías y aplica las tres correcciones que existen, midiendo
lo que cada una cuesta.

## 🔬 Hipótesis

1. Con un retraso de réplica de 2 y 5 ticks, **todas** las relecturas inmediatas contra un
   seguidor devolverán una versión anterior a la que el cliente acaba de escribir.
2. Repartir las lecturas entre dos seguidores con retrasos distintos producirá lecturas **no
   monótonas**: el cliente verá desaparecer datos que ya había visto.
3. Leer del líder, esperar la posición propia y exigir quórum eliminan las dos anomalías, con
   costos distintos: carga, latencia y número de peticiones.
4. Con un retraso constante, la cola de escrituras pendientes en el seguidor más lento se
   **estabiliza**, no crece: el retraso es un desfase, no una fuga.

## ▶️ Ejecutar

```bash
python labs/07-replication/run_replication_lab.py
```

## 📊 Lo que verás

| Estrategia de lectura | Sin lectura propia | Obsoletas | No monótonas | Esperas |
| --- | ---: | ---: | ---: | ---: |
| líder | 0 | 0 | 0 | 0 |
| seguidor | 6 | 6 | 2 | 0 |
| sesión (esperar la posición propia) | 0 | 0 | 0 | 15 |
| quórum (R + W > N) | 0 | 0 | 0 | 0 |

Y la cola del seguidor más lento, que sube hasta estabilizarse en `retraso − 1`: la escritura
del tick en curso todavía no ha tenido ocasión de viajar. Ese uno de diferencia es justo lo que
aparece en un panel de monitorización y nadie sabe explicar.

## 🧠 Por qué está hecho así

- **Reloj lógico, no cronómetro.** El retraso se declara en ticks. Un milisegundo depende de la
  máquina y de la red; «seis de seis lecturas no vieron la escritura propia» se sostiene en
  cualquier parte y se puede comparar entre ejecuciones.
- **Sin servidores.** Modela el mecanismo —registro, posición aplicada, retraso— en lugar de
  configurar un clúster. Lo que se aprende es transferible a PostgreSQL, MySQL o cualquier
  sistema con réplica asíncrona; lo que no cubre, se dice abajo.
- **La posición del registro (LSN) es el hilo conductor.** Es la misma idea que usan las
  garantías de sesión reales: el cliente lleva la marca de lo que escribió y exige no leer por
  debajo de ella.

## ⚠️ Lo que este laboratorio no demuestra

- No mide el rendimiento real de ningún motor ni el coste de red de la réplica.
- No cubre réplica multilíder ni resolución de conflictos: aquí el líder es único.
- No modela pérdida de mensajes ni particiones de red, que es donde aparecen CAP y PACELC.
- El quórum está simplificado (dos respuestas y gana la versión más alta); un sistema real
  también repara la réplica atrasada al leer.

## 🧪 Extensiones

1. Sube el retraso de `seguidor-b` a 12 ticks: la cola se estabiliza en 11 y las esperas de la
   estrategia de sesión se disparan. **Predice el número antes de ejecutar.**
2. Haz que el cliente relea tres ticks después en vez de uno: verás desaparecer las violaciones
   contra `seguidor-a` pero no contra `seguidor-b`. Esa es la ventana de inconsistencia.
3. Añade un tercer seguidor con retraso 1 y enruta al más adelantado: es el diseño de un
   balanceador consciente del retraso.
4. Rompe el quórum a propósito (una sola respuesta) y comprueba que las anomalías vuelven.

## 🏭 Llevarlo a un motor real

```bash
docker compose --profile relational up -d
```

En PostgreSQL, `pg_stat_replication` y `pg_last_wal_receive_lsn()` dan la posición real de cada
réplica; en MySQL, `SHOW REPLICA STATUS`. Repite el experimento: escribe, lee inmediatamente de
la réplica y registra cuántas veces no ves tu propia escritura. Compara la forma del resultado
—no los milisegundos— con la del laboratorio.

## 🎓 Dónde encaja

- **Clases:** [043 — Réplica](../../classes/part-10-distribucion-replica-y-consistencia/053-replica-lider-unico-multilider-y-sin-lider/README.md)
  y [046 — Modelos de consistencia y garantías de sesión](../../classes/part-10-distribucion-replica-y-consistencia/056-modelos-de-consistencia-y-garantias-de-sesion/README.md).
- **Rutas:** [DBA / SRE de datos](../../rutas/fiabilidad-y-operacion.md),
  [Arquitecto de datos](../../rutas/arquitectura.md), [Ingeniero de datos](../../rutas/ingenieria-de-datos.md).
- **Certificaciones:** el dominio de alta disponibilidad y recuperación del
  [DP-300](../../certificaciones/dp-300.md) evalúa geo-réplica y grupos de disponibilidad; este
  laboratorio prepara el concepto, no la consola.

## 📖 Fuentes

- **Jim Gray y otros**, *The Dangers of Replication and a Solution* — por qué la réplica
  síncrona no escala y qué se paga al elegir la asíncrona.
- **Peter Bailis y otros**, *Highly Available Transactions* — qué garantías siguen siendo
  posibles bajo alta disponibilidad, incluidas las de sesión.
- **Werner Vogels**, *Eventually Consistent* — la ventana de inconsistencia, explicada por
  quien la operó a escala.
- **PostgreSQL Documentation** — réplica en un motor real y sus métricas de retraso.

Fichas completas en el [registro de fuentes](../../catalog/sources.json).

## 🧹 Limpieza

No hace falta: el laboratorio no crea archivos ni procesos.
