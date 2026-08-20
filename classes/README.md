# Clases

64 clases repartidas en 14 partes, 210 horas estimadas.

Cada clase declara sus fuentes al final. Este índice y los README de clase se
generan con `python scripts/build_classes.py`; la materia se edita en el
`lesson.md` de cada carpeta.

## [Parte 00 — Fundamentos, sistemas y método](part-00-fundamentos-datos-sistemas-y-metodo/README.md)

Qué problema resuelve un gestor de bases de datos, qué hay dentro de él y cómo se monta un entorno donde cada afirmación pueda comprobarse.

*4 clases · 12 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [001](part-00-fundamentos-datos-sistemas-y-metodo/001-que-resuelve-un-sistema-de-bases-de-datos/README.md) | Qué resuelve un sistema de bases de datos y qué no | Fundamentos | 3 |
| [002](part-00-fundamentos-datos-sistemas-y-metodo/002-arquitectura-interna-de-un-gestor/README.md) | Arquitectura interna de un gestor, del cliente al disco | Fundamentos | 3 |
| [003](part-00-fundamentos-datos-sistemas-y-metodo/003-independencia-de-datos-y-niveles-de-esquema/README.md) | Independencia de datos y los tres niveles de esquema | Fundamentos | 3 |
| [004](part-00-fundamentos-datos-sistemas-y-metodo/004-entorno-reproducible-y-evidencia/README.md) | Entorno reproducible y evidencia comprobable | Fundamentos | 3 |

## [Parte 01 — Modelado conceptual y requisitos](part-01-modelado-conceptual-y-requisitos/README.md)

Del enunciado ambiguo al esquema defendible: entidades, claves, dependencias funcionales y la decisión consciente de desnormalizar.

*5 clases · 16 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [005](part-01-modelado-conceptual-y-requisitos/005-de-requisitos-a-entidades/README.md) | De requisitos ambiguos a entidades defendibles | Fundamentos | 3 |
| [006](part-01-modelado-conceptual-y-requisitos/006-entidad-relacion-cardinalidad-y-participacion/README.md) | Entidad-relación, cardinalidad y participación | Fundamentos | 3 |
| [007](part-01-modelado-conceptual-y-requisitos/007-claves-identidad-natural-y-sustituta/README.md) | Claves, identidad y el debate natural frente a sustituta | Fundamentos | 3 |
| [008](part-01-modelado-conceptual-y-requisitos/008-normalizacion-y-dependencias-funcionales/README.md) | Normalización de 1FN a BCFN con dependencias funcionales | Intermedio | 4 |
| [009](part-01-modelado-conceptual-y-requisitos/009-desnormalizacion-deliberada/README.md) | Desnormalización deliberada y patrones de acceso | Intermedio | 3 |

## [Parte 02 — Modelo relacional y álgebra](part-02-modelo-relacional-y-algebra/README.md)

La teoría que SQL implementa a medias: relaciones como conjuntos, operadores del álgebra, cálculo relacional e integridad declarada.

*4 clases · 13 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [010](part-02-modelo-relacional-y-algebra/010-la-relacion-como-conjunto/README.md) | La relación como conjunto: tuplas, dominios y acceso por valor | Fundamentos | 3 |
| [011](part-02-modelo-relacional-y-algebra/011-algebra-relacional-operadores/README.md) | Álgebra relacional: selección, proyección, producto y reunión | Fundamentos | 4 |
| [012](part-02-modelo-relacional-y-algebra/012-calculo-relacional-y-equivalencia/README.md) | Cálculo relacional y su equivalencia con el álgebra | Intermedio | 3 |
| [013](part-02-modelo-relacional-y-algebra/013-integridad-restricciones-y-acciones-referenciales/README.md) | Integridad: restricciones, claves foraneas y acciones referenciales | Intermedio | 3 |

## [Parte 03 — SQL en profundidad](part-03-sql-en-profundidad/README.md)

Escribir SQL cuya semántica se pueda defender: definición del esquema, reuniones, agregación, ventanas y el comportamiento real de los nulos.

