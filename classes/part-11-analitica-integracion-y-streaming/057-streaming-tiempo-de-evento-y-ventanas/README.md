# 057 — Streaming: tiempo de evento, ventanas y semántica de entrega

> [Programa](../../../README.md) · [Parte 11](../README.md) · [← Anterior](../../part-11-analitica-integracion-y-streaming/056-integracion-etl-elt-y-captura-de-cambios/README.md) · [Siguiente →](../../part-12-vectores-recuperacion-y-rag/058-embeddings-y-metricas-de-distancia/README.md)

Parte 11 — Analítica, integración y streaming · Avanzado ·
3 horas estimadas · motores `kafka`, `clickhouse` · laboratorio
[`labs/05-nosql-workloads`](../../../labs/05-nosql-workloads/README.md) · 3 fuentes.

**Conceptos centrales:** `tiempo de evento` · `marca de agua` · `ventana` · `entrega al menos una vez`

---

## Propósito

Procesar datos que no dejan de llegar. La dificultad no es el caudal: es que los eventos llegan tarde, desordenados y a veces dos veces, y hay que decidir cuándo se cierra un resultado.

## Resultados de aprendizaje

Al terminar podrás:

1. Distinguir tiempo de evento, de ingesta y de procesamiento.
2. Elegir el tipo de ventana adecuado a la pregunta.
3. Explicar qué es una marca de agua y qué compromiso codifica.
4. Comparar las tres semánticas de entrega y cómo se consigue cada una.
5. Aplicar la dualidad flujo-tabla.

## Fundamentos

### Los tres tiempos

| Tiempo | Definición | Problema |
|---|---|---|
| **De evento** | Cuando ocurrió en el mundo | Llega tarde y desordenado |
| **De ingesta** | Cuando entró al sistema | No refleja la realidad |
| **De procesamiento** | Cuando se calculó | Reprocesar da otro resultado |

Akidau, Chernyak y Lax establecen la regla: **si la pregunta es sobre el mundo, se usa tiempo de evento**. «¿Cuántas inscripciones hubo el martes?» se refiere al martes real, no a cuándo llegaron los mensajes.

El desfase entre evento y procesamiento no está acotado: un móvil sin cobertura puede enviar eventos de hace tres días.

### Tipos de ventana

| Ventana | Forma | Pregunta que responde |
|---|---|---|
| **Fija** (tumbling) | Intervalos contiguos sin solape | «Inscripciones por hora» |
| **Deslizante** (sliding) | Tamaño y desplazamiento independientes | «Media de los últimos 10 min, cada minuto» |
| **De sesión** | Agrupa por inactividad | «Actividad de un usuario hasta 30 min de pausa» |
| **Global** | Todo el flujo | «Total desde siempre» |

### Marcas de agua

Una **marca de agua** es la afirmación del sistema: *«creo que ya no llegarán eventos anteriores a T»*. Es la que permite cerrar una ventana y emitir un resultado.

Es una **heurística**, no una certeza. De ahí el compromiso central del streaming:

```text
marca de agua agresiva  → resultados rápidos, más eventos rezagados descartados
marca de agua permisiva → resultados tardíos, menos pérdida
```

Y las tres políticas para lo que llega después de la marca:

| Política | Qué hace | Cuándo |
|---|---|---|
| **Descartar** | Ignora el rezagado | El error es tolerable |
| **Emitir corrección** | Reemite la ventana actualizada | El consumidor sabe reconciliar |
| **Desviar** | A un canal aparte para revisión | Auditoría, cumplimiento |

```mermaid
flowchart LR
    E["Eventos<br/>desordenados"] --> B["Asignar a ventana<br/>por tiempo de EVENTO"]
    B --> W{"¿Marca de agua<br/>pasó el fin<br/>de la ventana?"}
    W -- "No" --> ACC["Acumular"]
    W -- "Sí" --> EM["Emitir resultado"]
    EM --> L{"Llega un rezagado"}
    L --> P{"Política"}
    P --> P1["Descartar"]
    P --> P2["Emitir corrección"]
    P --> P3["Desviar a revisión"]
```

### Semánticas de entrega

| Semántica | Garantía | Cómo |
|---|---|---|
| **Como mucho una vez** | Puede perder | Sin reintentos |
| **Al menos una vez** | Puede duplicar | Reintentos + confirmación tras procesar |
| **Exactamente una vez** | Ni pierde ni duplica | Al menos una vez **+ receptor idempotente**, o transacciones del propio sistema |

