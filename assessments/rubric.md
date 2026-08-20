# Rúbrica del proyecto final

Esta rúbrica está pensada para que **la aplique alguien que no conoce el programa**: cada
dimensión dice qué pregunta responde, qué evidencia hay que ver y qué separa un nivel del
siguiente. Dos correctores que la usen bien deberían llegar al mismo número sin hablar entre
ellos.

Escala común: **1** Inicial · **2** Funcional · **3** Sólido · **4** Profesional.

**Aprobación:** 80 de 100 puntos **y** el mínimo declarado en
cada dimensión. Una nota alta con un mínimo incumplido no aprueba: significa que el trabajo es
bueno en lo que no compromete y flojo justo donde duele.

Un resultado correcto sin explicación no demuestra transferencia. La aprobación exige ademas evidencia de restauración probada, control de acceso y pruebas.

## Resumen

| Dimensión | Peso | Mínimo | Qué pregunta responde |
|---|---:|---|---|
| Requisitos e invariantes | 10 | Funcional (2) | ¿Se sabe qué tiene que ser siempre verdad en este sistema? |
| Modelado | 12 | Sólido (3) | ¿El modelo responde a los patrones de acceso declarados? |
| Consultas y contratos | 8 | Sólido (3) | ¿Las consultas son correctas también en los límites? |
| Transacciones y concurrencia | 10 | Sólido (3) | ¿Qué pasa cuando dos procesos hacen lo mismo a la vez? |
| Rendimiento y planes | 10 | Funcional (2) | ¿La conclusión de rendimiento se puede repetir? |
| Distribución y consistencia | 8 | Funcional (2) | ¿Qué garantía pierde el usuario cuando algo falla? |
| Seguridad y privacidad | 12 | Sólido (3) | ¿Quién accede a qué, y qué pasa con el dato personal? |
| Respaldo y recuperación | 12 | Sólido (3) | ¿Cuánto dato se puede perder y cuánto cuesta volver? |
| Operación y observabilidad | 8 | Funcional (2) | ¿Cómo se sabe que el sistema está sano antes de que alguien se queje? |
| Decisiones y comunicación | 10 | Sólido (3) | ¿Puede otra persona revisar la decisión dentro de dos años? |

## Dimensión por dimensión

### Requisitos e invariantes · 10 puntos

**La pregunta que responde:** ¿Se sabe qué tiene que ser siempre verdad en este sistema?

**Evidencia que hay que ver:** Lista de invariantes con la prueba que los comprueba.

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | Requisitos narrados, sin invariantes explícitos. |
| 2 · Funcional | Invariantes declarados, pero ninguno comprobado por código. |
| 3 · Sólido | Invariantes declarados, priorizados y comprobados al menos por una prueba. |
| 4 · Profesional | Invariantes medibles y trazables hasta la consulta o restricción que los sostiene. |

Mínimo para aprobar: **Funcional (2)**. Clases: [005](../classes/part-01-modelado-conceptual-y-requisitos/005-de-requisitos-a-entidades/README.md) · [013](../classes/part-02-modelo-relacional-y-algebra/013-integridad-restricciones-y-acciones-referenciales/README.md)

### Modelado · 12 puntos

**La pregunta que responde:** ¿El modelo responde a los patrones de acceso declarados?

**Evidencia que hay que ver:** Modelo conceptual, lógico y físico, con los patrones de acceso al lado.

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | Tablas dibujadas sin patrones de acceso. |
| 2 · Funcional | Modelo correcto pero desconectado de las consultas que tendrá que servir. |
| 3 · Sólido | Modelo coherente con los accesos, con normalización justificada. |
| 4 · Profesional | Coherente en los tres niveles, con la desnormalización deliberada y su costo declarado. |

Mínimo para aprobar: **Sólido (3)**. Clases: [006](../classes/part-01-modelado-conceptual-y-requisitos/006-entidad-relacion-cardinalidad-y-participacion/README.md) · [008](../classes/part-01-modelado-conceptual-y-requisitos/008-normalizacion-y-dependencias-funcionales/README.md) · [009](../classes/part-01-modelado-conceptual-y-requisitos/009-desnormalizacion-deliberada/README.md)

### Consultas y contratos · 8 puntos

**La pregunta que responde:** ¿Las consultas son correctas también en los límites?

