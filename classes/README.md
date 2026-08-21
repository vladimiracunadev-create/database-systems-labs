# Clases

74 clases repartidas en 15 partes, 230 horas estimadas.

Cada clase declara sus fuentes al final. Este índice y los README de clase se
generan con `python scripts/build_classes.py`; la materia se edita en el
`lesson.md` de cada carpeta.

## [Parte 00 — Primeros pasos: del archivo a la base de datos](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/README.md)

La rampa de entrada. Qué es un dato, por qué una hoja de cálculo deja de servir, y las primeras órdenes de SQL —crear, insertar, leer, cambiar— hasta llegar a dos tablas relacionadas. Termina con las dos preguntas que hay que saber contestar antes de seguir: cuándo NO hace falta una base de datos y qué familias de motores existen.

*10 clases · 20 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [001](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md) | Qué es un dato, un registro y una tabla | Fundamentos | 2 |
| [002](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) | Del archivo y la hoja de cálculo a la base de datos | Fundamentos | 2 |
| [003](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/003-tu-primera-base-de-datos/README.md) | Tu primera base de datos: crear, insertar y leer | Fundamentos | 2 |
| [004](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/004-leer-datos-select-where-y-order-by/README.md) | Leer datos: SELECT, WHERE y ORDER BY | Fundamentos | 2 |
| [005](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/005-cambiar-datos-insert-update-delete/README.md) | Cambiar datos: INSERT, UPDATE, DELETE y el WHERE que salva | Fundamentos | 2 |
| [006](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/006-tipos-de-datos-un-numero-no-es-un-texto/README.md) | Tipos de datos: por qué un número no es un texto | Fundamentos | 2 |
| [007](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/007-la-clave-primaria/README.md) | La clave primaria: cómo se distingue una fila de otra | Fundamentos | 2 |
| [008](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/008-dos-tablas-y-una-relacion/README.md) | Dos tablas y una relación: la clave foránea | Fundamentos | 2 |
| [009](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/009-cuando-no-necesitas-una-base-de-datos/README.md) | Cuándo NO necesitas una base de datos | Fundamentos | 2 |
| [010](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/010-el-mapa-de-los-motores/README.md) | El mapa de los motores: seis familias y un criterio | Fundamentos | 2 |

## [Parte 01 — Fundamentos, sistemas y método](part-01-fundamentos-datos-sistemas-y-metodo/README.md)

Qué problema resuelve un gestor de bases de datos, qué hay dentro de él y cómo se monta un entorno donde cada afirmación pueda comprobarse.

*4 clases · 12 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [011](part-01-fundamentos-datos-sistemas-y-metodo/011-que-resuelve-un-sistema-de-bases-de-datos/README.md) | Qué resuelve un sistema de bases de datos y qué no | Fundamentos | 3 |
| [012](part-01-fundamentos-datos-sistemas-y-metodo/012-arquitectura-interna-de-un-gestor/README.md) | Arquitectura interna de un gestor, del cliente al disco | Fundamentos | 3 |
| [013](part-01-fundamentos-datos-sistemas-y-metodo/013-independencia-de-datos-y-niveles-de-esquema/README.md) | Independencia de datos y los tres niveles de esquema | Fundamentos | 3 |
| [014](part-01-fundamentos-datos-sistemas-y-metodo/014-entorno-reproducible-y-evidencia/README.md) | Entorno reproducible y evidencia comprobable | Fundamentos | 3 |

## [Parte 02 — Modelado conceptual y requisitos](part-02-modelado-conceptual-y-requisitos/README.md)

Del enunciado ambiguo al esquema defendible: entidades, claves, dependencias funcionales y la decisión consciente de desnormalizar.

*5 clases · 16 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [015](part-02-modelado-conceptual-y-requisitos/015-de-requisitos-a-entidades/README.md) | De requisitos ambiguos a entidades defendibles | Fundamentos | 3 |
| [016](part-02-modelado-conceptual-y-requisitos/016-entidad-relacion-cardinalidad-y-participacion/README.md) | Entidad-relación, cardinalidad y participación | Fundamentos | 3 |
| [017](part-02-modelado-conceptual-y-requisitos/017-claves-identidad-natural-y-sustituta/README.md) | Claves, identidad y el debate natural frente a sustituta | Fundamentos | 3 |
| [018](part-02-modelado-conceptual-y-requisitos/018-normalizacion-y-dependencias-funcionales/README.md) | Normalización de 1FN a BCFN con dependencias funcionales | Intermedio | 4 |
| [019](part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md) | Desnormalización deliberada y patrones de acceso | Intermedio | 3 |

