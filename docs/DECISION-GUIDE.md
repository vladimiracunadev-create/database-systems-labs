# Guía de selección

## Secuencia

1. Define invariantes y consecuencias de perder datos.
2. Enumera patrones de lectura y escritura.
3. Estima volumen, crecimiento, concurrencia y distribución.
4. Fija latencia, disponibilidad, RPO y RTO.
5. Clasifica datos y requisitos regulatorios.
6. Evalúa competencias del equipo y operación disponible.
7. Prueba primero la alternativa más simple.
8. Ejecuta una carga representativa.
9. Diseña migración, respaldo y salida.
10. Registra la decisión y sus disparadores de revisión.

## Señales de alerta

- selección basada solo en una encuesta;
- “esquema flexible” sin validación;
- “escala horizontal” sin clave de partición;
- “serverless” sin límites y costos modelados;
- varios motores sin responsables operativos;
- comparación de servicios gratuitos con producción;
- ausencia de restauración o estrategia de salida.

## Resultado

La salida no es el nombre de un motor: es una decisión condicionada, con supuestos, evidencia, riesgos y alternativa descartada.
