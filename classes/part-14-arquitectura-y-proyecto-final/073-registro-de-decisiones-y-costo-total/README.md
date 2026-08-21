# 073 — Registro de decisiones de arquitectura y costo total

![🗂️ parte](https://img.shields.io/badge/%F0%9F%97%82%EF%B8%8F%20parte-14-2e8b57?style=flat-square) ![🎚️ nivel](https://img.shields.io/badge/%F0%9F%8E%9A%EF%B8%8F%20nivel-Avanzado-8250df?style=flat-square) ![⏱️ duración](https://img.shields.io/badge/%E2%8F%B1%EF%B8%8F%20duraci%C3%B3n-3%20h-24292f?style=flat-square) ![📗 clase](https://img.shields.io/badge/%F0%9F%93%97%20clase-073%20%2F%2074-6e7781?style=flat-square)

> [Programa](../../../README.md) · [Parte 14](../README.md) · [← Anterior](../../part-14-arquitectura-y-proyecto-final/072-persistencia-poliglota-por-evidencia/README.md) · [Siguiente →](../../part-14-arquitectura-y-proyecto-final/074-proyecto-final-disenar-medir-y-defender/README.md)

Parte 14 — Arquitectura y proyecto final · Avanzado ·
3 horas estimadas · motores `postgresql` · laboratorio
[`labs/02-polyglot-modeling`](../../../labs/02-polyglot-modeling/README.md) · 3 fuentes.

**Conceptos centrales:** `ADR` · `contexto` · `consecuencia` · `costo total de propiedad` · `reversibilidad`

**En este caso se comparan 7 motores**: 6 lo resuelven (0 con el resultado comprobado por máquina) y 1 no, con el motivo escrito.

```mermaid
flowchart LR
    C["🗄️ Clase 073"]
    C --> K1["ADR"]
    C --> K2["contexto"]
    C --> K3["consecuencia"]
    C --> K4["costo total de propiedad"]
    C --> K5["reversibilidad"]
    classDef raiz fill:#0b3d2e,stroke:#3fb950,color:#fff
    class C raiz
```

---

## Propósito

Dejar constancia de por qué el sistema es como es. Sin registro de decisiones, cada relevo del equipo debe reconstruir el razonamiento por arqueología, o lo cambia sin saber qué rompe.

## Resultados de aprendizaje

Al terminar podrás:

1. Escribir un registro de decisión de arquitectura (ADR) completo.
2. Distinguir contexto, decisión, alternativas y consecuencias.
3. Calcular el costo total de propiedad de una opción de datos.
4. Evaluar la reversibilidad de una decisión y ajustar el rigor a ella.
5. Escribir la condición de revisión que evita que la decisión se vuelva dogma.

## Fundamentos

### El ADR

Documento corto, versionado junto al código, inmutable una vez aceptado. Si la decisión cambia, se escribe un ADR nuevo que **supersede** al anterior; no se edita el viejo, porque el histórico es el valor.

```markdown
# ADR-007: Usar pgvector en lugar de un motor vectorial dedicado

- Estado: aceptado
- Fecha: 2026-08-19
- Decide: equipo de plataforma
- Supersede a: —

## Contexto
[Situación, restricciones y cifras medidas. Sin opiniones.]

## Decisión
[Qué se hace, en una frase.]

## Alternativas consideradas
[Cada una con por qué se descartó, no solo que se descartó.]

## Consecuencias
[Positivas, negativas y neutras. Las negativas son obligatorias.]

## Condición de revisión
[El umbral medible que obliga a reabrir esta decisión.]
```

La sección que casi siempre falta es **consecuencias negativas**. Un ADR sin ellas no documenta una decisión: la vende. Y la que casi nadie escribe es la **condición de revisión**, que es la que impide que una elección correcta en 2026 siga vigente por inercia en 2030.

### Costo total de propiedad

El costo de una decisión de datos no es la licencia ni la instancia:

| Componente | Cómo estimarlo |
|---|---|
| Infraestructura | Instancias, almacenamiento, red, copias |
| Licencias | Si aplica, con su modelo de crecimiento |
| Operación | Horas/mes de mantenimiento × costo/hora |
| Guardia | Incidentes esperados/mes × horas × costo |
| Aprendizaje | Horas hasta competencia, por persona, incluido el suplente |
| Migración de salida | **Costo de deshacer la decisión** |
| Oportunidad | Lo que el equipo no hace mientras hace esto |

La penúltima fila es la que convierte el análisis en útil: una decisión barata de tomar y carísima de revertir merece mucho más rigor que una reversible.

### Reversibilidad

| Tipo | Ejemplo | Rigor exigible |
|---|---|---|
| **Reversible** | Añadir un índice, ajustar un parámetro | Bajo: probar y medir |
| **Costosa de revertir** | Añadir un almacén, cambiar de modelo de embeddings | Medio: ADR y prueba de concepto |
| **Prácticamente irreversible** | Clave de partición, clave primaria, formato de datos históricos | **Alto**: ADR, prototipo y revisión externa |

El error clásico es aplicar rigor uniforme: se debate una semana sobre un índice —reversible en dos minutos— y se elige la clave de partición en una reunión de media hora.

```mermaid
flowchart TD
    D["Decisión pendiente"] --> R{"¿Reversibilidad?"}
    R -- "Alta" --> F["Probar, medir,<br/>decidir rápido"]
    R -- "Media" --> A["ADR + prueba de concepto<br/>con datos reales"]
    R -- "Baja" --> P["ADR + prototipo +<br/>revisión + plan de salida"]
    F --> W["Registrar solo si<br/>sorprende el resultado"]
    A --> W2["ADR con consecuencias<br/>y condición de revisión"]
    P --> W2
    W2 --> M["Alerta sobre el umbral<br/>de revisión"]
```

## Ejemplo trabajado

ADR completo de la decisión de la clase 062.

```markdown
# ADR-007: Búsqueda semántica con pgvector en lugar de un motor dedicado

- Estado: aceptado
- Fecha: 2026-08-19
- Decide: equipo de plataforma (3 personas)
- Supersede a: —

## Contexto

El buscador debe responder preguntas en lenguaje natural sobre 200 000
fragmentos de contenido del programa.

Cifras medidas sobre el conjunto de evaluación de 60 consultas juzgadas:

| Opción                         | p99    | recall@5 | Sistemas |
|--------------------------------|--------|----------|----------|
| PostgreSQL: tsvector + pgvector|  84 ms |    0,89  |    0     |
| Qdrant + OpenSearch            |  31 ms |    0,91  |    2     |

Exigencia de producto: p99 < 200 ms, recall@5 ≥ 0,85.
El equipo son 3 personas y ya opera PostgreSQL con guardia 24/7.
El corpus crece ~15 % anual.

## Decisión

Implementar la búsqueda híbrida dentro de PostgreSQL, con `tsvector` para la
rama léxica y `pgvector` (HNSW, m=16, ef_search=100) para la vectorial,
fusionando con RRF (k=60).

## Alternativas consideradas

1. **Qdrant + OpenSearch.** Mejor latencia (31 ms frente a 84) y recall
   equivalente (0,91 frente a 0,89). Descartada porque ambas cifras superan la
   exigencia con margen y añade dos sistemas: dos planes de copia, dos modelos
   de control de acceso, dos canales de sincronización y dos fuentes de guardia
   para un equipo de tres personas.

2. **Solo búsqueda léxica.** Descartada: recall@5 = 0,74, por debajo de la
   exigencia. Falla en las preguntas de intención, que son el 45 % del tráfico
   observado.

3. **Servicio gestionado de búsqueda.** Descartada por costo (estimado 4× la
   opción elegida) y porque enviaría contenido a un tercero, lo que exigiría
   revisar el registro de tratamiento (ADR-004).

## Consecuencias

**Positivas**
- Un solo sistema que operar, respaldar y asegurar.
- Los filtros por metadatos son SQL ordinario y se combinan con cualquier
  consulta relacional.
- La consistencia entre contenido y su índice es transaccional: no hay canal
  que pueda desincronizarse.

**Negativas**
- Latencia 2,7× superior a la alternativa dedicada. Aceptable hoy; dejará de
  serlo si la exigencia baja de 100 ms.
- El índice HNSW compite por `shared_buffers` con la carga transaccional.
  Vigilado con la métrica de aciertos de buffer.
- Reconstruir el índice HNSW tras un cambio de modelo bloquea la tabla; hay que
  usar `CREATE INDEX CONCURRENTLY` (clase 049).
- Menos funcionalidad de búsqueda: sin facetas nativas, sin sugerencias, sin
  tolerancia a erratas más allá de `pg_trgm`.

**Neutras**
- El equipo debe aprender `pgvector`: estimado en 8 horas por persona.

## Costo total de propiedad a 3 años

| Componente          | pgvector | Qdrant + OpenSearch |
|---------------------|---------:|--------------------:|
| Infraestructura     |  $ 1 800 |            $ 12 600 |
| Operación (h/mes)   |      1 h |                 8 h |
| Guardia (incid/mes) |      0,2 |                 1,5 |
| Aprendizaje inicial |     24 h |               120 h |
| Migración de salida |     40 h |                80 h |
| **Total estimado**  | **$ 9 400** |       **$ 48 200** |

## Condición de revisión

Se reabre esta decisión si se cumple **cualquiera**:

- El corpus supera 5 000 000 de fragmentos.
- El p99 de búsqueda supera 150 ms durante 7 días seguidos.
- El recall@5 medido cae por debajo de 0,85.
- El producto exige facetas o tolerancia a erratas.

Las tres primeras tienen alerta configurada en el panel de búsqueda.
La cuarta se revisa en cada planificación trimestral.
```

**Lo que hace útil a este ADR y no a uno genérico:**

1. **Las cifras son medidas**, con el conjunto de evaluación nombrado. No hay «es más rápido».
2. **La alternativa descartada era mejor en su métrica principal.** Se explica por qué se descarta igualmente. Un ADR donde la opción elegida gana en todo es sospechoso.
3. **Las consecuencias negativas son concretas y verificables**, incluida la que ya tiene mitigación.
4. **La condición de revisión tiene umbrales medibles y alertas configuradas.** No es «lo revisaremos si hace falta».
5. **El costo incluye la salida.** 40 horas de migración es lo que cuesta cambiar de opinión.

## Comparación

| Documento | Responde | Cuándo se escribe |
|---|---|---|
| ADR | **Por qué** es así | Al decidir |
| Documentación de arquitectura | **Cómo** es | Al construir y al cambiar |
| Runbook | **Qué hacer** cuando falla | Antes de la guardia |
| Postmortem | **Qué pasó** y qué se aprendió | Tras el incidente |
| Registro de tratamiento | **Qué datos** y con qué fin | Al diseñar el esquema (clase 053) |

## Errores frecuentes

1. **ADR sin consecuencias negativas.** Es publicidad, no documentación.
2. **Sin condición de revisión.** La decisión se convierte en dogma.
3. **Editar un ADR aceptado.** Se pierde el histórico; hay que superponer uno nuevo.
4. **Alternativas listadas sin explicar el descarte.** No aporta nada al lector futuro.
5. **Costo solo de infraestructura.** Omite operación, guardia y aprendizaje.
6. **Rigor uniforme.** Se debate lo reversible y se improvisa lo irreversible.
7. **ADR escrito después, para justificar.** Documenta la racionalización, no la decisión.

## De la clase a la operación

El valor del ADR se cobra dos años después, cuando alguien propone cambiar algo y puede leer por qué está así, con qué números y bajo qué condición debería cambiarse. Es el documento con mejor relación entre esfuerzo de escritura y utilidad futura de todo el repositorio.

## Reto de transferencia

1. Escribe el ADR de la decisión de datos más importante de tu sistema actual.
2. Incluye una alternativa que fuese mejor en alguna métrica y explica el descarte.
3. Calcula el costo total a tres años, incluida la migración de salida.
4. Define la condición de revisión con umbrales medibles y configura su alerta.

## Preguntas de evaluación

1. ¿Por qué un ADR aceptado no se edita?
2. Da una decisión tuya prácticamente irreversible y di qué rigor recibió.
3. Estima el costo de salida de tu almacén principal, en horas.
4. Escribe la condición de revisión de una decisión vigente en tu equipo.

---

## 🌐 El mismo problema en cada motor

**Caso:** Lo que cuesta un motor cuando ya nadie mira la comparativa

Las comparativas de motores hablan de rendimiento y de funcionalidades. El
costo total de una decisión de persistencia está en otro sitio, y se paga
durante años: **licencia**, **operación** —respaldos, actualizaciones, alta
disponibilidad, vigilancia—, **personal** que sepa diagnosticarlo a las tres
de la mañana, y **salida**, que es lo que costaría dejarlo.

Un registro de decisión de arquitectura sirve exactamente para dejar eso por
escrito: el contexto, las alternativas consideradas, la decisión, las
consecuencias aceptadas y **qué evidencia obligaría a revisarla**. Sin ese
último punto, un registro es una justificación; con él, es una decisión de
ingeniería.

Esta comparación no mide nada: enumera, motor por motor, dónde está el costo
que no aparece en la portada.

Esta comparación es **conceptual**: la decisión no se reduce a una consulta con
resultado, así que aquí no hay sello de máquina. Lo que se compara es lo que
cada motor **ofrece** y a qué precio, con la página oficial al lado de cada
afirmación.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| PostgreSQL | sí | conceptual | — | [doc oficial](https://www.postgresql.org/about/licence/) |
| Oracle Database | sí | conceptual | — | [doc oficial](https://docs.oracle.com/en/database/oracle/oracle-database/23/dblic/) |
| Microsoft SQL Server | sí | conceptual | — | [doc oficial](https://learn.microsoft.com/sql/sql-server/editions-and-components-of-sql-server-2022) |
| MongoDB | sí | conceptual | — | [doc oficial](https://www.mongodb.com/legal/licensing/server-side-public-license) |
| Redis | sí | conceptual | — | [doc oficial](https://redis.io/legal/licenses/) |
| Google BigQuery | sí | conceptual | — | [doc oficial](https://cloud.google.com/bigquery/pricing) |
| SQLite | **no** | — | — | [doc oficial](https://sqlite.org/copyright.html) |

### Los que resuelven el caso

#### PostgreSQL

- **Cómo se hace aquí:** Licencia permisiva y sin costo. El costo real es de **operación**: la alta disponibilidad la aporta una herramienta externa que hay que elegir y operar, el vacío hay que vigilarlo, y las actualizaciones de versión mayor exigen planificación. A cambio, el conocimiento es abundante y transferible.
- **Por qué sí:** Coste de salida bajo: es SQL estándar en su mayor parte, hay decenas de servicios administrados compatibles y el volcado es portable. La decisión se puede revertir.
- **Por qué no:** «Gratis» esconde el costo de personal: una instalación sin nadie que entienda el vacío, los planes y la réplica acaba siendo más cara que un servicio administrado que nadie tiene que atender de madrugada.
- 📄 Documentación oficial: <https://www.postgresql.org/about/licence/>

#### Oracle Database

- **Cómo se hace aquí:** Licencia por núcleo, con opciones que se cobran aparte —particionado, diagnóstico, alta disponibilidad avanzada— y auditorías de cumplimiento. El costo es explícito, alto y predecible.
- **Por qué sí:** A cambio hay soporte contractual, herramientas de diagnóstico muy maduras y un mercado de profesionales con décadas de experiencia. En sistemas donde una hora de caída cuesta más que la licencia anual, la cuenta sale.
- **Por qué no:** El costo de **salida** es el más alto de la lista: PL/SQL, paquetes, disparadores y particularidades del dialecto atan la aplicación al motor. Migrar de Oracle es un proyecto de años, y eso forma parte del precio aunque no aparezca en la factura.
- 📄 Documentación oficial: <https://docs.oracle.com/en/database/oracle/oracle-database/23/dblic/>

#### Microsoft SQL Server

- **Cómo se hace aquí:** Licencia por núcleo con ediciones escalonadas; la gratuita, Express, está limitada a 10 GB por base y a un socket. Integración muy fuerte con el resto del ecosistema de su fabricante.
- **Por qué sí:** Herramientas de administración y diagnóstico excelentes y un costo de personal bajo en organizaciones que ya trabajan con ese ecosistema: la curva de aprendizaje ya está pagada.
- **Por qué no:** El límite de la edición gratuita se alcanza antes de lo que parece, y el salto a la de pago es escalonado y caro. Y la decisión rara vez es técnica: la toma el contrato marco de la organización.
- 📄 Documentación oficial: <https://learn.microsoft.com/sql/sql-server/editions-and-components-of-sql-server-2022>

#### MongoDB

- **Cómo se hace aquí:** La edición Community usa la licencia SSPL, que **no** está reconocida como libre por la OSI y afecta a quien quiera ofrecerlo como servicio. Para uso interno no cambia nada; para un producto que se despliega en casa del cliente, hay que leerla.
- **Por qué sí:** Costo de operación bajo para lo que ofrece: la alta disponibilidad viene en el producto, sin herramientas externas, y su servicio administrado quita casi toda la administración.
- **Por qué no:** El costo de salida es alto de una forma poco visible: no es el motor, es el **modelo de datos**. Los documentos incrustados y la ausencia de esquema no se traducen a tablas sin rediseñar la aplicación.
- 📄 Documentación oficial: <https://www.mongodb.com/legal/licensing/server-side-public-license>

#### Redis

- **Cómo se hace aquí:** Su licencia cambió en 2024 —a un esquema dual que no es libre según la OSI— y de ahí salieron bifurcaciones mantenidas por fundaciones. Es el ejemplo más reciente de un riesgo real: **la licencia de un motor puede cambiar después de haberlo adoptado**.
- **Por qué sí:** Operación mínima y costo de salida bajo: se usa para datos desechables, y cambiar de implementación compatible es de las migraciones más baratas que existen.
- **Por qué no:** El costo oculto es la memoria: es el almacenamiento más caro por gibibyte, y un conjunto de datos que crece sin política de caducidad se traduce directamente en factura.
- 📄 Documentación oficial: <https://redis.io/legal/licenses/>

#### Google BigQuery

- **Cómo se hace aquí:** Sin licencia y sin operación: se paga por almacenamiento y por **bytes leídos** en cada consulta, o por capacidad reservada. El costo se traslada por completo del personal a la factura.
- **Por qué sí:** Para una carga analítica esporádica es imbatible en costo total: cero administración, cero servidores y cero personal dedicado.
- **Por qué no:** El costo es **variable y lo controla quien escribe las consultas**: un `SELECT *` mal filtrado sobre una tabla grande cuesta dinero real, y se repite cada vez que alguien recarga un panel. Hay que poner cuotas antes de dar acceso, no después.
- 📄 Documentación oficial: <https://cloud.google.com/bigquery/pricing>

### Los que no resuelven este caso — y qué se hace en su lugar

Descartar un motor con un argumento es tan formativo como usarlo. Ninguna de estas filas dice que el motor sea peor: dice que este problema no es el suyo.

| Motor | Por qué no | Qué se hace en su lugar | Fuente |
|---|---|---|---|
| SQLite | Es de dominio público y su costo de operación es cero porque no hay nada que operar: no hay decisión de costo total que documentar. Incluirlo aquí sería rellenar la matriz. | Su costo aparece en otro sitio y es real: el día en que el sistema necesita dos escritores o acceso remoto, hay que migrar. Ese es el registro de decisión que conviene escribir el primer día, no el último. | [doc](https://sqlite.org/copyright.html) |

---

## Laboratorio

```bash
python scripts/validate_repository.py
# labs/02-polyglot-modeling se entrega escrito: no hay guion que ejecutar
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

- **Peter Bailis, Joseph M. Hellerstein, Michael Stonebraker** (2015). [Readings in Database Systems](http://www.redbook.io/). 5.a ed. MIT Press. ISBN 978-0-262-52964-3.  
  Antologia comentada de acceso libre. Cada capitulo situa los papers en su discusión.
- **Joe Reis, Matt Housley** (2022). [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/). O'Reilly. ISBN 978-1-0981-0830-4.  
  Ciclo de vida de la ingenieria de datos e integración entre sistemas.
- **Laine Campbell, Charity Majors** (2017). [Database Reliability Engineering](https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/). O'Reilly. ISBN 978-1-4919-2594-2.  
  Operación, respaldos, objetivos de servicio y gestion de cambios.

---

> [Programa](../../../README.md) · [Parte 14](../README.md) · [← Anterior](../../part-14-arquitectura-y-proyecto-final/072-persistencia-poliglota-por-evidencia/README.md) · [Siguiente →](../../part-14-arquitectura-y-proyecto-final/074-proyecto-final-disenar-medir-y-defender/README.md)