La entrega exactamente-una-vez **de extremo a extremo no existe** como propiedad de la red: se construye combinando entrega al-menos-una-vez con un receptor que deduplica por identificador (clase 037). Kafka ofrece transacciones que dan «procesamiento exactamente una vez» dentro de Kafka; en cuanto un efecto sale del sistema —una fila en otra base, un correo—, la idempotencia vuelve a ser responsabilidad del receptor.

### Dualidad flujo-tabla

- Un **flujo** es la secuencia de cambios.
- Una **tabla** es el estado acumulado de esos cambios.

Cada uno se deriva del otro: agregar un flujo produce una tabla; observar los cambios de una tabla produce un flujo. Es exactamente lo que hace la captura de cambios de la clase 056, y es la misma idea del WAL de la clase 036 vista desde otro ángulo.

## Ejemplo trabajado

Métrica: inscripciones por curso y por hora, con paneles casi en tiempo real. Los eventos llegan de móviles con conectividad variable.

**Observación previa, imprescindible:** medir el retraso real antes de elegir la marca de agua.

```sql
SELECT percentile_disc(0.50) WITHIN GROUP (ORDER BY retraso_s) AS p50,
       percentile_disc(0.95) WITHIN GROUP (ORDER BY retraso_s) AS p95,
       percentile_disc(0.99) WITHIN GROUP (ORDER BY retraso_s) AS p99,
       max(retraso_s)                                          AS maximo
FROM (SELECT extract(epoch FROM (ingerido_en - ocurrido_en)) AS retraso_s
      FROM eventos WHERE ingerido_en > now() - interval '7 days') t;
```

```text
p50 = 0,8 s      p95 = 45 s      p99 = 340 s      máximo = 3 días
```

Ese `máximo` de 3 días es un móvil que estuvo sin cobertura. Esperar tres días para cerrar una ventana horaria es absurdo; descartarlo sin más, tampoco es aceptable si son inscripciones.

**Decisión, justificada con los percentiles:**

```text
Marca de agua: tiempo de evento máximo visto − 10 minutos
   → cubre el p99 (340 s) con margen
Política para rezagados: emitir corrección hasta 24 h; después, desviar a revisión
   → el panel se corrige solo; lo muy tardío no se pierde, se revisa
```

**Implementación en SQL de ventanas, sobre la tabla cruda:**

```sql
-- Ventana fija de una hora, por tiempo de EVENTO
CREATE MATERIALIZED VIEW inscripciones_hora AS
SELECT date_trunc('hour', ocurrido_en) AS hora,
       course_id,
       count(*)                        AS n,
       max(ingerido_en)                AS ultima_actualizacion
FROM eventos
WHERE tipo = 'inscripcion.creada'
GROUP BY 1, 2;
```

Una ventana que se recalcula incorpora automáticamente los rezagados: es la política de «emitir corrección», implementada sin ningún motor de streaming.

**Marca de agua y estado de cada ventana:**

```sql
WITH marca AS (
  SELECT max(ocurrido_en) - interval '10 minutes' AS w FROM eventos
)
SELECT h.hora, h.course_id, h.n,
       CASE WHEN h.hora + interval '1 hour' < (SELECT w FROM marca)
            THEN 'cerrada' ELSE 'provisional' END AS estado
FROM inscripciones_hora h
ORDER BY h.hora DESC LIMIT 24;
```

**Esta columna `estado` es el entregable pedagógico de la clase.** Un panel que muestra cifras sin decir si son definitivas o provisionales genera desconfianza: alguien anota el número de las 14:00, vuelve a mirar y ve otro. Con la marca explícita, el cambio es esperado y comprensible.

**Rezagados muy tardíos:**

```sql
INSERT INTO eventos_tardios
SELECT * FROM eventos
WHERE ingerido_en - ocurrido_en > interval '24 hours';
```

No se descartan: se desvían. Para inscripciones, perder un evento es perder una matrícula.

**Ventana de sesión**, para «cuánto dura una sesión de estudio»:

```sql
WITH marcado AS (
  SELECT student_id, ocurrido_en,
         CASE WHEN ocurrido_en - lag(ocurrido_en)
                   OVER (PARTITION BY student_id ORDER BY ocurrido_en)
                   > interval '30 minutes'
              THEN 1 ELSE 0 END AS nueva
  FROM eventos WHERE tipo = 'actividad'
),
sesiones AS (
  SELECT student_id, ocurrido_en,
         sum(nueva) OVER (PARTITION BY student_id ORDER BY ocurrido_en) AS sesion
  FROM marcado
)
SELECT student_id, sesion, min(ocurrido_en) AS inicio, max(ocurrido_en) AS fin,
       max(ocurrido_en) - min(ocurrido_en) AS duracion, count(*) AS eventos
FROM sesiones GROUP BY student_id, sesion;
```