**Evidencia que hay que ver:** Consultas con sus casos de borde probados (nulos, vacíos, duplicados).

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | Consultas que funcionan con el caso feliz. |
| 2 · Funcional | Consultas correctas, sin parametrizar o sin probar límites. |
| 3 · Sólido | Consultas parametrizadas y probadas con nulos, vacíos y duplicados. |
| 4 · Profesional | Además, contrato de esquema versionado y probado ante cambios. |

Mínimo para aprobar: **Sólido (3)**. Clases: [014](../classes/part-03-sql-en-profundidad/014-ddl-el-esquema-como-contrato/README.md) · [016](../classes/part-03-sql-en-profundidad/016-reuniones-inner-outer-semi-y-anti/README.md) · [019](../classes/part-03-sql-en-profundidad/019-nulos-y-logica-de-tres-valores/README.md) · [051](../classes/part-10-operacion-seguridad-y-gobierno/051-inyeccion-sql-y-parametrizacion/README.md)

### Transacciones y concurrencia · 10 puntos

**La pregunta que responde:** ¿Qué pasa cuando dos procesos hacen lo mismo a la vez?

**Evidencia que hay que ver:** Una anomalía reproducida y su corrección, con la traza de ambas.

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | Se menciona que hay transacciones. |
| 2 · Funcional | Se usan transacciones sin declarar nivel de aislamiento ni anomalías. |
| 3 · Sólido | Una anomalía reproducida y corregida, con el mecanismo explicado. |
| 4 · Profesional | Anomalías reproducidas, corregidas y protegidas por una prueba automática. |

Mínimo para aprobar: **Sólido (3)**. Clases: [034](../classes/part-07-transacciones-concurrencia-y-recuperacion/034-anomalias-de-aislamiento-y-la-critica-ansi/README.md) · [037](../classes/part-07-transacciones-concurrencia-y-recuperacion/037-concurrencia-en-la-aplicacion/README.md) · Laboratorios: [03](../labs/03-transactions/README.md)

### Rendimiento y planes · 10 puntos

**La pregunta que responde:** ¿La conclusión de rendimiento se puede repetir?

**Evidencia que hay que ver:** Plan de ejecución antes y después, con protocolo y límites declarados.

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | Afirmaciones de rendimiento sin medición. |
| 2 · Funcional | Medición sin protocolo ni repeticiones. |
| 3 · Sólido | Protocolo reproducible, plan de ejecución leído y conclusión acotada a la carga. |
| 4 · Profesional | Además, costo de escritura del índice medido y decisión justificada con números. |

Mínimo para aprobar: **Funcional (2)**. Clases: [042](../classes/part-08-almacenamiento-indices-y-planes/042-planes-de-ejecucion-y-refutacion/README.md) · Laboratorios: [04](../labs/04-indexing/README.md)

### Distribución y consistencia · 8 puntos

**La pregunta que responde:** ¿Qué garantía pierde el usuario cuando algo falla?

**Evidencia que hay que ver:** Modelo de consistencia declarado y una lectura obsoleta observada.

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | Se dice "eventualmente consistente" sin definir nada. |
| 2 · Funcional | Se declara el modelo de consistencia, sin observar su efecto. |
| 3 · Sólido | Se observa el efecto de la réplica en una lectura y se declara la garantía de sesión. |
| 4 · Profesional | Además, se mide el retraso y se elige la corrección con su costo. |

Mínimo para aprobar: **Funcional (2)**. Clases: [045](../classes/part-09-distribucion-replica-y-consistencia/045-cap-pacelc-y-lo-que-realmente-se-elige/README.md) · [046](../classes/part-09-distribucion-replica-y-consistencia/046-modelos-de-consistencia-y-garantias-de-sesion/README.md) · Laboratorios: [07](../labs/07-replication/README.md)

### Seguridad y privacidad · 12 puntos

**La pregunta que responde:** ¿Quién accede a qué, y qué pasa con el dato personal?

**Evidencia que hay que ver:** Roles con privilegio mínimo probados y política de retención implementada.

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | Un usuario administrador para todo. |
| 2 · Funcional | Roles separados, sin prueba de que restringen. |
| 3 · Sólido | Privilegio mínimo demostrado con una consulta que falla como debe, y datos sintéticos. |
| 4 · Profesional | Además, retención implementada, minimización declarada y secretos fuera del repositorio. |

