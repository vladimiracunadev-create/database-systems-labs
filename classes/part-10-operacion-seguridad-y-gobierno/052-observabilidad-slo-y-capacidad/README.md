# 052 — Observabilidad, objetivos de servicio y capacidad

> [Programa](../../../README.md) · [Parte 10](../README.md) · [← Anterior](../../part-10-operacion-seguridad-y-gobierno/051-inyeccion-sql-y-parametrizacion/README.md) · [Siguiente →](../../part-10-operacion-seguridad-y-gobierno/053-privacidad-retencion-y-gobierno-del-dato/README.md)

Parte 10 — Operación, seguridad y gobierno · Avanzado ·
3 horas estimadas · motores `postgresql`, `mongodb` · laboratorio
[`labs/04-indexing`](../../../labs/04-indexing/README.md) · 3 fuentes.

**Conceptos centrales:** `percentil` · `presupuesto de error` · `saturación` · `consulta lenta`

---

## Propósito

Saber cómo está la base antes de que alguien se queje, y expresar «está bien» como un número acordado en lugar de una impresión.

## Resultados de aprendizaje

Al terminar podrás:

1. Definir un SLI y un SLO de base de datos y derivar el presupuesto de error.
2. Explicar por qué la latencia se mide en percentiles y nunca en medias.
3. Instrumentar las cuatro señales de un almacén de datos.
4. Identificar las consultas que consumen el tiempo total, no las más lentas.
5. Estimar capacidad con un criterio de saturación.

## Fundamentos

### SLI, SLO y presupuesto de error

- **SLI:** lo que se mide (`% de consultas por debajo de 100 ms`).
- **SLO:** el objetivo acordado (`99,9 % de las consultas por debajo de 100 ms en 30 días`).
- **Presupuesto de error:** lo que se permite fallar. Con un SLO del 99,9 % son **43 minutos al mes**.

El presupuesto es una herramienta de decisión: mientras quede, se puede desplegar y experimentar; si se agota, se para y se estabiliza. Convierte una discusión de opiniones en una regla.

### Percentiles, no medias

Dean y Barroso lo demuestran: la media oculta exactamente lo que importa.

```text
1 000 consultas: 990 de 5 ms, 10 de 2 000 ms
media   = (990·5 + 10·2000) / 1000 = 24,95 ms      ← «todo bien»
p50     = 5 ms
p99     = 2 000 ms                                  ← 10 usuarios esperaron 2 s
```

Y el efecto se **amplifica** cuando una petición hace varias consultas. Si una página lanza 20 consultas en serie con p99 de 100 ms:

```text
P(al menos una consulta cae en el p99) = 1 - 0,99²⁰ = 18,2 %
```

Casi una de cada cinco cargas de página sufre la latencia del p99. Por eso la cola alta importa mucho más de lo que su porcentaje sugiere, y por eso reducir el número de consultas por petición suele mejorar más que optimizar cada una.

### Las cuatro señales

| Señal | Qué medir en una base de datos |
|---|---|
| **Latencia** | p50, p95, p99 por tipo de consulta; separando errores de aciertos |
| **Tráfico** | Consultas/s, transacciones/s, filas devueltas/s |
| **Errores** | Fallos de serialización, interbloqueos, tiempos agotados, conexiones rechazadas |
| **Saturación** | Conexiones usadas / máximo, retraso de réplica, filas muertas, espacio, aciertos de caché |

La saturación es la que **predice**; las otras tres describen el presente.

### Las consultas que importan

El error habitual es optimizar la consulta más lenta. Lo correcto es optimizar la que consume **más tiempo total**:

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT substring(query, 1, 70) AS consulta,
       calls,
       round(mean_exec_time::numeric, 2)  AS media_ms,
       round(total_exec_time::numeric)    AS total_ms,
       round(100 * total_exec_time / sum(total_exec_time) OVER (), 1) AS pct
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```

```text
consulta                              calls    media_ms   total_ms   pct
SELECT ... FROM enrollments WHERE ... 4 200 000     2,10  8 820 000  61,2   ← aquí
SELECT ... FROM courses c JOIN ...           40  8 100,00   324 000   2,2   ← no aquí
```

Una consulta de 2 ms ejecutada cuatro millones de veces consume 27 veces más tiempo que una de 8 segundos ejecutada 40 veces. Bajarla de 2,1 ms a 0,8 ms libera más capacidad que cualquier trabajo sobre la lenta.

### Consultas en curso

```sql
SELECT pid, now() - query_start AS duracion, state, wait_event_type, wait_event,
       substring(query, 1, 80)