## [Parte 03 — Modelo relacional y álgebra](part-03-modelo-relacional-y-algebra/README.md)

La teoría que SQL implementa a medias: relaciones como conjuntos, operadores del álgebra, cálculo relacional e integridad declarada.

*4 clases · 13 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [020](part-03-modelo-relacional-y-algebra/020-la-relacion-como-conjunto/README.md) | La relación como conjunto: tuplas, dominios y acceso por valor | Fundamentos | 3 |
| [021](part-03-modelo-relacional-y-algebra/021-algebra-relacional-operadores/README.md) | Álgebra relacional: selección, proyección, producto y reunión | Fundamentos | 4 |
| [022](part-03-modelo-relacional-y-algebra/022-calculo-relacional-y-equivalencia/README.md) | Cálculo relacional y su equivalencia con el álgebra | Intermedio | 3 |
| [023](part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md) | Integridad: restricciones, claves foraneas y acciones referenciales | Intermedio | 3 |

## [Parte 04 — SQL en profundidad](part-04-sql-en-profundidad/README.md)

Escribir SQL cuya semántica se pueda defender: definición del esquema, reuniones, agregación, ventanas y el comportamiento real de los nulos.

*6 clases · 20 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [024](part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md) | DDL: el esquema como contrato ejecutable | Fundamentos | 3 |
| [025](part-04-sql-en-profundidad/025-select-filtrado-proyeccion-y-orden/README.md) | SELECT: filtrado, proyección y orden con semántica precisa | Fundamentos | 3 |
| [026](part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md) | Reuniones: interna, externa, semi y anti | Intermedio | 4 |
| [027](part-04-sql-en-profundidad/027-agregacion-group-by-y-having/README.md) | Agregación, GROUP BY y HAVING sin duplicar filas | Intermedio | 3 |
| [028](part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md) | CTE, subconsultas y funciones de ventana | Intermedio | 4 |
| [029](part-04-sql-en-profundidad/029-nulos-y-logica-de-tres-valores/README.md) | Nulos y lógica de tres valores | Intermedio | 3 |

## [Parte 05 — Motores relacionales y dialectos](part-05-motores-relacionales-y-dialectos/README.md)

Que exige la norma, que añade cada producto y como se escribe código que sobrevive a un cambio de motor.

*4 clases · 12 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [030](part-05-motores-relacionales-y-dialectos/030-portabilidad-y-matriz-de-dialectos/README.md) | Portabilidad: qué exige la norma y qué añade cada motor | Intermedio | 3 |
| [031](part-05-motores-relacionales-y-dialectos/031-postgresql-tipos-extensiones-y-procesos/README.md) | PostgreSQL: tipos, extensiones y modelo de procesos | Intermedio | 3 |
| [032](part-05-motores-relacionales-y-dialectos/032-mysql-sqlserver-y-oracle-divergencias/README.md) | MySQL, MariaDB, SQL Server y Oracle: divergencias que rompen código | Intermedio | 3 |
| [033](part-05-motores-relacionales-y-dialectos/033-sqlite-y-duckdb-motores-embebidos/README.md) | SQLite y DuckDB: motores embebidos, transaccional frente a analítico | Intermedio | 3 |

## [Parte 06 — Documentos y clave-valor](part-06-documentos-y-clave-valor/README.md)

Modelos sin reunión en el servidor: el agregado como frontera de consistencia, cuando incrustar y que se pierde en una caché.

*4 clases · 13 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [034](part-06-documentos-y-clave-valor/034-el-agregado-como-unidad-de-consistencia/README.md) | El agregado como unidad de consistencia | Intermedio | 3 |
| [035](part-06-documentos-y-clave-valor/035-modelado-documental-incrustar-o-referenciar/README.md) | Modelado documental: incrustar o referenciar | Intermedio | 4 |
| [036](part-06-documentos-y-clave-valor/036-consultas-e-indices-sobre-documentos/README.md) | Consultas, índices y agregación sobre documentos | Intermedio | 3 |
| [037](part-06-documentos-y-clave-valor/037-clave-valor-cache-y-expiracion/README.md) | Clave-valor, caché y expiración: qué se pierde exactamente | Intermedio | 3 |