*6 clases · 20 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [014](part-03-sql-en-profundidad/014-ddl-el-esquema-como-contrato/README.md) | DDL: el esquema como contrato ejecutable | Fundamentos | 3 |
| [015](part-03-sql-en-profundidad/015-select-filtrado-proyeccion-y-orden/README.md) | SELECT: filtrado, proyección y orden con semántica precisa | Fundamentos | 3 |
| [016](part-03-sql-en-profundidad/016-reuniones-inner-outer-semi-y-anti/README.md) | Reuniones: interna, externa, semi y anti | Intermedio | 4 |
| [017](part-03-sql-en-profundidad/017-agregacion-group-by-y-having/README.md) | Agregación, GROUP BY y HAVING sin duplicar filas | Intermedio | 3 |
| [018](part-03-sql-en-profundidad/018-cte-subconsultas-y-funciones-de-ventana/README.md) | CTE, subconsultas y funciones de ventana | Intermedio | 4 |
| [019](part-03-sql-en-profundidad/019-nulos-y-logica-de-tres-valores/README.md) | Nulos y lógica de tres valores | Intermedio | 3 |

## [Parte 04 — Motores relacionales y dialectos](part-04-motores-relacionales-y-dialectos/README.md)

Que exige la norma, que añade cada producto y como se escribe código que sobrevive a un cambio de motor.

*4 clases · 12 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [020](part-04-motores-relacionales-y-dialectos/020-portabilidad-y-matriz-de-dialectos/README.md) | Portabilidad: qué exige la norma y qué añade cada motor | Intermedio | 3 |
| [021](part-04-motores-relacionales-y-dialectos/021-postgresql-tipos-extensiones-y-procesos/README.md) | PostgreSQL: tipos, extensiones y modelo de procesos | Intermedio | 3 |
| [022](part-04-motores-relacionales-y-dialectos/022-mysql-sqlserver-y-oracle-divergencias/README.md) | MySQL, MariaDB, SQL Server y Oracle: divergencias que rompen código | Intermedio | 3 |
| [023](part-04-motores-relacionales-y-dialectos/023-sqlite-y-duckdb-motores-embebidos/README.md) | SQLite y DuckDB: motores embebidos, transaccional frente a analítico | Intermedio | 3 |

## [Parte 05 — Documentos y clave-valor](part-05-documentos-y-clave-valor/README.md)

Modelos sin reunión en el servidor: el agregado como frontera de consistencia, cuando incrustar y que se pierde en una caché.

*4 clases · 13 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [024](part-05-documentos-y-clave-valor/024-el-agregado-como-unidad-de-consistencia/README.md) | El agregado como unidad de consistencia | Intermedio | 3 |
| [025](part-05-documentos-y-clave-valor/025-modelado-documental-incrustar-o-referenciar/README.md) | Modelado documental: incrustar o referenciar | Intermedio | 4 |
| [026](part-05-documentos-y-clave-valor/026-consultas-e-indices-sobre-documentos/README.md) | Consultas, índices y agregación sobre documentos | Intermedio | 3 |
| [027](part-05-documentos-y-clave-valor/027-clave-valor-cache-y-expiracion/README.md) | Clave-valor, caché y expiración: qué se pierde exactamente | Intermedio | 3 |

## [Parte 06 — Grafos, columnas, tiempo y búsqueda](part-06-grafos-columnas-tiempo-y-busqueda/README.md)

Modelos especializados y el criterio para saber cuando la carga de trabajo justifica salir del relacional.

*5 clases · 15 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [028](part-06-grafos-columnas-tiempo-y-busqueda/028-grafos-de-propiedades-y-recorridos/README.md) | Grafos de propiedades y los recorridos que SQL hace mal | Intermedio | 3 |
| [029](part-06-grafos-columnas-tiempo-y-busqueda/029-columnas-anchas-modelar-desde-la-consulta/README.md) | Columnas anchas: modelar desde la consulta | Avanzado | 3 |
| [030](part-06-grafos-columnas-tiempo-y-busqueda/030-series-temporales-cardinalidad-y-retencion/README.md) | Series temporales: cardinalidad, retención y agregados continuos | Intermedio | 3 |
| [031](part-06-grafos-columnas-tiempo-y-busqueda/031-busqueda-de-texto-indice-invertido-y-relevancia/README.md) | Búsqueda de texto: índice invertido, análisis y relevancia | Intermedio | 3 |
| [032](part-06-grafos-columnas-tiempo-y-busqueda/032-analitica-columnar-y-vectorizacion/README.md) | Analítica columnar: por qué el formato cambia el orden de magnitud | Avanzado | 3 |