Mínimo para aprobar: **Sólido (3)**. Clases: [050](../classes/part-10-operacion-seguridad-y-gobierno/050-control-de-acceso-y-seguridad-por-fila/README.md) · [051](../classes/part-10-operacion-seguridad-y-gobierno/051-inyeccion-sql-y-parametrizacion/README.md) · [053](../classes/part-10-operacion-seguridad-y-gobierno/053-privacidad-retencion-y-gobierno-del-dato/README.md)

### Respaldo y recuperación · 12 puntos

**La pregunta que responde:** ¿Cuánto dato se puede perder y cuánto cuesta volver?

**Evidencia que hay que ver:** Una restauración ejecutada, cronometrada y verificada contra el original.

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | Existe un respaldo. |
| 2 · Funcional | El respaldo se automatiza, pero nunca se ha restaurado. |
| 3 · Sólido | Restauración ejecutada y verificada, con RPO y RTO declarados. |
| 4 · Profesional | Además, restauración a un punto en el tiempo y prueba de que el archivo está íntegro. |

Mínimo para aprobar: **Sólido (3)**. Clases: [048](../classes/part-10-operacion-seguridad-y-gobierno/048-respaldo-y-restauracion-probada/README.md) · [036](../classes/part-07-transacciones-concurrencia-y-recuperacion/036-registro-anticipado-y-recuperacion/README.md) · Laboratorios: [08](../labs/08-recovery/README.md)

### Operación y observabilidad · 8 puntos

**La pregunta que responde:** ¿Cómo se sabe que el sistema está sano antes de que alguien se queje?

**Evidencia que hay que ver:** Objetivo de servicio, métricas que lo vigilan y un runbook.

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | No hay métricas. |
| 2 · Funcional | Métricas del sistema sin objetivo declarado. |
| 3 · Sólido | Objetivo de servicio con las métricas que lo miden y una alerta accionable. |
| 4 · Profesional | Además, capacidad proyectada y runbook probado por otra persona. |

Mínimo para aprobar: **Funcional (2)**. Clases: [052](../classes/part-10-operacion-seguridad-y-gobierno/052-observabilidad-slo-y-capacidad/README.md)

### Decisiones y comunicación · 10 puntos

**La pregunta que responde:** ¿Puede otra persona revisar la decisión dentro de dos años?

**Evidencia que hay que ver:** ADR con contexto, alternativas, consecuencias y criterio de revisión.

| Nivel | Qué se observa |
|---|---|
| 1 · Inicial | La decisión está en la cabeza de quien la tomó. |
| 2 · Funcional | Decisión documentada sin alternativas ni consecuencias. |
| 3 · Sólido | ADR completo, con alternativas descartadas y su porqué. |
| 4 · Profesional | Además, costo total estimado, criterio de revisión y plan de vuelta atrás. |

Mínimo para aprobar: **Sólido (3)**. Clases: [063](../classes/part-13-arquitectura-y-proyecto-final/063-registro-de-decisiones-y-costo-total/README.md) · [064](../classes/part-13-arquitectura-y-proyecto-final/064-proyecto-final-disenar-medir-y-defender/README.md)

## Faltas críticas

Suspenden con independencia de la nota. No son errores de ejecución: son incumplimientos del
contrato con el que se trabaja en este programa.

- Datos personales reales sin autorización, en cualquier parte de la entrega.
- Credenciales, tokens o cadenas de conexión en el repositorio.
- Medición de rendimiento inventada o imposible de repetir.
- Respaldo que nunca se restauró.
- Pérdida de un invariante en el caso concurrente obligatorio.
- Conclusión que el trabajo no sostiene: afirmar más de lo que se midió.

## Cómo se corrige, en la práctica

1. **Primero la evidencia, después el documento.** Si una afirmación no tiene salida, comando o
   traza que la respalde, se puntúa como si no estuviera.
2. **Reproduce una cosa.** Elige la afirmación más fuerte del trabajo e intenta repetirla con
   las instrucciones entregadas. Si no se puede, el nivel máximo de esa dimensión es 2.
3. **Pregunta por el límite.** Una entrega de nivel 4 sabe decir qué no demostró; una de nivel 2
   cree haberlo demostrado todo.
4. **Anota el nivel y una frase.** La frase es lo que convierte la nota en aprendizaje.

---

Generado desde `curriculum.yaml` por
[`scripts/generar_evaluacion.py`](../scripts/generar_evaluacion.py). Se edita ahí, no aquí.