## [Parte 07 — Grafos, columnas, tiempo y búsqueda](part-07-grafos-columnas-tiempo-y-busqueda/README.md)

Modelos especializados y el criterio para saber cuando la carga de trabajo justifica salir del relacional.

*5 clases · 15 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [038](part-07-grafos-columnas-tiempo-y-busqueda/038-grafos-de-propiedades-y-recorridos/README.md) | Grafos de propiedades y los recorridos que SQL hace mal | Intermedio | 3 |
| [039](part-07-grafos-columnas-tiempo-y-busqueda/039-columnas-anchas-modelar-desde-la-consulta/README.md) | Columnas anchas: modelar desde la consulta | Avanzado | 3 |
| [040](part-07-grafos-columnas-tiempo-y-busqueda/040-series-temporales-cardinalidad-y-retencion/README.md) | Series temporales: cardinalidad, retención y agregados continuos | Intermedio | 3 |
| [041](part-07-grafos-columnas-tiempo-y-busqueda/041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) | Búsqueda de texto: índice invertido, análisis y relevancia | Intermedio | 3 |
| [042](part-07-grafos-columnas-tiempo-y-busqueda/042-analitica-columnar-y-vectorizacion/README.md) | Analítica columnar: por qué el formato cambia el orden de magnitud | Avanzado | 3 |

## [Parte 08 — Transacciones, concurrencia y recuperación](part-08-transacciones-concurrencia-y-recuperacion/README.md)

Que garantiza realmente ACID, que anomalías sobreviven en cada nivel de aislamiento y como se vuelve de una caída.

*5 clases · 18 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [043](part-08-transacciones-concurrencia-y-recuperacion/043-acid-que-garantiza-cada-letra/README.md) | ACID: qué garantiza cada letra y quién la implementa | Intermedio | 3 |
| [044](part-08-transacciones-concurrencia-y-recuperacion/044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) | Anomalías de aislamiento y la crítica a los niveles ANSI | Avanzado | 4 |
| [045](part-08-transacciones-concurrencia-y-recuperacion/045-bloqueo-en-dos-fases-y-mvcc/README.md) | Bloqueo en dos fases, MVCC e instantáneas | Avanzado | 4 |
| [046](part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md) | Registro anticipado y recuperación: WAL y ARIES | Avanzado | 4 |
| [047](part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md) | Concurrencia en la aplicación: idempotencia, reintentos y bloqueo optimista | Avanzado | 3 |

## [Parte 09 — Almacenamiento, índices y planes](part-09-almacenamiento-indices-y-planes/README.md)

Por qué una consulta tarda: páginas, estructuras de índice, estadísticas y la lectura honesta de un plan de ejecución.

*5 clases · 17 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [048](part-09-almacenamiento-indices-y-planes/048-paginas-filas-y-buffer-pool/README.md) | Páginas, filas y buffer: por qué la entrada y salida manda | Intermedio | 3 |
| [049](part-09-almacenamiento-indices-y-planes/049-b-tree-orden-de-columnas-y-selectividad/README.md) | B-Tree: estructura, orden de columnas y selectividad | Intermedio | 4 |
| [050](part-09-almacenamiento-indices-y-planes/050-lsm-tree-compactacion-y-amplificacion/README.md) | LSM-Tree, compactación y amplificación de escritura | Avanzado | 3 |
| [051](part-09-almacenamiento-indices-y-planes/051-indices-especializados/README.md) | Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes | Avanzado | 3 |
| [052](part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md) | Planes de ejecución: leer EXPLAIN y refutar una hipótesis | Avanzado | 4 |

## [Parte 10 — Distribución, réplica y consistencia](part-10-distribucion-replica-y-consistencia/README.md)

Qué se gana y qué se paga al repartir los datos: replicación, partición, los teoremas que acotan lo posible y el consenso.