## [Parte 07 — Transacciones, concurrencia y recuperación](part-07-transacciones-concurrencia-y-recuperacion/README.md)

Que garantiza realmente ACID, que anomalías sobreviven en cada nivel de aislamiento y como se vuelve de una caída.

*5 clases · 18 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [033](part-07-transacciones-concurrencia-y-recuperacion/033-acid-que-garantiza-cada-letra/README.md) | ACID: qué garantiza cada letra y quién la implementa | Intermedio | 3 |
| [034](part-07-transacciones-concurrencia-y-recuperacion/034-anomalias-de-aislamiento-y-la-critica-ansi/README.md) | Anomalías de aislamiento y la crítica a los niveles ANSI | Avanzado | 4 |
| [035](part-07-transacciones-concurrencia-y-recuperacion/035-bloqueo-en-dos-fases-y-mvcc/README.md) | Bloqueo en dos fases, MVCC e instantáneas | Avanzado | 4 |
| [036](part-07-transacciones-concurrencia-y-recuperacion/036-registro-anticipado-y-recuperacion/README.md) | Registro anticipado y recuperación: WAL y ARIES | Avanzado | 4 |
| [037](part-07-transacciones-concurrencia-y-recuperacion/037-concurrencia-en-la-aplicacion/README.md) | Concurrencia en la aplicación: idempotencia, reintentos y bloqueo optimista | Avanzado | 3 |

## [Parte 08 — Almacenamiento, índices y planes](part-08-almacenamiento-indices-y-planes/README.md)

Por qué una consulta tarda: páginas, estructuras de índice, estadísticas y la lectura honesta de un plan de ejecución.

*5 clases · 17 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [038](part-08-almacenamiento-indices-y-planes/038-paginas-filas-y-buffer-pool/README.md) | Páginas, filas y buffer: por qué la entrada y salida manda | Intermedio | 3 |
| [039](part-08-almacenamiento-indices-y-planes/039-b-tree-orden-de-columnas-y-selectividad/README.md) | B-Tree: estructura, orden de columnas y selectividad | Intermedio | 4 |
| [040](part-08-almacenamiento-indices-y-planes/040-lsm-tree-compactacion-y-amplificacion/README.md) | LSM-Tree, compactación y amplificación de escritura | Avanzado | 3 |
| [041](part-08-almacenamiento-indices-y-planes/041-indices-especializados/README.md) | Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes | Avanzado | 3 |
| [042](part-08-almacenamiento-indices-y-planes/042-planes-de-ejecucion-y-refutacion/README.md) | Planes de ejecución: leer EXPLAIN y refutar una hipótesis | Avanzado | 4 |

## [Parte 09 — Distribución, réplica y consistencia](part-09-distribucion-replica-y-consistencia/README.md)

Qué se gana y qué se paga al repartir los datos: replicación, partición, los teoremas que acotan lo posible y el consenso.

*5 clases · 17 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [043](part-09-distribucion-replica-y-consistencia/043-replica-lider-unico-multilider-y-sin-lider/README.md) | Réplica: líder único, multilíder y sin líder | Avanzado | 4 |
| [044](part-09-distribucion-replica-y-consistencia/044-particionado-rebalanceo-y-claves-calientes/README.md) | Particionado, rebalanceo y claves calientes | Avanzado | 3 |
| [045](part-09-distribucion-replica-y-consistencia/045-cap-pacelc-y-lo-que-realmente-se-elige/README.md) | CAP, PACELC y lo que realmente se elige | Avanzado | 3 |
| [046](part-09-distribucion-replica-y-consistencia/046-modelos-de-consistencia-y-garantias-de-sesion/README.md) | Modelos de consistencia y garantías de sesión | Avanzado | 3 |
| [047](part-09-distribucion-replica-y-consistencia/047-consenso-y-transacciones-distribuidas/README.md) | Consenso y transacciones distribuidas: Raft, 2PC y sagas | Avanzado | 4 |

## [Parte 10 — Operación, seguridad y gobierno](part-10-operacion-seguridad-y-gobierno/README.md)

Lo que separa un ejercicio de un sistema: restauración probada, migraciones sin caída, control de acceso, observabilidad y privacidad.