Las funciones de ventana de la clase 018 resuelven ventanas de sesión sin ningún motor de streaming, y sobre datos históricos. Es el recordatorio útil: **muchos problemas de «streaming» son problemas de SQL sobre datos con marca de tiempo**.

**Idempotencia del consumidor**, que cierra el círculo:

```sql
CREATE TABLE eventos (
  evento_id   UUID PRIMARY KEY,     -- generado por el productor
  tipo        TEXT NOT NULL,
  ocurrido_en TIMESTAMPTZ NOT NULL,
  ingerido_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  carga       JSONB NOT NULL
);

INSERT INTO eventos (...) VALUES (...) ON CONFLICT (evento_id) DO NOTHING;
```

Con esto, la entrega al-menos-una-vez de Kafka se convierte en efecto exactamente-una-vez en el destino.

## Comparación

| Necesidad | Herramienta |
|---|---|
| Métricas por intervalo | Ventana fija |
| Media móvil | Ventana deslizante |
| Agrupar actividad | Ventana de sesión |
| Analítica histórica con marca de tiempo | **SQL con funciones de ventana** |
| Latencia de segundos | Motor de streaming |
| Un flujo, muchos consumidores | Kafka |
| No duplicar en el destino | Clave de evento + `ON CONFLICT` |

## Errores frecuentes

1. **Usar tiempo de procesamiento para preguntas del mundo.** Reprocesar da otro resultado.
2. **Marca de agua sin medir el retraso real.** Se elige a ojo y se descartan eventos válidos.
3. **Descartar rezagados sin registrarlos.** Se pierden datos y nadie lo sabe.
4. **Mostrar cifras sin marcar si son provisionales.** Destruye la confianza en el panel.
5. **Suponer entrega exactamente una vez de la infraestructura.** El receptor debe ser idempotente.
6. **Motor de streaming donde bastaba SQL.** Muchas ventanas se resuelven con `OVER`.
7. **Ventanas de sesión con tiempo de procesamiento.** Agrupan por latencia de red, no por conducta.

## De la clase a la operación

La pregunta que ordena cualquier discusión sobre streaming es: **¿cuánto se espera a un evento tardío y qué se hace con el que llega después?** Sin esa respuesta escrita, cada componente del canal toma la suya y las cifras dejan de cuadrar.

## Reto de transferencia

1. Mide la distribución real del retraso de tus eventos, con percentiles.
2. Elige la marca de agua justificándola con el p99 y define la política de rezagados.
3. Implementa una ventana fija con la columna `estado` de provisional o cerrada.
4. Calcula ventanas de sesión con funciones de ventana sobre datos históricos.

## Preguntas de evaluación

1. Da una pregunta de tu negocio que exija tiempo de evento y explica qué se rompería con tiempo de procesamiento.
2. ¿Qué compromiso codifica exactamente una marca de agua?
3. Explica por qué la entrega exactamente una vez de extremo a extremo no es una propiedad de la red.
4. Da un caso tuyo de «streaming» que en realidad se resuelva con SQL sobre una tabla con marca de tiempo.

---

## Laboratorio

```bash
python scripts/validate_repository.py
python labs/05-nosql-workloads/run_nosql_lab.py
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

- **Tyler Akidau, Slava Chernyak, Reuven Lax** (2018). [Streaming Systems](https://www.oreilly.com/library/view/streaming-systems/9781491983867/). O'Reilly. ISBN 978-1-4919-8387-4.  
  Tiempo de evento, ventanas, marcas de agua y la dualidad tabla-flujo.
- **Apache Software Foundation** (2026). [Apache Kafka Documentation](https://kafka.apache.org/documentation/).  
  Particiones, orden, retención y semántica de entrega.
- **Jay Kreps** (2013). [The Log: What Every Software Engineer Should Know About Real-Time Data's Unifying Abstraction](https://web.archive.org/web/2023/https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying). LinkedIn Engineering.  
  El registro append-only como nexo entre replicación, integración y streaming. Se cita la copia archivada: LinkedIn retiro el original.

---

> [Programa](../../../README.md) · [Parte 11](../README.md) · [← Anterior](../../part-11-analitica-integracion-y-streaming/056-integracion-etl-elt-y-captura-de-cambios/README.md) · [Siguiente →](../../part-12-vectores-recuperacion-y-rag/058-embeddings-y-metricas-de-distancia/README.md)