*5 clases · 17 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [053](part-10-distribucion-replica-y-consistencia/053-replica-lider-unico-multilider-y-sin-lider/README.md) | Réplica: líder único, multilíder y sin líder | Avanzado | 4 |
| [054](part-10-distribucion-replica-y-consistencia/054-particionado-rebalanceo-y-claves-calientes/README.md) | Particionado, rebalanceo y claves calientes | Avanzado | 3 |
| [055](part-10-distribucion-replica-y-consistencia/055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) | CAP, PACELC y lo que realmente se elige | Avanzado | 3 |
| [056](part-10-distribucion-replica-y-consistencia/056-modelos-de-consistencia-y-garantias-de-sesion/README.md) | Modelos de consistencia y garantías de sesión | Avanzado | 3 |
| [057](part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) | Consenso y transacciones distribuidas: Raft, 2PC y sagas | Avanzado | 4 |

## [Parte 11 — Operación, seguridad y gobierno](part-11-operacion-seguridad-y-gobierno/README.md)

Lo que separa un ejercicio de un sistema: restauración probada, migraciones sin caída, control de acceso, observabilidad y privacidad.

*6 clases · 19 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [058](part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md) | Respaldo y restauración: solo cuenta lo que se ha restaurado | Intermedio | 4 |
| [059](part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md) | Migraciones evolutivas sin ventana de caída | Avanzado | 3 |
| [060](part-11-operacion-seguridad-y-gobierno/060-control-de-acceso-y-seguridad-por-fila/README.md) | Control de acceso: privilegio mínimo, roles y seguridad por fila | Intermedio | 3 |
| [061](part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md) | Inyección SQL y el contrato de parametrización | Fundamentos | 3 |
| [062](part-11-operacion-seguridad-y-gobierno/062-observabilidad-slo-y-capacidad/README.md) | Observabilidad, objetivos de servicio y capacidad | Avanzado | 3 |
| [063](part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) | Privacidad, retención y gobierno del dato | Intermedio | 3 |

## [Parte 12 — Analítica, integración y streaming](part-12-analitica-integracion-y-streaming/README.md)

Sacar los datos del sistema que los produjo sin perder su significado: almacen dimensional, captura de cambios y procesamiento continuo.

*4 clases · 13 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [064](part-12-analitica-integracion-y-streaming/064-oltp-frente-a-olap/README.md) | OLTP frente a OLAP: por qué se separan | Intermedio | 3 |
| [065](part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) | Modelado dimensional: hechos, dimensiones y cambios lentos | Intermedio | 4 |
| [066](part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md) | Integración: ETL, ELT, captura de cambios y el registro como nexo | Avanzado | 3 |
| [067](part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md) | Streaming: tiempo de evento, ventanas y semántica de entrega | Avanzado | 3 |

## [Parte 13 — Vectores, recuperación y RAG](part-13-vectores-recuperacion-y-rag/README.md)

La base de datos como componente de un sistema de inteligencia artificial: distancias, indices aproximados y recuperación medida.

*4 clases · 13 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [068](part-13-vectores-recuperacion-y-rag/068-embeddings-y-metricas-de-distancia/README.md) | Embeddings y métricas de distancia: qué significa parecido | Intermedio | 3 |
| [069](part-13-vectores-recuperacion-y-rag/069-indices-vectoriales-aproximados/README.md) | Índices vectoriales aproximados: HNSW, IVF y el recall | Avanzado | 4 |
| [070](part-13-vectores-recuperacion-y-rag/070-busqueda-hibrida-y-filtrado/README.md) | Búsqueda híbrida: léxica más vectorial y filtrado por metadatos | Avanzado | 3 |
| [071](part-13-vectores-recuperacion-y-rag/071-rag-evaluable/README.md) | RAG evaluable: medir la recuperación antes que la generación | Avanzado | 3 |

## [Parte 14 — Arquitectura y proyecto final](part-14-arquitectura-y-proyecto-final/README.md)

Cerrar el programa con una decisión defendible: comparación por evidencia, costo total y una demostración que se pueda auditar.

*3 clases · 12 horas*

| # | Clase | Nivel | Horas |
|---|---|---|---:|
| [072](part-14-arquitectura-y-proyecto-final/072-persistencia-poliglota-por-evidencia/README.md) | Persistencia políglota: decidir por evidencia y no por moda | Avanzado | 3 |
| [073](part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md) | Registro de decisiones de arquitectura y costo total | Avanzado | 3 |
| [074](part-14-arquitectura-y-proyecto-final/074-proyecto-final-disenar-medir-y-defender/README.md) | Proyecto final: diseñar, medir y defender | Avanzado | 6 |