*6 clases · 19 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [048](part-10-operacion-seguridad-y-gobierno/048-respaldo-y-restauracion-probada/README.md) | Respaldo y restauración: solo cuenta lo que se ha restaurado | Intermedio | 4 |
| [049](part-10-operacion-seguridad-y-gobierno/049-migraciones-evolutivas-sin-caida/README.md) | Migraciones evolutivas sin ventana de caída | Avanzado | 3 |
| [050](part-10-operacion-seguridad-y-gobierno/050-control-de-acceso-y-seguridad-por-fila/README.md) | Control de acceso: privilegio mínimo, roles y seguridad por fila | Intermedio | 3 |
| [051](part-10-operacion-seguridad-y-gobierno/051-inyeccion-sql-y-parametrizacion/README.md) | Inyección SQL y el contrato de parametrización | Fundamentos | 3 |
| [052](part-10-operacion-seguridad-y-gobierno/052-observabilidad-slo-y-capacidad/README.md) | Observabilidad, objetivos de servicio y capacidad | Avanzado | 3 |
| [053](part-10-operacion-seguridad-y-gobierno/053-privacidad-retencion-y-gobierno-del-dato/README.md) | Privacidad, retención y gobierno del dato | Intermedio | 3 |

## [Parte 11 — Analítica, integración y streaming](part-11-analitica-integracion-y-streaming/README.md)

Sacar los datos del sistema que los produjo sin perder su significado: almacen dimensional, captura de cambios y procesamiento continuo.

*4 clases · 13 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [054](part-11-analitica-integracion-y-streaming/054-oltp-frente-a-olap/README.md) | OLTP frente a OLAP: por qué se separan | Intermedio | 3 |
| [055](part-11-analitica-integracion-y-streaming/055-modelado-dimensional/README.md) | Modelado dimensional: hechos, dimensiones y cambios lentos | Intermedio | 4 |
| [056](part-11-analitica-integracion-y-streaming/056-integracion-etl-elt-y-captura-de-cambios/README.md) | Integración: ETL, ELT, captura de cambios y el registro como nexo | Avanzado | 3 |
| [057](part-11-analitica-integracion-y-streaming/057-streaming-tiempo-de-evento-y-ventanas/README.md) | Streaming: tiempo de evento, ventanas y semántica de entrega | Avanzado | 3 |

## [Parte 12 — Vectores, recuperación y RAG](part-12-vectores-recuperacion-y-rag/README.md)

La base de datos como componente de un sistema de inteligencia artificial: distancias, indices aproximados y recuperación medida.

*4 clases · 13 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [058](part-12-vectores-recuperacion-y-rag/058-embeddings-y-metricas-de-distancia/README.md) | Embeddings y métricas de distancia: qué significa parecido | Intermedio | 3 |
| [059](part-12-vectores-recuperacion-y-rag/059-indices-vectoriales-aproximados/README.md) | Índices vectoriales aproximados: HNSW, IVF y el recall | Avanzado | 4 |
| [060](part-12-vectores-recuperacion-y-rag/060-busqueda-hibrida-y-filtrado/README.md) | Búsqueda híbrida: léxica más vectorial y filtrado por metadatos | Avanzado | 3 |
| [061](part-12-vectores-recuperacion-y-rag/061-rag-evaluable/README.md) | RAG evaluable: medir la recuperación antes que la generación | Avanzado | 3 |

## [Parte 13 — Arquitectura y proyecto final](part-13-arquitectura-y-proyecto-final/README.md)

Cerrar el programa con una decisión defendible: comparación por evidencia, costo total y una demostración que se pueda auditar.

*3 clases · 12 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [062](part-13-arquitectura-y-proyecto-final/062-persistencia-poliglota-por-evidencia/README.md) | Persistencia políglota: decidir por evidencia y no por moda | Avanzado | 3 |
| [063](part-13-arquitectura-y-proyecto-final/063-registro-de-decisiones-y-costo-total/README.md) | Registro de decisiones de arquitectura y costo total | Avanzado | 3 |
| [064](part-13-arquitectura-y-proyecto-final/064-proyecto-final-disenar-medir-y-defender/README.md) | Proyecto final: diseñar, medir y defender | Avanzado | 6 |