FROM pg_stat_activity
WHERE state <> 'idle' ORDER BY duracion DESC LIMIT 10;
```

`wait_event` dice **por qué** espera: bloqueo, E/S, red o cliente. Un `Client:ClientRead` prolongado significa que el motor terminó y la aplicación no lee: el problema no está en la base.

```mermaid
flowchart TD
    M["Métricas"] --> L["Latencia p50/p95/p99"]
    M --> T["Tráfico"]
    M --> E["Errores"]
    M --> S["Saturación"]
    S --> S1["conexiones / máx"]
    S --> S2["retraso de réplica"]
    S --> S3["filas muertas"]
    S --> S4["espacio en disco"]
    L --> SLO{"¿Dentro del SLO?"}
    SLO -- "Sí" --> PB["Queda presupuesto:<br/>se puede desplegar"]
    SLO -- "No" --> A["Alerta → diagnóstico"]
    A --> D1["pg_stat_statements:<br/>¿qué consume el tiempo total?"]
    A --> D2["pg_stat_activity:<br/>¿qué está esperando ahora?"]
    A --> D3["EXPLAIN ANALYZE (clase 042)"]
```

## Ejemplo trabajado

Plataforma con SLO: *«99,5 % de las consultas de lectura por debajo de 200 ms, medido en ventanas de 30 días»*.

**Presupuesto de error:**

```text
0,5 % de 30 días = 3 h 39 min de incumplimiento permitido
con 50 M de consultas mensuales: 250 000 consultas pueden exceder 200 ms
```

**Panel mínimo:**

```sql
-- Latencia por tipo, desde pg_stat_statements (media; los percentiles reales
-- vienen del cliente, que es donde se percibe la latencia de verdad)
SELECT queryid, calls, mean_exec_time, max_exec_time FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 20;

-- Saturación de conexiones
SELECT count(*) FILTER (WHERE state = 'active')          AS activas,
       count(*)                                          AS totales,
       current_setting('max_connections')::int           AS maximo,
       round(100.0 * count(*) / current_setting('max_connections')::int, 1) AS pct
FROM pg_stat_activity;

-- Retraso de réplica en segundos
SELECT client_addr, extract(epoch FROM replay_lag) AS retraso_s FROM pg_stat_replication;

-- Deuda de vacuum
SELECT relname, n_dead_tup,
       round(100.0*n_dead_tup/NULLIF(n_live_tup+n_dead_tup,0),1) AS pct_muertas
FROM pg_stat_user_tables WHERE n_dead_tup > 100000 ORDER BY n_dead_tup DESC;
```

**Alertas, con la distinción que importa:**

| Alerta | Umbral | Tipo |
|---|---|---|
| p99 de lectura > 200 ms durante 10 min | SLO | **Página**: afecta a usuarios |
| Conexiones > 80 % del máximo | Saturación | **Página**: precede a un rechazo |
| Retraso de réplica > 30 s | Saturación | Página |
| Espacio libre < 20 % | Saturación | Página |
| Filas muertas > 30 % en tabla grande | Saturación | **Ticket**: degradación lenta |
| Interbloqueos > 10/h | Errores | Ticket |
| Sin restauración verificada en 35 días | Proceso | Ticket |

La distinción página/ticket es la que hace sostenible la guardia: solo despierta a alguien lo que afecta a usuarios o lo que va a hacerlo pronto.

**Capacidad.** La regla operativa más útil para una base transaccional:

```text
Con utilización > 70 % sostenida, la latencia crece de forma no lineal
(teoría de colas: el tiempo de espera tiende a infinito al acercarse a 1)

