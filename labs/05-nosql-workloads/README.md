# Laboratorio 05 — NoSQL por carga de trabajo

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

No se acepta “es más escalable” como justificación.
