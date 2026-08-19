# Rúbrica de proyecto final

Escala por dimensión: 1 inicial, 2 funcional, 3 sólido, 4 profesional. Para aprobar se requiere 80/100 y al menos nivel 3 en seguridad, recuperación e integridad.

| Dimensión | Peso | Nivel 4 |
| --- | ---: | --- |
| Requisitos e invariantes | 10 | medibles, priorizados y trazables |
| Modelado | 12 | conceptual, lógico y físico coherentes con accesos |
| Consultas y contratos | 8 | correctos, parametrizados y probados en límites |
| Transacciones | 10 | anomalías reproducidas y controles demostrados |
| Rendimiento | 10 | protocolo reproducible y conclusión limitada |
| Distribución | 8 | fallos y consistencia visibles para el usuario |
| Seguridad y privacidad | 12 | amenazas, privilegios, secretos y ciclo de datos |
| Respaldo y recuperación | 12 | restauración limpia medida y verificada |
| Operación y observabilidad | 8 | SLO, métricas, capacidad y runbook |
| Decisiones y comunicación | 10 | ADR claro, alternativas y límites reconocidos |

## Faltas críticas

- uso de datos reales no autorizados;
- credenciales expuestas;
- benchmark inventado o irreproducible;
- respaldo no restaurado;
- pérdida de invariantes bajo el caso concurrente obligatorio.