utilización actual: 45 %
crecimiento:        8 % mensual
meses hasta el 70 %: ln(70/45) / ln(1,08) ≈ 5,7 meses
```

Ese número —cinco meses y medio— es lo que convierte «hay que crecer en algún momento» en una tarea con fecha.

**Contraejemplo instructivo.** Un servicio reportaba latencia alta; el panel de la base mostraba p99 de 3 ms y utilización del 30 %.

```sql
SELECT wait_event_type, wait_event, count(*)
FROM pg_stat_activity WHERE state <> 'idle' GROUP BY 1,2 ORDER BY 3 DESC;
```

```text
Client   ClientRead    47
```

Cuarenta y siete conexiones esperando a que la aplicación **leyera** el resultado. El motor había terminado. El cuello de botella estaba en el cliente, que procesaba fila a fila. La base estaba sana y el panel de la base lo decía; sin esa consulta, el equipo habría pasado días optimizando consultas que ya eran rápidas.

## Comparación

| Pregunta | Fuente |
|---|---|
| ¿Qué consume el tiempo total? | `pg_stat_statements` por `total_exec_time` |
| ¿Qué pasa ahora mismo? | `pg_stat_activity` |
| ¿Por qué esta consulta es lenta? | `EXPLAIN ANALYZE` (clase 042) |
| ¿Estamos saturando? | Conexiones, retraso, espacio, filas muertas |
| ¿Cumplimos lo prometido? | SLI frente a SLO, con percentiles del cliente |
| ¿Cuánto aguantamos? | Utilización + tasa de crecimiento |

## Errores frecuentes

1. **Medir la media.** Oculta la cola, que es lo que sufre el usuario.
2. **Optimizar la consulta más lenta.** Casi nunca es la que consume el tiempo.
3. **Alertar sobre CPU.** Rara vez es la causa en una base de datos.
4. **Medir la latencia solo en el servidor.** El usuario percibe la del cliente, con red y agrupador incluidos.
5. **Alertas sin distinguir página de ticket.** Fatiga de alertas y guardias que se ignoran.
6. **SLO sin acuerdo con el negocio.** Un objetivo que nadie firmó no dirige ninguna decisión.
7. **No medir la saturación.** Se descubre el límite cuando se cruza.

## De la clase a la operación

La instrumentación se instala **antes** del incidente. Durante uno, no hay tiempo de crear un panel, y las decisiones se toman con la intuición de quien habla más fuerte. `pg_stat_statements` activado desde el primer día es la inversión de menor costo y mayor retorno.

## Reto de transferencia

1. Define un SLI y un SLO para una operación crítica y calcula su presupuesto de error.
2. Instala `pg_stat_statements` y ordena por tiempo total; identifica la consulta dominante.
3. Construye el panel con las cuatro señales y clasifica cada alerta en página o ticket.
4. Calcula los meses que faltan hasta el 70 % de utilización con tu crecimiento real.

## Preguntas de evaluación

1. Con p99 de 100 ms y 20 consultas por petición, ¿qué fracción de peticiones sufre la cola?
2. ¿Por qué una consulta de 2 ms puede ser más urgente que una de 8 s?
3. Da tres métricas de saturación de tu base y el umbral que elegirías para cada una.
4. Interpreta un `wait_event` de `Client:ClientRead` sostenido en 50 conexiones.

---

## Laboratorio

```bash
python scripts/validate_repository.py
python labs/04-indexing/run_indexing_lab.py
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

- **Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy** (2016). [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/). O'Reilly. ISBN 978-1-4919-2912-4.  
  Lectura libre. Objetivos de nivel de servicio y presupuesto de error.
- **Jeffrey Dean, Luiz Andre Barroso** (2013). [The Tail at Scale](https://dl.acm.org/doi/10.1145/2408776.2408794). Communications of the ACM 56(2). DOI [10.1145/2408776.2408794](https://doi.org/10.1145/2408776.2408794).  
  Por qué la latencia se mide en percentiles altos y no en promedio.
- **Laine Campbell, Charity Majors** (2017). [Database Reliability Engineering](https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/). O'Reilly. ISBN 978-1-4919-2594-2.  
  Operación, respaldos, objetivos de servicio y gestion de cambios.

---

> [Programa](../../../README.md) · [Parte 10](../README.md) · [← Anterior](../../part-10-operacion-seguridad-y-gobierno/051-inyeccion-sql-y-parametrizacion/README.md) · [Siguiente →](../../part-10-operacion-seguridad-y-gobierno/053-privacidad-retencion-y-gobierno-del-dato/README.md)
