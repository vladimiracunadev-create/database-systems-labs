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

Nivel entrada · 11 partes · 172 horas ·
[guía de la ruta](../rutas/desarrollo-de-aplicaciones.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Primeros pasos: del archivo a la base de datos) · 01 (Fundamentos, sistemas y método) · 02 (Modelado conceptual y requisitos) · 03 (Modelo relacional y álgebra)…
  Las clases que no se saltan: [017](../classes/part-02-modelado-conceptual-y-requisitos/017-claves-identidad-natural-y-sustituta/README.md) · [024](../classes/part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md) · [026](../classes/part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md) · [029](../classes/part-04-sql-en-profundidad/029-nulos-y-logica-de-tres-valores/README.md) · [047](../classes/part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md) · [059](../classes/part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md) · [061](../classes/part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md).
- **Práctica (50 pt):** Ejecuta 01, 03, 04 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [03 — Actualización perdida y sus tres correcciones](../labs/03-transactions/README.md) · [04 — Planes de ejecución y costo real de un índice](../labs/04-indexing/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Desarrollador backend, Desarrollador full-stack, Ingeniero de software.

## Ingeniero de datos

Nivel intermedio · 10 partes · 151 horas ·
[guía de la ruta](../rutas/ingenieria-de-datos.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Primeros pasos: del archivo a la base de datos) · 01 (Fundamentos, sistemas y método) · 02 (Modelado conceptual y requisitos) · 03 (Modelo relacional y álgebra)…
  Las clases que no se saltan: [040](../classes/part-07-grafos-columnas-tiempo-y-busqueda/040-series-temporales-cardinalidad-y-retencion/README.md) · [042](../classes/part-07-grafos-columnas-tiempo-y-busqueda/042-analitica-columnar-y-vectorizacion/README.md) · [064](../classes/part-12-analitica-integracion-y-streaming/064-oltp-frente-a-olap/README.md) · [065](../classes/part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) · [066](../classes/part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md) · [067](../classes/part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md).
- **Práctica (50 pt):** Ejecuta 01, 05 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [02 — Modelado políglota del mismo dominio](../labs/02-polyglot-modeling/README.md) · [05 — Elección por carga de trabajo en almacenes no relacionales](../labs/05-nosql-workloads/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Ingeniero de datos, Ingeniero de plataforma de datos, Ingeniero de streaming.

## DBA / SRE de datos

Nivel intermedio · 10 partes · 163 horas ·
[guía de la ruta](../rutas/fiabilidad-y-operacion.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Primeros pasos: del archivo a la base de datos) · 01 (Fundamentos, sistemas y método) · 02 (Modelado conceptual y requisitos) · 04 (SQL en profundidad)…
  Las clases que no se saltan: [046](../classes/part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md) · [048](../classes/part-09-almacenamiento-indices-y-planes/048-paginas-filas-y-buffer-pool/README.md) · [052](../classes/part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md) · [058](../classes/part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md) · [059](../classes/part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md) · [062](../classes/part-11-operacion-seguridad-y-gobierno/062-observabilidad-slo-y-capacidad/README.md).
- **Práctica (50 pt):** Ejecuta 01, 03, 04 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [03 — Actualización perdida y sus tres correcciones](../labs/03-transactions/README.md) · [04 — Planes de ejecución y costo real de un índice](../labs/04-indexing/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Administrador de bases de datos, SRE de datos, Ingeniero de fiabilidad.

## Arquitecto de datos

Nivel avanzado · 15 partes · 230 horas ·
[guía de la ruta](../rutas/arquitectura.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Primeros pasos: del archivo a la base de datos) · 01 (Fundamentos, sistemas y método) · 02 (Modelado conceptual y requisitos) · 03 (Modelo relacional y álgebra)…
  Las clases que no se saltan: [055](../classes/part-10-distribucion-replica-y-consistencia/055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) · [056](../classes/part-10-distribucion-replica-y-consistencia/056-modelos-de-consistencia-y-garantias-de-sesion/README.md) · [057](../classes/part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) · [072](../classes/part-14-arquitectura-y-proyecto-final/072-persistencia-poliglota-por-evidencia/README.md) · [073](../classes/part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md) · [074](../classes/part-14-arquitectura-y-proyecto-final/074-proyecto-final-disenar-medir-y-defender/README.md).
- **Práctica (50 pt):** Ejecuta 04, 06 y extiende uno con un caso propio. Laboratorios de la ruta:
  [02 — Modelado políglota del mismo dominio](../labs/02-polyglot-modeling/README.md) · [04 — Planes de ejecución y costo real de un índice](../labs/04-indexing/README.md) · [06 — Recuperación vectorial explicable](../labs/06-vector-search/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Arquitecto de datos, Arquitecto de soluciones, Ingeniero de staff.

## Analytics engineer / BI

Nivel intermedio · 9 partes · 135 horas ·
[guía de la ruta](../rutas/analitica-y-bi.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Primeros pasos: del archivo a la base de datos) · 01 (Fundamentos, sistemas y método) · 02 (Modelado conceptual y requisitos) · 03 (Modelo relacional y álgebra)…
  Las clases que no se saltan: [027](../classes/part-04-sql-en-profundidad/027-agregacion-group-by-y-having/README.md) · [028](../classes/part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md) · [042](../classes/part-07-grafos-columnas-tiempo-y-busqueda/042-analitica-columnar-y-vectorizacion/README.md) · [064](../classes/part-12-analitica-integracion-y-streaming/064-oltp-frente-a-olap/README.md) · [065](../classes/part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) · [066](../classes/part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md).
- **Práctica (50 pt):** Ejecuta 01, 04 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [04 — Planes de ejecución y costo real de un índice](../labs/04-indexing/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Analytics engineer, Ingeniero de BI, Analista de datos sénior.

## Ingeniero de IA aplicada y recuperación

Nivel avanzado · 10 partes · 151 horas ·
[guía de la ruta](../rutas/ia-y-recuperacion.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Primeros pasos: del archivo a la base de datos) · 01 (Fundamentos, sistemas y método) · 02 (Modelado conceptual y requisitos) · 03 (Modelo relacional y álgebra)…
  Las clases que no se saltan: [041](../classes/part-07-grafos-columnas-tiempo-y-busqueda/041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) · [051](../classes/part-09-almacenamiento-indices-y-planes/051-indices-especializados/README.md) · [068](../classes/part-13-vectores-recuperacion-y-rag/068-embeddings-y-metricas-de-distancia/README.md) · [069](../classes/part-13-vectores-recuperacion-y-rag/069-indices-vectoriales-aproximados/README.md) · [070](../classes/part-13-vectores-recuperacion-y-rag/070-busqueda-hibrida-y-filtrado/README.md) · [071](../classes/part-13-vectores-recuperacion-y-rag/071-rag-evaluable/README.md).
- **Práctica (50 pt):** Ejecuta 01, 05, 06 y extiende uno con un caso propio. Laboratorios de la ruta:
  [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [05 — Elección por carga de trabajo en almacenes no relacionales](../labs/05-nosql-workloads/README.md) · [06 — Recuperación vectorial explicable](../labs/06-vector-search/README.md).
- **Informe (25 pt):** una decisión de tu contexto real, con la
  evidencia que la sostiene y sus límites, defendida en quince minutos.
- **Cargos a los que apunta:** Ingeniero de IA aplicada, Ingeniero de búsqueda y recuperación, ML engineer de producto.

## Gobierno y privacidad del dato

Nivel intermedio · 9 partes · 147 horas ·
[guía de la ruta](../rutas/gobierno-y-privacidad.md)

- **Teoría (25 pt):** seis preguntas del
  [banco de autoevaluación](../assessments/README.md) sobre las partes 00 (Primeros pasos: del archivo a la base de datos) · 01 (Fundamentos, sistemas y método) · 02 (Modelado conceptual y requisitos) · 04 (SQL en profundidad)…
  Las clases que no se saltan: [023](../classes/part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md) · [058](../classes/part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md) · [060](../classes/part-11-operacion-seguridad-y-gobierno/060-control-de-acceso-y-seguridad-por-fila/README.md) · [061](../classes/part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md) · [063](../classes/part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) · [073](../classes/part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md).
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
