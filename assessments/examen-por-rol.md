# Examen final por rol

Cada [ruta por rol](../rutas/README.md) cierra con el mismo examen: teoría, práctica y defensa.
No es un formulario de opción múltiple, porque este programa no evalúa memoria: **un resultado
correcto sin explicación no demuestra transferencia**.

## Estructura común

| Bloque | Puntos | Formato |
|---|---:|---|
| **Teoría** | 25 | Responder por escrito seis preguntas del banco de autoevaluación, elegidas entre las partes de la ruta. Se corrige con la dimensión de decisiones y comunicación: explicar el mecanismo, no repetir la definición. |
| **Práctica** | 50 | Ejecutar los laboratorios de la ruta, extender uno de ellos con un caso propio y entregar la evidencia: comando, salida completa, entorno y explicación de por qué el resultado es el que es. |
| **Informe y defensa** | 25 | Un documento breve —decisión, evidencia y límites— defendido en quince minutos ante alguien que pregunte. Se corrige con la rúbrica del proyecto final. |

**Aprobado:** 70 de 100 · Práctica ≥ 30/50.

La teoría y el informe se corrigen con la [rúbrica del proyecto final](rubric.md); la práctica,
con la evidencia entregada. Las [faltas críticas](rubric.md#faltas-críticas) suspenden aquí
también.

## Por qué la práctica pesa la mitad

Porque es lo único que no se puede fingir. Una respuesta teórica se puede leer en cualquier
sitio; una salida de laboratorio con su comando, su entorno y su explicación solo la tiene quien
la ejecutó y entendió.

## Desarrollador de aplicaciones

Nivel entrada · 10 partes · 152 horas ·
[guía de la ruta](../rutas/desarrollo-de-aplicaciones.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Fundamentos, sistemas y método) · 01 (Modelado conceptual y requisitos) · 02 (Modelo relacional y álgebra) · 03 (SQL en profundidad)…
  Las clases que no se saltan: [007](../classes/part-01-modelado-conceptual-y-requisitos/007-claves-identidad-natural-y-sustituta/README.md) · [014](../classes/part-03-sql-en-profundidad/014-ddl-el-esquema-como-contrato/README.md) · [016](../classes/part-03-sql-en-profundidad/016-reuniones-inner-outer-semi-y-anti/README.md) · [019](../classes/part-03-sql-en-profundidad/019-nulos-y-logica-de-tres-valores/README.md) · [037](../classes/part-07-transacciones-concurrencia-y-recuperacion/037-concurrencia-en-la-aplicacion/README.md) · [049](../classes/part-10-operacion-seguridad-y-gobierno/049-migraciones-evolutivas-sin-caida/README.md) · [051](../classes/part-10-operacion-seguridad-y-gobierno/051-inyeccion-sql-y-parametrizacion/README.md).
- **Práctica (50 pt):** Ejecuta 01, 03, 04 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [03 — Actualización perdida y sus tres correcciones](../labs/03-transactions/README.md) · [04 — Planes de ejecución y costo real de un índice](../labs/04-indexing/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Desarrollador backend, Desarrollador full-stack, Ingeniero de software.

## Ingeniero de datos

Nivel intermedio · 9 partes · 131 horas ·
[guía de la ruta](../rutas/ingenieria-de-datos.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Fundamentos, sistemas y método) · 01 (Modelado conceptual y requisitos) · 02 (Modelo relacional y álgebra) · 03 (SQL en profundidad)…
  Las clases que no se saltan: [030](../classes/part-06-grafos-columnas-tiempo-y-busqueda/030-series-temporales-cardinalidad-y-retencion/README.md) · [032](../classes/part-06-grafos-columnas-tiempo-y-busqueda/032-analitica-columnar-y-vectorizacion/README.md) · [054](../classes/part-11-analitica-integracion-y-streaming/054-oltp-frente-a-olap/README.md) · [055](../classes/part-11-analitica-integracion-y-streaming/055-modelado-dimensional/README.md) · [056](../classes/part-11-analitica-integracion-y-streaming/056-integracion-etl-elt-y-captura-de-cambios/README.md) · [057](../classes/part-11-analitica-integracion-y-streaming/057-streaming-tiempo-de-evento-y-ventanas/README.md).
- **Práctica (50 pt):** Ejecuta 01, 05 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [02 — Modelado políglota del mismo dominio](../labs/02-polyglot-modeling/README.md) · [05 — Elección por carga de trabajo en almacenes no relacionales](../labs/05-nosql-workloads/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Ingeniero de datos, Ingeniero de plataforma de datos, Ingeniero de streaming.

## DBA / SRE de datos

Nivel intermedio · 9 partes · 143 horas ·
[guía de la ruta](../rutas/fiabilidad-y-operacion.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Fundamentos, sistemas y método) · 01 (Modelado conceptual y requisitos) · 03 (SQL en profundidad) · 04 (Motores relacionales y dialectos)…
  Las clases que no se saltan: [036](../classes/part-07-transacciones-concurrencia-y-recuperacion/036-registro-anticipado-y-recuperacion/README.md) · [038](../classes/part-08-almacenamiento-indices-y-planes/038-paginas-filas-y-buffer-pool/README.md) · [042](../classes/part-08-almacenamiento-indices-y-planes/042-planes-de-ejecucion-y-refutacion/README.md) · [048](../classes/part-10-operacion-seguridad-y-gobierno/048-respaldo-y-restauracion-probada/README.md) · [049](../classes/part-10-operacion-seguridad-y-gobierno/049-migraciones-evolutivas-sin-caida/README.md) · [052](../classes/part-10-operacion-seguridad-y-gobierno/052-observabilidad-slo-y-capacidad/README.md).
- **Práctica (50 pt):** Ejecuta 01, 03, 04 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [03 — Actualización perdida y sus tres correcciones](../labs/03-transactions/README.md) · [04 — Planes de ejecución y costo real de un índice](../labs/04-indexing/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Administrador de bases de datos, SRE de datos, Ingeniero de fiabilidad.

## Arquitecto de datos

Nivel avanzado · 14 partes · 210 horas ·
[guía de la ruta](../rutas/arquitectura.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Fundamentos, sistemas y método) · 01 (Modelado conceptual y requisitos) · 02 (Modelo relacional y álgebra) · 03 (SQL en profundidad)…
  Las clases que no se saltan: [045](../classes/part-09-distribucion-replica-y-consistencia/045-cap-pacelc-y-lo-que-realmente-se-elige/README.md) · [046](../classes/part-09-distribucion-replica-y-consistencia/046-modelos-de-consistencia-y-garantias-de-sesion/README.md) · [047](../classes/part-09-distribucion-replica-y-consistencia/047-consenso-y-transacciones-distribuidas/README.md) · [062](../classes/part-13-arquitectura-y-proyecto-final/062-persistencia-poliglota-por-evidencia/README.md) · [063](../classes/part-13-arquitectura-y-proyecto-final/063-registro-de-decisiones-y-costo-total/README.md) · [064](../classes/part-13-arquitectura-y-proyecto-final/064-proyecto-final-disenar-medir-y-defender/README.md).
- **Práctica (50 pt):** Ejecuta 04, 06 y extiende uno con un caso propio. Laboratorios de la ruta:
  [02 — Modelado políglota del mismo dominio](../labs/02-polyglot-modeling/README.md) · [04 — Planes de ejecución y costo real de un índice](../labs/04-indexing/README.md) · [06 — Recuperación vectorial explicable](../labs/06-vector-search/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Arquitecto de datos, Arquitecto de soluciones, Ingeniero de staff.

## Analytics engineer / BI

Nivel intermedio · 8 partes · 115 horas ·
[guía de la ruta](../rutas/analitica-y-bi.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Fundamentos, sistemas y método) · 01 (Modelado conceptual y requisitos) · 02 (Modelo relacional y álgebra) · 03 (SQL en profundidad)…
  Las clases que no se saltan: [017](../classes/part-03-sql-en-profundidad/017-agregacion-group-by-y-having/README.md) · [018](../classes/part-03-sql-en-profundidad/018-cte-subconsultas-y-funciones-de-ventana/README.md) · [032](../classes/part-06-grafos-columnas-tiempo-y-busqueda/032-analitica-columnar-y-vectorizacion/README.md) · [054](../classes/part-11-analitica-integracion-y-streaming/054-oltp-frente-a-olap/README.md) · [055](../classes/part-11-analitica-integracion-y-streaming/055-modelado-dimensional/README.md) · [056](../classes/part-11-analitica-integracion-y-streaming/056-integracion-etl-elt-y-captura-de-cambios/README.md).
- **Práctica (50 pt):** Ejecuta 01, 04 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [04 — Planes de ejecución y costo real de un índice](../labs/04-indexing/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Analytics engineer, Ingeniero de BI, Analista de datos sénior.

## Ingeniero de IA aplicada y recuperación

Nivel avanzado · 9 partes · 131 horas ·
[guía de la ruta](../rutas/ia-y-recuperacion.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Fundamentos, sistemas y método) · 01 (Modelado conceptual y requisitos) · 02 (Modelo relacional y álgebra) · 03 (SQL en profundidad)…
  Las clases que no se saltan: [031](../classes/part-06-grafos-columnas-tiempo-y-busqueda/031-busqueda-de-texto-indice-invertido-y-relevancia/README.md) · [041](../classes/part-08-almacenamiento-indices-y-planes/041-indices-especializados/README.md) · [058](../classes/part-12-vectores-recuperacion-y-rag/058-embeddings-y-metricas-de-distancia/README.md) · [059](../classes/part-12-vectores-recuperacion-y-rag/059-indices-vectoriales-aproximados/README.md) · [060](../classes/part-12-vectores-recuperacion-y-rag/060-busqueda-hibrida-y-filtrado/README.md) · [061](../classes/part-12-vectores-recuperacion-y-rag/061-rag-evaluable/README.md).
- **Práctica (50 pt):** Ejecuta 01, 05, 06 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [05 — Elección por carga de trabajo en almacenes no relacionales](../labs/05-nosql-workloads/README.md) · [06 — Recuperación vectorial explicable](../labs/06-vector-search/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Ingeniero de IA aplicada, Ingeniero de búsqueda y recuperación, ML engineer de producto.

## Gobierno y privacidad del dato

Nivel intermedio · 8 partes · 127 horas ·
[guía de la ruta](../rutas/gobierno-y-privacidad.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Fundamentos, sistemas y método) · 01 (Modelado conceptual y requisitos) · 03 (SQL en profundidad) · 07 (Transacciones, concurrencia y recuperación)…
  Las clases que no se saltan: [013](../classes/part-02-modelo-relacional-y-algebra/013-integridad-restricciones-y-acciones-referenciales/README.md) · [048](../classes/part-10-operacion-seguridad-y-gobierno/048-respaldo-y-restauracion-probada/README.md) · [050](../classes/part-10-operacion-seguridad-y-gobierno/050-control-de-acceso-y-seguridad-por-fila/README.md) · [051](../classes/part-10-operacion-seguridad-y-gobierno/051-inyeccion-sql-y-parametrizacion/README.md) · [053](../classes/part-10-operacion-seguridad-y-gobierno/053-privacidad-retencion-y-gobierno-del-dato/README.md) · [063](../classes/part-13-arquitectura-y-proyecto-final/063-registro-de-decisiones-y-costo-total/README.md).
- **Práctica (50 pt):** Ejecuta 01, 03 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [03 — Actualización perdida y sus tres correcciones](../labs/03-transactions/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Responsable de gobierno del dato, Especialista en cumplimiento de datos, Delegado de protección de datos técnico.

## Qué entregar

Un repositorio —o una carpeta— con:

```text
evidencia/
  01-teoria.md          seis preguntas respondidas, con el mecanismo explicado
  02-practica/
    comando.txt         lo que ejecutaste, literal
    salida.txt          la salida completa, sin recortar
    entorno.md          versión del motor, del sistema y de Python
    explicacion.md      por qué el resultado es el que es, y qué NO demuestra
  03-informe.md         decisión, evidencia y límites
```

Una captura sin comando no es evidencia: no se puede repetir.

---

Generado desde `curriculum.yaml` por
[`scripts/generar_evaluacion.py`](../scripts/generar_evaluacion.py). Se edita ahí, no aquí.
