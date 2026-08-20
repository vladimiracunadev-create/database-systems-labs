# Proyecto final — una plataforma de datos que puedas defender

> El encargo no es construir algo que funcione. Es construir algo que puedas **defender ante
> alguien que pregunte**, con la medición delante y los límites declarados.

**Duración estimada:** 25–40 horas · **Peso:** 25 % de la nota ·
**Se corrige con:** [la rúbrica](../assessments/rubric.md) ·
**Cierra:** las siete [rutas por rol](../rutas/README.md)

## El encargo

Elige uno de los [dominios canónicos](canonical-domains.md) y diseña su plataforma de datos
para dos horizontes: **una primera versión que salga a producción** y **una evolución a tres
años**. Después demuestra, con evidencia, que las decisiones que tomaste eran las correctas
para la carga que declaraste, y di en qué condiciones dejarían de serlo.

No se evalúa la ambición del sistema. Un proyecto con un solo motor, bien medido y bien
defendido, saca mejor nota que uno con cinco motores y ninguna medición.

## Las nueve fases y su entregable

Cada fase produce algo concreto. Si una fase no deja rastro, no ocurrió.

| # | Fase | Entregable | Dimensión de la rúbrica |
|---|---|---|---|
| 1 | Requisitos, invariantes y amenazas | Lista de invariantes y de datos sensibles, con su clasificación | Requisitos · Seguridad |
| 2 | Modelo conceptual y patrones de acceso | Modelo y la tabla de consultas que tendrá que servir | Modelado |
| 3 | Alternativa más simple | Diseño con **un solo motor** y por qué bastaría o no | Decisiones |
| 4 | Prototipo ejecutable | Esquema, datos sintéticos y pruebas de invariantes que se ejecutan | Requisitos · Consultas |
| 5 | Prueba de concurrencia | Una anomalía reproducida y corregida, con su traza | Transacciones |
| 6 | Prueba de rendimiento | Plan de ejecución antes y después, con protocolo declarado | Rendimiento |
| 7 | Respaldo, destrucción y restauración | Restauración ejecutada, cronometrada y verificada | Recuperación |
| 8 | Operación | Objetivo de servicio, métricas que lo vigilan y runbook | Operación |
| 9 | Decisión y defensa | ADR final y defensa de veinte minutos | Decisiones |

Las fases 5, 6 y 7 son las que separan este proyecto de un trabajo de clase: son las tres que
exigen **provocar el problema** en vez de esperar a que aparezca.

## Restricciones

- **Datos sintéticos.** Ningún dato personal real, ni siquiera «anonimizado».
- **Sin secretos en el repositorio.** Ni cadenas de conexión, ni tokens, ni volcados.
- **No más de tres motores** sin una justificación medida. Cada motor añadido se paga en
  respaldo, monitorización, actualizaciones y personas que deben saber operarlo.
- **Una ruta local reproducible.** Otra persona clona, ejecuta y obtiene lo mismo.
- **Toda medición con su protocolo** y su entorno declarado.
- **Plan de salida** para cualquier servicio propietario que uses.

## Definición de terminado

> Otra persona puede clonar el repositorio, levantar el entorno, ejecutar las pruebas,
> destruir los datos y restaurarlos siguiendo solo tu documentación.

Si algo de esa frase falla, el proyecto no está terminado, por muy bien que funcione en tu
máquina.

## La defensa

Veinte minutos: diez de exposición y diez de preguntas. Quien pregunta no busca que falles,
busca el borde de lo que sabes. Prepárate para estas, que son las que siempre salen:

1. **«¿Por qué no lo hiciste con una sola base de datos?»** Si tu respuesta no incluye una
   medición o una restricción concreta, la arquitectura no está justificada.
2. **«Enséñame la restauración.»** No la política: la ejecución, con su duración.
3. **«¿Qué pasa si dos usuarios hacen esto a la vez?»** Debes poder mostrarlo, no describirlo.
4. **«¿Qué mediste y en qué máquina?»** Un número sin protocolo no se acepta.
5. **«¿Qué se rompe cuando esto crezca diez veces?»** La respuesta correcta suele ser un
   componente concreto, no «escalamos horizontalmente».
6. **«¿Qué harías distinto si empezaras hoy?»** Es la pregunta que distingue el nivel 3 del 4.
7. **«¿Qué **no** demuestra tu trabajo?»** Si no tienes respuesta preparada, no terminaste.

## Estructura de entrega sugerida

```text
mi-proyecto/
  README.md                 qué es, cómo se levanta, cómo se prueba
  docs/
    01-requisitos.md        invariantes, patrones de acceso, clasificación de datos
    02-modelo.md            conceptual, lógico y físico
    03-alternativa-simple.md   el diseño de un solo motor y por qué se descartó (o no)
    adr/
      0001-eleccion-motor.md
      0002-modelo-de-consistencia.md
  esquema/                  DDL versionado y migraciones reversibles
  datos/                    generador de datos sintéticos (determinista)
  pruebas/
    invariantes.py          las reglas que siempre deben cumplirse
    concurrencia.py         la anomalía reproducida y su corrección
    rendimiento.md          protocolo, planes y conclusión acotada
  operacion/
    respaldo.md             estrategia, y la restauración ejecutada con su tiempo
    slo.md                  objetivo de servicio, métricas y alertas
    runbook.md              qué hacer cuando suena la alerta
  defensa.md                el guion de los veinte minutos
```

## Variantes por rol

El encargo es el mismo; el peso cambia según tu [ruta](../rutas/README.md). Sin cambiar la
rúbrica, esto es lo que se espera que **brille** en cada caso:

| Ruta | Lo que tiene que estar impecable |
|---|---|
| [Desarrollador de aplicaciones](../rutas/desarrollo-de-aplicaciones.md) | Esquema como contrato, concurrencia en la aplicación y migraciones reversibles |
| [Ingeniero de datos](../rutas/ingenieria-de-datos.md) | Ingesta idempotente, modelo analítico con su grano y semántica del tiempo |
| [DBA / SRE de datos](../rutas/fiabilidad-y-operacion.md) | Restauración cronometrada, planes de ejecución y objetivos de servicio |
| [Arquitecto de datos](../rutas/arquitectura.md) | Alternativa simple, ADR con costo total y criterio de revisión |
| [Analytics engineer / BI](../rutas/analitica-y-bi.md) | Grano de los hechos, definiciones de métrica y pruebas de datos |
| [IA aplicada y recuperación](../rutas/ia-y-recuperacion.md) | Conjunto de evaluación propio, `recall@k` y filtrado por permisos |
| [Gobierno y privacidad](../rutas/gobierno-y-privacidad.md) | Privilegio mínimo demostrado, retención implementada y trazabilidad |

## Antes de entregar

- [ ] Los invariantes tienen una prueba que los comprueba, no un párrafo que los describe.
- [ ] La anomalía de concurrencia está **reproducida**, no citada.
- [ ] Hay un plan de ejecución antes y después de la decisión de índice.
- [ ] La restauración se ejecutó y está cronometrada; el RPO y el RTO son números.
- [ ] Ningún secreto, ningún dato real, ninguna medición sin protocolo.
- [ ] Cada ADR dice qué alternativa se descartó y qué haría revisarla.
- [ ] Está escrito qué **no** demuestra el trabajo.
- [ ] Otra persona lo levantó siguiendo solo tu documentación. (Que lo intente de verdad.)

Cuando termines, la evidencia acumulada es tu portafolio: cómo convertirla en algo que se
enseñe está en [`portafolio.md`](portafolio.md).
