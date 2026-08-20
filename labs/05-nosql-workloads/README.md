# Laboratorio 05 — NoSQL por carga de trabajo

Duración: 90 minutos. Dependencia: Python 3.11+. MongoDB y Redis, opcionales.

## Ejecución

```bash
python labs/05-nosql-workloads/run_nosql_lab.py
```

Modela tres riesgos y los cuenta en accesos, bytes y tamaño de partición —nunca en tiempo—, sobre un reloj lógico que nunca duerme. Debe terminar con `NOSQL_LAB_OK`.

| Lo que mide | Resultado que imprime |
| --- | --- |
| TTL frente a coherencia | 5 lecturas obsoletas sin invalidar, 0 invalidando en la escritura |
| incrustar frente a referenciar, lectura dominante | incrustar: 1 acceso por lectura; referenciar: 13 |
| incrustar frente a referenciar, escritura dominante | incrustar reescribe 13× más bytes |
| crecimiento del agregado | cuántos comentarios caben antes del límite de 16 MiB por documento |
| clave de partición caliente | 30 000 eventos en una partición frente a 5000 al compartimentar por mes |

La conclusión que fuerza el laboratorio: la misma pareja de modelos gana o pierde según la relación entre lecturas y escrituras, así que **una decisión de modelado sin carga declarada no es una decisión, es una preferencia**.

Los números modelan el comportamiento; antes de llevarlos a producción hay que verificarlos contra el motor real.

## Casos

| Caso | Candidato inicial | Riesgo que debe probarse |
| --- | --- | --- |
| ficha agregada de curso | documento | crecimiento y actualización concurrente |
| sesión temporal | clave-valor con TTL | pérdida e invalidación |
| actividad masiva por estudiante | columna ancha | clave caliente y consulta no modelada |
| ruta de aprendizaje | grafo | costo operativo frente a SQL recursivo |
| búsqueda de materiales | índice invertido | consistencia con la fuente de verdad |

## Entrega

Para dos casos:

1. define patrón de acceso y SLO;
2. diseña claves o documentos;
3. escribe una operación normal y una de fallo;
4. explica consistencia e idempotencia;
5. compara con PostgreSQL;
6. incluye estrategia de respaldo y salida.

No se acepta “es más escalable” como justificación. Si quieres contrastar el modelo contra los motores reales:

```bash
docker compose --profile document --profile cache up -d
```
