# AWS Certified Data Engineer – Associate

> **Código:** DEA-C01 · **Proveedor:** Amazon Web Services ·
> **Nivel:** Intermedio · **Renovación:** 3 años ·
> [Página oficial](https://aws.amazon.com/certification/certified-data-engineer-associate/) · [Temario oficial](https://d1.awsstatic.com/training-and-certification/docs-data-engineer-associate/AWS-Certified-Data-Engineer-Associate_Exam-Guide.pdf)

[⬅️ Volver al índice de certificaciones](README.md)

La credencial de ingeniería de datos de AWS: ingesta y transformación, gestión de almacenes, operación y gobierno. Los pesos por dominio son oficiales; el desglose por tarea vive en un PDF que este repositorio no puede citar con exactitud, así que la cobertura se declara por dominio y se marca como estimación.

## 📊 Cobertura del programa: 62 %

`██████░░░░` 62.4 % — media ponderada por el peso oficial de cada dominio.

**Método:** El proveedor publica el peso del dominio pero no un desglose citable con exactitud, así que la cobertura del dominio es una estimación declarada, justificada con las partes y clases que la sostienen. Se marca como estimación en la ficha.

| Dominio del examen | Peso oficial | Base del cálculo | Cobertura |
|---|---|---|---:|
| Data Ingestion and Transformation | 34% | estimación declarada | 60 % |
| Data Store Management | 26% | estimación declarada | 70 % |
| Data Operations and Support | 22% | estimación declarada | 55 % |
| Data Security and Governance | 18% | estimación declarada | 65 % |

Temario vigente comprobado el **2026-08-20**.

## Mapeo dominio a dominio

### Data Ingestion and Transformation · 34%

**Cobertura estimada: 60 %.** El programa cubre ETL/ELT, captura de cambios, streaming con tiempo de evento y transformación en SQL. No cubre los servicios de AWS (Glue, Kinesis, EMR, Lambda) que el examen evalúa por nombre.

Clases que la sostienen: [066](../classes/part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md) [067](../classes/part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md) [040](../classes/part-07-grafos-columnas-tiempo-y-busqueda/040-series-temporales-cardinalidad-y-retencion/README.md) [028](../classes/part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md)

### Data Store Management · 26%

**Cobertura estimada: 70 %.** Elección de almacén por carga, formato columnar, particionado, modelado y ciclo de vida del dato están cubiertos como mecanismo; el catálogo de servicios de AWS, no.

Clases que la sostienen: [030](../classes/part-05-motores-relacionales-y-dialectos/030-portabilidad-y-matriz-de-dialectos/README.md) [033](../classes/part-05-motores-relacionales-y-dialectos/033-sqlite-y-duckdb-motores-embebidos/README.md) [042](../classes/part-07-grafos-columnas-tiempo-y-busqueda/042-analitica-columnar-y-vectorizacion/README.md) [048](../classes/part-09-almacenamiento-indices-y-planes/048-paginas-filas-y-buffer-pool/README.md) [065](../classes/part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md)

### Data Operations and Support · 22%

**Cobertura estimada: 55 %.** SQL analítico, planes y observabilidad sí; la automatización con servicios de AWS y sus herramientas de calidad de datos, no.

Clases que la sostienen: [027](../classes/part-04-sql-en-profundidad/027-agregacion-group-by-y-having/README.md) [028](../classes/part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md) [052](../classes/part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md) [062](../classes/part-11-operacion-seguridad-y-gobierno/062-observabilidad-slo-y-capacidad/README.md)

### Data Security and Governance · 18%

**Cobertura estimada: 65 %.** Autenticación, autorización, privilegio mínimo, privacidad y retención están cubiertos; el cifrado gestionado y la auditoría específicos de AWS, no.

Clases que la sostienen: [060](../classes/part-11-operacion-seguridad-y-gobierno/060-control-de-acceso-y-seguridad-por-fila/README.md) [061](../classes/part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md) [063](../classes/part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) [023](../classes/part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md)

## 🎯 La brecha, y cómo cerrarla

Todo el catálogo de servicios de AWS. El programa te deja el criterio —qué almacén, qué formato, qué semántica de entrega— y el examen te pedirá además el nombre del servicio que lo hace. Complétalo con la documentación oficial y con práctica en una cuenta real.

## 🧭 Por dónde empezar aquí

- **Ruta recomendada:** [Ingeniero de datos](../rutas/ingenieria-de-datos.md) — Tuberías que otros usan para decidir: integración, captura de cambios, modelado analítico y streaming con semántica declarada.
- **Laboratorios que la preparan:** [01 — Fundamentos de SQL sobre el dominio educativo](../labs/01-sql-foundations/README.md) · [02 — Modelado políglota del mismo dominio](../labs/02-polyglot-modeling/README.md) · [05 — Elección por carga de trabajo en almacenes no relacionales](../labs/05-nosql-workloads/README.md)
- **Para quién tiene sentido:** Quien construye tuberías sobre AWS y necesita una credencial que lo acredite ante clientes.

---

> Mapeo orientativo, no avalado por Microsoft, Amazon Web Services ni ningún otro proveedor. Los temarios cambian: la fecha de verificación de cada uno está en su ficha, y conviene comprobar la versión vigente antes de inscribirse.
