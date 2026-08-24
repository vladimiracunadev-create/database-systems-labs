# Glosario del programa

306 términos: todos los conceptos que las 74 clases
declaran, definidos una sola vez y con la misma palabra significando lo mismo de
principio a fin. Cada entrada dice dónde se trabaja el término, con qué otros se
relaciona y de qué obra procede la definición.

> [Programa](README.md) · [Índice de clases](classes/README.md) ·
> [Registro de fuentes](catalog/sources.json) ·
> [Modelo de aprendizaje](docs/LEARNING-MODEL.md)

Este archivo se genera desde [`catalog/glosario.json`](catalog/glosario.json) con
`python scripts/build_classes.py`. Editarlo a mano no sirve de nada: el cambio se
pierde en la siguiente generación. `scripts/validate_repository.py` comprueba que
no haya ningún concepto del currículo sin definición ni ninguna definición sin
concepto.

**Índice alfabético:** [2](#2) · [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w)

## 2

### 2PL

Bloqueo en dos fases: una fase en la que la transacción solo adquiere cerrojos y otra en la que solo los libera. Es la técnica clásica que garantiza serializabilidad, al precio de que los lectores bloqueen a los escritores.

- **Se trabaja en:** [045 — Bloqueo en dos fases, MVCC e instantáneas](classes/part-08-transacciones-concurrencia-y-recuperacion/045-bloqueo-en-dos-fases-y-mvcc/README.md) (parte 08)
- **Ver también:** [interbloqueo](#interbloqueo), [aislamiento](#aislamiento), [versión de fila](#versión-de-fila)
- **Fuente:** Jim Gray, Andreas Reuter (1992), [Transaction Processing: Concepts and Techniques](https://www.sciencedirect.com/book/9781558601901/transaction-processing)

## A

### acceso por valor

En el modelo relacional se llega a un dato por lo que vale, nunca por un puntero o una posición física. Es lo que hace posible la independencia de datos: el motor puede reorganizar el almacenamiento sin invalidar ninguna referencia.

- **Se trabaja en:** [020 — La relación como conjunto: tuplas, dominios y acceso por valor](classes/part-03-modelo-relacional-y-algebra/020-la-relacion-como-conjunto/README.md) (parte 03)
- **Ver también:** [independencia de datos](#independencia-de-datos), [clave primaria](#clave-primaria), [tupla](#tupla)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

### actividad

Hecho que ocurre en un instante y relaciona entidades: un pedido, un pago, una inscripción. Su volumen crece sin límite con el tiempo, lo que la convierte en la candidata natural a tabla de hechos o a flujo de eventos, y en la mala candidata a incrustarse dentro de una entidad.

- **Se trabaja en:** [034 — El agregado como unidad de consistencia](classes/part-06-documentos-y-clave-valor/034-el-agregado-como-unidad-de-consistencia/README.md) (parte 06)
- **Ver también:** [entidad](#entidad), [tabla de hechos](#tabla-de-hechos), [crecimiento no acotado](#crecimiento-no-acotado)
- **Fuente:** Pat Helland (2007), [Life beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf)

### ADR

Registro de decisión de arquitectura: un documento corto y numerado con el contexto, la decisión, las alternativas descartadas y las consecuencias. Su valor aparece dos años después, cuando alguien pregunta por qué esto es así y nadie lo recuerda.

- **Se trabaja en:** [073 — Registro de decisiones de arquitectura y costo total](classes/part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md) (parte 14)
- **Ver también:** [contexto](#contexto), [consecuencia](#consecuencia), [reversibilidad](#reversibilidad)
- **Fuente:** Peter Bailis, Joseph M. Hellerstein, Michael Stonebraker (2015), [Readings in Database Systems](http://www.redbook.io/)

### afinidad de tipos

Regla de SQLite por la que la columna sugiere un tipo pero acepta valores de otro y los convierte cuando puede. Explica por qué en SQLite entra un texto en una columna `INTEGER` y por qué ese mismo dato es rechazado en PostgreSQL.

- **Se trabaja en:** [006 — Tipos de datos: por qué un número no es un texto](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/006-tipos-de-datos-un-numero-no-es-un-texto/README.md) (parte 00)
- **Ver también:** [tipado dinamico](#tipado-dinamico), [tipo](#tipo), [modo estricto](#modo-estricto)
- **Fuente:** SQLite Consortium (2026), [SQLite Documentation](https://sqlite.org/docs.html)

### agregado

Conjunto de datos que se trata como una unidad para leer, escribir y garantizar consistencia: un pedido con sus líneas. Sadalage y Fowler lo toman del diseño dirigido por el dominio y lo convierten en el criterio que separa a los motores NoSQL del relacional. (En la clase 027 la palabra se usa en su otro sentido: el resultado de una función de agregación como `SUM` o `COUNT`.)

- **Se trabaja en:** [019 — Desnormalización deliberada y patrones de acceso](classes/part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md) (parte 02)
- **Ver también:** [frontera transaccional](#frontera-transaccional), [modelo de agregado](#modelo-de-agregado), [incrustación](#incrustación), [agrupación](#agrupación)
- **Fuente:** Pramod J. Sadalage, Martin Fowler (2012), [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html)

### agregado continuo

Vista materializada que se actualiza de forma incremental según llegan datos nuevos, típicamente con medias u otros resúmenes por intervalo. Permite responder «el promedio por hora del último año» sin recorrer mil millones de puntos en cada consulta.

- **Se trabaja en:** [040 — Series temporales: cardinalidad, retención y agregados continuos](classes/part-07-grafos-columnas-tiempo-y-busqueda/040-series-temporales-cardinalidad-y-retencion/README.md) (parte 07)
- **Ver también:** [submuestreo](#submuestreo), [ventana](#ventana), [carga analítica](#carga-analítica)
- **Fuente:** Timescale, Inc. (2026), [TimescaleDB Documentation](https://docs.timescale.com/)

### agregados y nulos

Las funciones de agregado ignoran los nulos, salvo `COUNT(*)` que cuenta filas. Por eso `COUNT(columna)` y `COUNT(*)` difieren, y por eso un `AVG` sobre una columna con huecos es la media de los presentes, no del total.

- **Se trabaja en:** [029 — Nulos y lógica de tres valores](classes/part-04-sql-en-profundidad/029-nulos-y-logica-de-tres-valores/README.md) (parte 04)
- **Ver también:** [NULL](#null), [agrupación](#agrupación), [doble conteo](#doble-conteo)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### agrupación

Partir las filas en grupos por los valores de unas columnas (`GROUP BY`) y producir una fila de resultado por grupo. Todo lo que aparezca en el `SELECT` debe ser o columna de agrupación o resultado de una función de agregado.

- **Se trabaja en:** [027 — Agregación, GROUP BY y HAVING sin duplicar filas](classes/part-04-sql-en-profundidad/027-agregacion-group-by-y-having/README.md) (parte 04)
- **Ver también:** [HAVING](#having), [dependencia funcional en GROUP BY](#dependencia-funcional-en-group-by), [orden de evaluación](#orden-de-evaluación)
- **Fuente:** Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom (2008), [Database Systems: The Complete Book](http://infolab.stanford.edu/~ullman/dscb.html)

### aislamiento

Grado en que una transacción concurrente no ve los pasos intermedios de otra. Es la única letra de ACID que se vende por niveles, y el nivel por defecto de casi todos los motores no es el más fuerte.

- **Se trabaja en:** [043 — ACID: qué garantiza cada letra y quién la implementa](classes/part-08-transacciones-concurrencia-y-recuperacion/043-acid-que-garantiza-cada-letra/README.md) (parte 08)
- **Ver también:** [snapshot isolation](#snapshot-isolation), [2PL](#2pl), [lectura sucia](#lectura-sucia)
- **Fuente:** Jim Gray, Andreas Reuter (1992), [Transaction Processing: Concepts and Techniques](https://www.sciencedirect.com/book/9781558601901/transaction-processing)

### alcance

Lo que el modelo decide representar y lo que decide ignorar. Kent lo formula sin rodeos: ningún modelo captura el mundo, siempre hay un recorte, y ese recorte es una decisión humana que conviene escribir en lugar de sufrir después.

- **Se trabaja en:** [015 — De requisitos ambiguos a entidades defendibles](classes/part-02-modelado-conceptual-y-requisitos/015-de-requisitos-a-entidades/README.md) (parte 02)
- **Ver también:** [información](#información), [esquema conceptual](#esquema-conceptual), [límite declarado](#límite-declarado)
- **Fuente:** William Kent (2012), [Data and Reality](https://technicspub.com/data-and-reality/)

### alcance del cambio

Cuántas filas toca realmente una orden de escritura. La disciplina es comprobarlo antes: escribir el `SELECT` con el mismo `WHERE`, contar, y solo entonces convertirlo en `UPDATE` o `DELETE`.

- **Se trabaja en:** [005 — Cambiar datos: INSERT, UPDATE, DELETE y el WHERE que salva](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/005-cambiar-datos-insert-update-delete/README.md) (parte 00)
- **Ver también:** [filas afectadas](#filas-afectadas), [UPDATE](#update), [DELETE](#delete)
- **Fuente:** Bill Karwin (2010), [SQL Antipatterns: Avoiding the Pitfalls of Database Programming](https://pragprog.com/titles/bksqla/sql-antipatterns/)

### almacenamiento columnar

Guardar juntos todos los valores de una misma columna en lugar de todas las columnas de una misma fila. Una consulta analítica lee solo las columnas que necesita y comprime mucho mejor, porque los valores contiguos se parecen entre sí.

- **Se trabaja en:** [033 — SQLite y DuckDB: motores embebidos, transaccional frente a analítico](classes/part-05-motores-relacionales-y-dialectos/033-sqlite-y-duckdb-motores-embebidos/README.md) (parte 05)
- **Ver también:** [compresión](#compresión), [ejecución vectorizada](#ejecución-vectorizada), [carga analítica](#carga-analítica)
- **Fuente:** DuckDB Foundation (2026), [DuckDB Documentation](https://duckdb.org/docs/)

### alternativas

Lo que se usa cuando una base de datos no está justificada: un CSV o un Parquet, un JSON versionado, una hoja de cálculo compartida, un fichero por proceso. Nombrarlas obliga a defender la elección de motor en lugar de darla por hecha.

- **Se trabaja en:** [009 — Cuándo NO necesitas una base de datos](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/009-cuando-no-necesitas-una-base-de-datos/README.md) (parte 00)
- **Ver también:** [criterio de decisión](#criterio-de-decisión), [motor embebido](#motor-embebido)
- **Fuente:** DuckDB Foundation (2026), [DuckDB Documentation](https://duckdb.org/docs/)

### amplificación de escritura

Cuántos bytes acaba escribiendo el motor en disco por cada byte que escribió la aplicación, sumando registro y compactaciones sucesivas. Es la métrica que decide el desgaste del disco y el techo real de escritura de un motor LSM.

- **Se trabaja en:** [050 — LSM-Tree, compactación y amplificación de escritura](classes/part-09-almacenamiento-indices-y-planes/050-lsm-tree-compactacion-y-amplificacion/README.md) (parte 09)
- **Ver también:** [compactación](#compactación), [costo de escritura](#costo-de-escritura), [memtable](#memtable)
- **Fuente:** Alex Petrov (2019), [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/)

### analizador

Primer componente del gestor: convierte el texto SQL en un árbol sintáctico y comprueba que los objetos citados existen y que los tipos encajan. Aquí mueren los errores de sintaxis, antes de tocar un solo dato. (En la clase 041 la misma palabra nombra otra cosa: el analizador de texto que parte un documento en términos indexables.)

- **Se trabaja en:** [012 — Arquitectura interna de un gestor, del cliente al disco](classes/part-01-fundamentos-datos-sistemas-y-metodo/012-arquitectura-interna-de-un-gestor/README.md) (parte 01)
- **Ver también:** [planificador](#planificador), [ejecutor](#ejecutor), [optimizador por costos](#optimizador-por-costos), [índice invertido](#índice-invertido)
- **Fuente:** Joseph M. Hellerstein, Michael Stonebraker, James Hamilton (2007), [Architecture of a Database System](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf)

### anomalía de actualización

Consecuencia de guardar un hecho en varias filas: corregirlo exige tocarlas todas, y la que se olvida deja la base contradiciéndose a sí misma. Junto con las anomalías de inserción y borrado, es lo que la normalización elimina.

- **Se trabaja en:** [018 — Normalización de 1FN a BCFN con dependencias funcionales](classes/part-02-modelado-conceptual-y-requisitos/018-normalizacion-y-dependencias-funcionales/README.md) (parte 02)
- **Ver también:** [anomalías de repetición](#anomalías-de-repetición), [redundancia controlada](#redundancia-controlada), [dependencia funcional](#dependencia-funcional)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

### anomalías de repetición

Los tres desastres de guardar el mismo hecho en varios sitios: al insertar hay que repetir datos, al actualizar se corrige una copia y no las otras, y al borrar se pierde información que solo vivía ahí. Son el argumento original de la normalización.

- **Se trabaja en:** [008 — Dos tablas y una relación: la clave foránea](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/008-dos-tablas-y-una-relacion/README.md) (parte 00)
- **Ver también:** [anomalía de actualización](#anomalía-de-actualización), [dependencia funcional](#dependencia-funcional), [redundancia controlada](#redundancia-controlada)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

### antirreunion

Quedarse con las filas que *no* tienen pareja: `NOT EXISTS`, o `LEFT JOIN … WHERE clave IS NULL`. `NOT IN` parece equivalente y no lo es: basta un nulo en la subconsulta para que devuelva el conjunto vacío.

- **Se trabaja en:** [026 — Reuniones: interna, externa, semi y anti](classes/part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md) (parte 04)
- **Ver también:** [NOT IN con nulos](#not-in-con-nulos), [semirreunion](#semirreunion), [reunión externa](#reunión-externa)
- **Fuente:** Anthony Molinaro, Robert de Graaf (2020), [SQL Cookbook](https://www.oreilly.com/library/view/sql-cookbook-2nd/9781492077435/)

### aplazamiento

Postergar la comprobación de una restricción hasta el `COMMIT` (`DEFERRABLE INITIALLY DEFERRED`). Permite estados intermedios inválidos dentro de la transacción —como insertar dos filas que se referencian mutuamente— sin renunciar a la garantía final.

- **Se trabaja en:** [023 — Integridad: restricciones, claves foraneas y acciones referenciales](classes/part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md) (parte 03)
- **Ver también:** [integridad referencial](#integridad-referencial), [atomicidad](#atomicidad), [frontera transaccional](#frontera-transaccional)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

### arista

Relación dirigida y con tipo entre dos nodos, que puede llevar sus propias propiedades. En un motor de grafos es un puntero real, no una clave foránea que haya que buscar en un índice, y de ahí viene su ventaja al recorrer.

- **Se trabaja en:** [038 — Grafos de propiedades y los recorridos que SQL hace mal](classes/part-07-grafos-columnas-tiempo-y-busqueda/038-grafos-de-propiedades-y-recorridos/README.md) (parte 07)
- **Ver también:** [nodo](#nodo), [reunión sin índice](#reunión-sin-índice), [atributo de relación](#atributo-de-relación)
- **Fuente:** Ian Robinson, Jim Webber, Emil Eifrem (2015), [Graph Databases](https://neo4j.com/graph-databases-book/)

### atomicidad

Todo o nada: la transacción se aplica entera o no deja rastro. No promete que sea correcta ni que sea rápida, solo que no habrá estados a medias visibles para nadie.

- **Se trabaja en:** [043 — ACID: qué garantiza cada letra y quién la implementa](classes/part-08-transacciones-concurrencia-y-recuperacion/043-acid-que-garantiza-cada-letra/README.md) (parte 08)
- **Ver también:** [unidad de recuperación](#unidad-de-recuperación), [deshacer](#deshacer), [frontera transaccional](#frontera-transaccional)
- **Fuente:** Jim Gray (1981), [The Transaction Concept: Virtues and Limitations](https://jimgray.azurewebsites.net/papers/thetransactionconcept.pdf)

### atributo de relación

Dato que no pertenece a ninguna de las dos entidades sino al hecho de que estén relacionadas: la fecha de inscripción no es del estudiante ni del curso, es de la inscripción. Es la señal de que la tabla intermedia es una entidad de pleno derecho.

- **Se trabaja en:** [016 — Entidad-relación, cardinalidad y participación](classes/part-02-modelado-conceptual-y-requisitos/016-entidad-relacion-cardinalidad-y-participacion/README.md) (parte 02)
- **Ver también:** [tabla de relación](#tabla-de-relación), [entidad](#entidad), [cardinalidad](#cardinalidad)
- **Fuente:** Peter Pin-Shan Chen (1976), [The Entity-Relationship Model - Toward a Unified View of Data](https://dl.acm.org/doi/10.1145/320434.320440)

### autovacuum

Proceso que recupera el espacio de las versiones de fila muertas que deja MVCC y actualiza las estadísticas del planificador. Cuando se queda atrás, la tabla se hincha y los planes se degradan: dos síntomas que se ven antes en el monitor que en el error.

- **Se trabaja en:** [031 — PostgreSQL: tipos, extensiones y modelo de procesos](classes/part-05-motores-relacionales-y-dialectos/031-postgresql-tipos-extensiones-y-procesos/README.md) (parte 05)
- **Ver también:** [vacuum](#vacuum), [versión de fila](#versión-de-fila), [estadística](#estadística)
- **Fuente:** Egor Rogov (2022), [PostgreSQL 14 Internals](https://postgrespro.com/community/books/internals)

## B

### B-Tree

Árbol equilibrado de páginas ordenadas, con todos los datos en hojas enlazadas entre sí. Sirve para igualdad, para rangos y para devolver ya ordenado, con un número de accesos que crece logarítmicamente. Es la estructura por defecto de casi todos los motores relacionales.

- **Se trabaja en:** [049 — B-Tree: estructura, orden de columnas y selectividad](classes/part-09-almacenamiento-indices-y-planes/049-b-tree-orden-de-columnas-y-selectividad/README.md) (parte 09)
- **Ver también:** [prefijo más a la izquierda](#prefijo-más-a-la-izquierda), [selectividad](#selectividad), [memtable](#memtable)
- **Fuente:** R. Bayer, E. McCreight (1972), [Organization and Maintenance of Large Ordered Indices](https://link.springer.com/article/10.1007/BF00288683)

### BCFN

Forma normal de Boyce-Codd: toda dependencia funcional no trivial tiene como determinante una clave candidata. Es más estricta que la tercera forma normal y es el listón práctico de este programa para un esquema transaccional.

- **Se trabaja en:** [018 — Normalización de 1FN a BCFN con dependencias funcionales](classes/part-02-modelado-conceptual-y-requisitos/018-normalizacion-y-dependencias-funcionales/README.md) (parte 02)
- **Ver también:** [dependencia funcional](#dependencia-funcional), [descomposición sin pérdida](#descomposición-sin-pérdida), [clave candidata](#clave-candidata)
- **Fuente:** Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom (2008), [Database Systems: The Complete Book](http://infolab.stanford.edu/~ullman/dscb.html)

### bloqueo optimista

En lugar de bloquear, se lee una versión y al escribir se comprueba que no haya cambiado (`WHERE version = ?`). Si cambió, se reintenta. Rinde mejor que el bloqueo cuando los conflictos son raros, y peor cuando son frecuentes.

- **Se trabaja en:** [047 — Concurrencia en la aplicación: idempotencia, reintentos y bloqueo optimista](classes/part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md) (parte 08)
- **Ver también:** [sesgo de escritura](#sesgo-de-escritura), [reintento con retroceso](#reintento-con-retroceso), [interbloqueo](#interbloqueo)
- **Fuente:** Philip A. Bernstein, Eric Newcomer (2009), [Principles of Transaction Processing](https://www.sciencedirect.com/book/9781558606234/principles-of-transaction-processing)

### BM25

Función de relevancia que refina TF-IDF con saturación de la frecuencia y normalización por longitud del documento, gobernadas por los parámetros `k1` y `b`. Es la referencia léxica contra la que se compara cualquier buscador, incluidos los vectoriales.

- **Se trabaja en:** [041 — Búsqueda de texto: índice invertido, análisis y relevancia](classes/part-07-grafos-columnas-tiempo-y-busqueda/041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) (parte 07)
- **Ver también:** [TF-IDF](#tf-idf), [fusión de rangos](#fusión-de-rangos), [índice invertido](#índice-invertido)
- **Fuente:** Stephen Robertson, Hugo Zaragoza (2009), [The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)

### BRIN

Índice de rangos por bloque: guarda el mínimo y el máximo de cada grupo de páginas. Diminuto y utilísimo cuando el orden físico se correlaciona con la columna —una tabla de eventos por fecha—, e inútil cuando no.

- **Se trabaja en:** [051 — Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes](classes/part-09-almacenamiento-indices-y-planes/051-indices-especializados/README.md) (parte 09)
- **Ver también:** [poda de particiones](#poda-de-particiones), [localidad](#localidad), [índice parcial](#índice-parcial)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Indexes](https://www.postgresql.org/docs/current/indexes.html)

### buffer pool

La memoria donde el motor mantiene las páginas leídas para no volver a pedirlas al disco. Su tasa de acierto explica la mayor parte de la diferencia entre una consulta de 2 ms y la misma consulta de 200 ms.

- **Se trabaja en:** [012 — Arquitectura interna de un gestor, del cliente al disco](classes/part-01-fundamentos-datos-sistemas-y-metodo/012-arquitectura-interna-de-un-gestor/README.md) (parte 01)
- **Ver también:** [pagina](#pagina), [localidad](#localidad), [lectura secuencial](#lectura-secuencial)
- **Fuente:** Egor Rogov (2022), [PostgreSQL 14 Internals](https://postgrespro.com/community/books/internals)

### búsqueda aproximada

Renunciar a encontrar con certeza los K vecinos más cercanos a cambio de responder en milisegundos en lugar de en minutos. La búsqueda exacta compara contra todos los vectores; la aproximada explora solo una parte del espacio y acepta perderse algunos.

- **Se trabaja en:** [069 — Índices vectoriales aproximados: HNSW, IVF y el recall](classes/part-13-vectores-recuperacion-y-rag/069-indices-vectoriales-aproximados/README.md) (parte 13)
- **Ver también:** [recall](#recall), [HNSW](#hnsw), [latencia frente a exactitud](#latencia-frente-a-exactitud)
- **Fuente:** Yu A. Malkov, D. A. Yashunin (2020), [Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs](https://arxiv.org/abs/1603.09320)

## C

### cadena vacia frente a nulo

Divergencia que rompe código al migrar: Oracle trata la cadena vacía `''` como `NULL`, y el resto de motores la distingue. Una condición `= ''` cambia de significado según el producto, y un `NOT NULL` deja de proteger lo que se creía.

- **Se trabaja en:** [032 — MySQL, MariaDB, SQL Server y Oracle: divergencias que rompen código](classes/part-05-motores-relacionales-y-dialectos/032-mysql-sqlserver-y-oracle-divergencias/README.md) (parte 05)
- **Ver también:** [NULL](#null), [modo estricto](#modo-estricto), [norma frente a producto](#norma-frente-a-producto)
- **Fuente:** Oracle (2026), [Oracle Database Documentation](https://docs.oracle.com/en/database/)

### cálculo de tuplas

Formalismo que describe el resultado con una fórmula lógica —«las tuplas t tales que…»— en lugar de con una secuencia de operadores. Es el antepasado directo de SQL y la razón formal de que SQL sea declarativo.

- **Se trabaja en:** [022 — Cálculo relacional y su equivalencia con el álgebra](classes/part-03-modelo-relacional-y-algebra/022-calculo-relacional-y-equivalencia/README.md) (parte 03)
- **Ver también:** [declaratividad](#declaratividad), [equivalencia](#equivalencia), [seguridad de expresión](#seguridad-de-expresión)
- **Fuente:** Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom (2008), [Database Systems: The Complete Book](http://infolab.stanford.edu/~ullman/dscb.html)

### campo

Una columna: un dato con nombre, tipo y —a veces— una regla. El nombre dice qué significa, el tipo dice qué valores son posibles y la restricción dice cuáles son admisibles.

- **Se trabaja en:** [001 — Qué es un dato, un registro y una tabla](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md) (parte 00)
- **Ver también:** [tipo](#tipo), [restricción](#restricción), [dato](#dato)
- **Fuente:** Michael J. Hernandez (2020), [Database Design for Mere Mortals](https://www.informit.com/store/database-design-for-mere-mortals-a-hands-on-guide-to-9780136788041)

### canalización de agregación

Secuencia de etapas (`$match`, `$group`, `$sort`, `$lookup`) por las que pasan los documentos en MongoDB. El orden importa de verdad: poner `$match` al principio permite usar el índice, ponerlo después obliga a recorrer la colección entera.

- **Se trabaja en:** [036 — Consultas, índices y agregación sobre documentos](classes/part-06-documentos-y-clave-valor/036-consultas-e-indices-sobre-documentos/README.md) (parte 06)
- **Ver también:** [agrupación](#agrupación), [índice compuesto](#índice-compuesto), [referencia](#referencia)
- **Fuente:** MongoDB, Inc. (2026), [MongoDB Manual](https://www.mongodb.com/docs/manual/)

### cardinalidad

Cuántas instancias de una entidad pueden relacionarse con cuántas de la otra: uno a uno, uno a muchos, muchos a muchos. Determina directamente dónde va la clave foránea y si hace falta una tabla intermedia.

- **Se trabaja en:** [016 — Entidad-relación, cardinalidad y participación](classes/part-02-modelado-conceptual-y-requisitos/016-entidad-relacion-cardinalidad-y-participacion/README.md) (parte 02)
- **Ver también:** [participación total](#participación-total), [tabla de relación](#tabla-de-relación), [clave foránea](#clave-foránea)
- **Fuente:** Peter Pin-Shan Chen (1976), [The Entity-Relationship Model - Toward a Unified View of Data](https://dl.acm.org/doi/10.1145/320434.320440)

### cardinalidad de etiquetas

Número de combinaciones distintas de etiquetas en una base de series temporales; cada combinación es una serie con su índice y su memoria. Meter un identificador de usuario o de petición como etiqueta produce una explosión de cardinalidad que tumba el motor.

- **Se trabaja en:** [040 — Series temporales: cardinalidad, retención y agregados continuos](classes/part-07-grafos-columnas-tiempo-y-busqueda/040-series-temporales-cardinalidad-y-retencion/README.md) (parte 07)
- **Ver también:** [punto caliente](#punto-caliente), [retención](#retención), [submuestreo](#submuestreo)
- **Fuente:** InfluxData (2026), [InfluxDB Documentation](https://docs.influxdata.com/)

### carga analítica

Pocas consultas que recorren millones de filas y agregan unas pocas columnas: OLAP. Favorece almacenamiento columnar, compresión y ejecución vectorizada, y tolera latencias de segundos.

- **Se trabaja en:** [064 — OLTP frente a OLAP: por qué se separan](classes/part-12-analitica-integracion-y-streaming/064-oltp-frente-a-olap/README.md) (parte 12)
- **Ver también:** [carga transaccional](#carga-transaccional), [almacenamiento columnar](#almacenamiento-columnar), [ejecución vectorizada](#ejecución-vectorizada)
- **Fuente:** Michael Stonebraker, Samuel Madden, Daniel J. Abadi, Stavros Harizopoulos, Nabil Hachem, Pat Helland (2007), [The End of an Architectural Era (It's Time for a Complete Rewrite)](https://cs.brown.edu/courses/cs227/archives/2008/Papers/OLTP/hstore.pdf)

### carga de trabajo

La descripción cuantificada de lo que el sistema tendrá que aguantar: volumen, proporción de lecturas y escrituras, latencia objetivo, consultas dominantes, crecimiento previsto. Es lo que convierte la elección de motor en una decisión técnica y no en una preferencia.

- **Se trabaja en:** [072 — Persistencia políglota: decidir por evidencia y no por moda](classes/part-14-arquitectura-y-proyecto-final/072-persistencia-poliglota-por-evidencia/README.md) (parte 14)
- **Ver también:** [patrón de acceso](#patrón-de-acceso), [criterio de selección](#criterio-de-selección), [percentil](#percentil)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### carga transaccional

Muchas operaciones pequeñas que leen y escriben pocas filas por identificador, con latencia de milisegundos: OLTP. Favorece filas juntas, índices B-Tree y transacciones cortas.

- **Se trabaja en:** [064 — OLTP frente a OLAP: por qué se separan](classes/part-12-analitica-integracion-y-streaming/064-oltp-frente-a-olap/README.md) (parte 12)
- **Ver también:** [carga analítica](#carga-analítica), [contención](#contención), [patrón de acceso](#patrón-de-acceso)
- **Fuente:** Michael Stonebraker, Samuel Madden, Daniel J. Abadi, Stavros Harizopoulos, Nabil Hachem, Pat Helland (2007), [The End of an Architectural Era (It's Time for a Complete Rewrite)](https://cs.brown.edu/courses/cs227/archives/2008/Papers/OLTP/hstore.pdf)

### CDC

Captura de cambios: leer el registro de transacciones del origen para publicar cada `INSERT`, `UPDATE` y `DELETE` como un evento. Frente al muestreo periódico, no pierde cambios intermedios, no requiere columna de marca temporal y no carga el origen con consultas.

- **Se trabaja en:** [066 — Integración: ETL, ELT, captura de cambios y el registro como nexo](classes/part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md) (parte 12)
- **Ver también:** [WAL](#wal), [escritura dual](#escritura-dual), [tiempo de evento](#tiempo-de-evento)
- **Fuente:** Debezium Community (2026), [Debezium Documentation](https://debezium.io/documentation/)

### CHECK

Restricción que exige que una expresión sea verdadera en cada fila: `CHECK (precio >= 0)`. Convierte una regla de negocio en algo que el motor impone; cuidado con los nulos, porque `UNKNOWN` no viola un `CHECK`.

- **Se trabaja en:** [023 — Integridad: restricciones, claves foraneas y acciones referenciales](classes/part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md) (parte 03)
- **Ver también:** [restricción](#restricción), [invariante](#invariante), [UNKNOWN](#unknown)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

### cierre

Propiedad por la que toda operación del álgebra relacional sobre relaciones devuelve una relación. Es lo que permite anidar y componer consultas indefinidamente, y lo que sostiene las vistas y las CTE.

- **Se trabaja en:** [020 — La relación como conjunto: tuplas, dominios y acceso por valor](classes/part-03-modelo-relacional-y-algebra/020-la-relacion-como-conjunto/README.md) (parte 03)
- **Ver también:** [relación](#relación), [CTE](#cte), [selección](#selección)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### clave candidata

Cualquier conjunto mínimo de atributos que identifica unívocamente una fila. Una tabla puede tener varias; elegir una como primaria no anula a las demás, que deben seguir protegidas con `UNIQUE`.

- **Se trabaja en:** [017 — Claves, identidad y el debate natural frente a sustituta](classes/part-02-modelado-conceptual-y-requisitos/017-claves-identidad-natural-y-sustituta/README.md) (parte 02)
- **Ver también:** [clave primaria](#clave-primaria), [clave natural](#clave-natural), [UNIQUE](#unique)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### clave compuesta

Clave primaria formada por dos o más columnas, típica de las tablas de relación: `(estudiante_id, curso_id)`. Fija además el orden de las columnas del índice que la sostiene, y ese orden decide qué consultas se aceleran.

- **Se trabaja en:** [007 — La clave primaria: cómo se distingue una fila de otra](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/007-la-clave-primaria/README.md) (parte 00)
- **Ver también:** [tabla de relación](#tabla-de-relación), [prefijo más a la izquierda](#prefijo-más-a-la-izquierda), [clave primaria](#clave-primaria)
- **Fuente:** Ramez Elmasri, Shamkant B. Navathe (2015), [Fundamentals of Database Systems](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003546)

### clave de agrupamiento

La parte de la clave primaria que ordena las filas dentro de una partición. Es lo que permite leer rangos —«los últimos 20 mensajes de este chat»— con una sola lectura secuencial, y por eso el orden se decide al crear la tabla, no al consultar.

- **Se trabaja en:** [039 — Columnas anchas: modelar desde la consulta](classes/part-07-grafos-columnas-tiempo-y-busqueda/039-columnas-anchas-modelar-desde-la-consulta/README.md) (parte 07)
- **Ver también:** [clave de partición](#clave-de-partición), [desnormalización por consulta](#desnormalización-por-consulta), [B-Tree](#b-tree)
- **Fuente:** Jeff Carpenter, Eben Hewitt (2020), [Cassandra: The Definitive Guide](https://www.oreilly.com/library/view/cassandra-the-definitive/9781098115159/)

### clave de idempotencia

Identificador que el cliente genera y envía con la petición para que el servidor reconozca un reintento y devuelva el resultado anterior en lugar de ejecutar dos veces. Es cómo se cobra una tarjeta una sola vez aunque el navegador reenvíe.

- **Se trabaja en:** [047 — Concurrencia en la aplicación: idempotencia, reintentos y bloqueo optimista](classes/part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md) (parte 08)
- **Ver también:** [idempotencia](#idempotencia), [reintento con retroceso](#reintento-con-retroceso), [UNIQUE](#unique)
- **Fuente:** Philip A. Bernstein, Eric Newcomer (2009), [Principles of Transaction Processing](https://www.sciencedirect.com/book/9781558606234/principles-of-transaction-processing)

### clave de partición

La parte de la clave primaria que decide en qué nodo vive la fila. Toda consulta eficiente debe fijarla; una consulta sin ella obliga a preguntar a todo el anillo, y es el error de diseño número uno en columnas anchas.

- **Se trabaja en:** [039 — Columnas anchas: modelar desde la consulta](classes/part-07-grafos-columnas-tiempo-y-busqueda/039-columnas-anchas-modelar-desde-la-consulta/README.md) (parte 07)
- **Ver también:** [clave de agrupamiento](#clave-de-agrupamiento), [hash consistente](#hash-consistente), [punto caliente](#punto-caliente)
- **Fuente:** Apache Software Foundation (2026), [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/)

### clave foránea

Columna que referencia la clave primaria de otra tabla y a la que el gestor obliga a apuntar a una fila existente. Es la integridad referencial hecha declaración: sin ella, las relaciones son una convención que alguien acabará rompiendo.

- **Se trabaja en:** [008 — Dos tablas y una relación: la clave foránea](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/008-dos-tablas-y-una-relacion/README.md) (parte 00)
- **Ver también:** [integridad referencial](#integridad-referencial), [ON DELETE](#on-delete), [tabla de relación](#tabla-de-relación)
- **Fuente:** Peter Pin-Shan Chen (1976), [The Entity-Relationship Model - Toward a Unified View of Data](https://dl.acm.org/doi/10.1145/320434.320440)

### clave natural

Identificador que ya existe en el dominio —RUT, ISBN, matrícula—. Ventaja: significa algo. Riesgo: el mundo la cambia —una persona corrige su documento, un organismo reasigna códigos— y el cambio arrastra a todas las filas que la referencian.

- **Se trabaja en:** [007 — La clave primaria: cómo se distingue una fila de otra](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/007-la-clave-primaria/README.md) (parte 00)
- **Ver también:** [clave sustituta](#clave-sustituta), [identidad estable](#identidad-estable), [clave primaria](#clave-primaria)
- **Fuente:** Michael J. Hernandez (2020), [Database Design for Mere Mortals](https://www.informit.com/store/database-design-for-mere-mortals-a-hands-on-guide-to-9780136788041)

### clave primaria

La clave candidata elegida para identificar cada fila: única, no nula y estable en el tiempo. Es la dirección por la que el resto del esquema se referirá a esa fila.

- **Se trabaja en:** [007 — La clave primaria: cómo se distingue una fila de otra](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/007-la-clave-primaria/README.md) (parte 00)
- **Ver también:** [clave candidata](#clave-candidata), [clave natural](#clave-natural), [clave sustituta](#clave-sustituta), [UNIQUE](#unique)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### clave sustituta

Identificador inventado por el sistema y sin significado externo: entero autoincremental, UUID. No cambia nunca porque no depende del mundo, a costa de necesitar además una restricción `UNIQUE` sobre la clave natural real.

- **Se trabaja en:** [007 — La clave primaria: cómo se distingue una fila de otra](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/007-la-clave-primaria/README.md) (parte 00)
- **Ver también:** [clave natural](#clave-natural), [identidad estable](#identidad-estable), [UNIQUE](#unique)
- **Fuente:** Bill Karwin (2010), [SQL Antipatterns: Avoiding the Pitfalls of Database Programming](https://pragprog.com/titles/bksqla/sql-antipatterns/)

### cobertura

Que el índice contenga todas las columnas que la consulta necesita, de modo que el motor responda sin tocar la tabla. Es la diferencia entre una lectura y dos, y suele ser la optimización con mejor relación entre esfuerzo y resultado.

- **Se trabaja en:** [036 — Consultas, índices y agregación sobre documentos](classes/part-06-documentos-y-clave-valor/036-consultas-e-indices-sobre-documentos/README.md) (parte 06)
- **Ver también:** [índice cubriente](#índice-cubriente), [índice compuesto](#índice-compuesto), [pagina](#pagina)
- **Fuente:** Markus Winand (2012), [SQL Performance Explained](https://use-the-index-luke.com/)

### colación

El conjunto de reglas que decide cómo se comparan y ordenan los textos: si `a` = `A`, dónde va la `ñ`, si los acentos cuentan. Cambia el resultado de `ORDER BY`, de `=` y de un `UNIQUE`, y es distinta por defecto en cada motor.

- **Se trabaja en:** [025 — SELECT: filtrado, proyección y orden con semántica precisa](classes/part-04-sql-en-profundidad/025-select-filtrado-proyeccion-y-orden/README.md) (parte 04)
- **Ver también:** [determinismo de orden](#determinismo-de-orden), [modo estricto](#modo-estricto), [orden](#orden)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### coma flotante

Representación binaria aproximada (`REAL`, `DOUBLE`) según IEEE 754. Rápida y adecuada para magnitudes físicas, ruinosa para dinero: `0.1 + 0.2` no da `0.3` y la diferencia se acumula fila a fila.

- **Se trabaja en:** [006 — Tipos de datos: por qué un número no es un texto](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/006-tipos-de-datos-un-numero-no-es-un-texto/README.md) (parte 00)
- **Ver también:** [decimal exacto](#decimal-exacto), [tipo de dato](#tipo-de-dato)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### commit en dos fases

Protocolo para confirmar una transacción que abarca varios sistemas: primero se pregunta a todos si pueden, después se les ordena confirmar. Es correcto y es frágil: si el coordinador cae entre las dos fases, los participantes quedan bloqueados con los cerrojos tomados.

- **Se trabaja en:** [057 — Consenso y transacciones distribuidas: Raft, 2PC y sagas](classes/part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) (parte 10)
- **Ver también:** [saga](#saga), [consenso](#consenso), [atomicidad](#atomicidad)
- **Fuente:** Philip A. Bernstein, Eric Newcomer (2009), [Principles of Transaction Processing](https://www.sciencedirect.com/book/9781558606234/principles-of-transaction-processing)

### compactación

Proceso de fusionar SSTables, descartar versiones antiguas y aplicar los borrados. Es lo que impide que las lecturas se degraden sin fin, y también lo que consume entrada y salida en segundo plano justo cuando el sistema está cargado.

- **Se trabaja en:** [050 — LSM-Tree, compactación y amplificación de escritura](classes/part-09-almacenamiento-indices-y-planes/050-lsm-tree-compactacion-y-amplificacion/README.md) (parte 09)
- **Ver también:** [amplificación de escritura](#amplificación-de-escritura), [SSTable](#sstable), [vacuum](#vacuum)
- **Fuente:** Alex Petrov (2019), [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/)

### compatibilidad hacia atras

Que el código nuevo siga entendiendo los datos escritos por el viejo, y que el viejo no se rompa con los del nuevo. Es obligatoria en cuanto el despliegue es gradual, porque durante un rato conviven las dos versiones.

- **Se trabaja en:** [059 — Migraciones evolutivas sin ventana de caída](classes/part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md) (parte 11)
- **Ver también:** [expandir y contraer](#expandir-y-contraer), [independencia lógica](#independencia-lógica), [reversibilidad](#reversibilidad)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### compensación

Operación de negocio que deshace el efecto de otra ya confirmada: reembolsar en vez de revertir, anular una reserva en vez de borrarla. No es un `ROLLBACK`, porque el estado intermedio existió y alguien pudo verlo.

- **Se trabaja en:** [057 — Consenso y transacciones distribuidas: Raft, 2PC y sagas](classes/part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) (parte 10)
- **Ver también:** [saga](#saga), [idempotencia](#idempotencia), [deshacer](#deshacer)
- **Fuente:** Pat Helland (2007), [Life beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf)

### complejidad añadida

Lo que cuesta cada sistema adicional: otro modelo de fallo, otro respaldo, otra guardia, otra consistencia que reconciliar. Es el argumento más fuerte a favor de un solo motor multimodelo mientras la carga lo permita.

- **Se trabaja en:** [072 — Persistencia políglota: decidir por evidencia y no por moda](classes/part-14-arquitectura-y-proyecto-final/072-persistencia-poliglota-por-evidencia/README.md) (parte 14)
- **Ver también:** [costo de operación](#costo-de-operación), [multimodelo](#multimodelo), [costo total de propiedad](#costo-total-de-propiedad)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### compresión

En un formato columnar, los valores contiguos se parecen, así que técnicas como el diccionario, la codificación por carrera o el delta reducen el tamaño en un orden de magnitud. Menos bytes leídos es menos entrada y salida, que es de donde sale casi toda la ventaja analítica.

- **Se trabaja en:** [042 — Analítica columnar: por qué el formato cambia el orden de magnitud](classes/part-07-grafos-columnas-tiempo-y-busqueda/042-analitica-columnar-y-vectorizacion/README.md) (parte 07)
- **Ver también:** [almacenamiento columnar](#almacenamiento-columnar), [poda de particiones](#poda-de-particiones), [pagina](#pagina)
- **Fuente:** ClickHouse, Inc. (2026), [ClickHouse Documentation](https://clickhouse.com/docs/)

### concurrencia

Varias sesiones leyendo y escribiendo a la vez sobre los mismos datos. Un archivo compartido no la resuelve: el último en guardar pisa al anterior. Un gestor la resuelve con transacciones, bloqueo o versiones.

- **Se trabaja en:** [002 — Del archivo y la hoja de cálculo a la base de datos](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) (parte 00)
- **Ver también:** [aislamiento](#aislamiento), [2PL](#2pl), [versión de fila](#versión-de-fila)
- **Fuente:** Abraham Silberschatz, Henry F. Korth, S. Sudarshan (2019), [Database System Concepts](https://db-book.com/)

### consecuencia

Lo que la decisión hace más fácil y lo que hace más difícil, incluidas las consecuencias negativas aceptadas. Un ADR que solo lista ventajas no es un registro de decisión: es un anuncio.

- **Se trabaja en:** [073 — Registro de decisiones de arquitectura y costo total](classes/part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md) (parte 14)
- **Ver también:** [ADR](#adr), [contexto](#contexto), [límite declarado](#límite-declarado)
- **Fuente:** Peter Bailis, Joseph M. Hellerstein, Michael Stonebraker (2015), [Readings in Database Systems](http://www.redbook.io/)

### consenso

Que un conjunto de nodos se ponga de acuerdo en un valor y no cambie de opinión, tolerando caídas de una minoría. Es el cimiento de la elección de líder, de la pertenencia al clúster y del commit atómico; Raft y Paxos son las dos formulaciones de referencia.

- **Se trabaja en:** [057 — Consenso y transacciones distribuidas: Raft, 2PC y sagas](classes/part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) (parte 10)
- **Ver también:** [elección de líder](#elección-de-líder), [commit en dos fases](#commit-en-dos-fases), [linealizabilidad](#linealizabilidad)
- **Fuente:** Diego Ongaro, John Ousterhout (2014), [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf)

### consistencia

La letra tramposa de ACID: significa que la transacción lleva la base de un estado válido a otro *según las restricciones declaradas*. Lo que el motor no sabe, no lo protege; la consistencia de negocio la pone quien declara las reglas, no el gestor.

- **Se trabaja en:** [043 — ACID: qué garantiza cada letra y quién la implementa](classes/part-08-transacciones-concurrencia-y-recuperacion/043-acid-que-garantiza-cada-letra/README.md) (parte 08)
- **Ver también:** [integridad declarada](#integridad-declarada), [invariante](#invariante), [CHECK](#check)
- **Fuente:** Jim Gray, Andreas Reuter (1992), [Transaction Processing: Concepts and Techniques](https://www.sciencedirect.com/book/9781558601901/transaction-processing)

### consistencia causal

Si un evento pudo influir en otro, todos los observadores los ven en ese orden; los eventos sin relación causal pueden verse en cualquier orden. Es el punto dulce entre lo débil y lo caro: evita el efecto «respuesta antes que la pregunta» sin exigir coordinación global.

- **Se trabaja en:** [056 — Modelos de consistencia y garantías de sesión](classes/part-10-distribucion-replica-y-consistencia/056-modelos-de-consistencia-y-garantias-de-sesion/README.md) (parte 10)
- **Ver también:** [linealizabilidad](#linealizabilidad), [lectura monotona](#lectura-monotona), [convergencia](#convergencia)
- **Fuente:** Leslie Lamport (1978), [Time, Clocks, and the Ordering of Events in a Distributed System](https://dl.acm.org/doi/10.1145/359545.359563)

### consulta declarativa

Se declara *qué* resultado se quiere y el motor decide *cómo* obtenerlo. Quien consulta no escribe recorridos ni bucles; el optimizador elige el plan y puede cambiarlo cuando cambian los datos, sin que nadie reescriba la consulta.

- **Se trabaja en:** [002 — Del archivo y la hoja de cálculo a la base de datos](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) (parte 00)
- **Ver también:** [declaratividad](#declaratividad), [optimizador por costos](#optimizador-por-costos), [cálculo de tuplas](#cálculo-de-tuplas)
- **Fuente:** Abraham Silberschatz, Henry F. Korth, S. Sudarshan (2019), [Database System Concepts](https://db-book.com/)

### consulta lenta

Registro de las consultas que superan un umbral, agrupadas por forma —`pg_stat_statements` y equivalentes—. Lo que importa no es la más lenta, sino la que multiplica tiempo por frecuencia: mil consultas de 50 ms pesan más que una de 5 s.

- **Se trabaja en:** [062 — Observabilidad, objetivos de servicio y capacidad](classes/part-11-operacion-seguridad-y-gobierno/062-observabilidad-slo-y-capacidad/README.md) (parte 11)
- **Ver también:** [percentil](#percentil), [estadística](#estadística), [costo frente a tiempo](#costo-frente-a-tiempo)
- **Fuente:** Laine Campbell, Charity Majors (2017), [Database Reliability Engineering](https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/)

### consulta parametrizada

Enviar la sentencia y los valores por canales distintos, de modo que el motor nunca interprete el dato como código. Es la defensa completa contra la inyección SQL, no una mitigación: bien usada, no hay cadena de entrada que cambie la estructura de la consulta.

- **Se trabaja en:** [061 — Inyección SQL y el contrato de parametrización](classes/part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md) (parte 11)
- **Ver también:** [identificador dinamico](#identificador-dinamico), [lista blanca](#lista-blanca), [defensa en profundidad](#defensa-en-profundidad)
- **Fuente:** OWASP (2026), [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

### contención

Lo que ocurre cuando la consulta analítica y la transaccional compiten por el mismo buffer, los mismos cerrojos y el mismo disco. Es la razón operativa —antes que la teórica— por la que el informe mensual acaba mudándose a otro sistema.

- **Se trabaja en:** [064 — OLTP frente a OLAP: por qué se separan](classes/part-12-analitica-integracion-y-streaming/064-oltp-frente-a-olap/README.md) (parte 12)
- **Ver también:** [carga analítica](#carga-analítica), [saturación](#saturación), [buffer pool](#buffer-pool)
- **Fuente:** Michael Stonebraker, Samuel Madden, Daniel J. Abadi, Stavros Harizopoulos, Nabil Hachem, Pat Helland (2007), [The End of an Architectural Era (It's Time for a Complete Rewrite)](https://cs.brown.edu/courses/cs227/archives/2008/Papers/OLTP/hstore.pdf)

### contenedor

Entorno de ejecución aislado con el motor y su versión congelados. Elimina el «en mi máquina funciona» y convierte la versión del motor en parte de la evidencia, no en un detalle olvidado.

- **Se trabaja en:** [014 — Entorno reproducible y evidencia comprobable](classes/part-01-fundamentos-datos-sistemas-y-metodo/014-entorno-reproducible-y-evidencia/README.md) (parte 01)
- **Ver también:** [reproducibilidad](#reproducibilidad), [costo de operación](#costo-de-operación)
- **Fuente:** Docker, Inc. (2026), [Docker Compose Documentation](https://docs.docker.com/compose/)

### contexto

La sección del ADR que describe las fuerzas del momento: restricciones, plazos, volúmenes y lo que se sabía entonces. Es lo que permite juzgar la decisión con justicia después, y lo que indica cuándo dejó de ser válida.

- **Se trabaja en:** [073 — Registro de decisiones de arquitectura y costo total](classes/part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md) (parte 14)
- **Ver también:** [ADR](#adr), [consecuencia](#consecuencia), [reversibilidad](#reversibilidad)
- **Fuente:** Peter Bailis, Joseph M. Hellerstein, Michael Stonebraker (2015), [Readings in Database Systems](http://www.redbook.io/)

### convergencia

Que las réplicas acaben en el mismo estado si cesan las escrituras. Es la promesa de la consistencia eventual, y solo se cumple si hay una regla determinista de resolución de conflictos, como la que dan los CRDT.

- **Se trabaja en:** [056 — Modelos de consistencia y garantías de sesión](classes/part-10-distribucion-replica-y-consistencia/056-modelos-de-consistencia-y-garantias-de-sesion/README.md) (parte 10)
- **Ver también:** [quórum](#quórum), [consistencia causal](#consistencia-causal), [compensación](#compensación)
- **Fuente:** Marc Shapiro, Nuno Preguica, Carlos Baquero, Marek Zawirski (2011), [Conflict-free Replicated Data Types](https://inria.hal.science/inria-00609399/document)

### coseno

Medida de similitud basada en el ángulo entre dos vectores, que ignora su magnitud. Es la métrica habitual con embeddings de texto, donde importa la dirección del significado y no la longitud del documento.

- **Se trabaja en:** [068 — Embeddings y métricas de distancia: qué significa parecido](classes/part-13-vectores-recuperacion-y-rag/068-embeddings-y-metricas-de-distancia/README.md) (parte 13)
- **Ver también:** [producto interno](#producto-interno), [normalización](#normalización), [espacio vectorial](#espacio-vectorial)
- **Fuente:** Andrew Kane (2026), [pgvector](https://github.com/pgvector/pgvector)

### costo de escritura

Lo que se paga en cada `INSERT` o `UPDATE` por las copias, los índices y los agregados que hay que mantener coherentes. Toda aceleración de lectura por duplicación se cobra aquí; el diseño consiste en decidir de qué lado se quiere el dolor.

- **Se trabaja en:** [019 — Desnormalización deliberada y patrones de acceso](classes/part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md) (parte 02)
- **Ver también:** [redundancia controlada](#redundancia-controlada), [costo de mantenimiento](#costo-de-mantenimiento), [amplificación de escritura](#amplificación-de-escritura)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### costo de mantenimiento

Lo que cada índice cobra en cada `INSERT`, `UPDATE` y `DELETE`, más el espacio que ocupa y el trabajo de reconstruirlo. Un índice que no usa ninguna consulta no es neutro: es una penalización permanente sobre todas las escrituras.

- **Se trabaja en:** [051 — Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes](classes/part-09-almacenamiento-indices-y-planes/051-indices-especializados/README.md) (parte 09)
- **Ver también:** [costo de escritura](#costo-de-escritura), [índice cubriente](#índice-cubriente), [estadística](#estadística)
- **Fuente:** Markus Winand (2012), [SQL Performance Explained](https://use-the-index-luke.com/)

### costo de operación

Todo lo que cuesta mantener vivo un motor después de instalarlo: respaldos probados, actualizaciones, monitorización, personas de guardia. Suele superar con creces el costo de licencia o de cómputo.

- **Se trabaja en:** [009 — Cuándo NO necesitas una base de datos](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/009-cuando-no-necesitas-una-base-de-datos/README.md) (parte 00)
- **Ver también:** [costo total de propiedad](#costo-total-de-propiedad), [complejidad añadida](#complejidad-añadida), [prueba de restauración](#prueba-de-restauración)
- **Fuente:** Laine Campbell, Charity Majors (2017), [Database Reliability Engineering](https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/)

### costo frente a tiempo

El `cost` de `EXPLAIN` es una unidad interna comparativa, no milisegundos; el tiempo real solo aparece con `EXPLAIN ANALYZE`. Comparar filas estimadas contra filas reales en cada nodo es la técnica central para refutar una hipótesis de rendimiento.

- **Se trabaja en:** [052 — Planes de ejecución: leer EXPLAIN y refutar una hipótesis](classes/part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md) (parte 09)
- **Ver también:** [estimación de cardinalidad](#estimación-de-cardinalidad), [ejecutor](#ejecutor), [evidencia](#evidencia)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)

### costo total de propiedad

La suma a varios años de licencias, infraestructura, personas, formación y migración de salida. Comparar solo el precio por hora de cómputo suele invertir el orden del ranking en cuanto se añaden las horas de operación.

- **Se trabaja en:** [073 — Registro de decisiones de arquitectura y costo total](classes/part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md) (parte 14)
- **Ver también:** [costo de operación](#costo-de-operación), [complejidad añadida](#complejidad-añadida), [reversibilidad](#reversibilidad)
- **Fuente:** Laine Campbell, Charity Majors (2017), [Database Reliability Engineering](https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/)

### CREATE TABLE

La orden que declara una tabla: columnas, tipos y restricciones. Es el contrato; a partir de ahí el motor rechaza todo lo que no lo cumpla, venga de donde venga.

- **Se trabaja en:** [003 — Tu primera base de datos: crear, insertar y leer](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/003-tu-primera-base-de-datos/README.md) (parte 00)
- **Ver también:** [definición frente a manipulación](#definición-frente-a-manipulación), [tipo de dato](#tipo-de-dato), [restricción](#restricción)
- **Fuente:** SQLite Consortium (2026), [SQLite Documentation](https://sqlite.org/docs.html)

### crecimiento no acotado

Un arreglo incrustado que puede crecer indefinidamente —los comentarios de una publicación viral, el histórico de un sensor—. Acaba chocando con el límite de tamaño del documento y degrada cada lectura, aunque solo se quería un campo. Es la señal de que ese arreglo debía ser una colección aparte.

- **Se trabaja en:** [035 — Modelado documental: incrustar o referenciar](classes/part-06-documentos-y-clave-valor/035-modelado-documental-incrustar-o-referenciar/README.md) (parte 06)
- **Ver también:** [incrustación](#incrustación), [patrón de extensión](#patrón-de-extensión), [retención](#retención)
- **Fuente:** Shannon Bradshaw, Eoin Brazil, Kristina Chodorow (2019), [MongoDB: The Definitive Guide](https://www.oreilly.com/library/view/mongodb-the-definitive/9781491954454/)

### criterio de decisión

La regla explícita por la que se elige —o se descarta— una tecnología: volumen, concurrencia, garantías necesarias y costo de operación. Sin criterio escrito, la elección se justifica a posteriori y ya no se puede revisar.

- **Se trabaja en:** [009 — Cuándo NO necesitas una base de datos](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/009-cuando-no-necesitas-una-base-de-datos/README.md) (parte 00)
- **Ver también:** [carga de trabajo](#carga-de-trabajo), [costo de operación](#costo-de-operación), [complejidad añadida](#complejidad-añadida)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### criterio de selección

La lista escrita de propiedades que se van a comparar entre candidatos, con su peso, fijada antes de mirar los productos. Escribirla después es escribir la justificación de lo que ya se había decidido.

- **Se trabaja en:** [072 — Persistencia políglota: decidir por evidencia y no por moda](classes/part-14-arquitectura-y-proyecto-final/072-persistencia-poliglota-por-evidencia/README.md) (parte 14)
- **Ver también:** [carga de trabajo](#carga-de-trabajo), [ADR](#adr), [complejidad añadida](#complejidad-añadida)
- **Fuente:** Pramod J. Sadalage, Martin Fowler (2012), [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html)

### CTE

Expresión de tabla común (`WITH … AS`): un resultado con nombre, visible en la consulta que la sigue. Sirve para nombrar pasos intermedios y hacer legible una consulta larga; en algunos motores es además una barrera de optimización, y eso puede ayudar o estorbar.

- **Se trabaja en:** [028 — CTE, subconsultas y funciones de ventana](classes/part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md) (parte 04)
- **Ver también:** [subconsulta correlacionada](#subconsulta-correlacionada), [recursión](#recursión), [cierre](#cierre)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### cuantización

Comprimir los vectores usando menos bits por componente —escalar, binaria o por producto—. Reduce la memoria en un orden de magnitud a cambio de precisión, y suele combinarse con un reordenamiento final sobre los vectores completos.

- **Se trabaja en:** [069 — Índices vectoriales aproximados: HNSW, IVF y el recall](classes/part-13-vectores-recuperacion-y-rag/069-indices-vectoriales-aproximados/README.md) (parte 13)
- **Ver también:** [compresión](#compresión), [recall](#recall), [HNSW](#hnsw)
- **Fuente:** Jeff Johnson, Matthijs Douze, Herve Jegou (2019), [Billion-scale Similarity Search with GPUs](https://arxiv.org/abs/1702.08734)

## D

### dato

Un valor registrado sin el contexto que lo interpreta: `38`, `Ada`, `2026-03-01`. Por sí solo no afirma nada, porque el mismo valor puede ser una edad, una temperatura o un número de camiseta. Toda base de datos existe para guardar el dato junto al contexto que lo convierte en información.

- **Se trabaja en:** [001 — Qué es un dato, un registro y una tabla](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md) (parte 00)
- **Ver también:** [información](#información), [campo](#campo), [tipo](#tipo)
- **Fuente:** William Kent (2012), [Data and Reality](https://technicspub.com/data-and-reality/)

### DDL transaccional

Capacidad de ejecutar `CREATE`, `ALTER` o `DROP` dentro de una transacción y poder revertirlos. PostgreSQL y SQLite la tienen; MySQL histórico y Oracle confirman implícitamente, lo que convierte una migración fallida a mitad en un estado sin retorno.

- **Se trabaja en:** [024 — DDL: el esquema como contrato ejecutable](classes/part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md) (parte 04)
- **Ver también:** [definición frente a manipulación](#definición-frente-a-manipulación), [atomicidad](#atomicidad), [expandir y contraer](#expandir-y-contraer)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

### decimal exacto

Tipo numérico de precisión y escala fijas (`NUMERIC`, `DECIMAL`) que representa exactamente los valores decimales. Es el tipo del dinero: no arrastra el error de representación binaria de la coma flotante.

- **Se trabaja en:** [006 — Tipos de datos: por qué un número no es un texto](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/006-tipos-de-datos-un-numero-no-es-un-texto/README.md) (parte 00)
- **Ver también:** [coma flotante](#coma-flotante), [tipo de dato](#tipo-de-dato)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

### declaratividad

Decir qué se quiere, no cómo obtenerlo. Su valor práctico es que el motor puede cambiar de estrategia —de recorrido completo a índice, de reunión anidada a hash— cuando cambian los datos, sin que nadie toque el código.

- **Se trabaja en:** [022 — Cálculo relacional y su equivalencia con el álgebra](classes/part-03-modelo-relacional-y-algebra/022-calculo-relacional-y-equivalencia/README.md) (parte 03)
- **Ver también:** [consulta declarativa](#consulta-declarativa), [equivalencia](#equivalencia), [optimizador por costos](#optimizador-por-costos)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### defensa en profundidad

Poner varias barreras independientes, de modo que fallar una no baste: parametrizar, además dar privilegio mínimo, además registrar, además limitar por fila. Cada capa asume que las otras pueden fallar.

- **Se trabaja en:** [061 — Inyección SQL y el contrato de parametrización](classes/part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md) (parte 11)
- **Ver también:** [privilegio mínimo](#privilegio-mínimo), [lista blanca](#lista-blanca), [seguridad por fila](#seguridad-por-fila)
- **Fuente:** OWASP (2021), [OWASP Top 10](https://owasp.org/Top10/)

### defensa técnica

Sostener una decisión ante preguntas hostiles: por qué este motor, qué mediste, qué alternativa descartaste y con qué dato. Es el formato de evaluación del proyecto final porque es el formato real de una revisión de arquitectura.

- **Se trabaja en:** [074 — Proyecto final: diseñar, medir y defender](classes/part-14-arquitectura-y-proyecto-final/074-proyecto-final-disenar-medir-y-defender/README.md) (parte 14)
- **Ver también:** [evidencia reproducible](#evidencia-reproducible), [límite declarado](#límite-declarado), [ADR](#adr)
- **Fuente:** Peter Bailis, Joseph M. Hellerstein, Michael Stonebraker (2015), [Readings in Database Systems](http://www.redbook.io/)

### definición frente a manipulación

SQL se separa en DDL, que define y cambia estructuras (`CREATE`, `ALTER`, `DROP`), y DML, que consulta y cambia contenido (`SELECT`, `INSERT`, `UPDATE`, `DELETE`). La distinción importa porque no todos los motores dan al DDL las mismas garantías transaccionales.

- **Se trabaja en:** [003 — Tu primera base de datos: crear, insertar y leer](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/003-tu-primera-base-de-datos/README.md) (parte 00)
- **Ver también:** [DDL transaccional](#ddl-transaccional), [CREATE TABLE](#create-table), [INSERT](#insert)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### DELETE

Borra las filas que cumplen el `WHERE`. Igual que `UPDATE`, sin `WHERE` alcanza a toda la tabla; a diferencia de `DROP`, deja la estructura en pie.

- **Se trabaja en:** [005 — Cambiar datos: INSERT, UPDATE, DELETE y el WHERE que salva](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/005-cambiar-datos-insert-update-delete/README.md) (parte 00)
- **Ver también:** [alcance del cambio](#alcance-del-cambio), [ON DELETE](#on-delete), [transacción como red](#transacción-como-red)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### dependencia funcional

Relación `X → Y`: conocido el valor de X queda determinado el de Y. Es la herramienta formal con la que se demuestra que una tabla está mal descompuesta, y no una intuición sobre qué «pertenece» a qué.

- **Se trabaja en:** [018 — Normalización de 1FN a BCFN con dependencias funcionales](classes/part-02-modelado-conceptual-y-requisitos/018-normalizacion-y-dependencias-funcionales/README.md) (parte 02)
- **Ver también:** [BCFN](#bcfn), [descomposición sin pérdida](#descomposición-sin-pérdida), [anomalía de actualización](#anomalía-de-actualización)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

### dependencia funcional en GROUP BY

Regla que permite seleccionar una columna no agrupada si depende funcionalmente de la clave de agrupación —agrupar por `id` y seleccionar `nombre`—. PostgreSQL la reconoce; otros motores exigen listar todo, y MySQL en modo laxo devuelve un valor arbitrario sin avisar.

- **Se trabaja en:** [027 — Agregación, GROUP BY y HAVING sin duplicar filas](classes/part-04-sql-en-profundidad/027-agregacion-group-by-y-having/README.md) (parte 04)
- **Ver también:** [dependencia funcional](#dependencia-funcional), [agrupación](#agrupación), [modo estricto](#modo-estricto)
- **Fuente:** Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom (2008), [Database Systems: The Complete Book](http://infolab.stanford.edu/~ullman/dscb.html)

### derecho de supresión

Obligación de borrar los datos de una persona cuando lo solicita y no hay base para conservarlos. Choca de frente con los respaldos, las réplicas y los registros de auditoría, y por eso hay que diseñar dónde vive el dato personal antes de que lo pidan.

- **Se trabaja en:** [063 — Privacidad, retención y gobierno del dato](classes/part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) (parte 11)
- **Ver también:** [retención](#retención), [limitación de finalidad](#limitación-de-finalidad), [prueba de restauración](#prueba-de-restauración)
- **Fuente:** Union Europea (2016), [Reglamento (UE) 2016/679 - Proteccion de datos personales](https://eur-lex.europa.eu/eli/reg/2016/679/oj)

### descomposición sin pérdida

Partir una tabla en dos de modo que reunirlas devuelva exactamente la original, ni una fila más ni una menos. Se garantiza cuando el atributo común es clave en al menos una de las dos; sin esa condición la normalización inventa datos.

- **Se trabaja en:** [018 — Normalización de 1FN a BCFN con dependencias funcionales](classes/part-02-modelado-conceptual-y-requisitos/018-normalizacion-y-dependencias-funcionales/README.md) (parte 02)
- **Ver también:** [dependencia funcional](#dependencia-funcional), [reunión natural](#reunión-natural), [BCFN](#bcfn)
- **Fuente:** Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom (2008), [Database Systems: The Complete Book](http://infolab.stanford.edu/~ullman/dscb.html)

### deshacer

Fase que revierte las transacciones que estaban a medias en el momento de la caída, usando la información de deshacer del registro. Es la implementación concreta de la atomicidad.

- **Se trabaja en:** [046 — Registro anticipado y recuperación: WAL y ARIES](classes/part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md) (parte 08)
- **Ver también:** [rehacer](#rehacer), [atomicidad](#atomicidad), [transacción como red](#transacción-como-red)
- **Fuente:** C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz (1992), [ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging](https://dl.acm.org/doi/10.1145/128765.128770)

### desnormalización por consulta

Método de diseño de columnas anchas: se escribe primero la lista de consultas y luego una tabla por consulta, aunque los mismos datos queden repetidos en cinco tablas. La coherencia entre copias pasa a ser responsabilidad de la aplicación.

- **Se trabaja en:** [039 — Columnas anchas: modelar desde la consulta](classes/part-07-grafos-columnas-tiempo-y-busqueda/039-columnas-anchas-modelar-desde-la-consulta/README.md) (parte 07)
- **Ver también:** [patrón de acceso](#patrón-de-acceso), [redundancia controlada](#redundancia-controlada), [escritura dual](#escritura-dual)
- **Fuente:** Jeff Carpenter, Eben Hewitt (2020), [Cassandra: The Definitive Guide](https://www.oreilly.com/library/view/cassandra-the-definitive/9781098115159/)

### determinismo de orden

Que dos ejecuciones de la misma consulta devuelvan las filas en el mismo orden. Solo lo garantiza un `ORDER BY` cuyas columnas no empaten; con empates, el desempate lo decide el plan y puede cambiar mañana.

- **Se trabaja en:** [025 — SELECT: filtrado, proyección y orden con semántica precisa](classes/part-04-sql-en-profundidad/025-select-filtrado-proyeccion-y-orden/README.md) (parte 04)
- **Ver también:** [orden](#orden), [LIMIT](#limit), [colación](#colación)
- **Fuente:** Anthony Molinaro, Robert de Graaf (2020), [SQL Cookbook](https://www.oreilly.com/library/view/sql-cookbook-2nd/9781492077435/)

### diccionario de datos

La lista de cada atributo con su significado exacto, su tipo, su unidad y su origen. Es lo que impide que «fecha» signifique alta para un equipo y último acceso para otro.

- **Se trabaja en:** [015 — De requisitos ambiguos a entidades defendibles](classes/part-02-modelado-conceptual-y-requisitos/015-de-requisitos-a-entidades/README.md) (parte 02)
- **Ver también:** [campo](#campo), [alcance](#alcance), [información](#información)
- **Fuente:** Michael J. Hernandez (2020), [Database Design for Mere Mortals](https://www.informit.com/store/database-design-for-mere-mortals-a-hands-on-guide-to-9780136788041)

### dimensión

Tabla que describe el contexto por el que se filtra y se agrupa: producto, cliente, tiempo, sucursal. Se desnormaliza a propósito para evitar reuniones en cada consulta, y es donde vive casi todo el significado del modelo. (En la parte 13 la misma palabra designa otra cosa: el número de componentes de un vector.)

- **Se trabaja en:** [065 — Modelado dimensional: hechos, dimensiones y cambios lentos](classes/part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) (parte 12)
- **Ver también:** [tabla de hechos](#tabla-de-hechos), [dimensión de cambio lento](#dimensión-de-cambio-lento), [espacio vectorial](#espacio-vectorial)
- **Fuente:** Ralph Kimball, Margy Ross (2013), [The Data Warehouse Toolkit](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

### dimensión de cambio lento

Técnica para tratar los atributos que cambian con el tiempo: sobrescribir y perder la historia (tipo 1), o añadir una fila nueva con vigencia y conservarla (tipo 2). Determina si un informe del año pasado sigue diciendo lo que decía entonces.

- **Se trabaja en:** [065 — Modelado dimensional: hechos, dimensiones y cambios lentos](classes/part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) (parte 12)
- **Ver también:** [dimensión](#dimensión), [identidad estable](#identidad-estable), [retención](#retención)
- **Fuente:** Ralph Kimball, Margy Ross (2013), [The Data Warehouse Toolkit](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

### disponibilidad

En el enunciado formal de CAP, que toda petición a un nodo no caído reciba respuesta. Es una definición mucho más estricta que el «99,9 % de tiempo activo» del lenguaje operativo, y confundirlas es el origen de casi todas las lecturas erróneas del teorema.

- **Se trabaja en:** [055 — CAP, PACELC y lo que realmente se elige](classes/part-10-distribucion-replica-y-consistencia/055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) (parte 10)
- **Ver también:** [partición de red](#partición-de-red), [presupuesto de error](#presupuesto-de-error), [linealizabilidad](#linealizabilidad)
- **Fuente:** Seth Gilbert, Nancy Lynch (2002), [Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services](https://dl.acm.org/doi/10.1145/564585.564601)

### división

Operador que responde a las preguntas de tipo «para todos»: qué estudiantes están inscritos en *todos* los cursos obligatorios. SQL no tiene un operador equivalente y se resuelve con doble negación (`NOT EXISTS` anidado) o contando.

- **Se trabaja en:** [021 — Álgebra relacional: selección, proyección, producto y reunión](classes/part-03-modelo-relacional-y-algebra/021-algebra-relacional-operadores/README.md) (parte 03)
- **Ver también:** [antirreunion](#antirreunion), [cálculo de tuplas](#cálculo-de-tuplas), [agrupación](#agrupación)
- **Fuente:** Abraham Silberschatz, Henry F. Korth, S. Sudarshan (2019), [Database System Concepts](https://db-book.com/)

### doble conteo

Sumar o contar sobre un resultado que una reunión ya había multiplicado. El síntoma es un total que crece al añadir un `JOIN` que «solo traía un dato más»; la cura es agregar en una subconsulta o CTE antes de reunir.

- **Se trabaja en:** [027 — Agregación, GROUP BY y HAVING sin duplicar filas](classes/part-04-sql-en-profundidad/027-agregacion-group-by-y-having/README.md) (parte 04)
- **Ver también:** [multiplicación de filas](#multiplicación-de-filas), [agrupación](#agrupación), [CTE](#cte)
- **Fuente:** Joe Celko (2014), [Joe Celko's SQL for Smarties: Advanced SQL Programming](https://www.sciencedirect.com/book/9780128007617/joe-celkos-sql-for-smarties)

### doble escritura

Fase transitoria en la que la aplicación escribe en la estructura vieja y en la nueva a la vez. Sostiene la migración mientras se rellena el histórico; hay que declarar desde el principio cuándo termina, porque si no se queda para siempre.

- **Se trabaja en:** [059 — Migraciones evolutivas sin ventana de caída](classes/part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md) (parte 11)
- **Ver también:** [expandir y contraer](#expandir-y-contraer), [relleno](#relleno), [escritura dual](#escritura-dual)
- **Fuente:** Scott W. Ambler, Pramod J. Sadalage (2006), [Refactoring Databases: Evolutionary Database Design](https://databaserefactoring.com/)

### dominio

El conjunto de valores admisibles de un atributo, con sus operaciones. Es el concepto del que los tipos de SQL son una aproximación pobre: SQL permite comparar un número de teléfono con un código postal si ambos son enteros.

- **Se trabaja en:** [020 — La relación como conjunto: tuplas, dominios y acceso por valor](classes/part-03-modelo-relacional-y-algebra/020-la-relacion-como-conjunto/README.md) (parte 03)
- **Ver también:** [tipo](#tipo), [tipo de dato](#tipo-de-dato), [CHECK](#check)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### durabilidad

Una vez confirmada la transacción, su efecto sobrevive a un corte de luz. Se consigue escribiendo el cambio en un registro secuencial y forzándolo al disco antes de responder «hecho».

- **Se trabaja en:** [002 — Del archivo y la hoja de cálculo a la base de datos](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) (parte 00)
- **Ver también:** [WAL](#wal), [atomicidad](#atomicidad), [punto de control](#punto-de-control)
- **Fuente:** SQLite Consortium (2026), [SQLite Documentation](https://sqlite.org/docs.html)

### durabilidad configurable

Poder elegir cuánta pérdida se acepta a cambio de latencia: Redis ofrece desde ninguna persistencia hasta `appendfsync always`, pasando por instantáneas periódicas. La decisión es de negocio, y hay que escribirla: «se pueden perder hasta N segundos de escrituras».

- **Se trabaja en:** [037 — Clave-valor, caché y expiración: qué se pierde exactamente](classes/part-06-documentos-y-clave-valor/037-clave-valor-cache-y-expiracion/README.md) (parte 06)
- **Ver también:** [durabilidad](#durabilidad), [RPO](#rpo), [WAL](#wal)
- **Fuente:** Redis Ltd. (2026), [Redis: Persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)

## E

### ejecución vectorizada

El ejecutor procesa lotes de valores por operador en lugar de fila a fila. Reduce el costo por fila del intérprete y permite usar instrucciones SIMD; combinada con el formato columnar, es la explicación de las diferencias de dos órdenes de magnitud frente a un motor de filas.

- **Se trabaja en:** [042 — Analítica columnar: por qué el formato cambia el orden de magnitud](classes/part-07-grafos-columnas-tiempo-y-busqueda/042-analitica-columnar-y-vectorizacion/README.md) (parte 07)
- **Ver también:** [vectorización](#vectorización), [almacenamiento columnar](#almacenamiento-columnar), [ejecutor](#ejecutor)
- **Fuente:** DuckDB Foundation (2026), [DuckDB Documentation](https://duckdb.org/docs/)

### ejecutor

Recorre el plan elegido operador a operador y produce las filas. Es donde `EXPLAIN ANALYZE` muestra los tiempos reales frente a los que el planificador había estimado.

- **Se trabaja en:** [012 — Arquitectura interna de un gestor, del cliente al disco](classes/part-01-fundamentos-datos-sistemas-y-metodo/012-arquitectura-interna-de-un-gestor/README.md) (parte 01)
- **Ver también:** [planificador](#planificador), [costo frente a tiempo](#costo-frente-a-tiempo), [ejecución vectorizada](#ejecución-vectorizada)
- **Fuente:** Joseph M. Hellerstein, Michael Stonebraker, James Hamilton (2007), [Architecture of a Database System](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf)

### elección de líder

Procedimiento por el que la mayoría acuerda quién ordena las escrituras durante un mandato. Que se necesite mayoría es lo que impide dos líderes simultáneos —el escenario de cerebro dividido— cuando la red se parte.

- **Se trabaja en:** [057 — Consenso y transacciones distribuidas: Raft, 2PC y sagas](classes/part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) (parte 10)
- **Ver también:** [consenso](#consenso), [partición de red](#partición-de-red), [quórum](#quórum)
- **Fuente:** Diego Ongaro, John Ousterhout (2014), [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf)

### ELT

Cargar los datos en crudo y transformarlos dentro del almacén, con SQL versionado y probado. Es el enfoque dominante desde que el cómputo del almacén es barato, y su ventaja real es que la transformación queda auditable y se puede rehacer.

- **Se trabaja en:** [066 — Integración: ETL, ELT, captura de cambios y el registro como nexo](classes/part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md) (parte 12)
- **Ver también:** [ETL](#etl), [idempotencia de carga](#idempotencia-de-carga), [carga analítica](#carga-analítica)
- **Fuente:** dbt Labs (2026), [dbt Documentation](https://docs.getdbt.com/)

### entidad

Cosa del dominio con identidad propia que persiste a lo largo del tiempo: un cliente, un producto, una cuenta. Se distingue de la actividad en que existe aunque no pase nada, y suele ser la raíz de un agregado.

- **Se trabaja en:** [034 — El agregado como unidad de consistencia](classes/part-06-documentos-y-clave-valor/034-el-agregado-como-unidad-de-consistencia/README.md) (parte 06)
- **Ver también:** [actividad](#actividad), [agregado](#agregado), [identidad estable](#identidad-estable)
- **Fuente:** Pramod J. Sadalage, Martin Fowler (2012), [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html)

### entidad débil

Entidad que no puede identificarse sin la entidad de la que depende: una línea de pedido existe solo dentro de su pedido. Su clave incluye la del padre, y su ciclo de vida termina cuando termina el del padre.

- **Se trabaja en:** [016 — Entidad-relación, cardinalidad y participación](classes/part-02-modelado-conceptual-y-requisitos/016-entidad-relacion-cardinalidad-y-participacion/README.md) (parte 02)
- **Ver también:** [clave compuesta](#clave-compuesta), [participación total](#participación-total), [ON DELETE](#on-delete)
- **Fuente:** Peter Pin-Shan Chen (1976), [The Entity-Relationship Model - Toward a Unified View of Data](https://dl.acm.org/doi/10.1145/320434.320440)

### entrega al menos una vez

Garantía de que ningún mensaje se pierde, admitiendo que alguno se repita. Es la garantía realista de las colas, y por eso el consumidor debe ser idempotente: el «exactamente una vez» de extremo a extremo se construye sobre esto, no en lugar de esto.

- **Se trabaja en:** [067 — Streaming: tiempo de evento, ventanas y semántica de entrega](classes/part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md) (parte 12)
- **Ver también:** [idempotencia](#idempotencia), [clave de idempotencia](#clave-de-idempotencia), [idempotencia de carga](#idempotencia-de-carga)
- **Fuente:** Apache Software Foundation (2026), [Apache Kafka Documentation](https://kafka.apache.org/documentation/)

### equivalencia

Dos expresiones son equivalentes si devuelven la misma relación para toda base de datos posible. Codd demostró que álgebra y cálculo tienen el mismo poder expresivo; sobre ese teorema descansa la libertad del optimizador para reescribir consultas.

- **Se trabaja en:** [022 — Cálculo relacional y su equivalencia con el álgebra](classes/part-03-modelo-relacional-y-algebra/022-calculo-relacional-y-equivalencia/README.md) (parte 03)
- **Ver también:** [cálculo de tuplas](#cálculo-de-tuplas), [optimizador por costos](#optimizador-por-costos), [declaratividad](#declaratividad)
- **Fuente:** Raghu Ramakrishnan, Johannes Gehrke (2002), [Database Management Systems](https://pages.cs.wisc.edu/~dbbook/)

### escritura dual

Que la aplicación escriba a la vez en la base y en la cola. Parece la solución obvia y es un antipatrón: no hay atomicidad entre los dos destinos, así que tarde o temprano uno recibe lo que el otro no. La alternativa correcta es CDC o el patrón de bandeja de salida.

- **Se trabaja en:** [066 — Integración: ETL, ELT, captura de cambios y el registro como nexo](classes/part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md) (parte 12)
- **Ver también:** [CDC](#cdc), [doble escritura](#doble-escritura), [frontera transaccional](#frontera-transaccional)
- **Fuente:** Jay Kreps (2013), [The Log: What Every Software Engineer Should Know About Real-Time Data's Unifying Abstraction](https://web.archive.org/web/2023/https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)

### espacio vectorial

Representación de un texto, una imagen o un usuario como un punto de N coordenadas, colocado por un modelo de forma que la cercanía refleje parecido semántico. El parecido es el que aprendió ese modelo concreto: cambiar de modelo cambia el significado de «cerca».

- **Se trabaja en:** [068 — Embeddings y métricas de distancia: qué significa parecido](classes/part-13-vectores-recuperacion-y-rag/068-embeddings-y-metricas-de-distancia/README.md) (parte 13)
- **Ver también:** [coseno](#coseno), [dimensión](#dimensión), [normalización](#normalización)
- **Fuente:** Vladimir Karpukhin, Barlas Oguz, Sewon Min (2020), [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)

### esquema conceptual

La descripción del qué: entidades, atributos y relaciones del dominio, sin decir cómo se guardan. Es el nivel en el que se discute con quien conoce el negocio.

- **Se trabaja en:** [013 — Independencia de datos y los tres niveles de esquema](classes/part-01-fundamentos-datos-sistemas-y-metodo/013-independencia-de-datos-y-niveles-de-esquema/README.md) (parte 01)
- **Ver también:** [esquema físico](#esquema-físico), [vista externa](#vista-externa), [entidad](#entidad)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

### esquema físico

Cómo se materializan realmente los datos: ficheros, páginas, índices, particiones, compresión. Debe poder cambiar —añadir un índice, particionar una tabla— sin que ninguna consulta se reescriba.

- **Se trabaja en:** [013 — Independencia de datos y los tres niveles de esquema](classes/part-01-fundamentos-datos-sistemas-y-metodo/013-independencia-de-datos-y-niveles-de-esquema/README.md) (parte 01)
- **Ver también:** [independencia de datos](#independencia-de-datos), [pagina](#pagina), [índice cubriente](#índice-cubriente)
- **Fuente:** Abraham Silberschatz, Henry F. Korth, S. Sudarshan (2019), [Database System Concepts](https://db-book.com/)

### estadística

Resúmenes que el motor guarda sobre los datos: número de filas, valores distintos, histogramas, valores más comunes. Cuando están obsoletas el optimizador estima mal y elige planes ruinosos, y ese es el primer sitio donde mirar ante una consulta que «de repente» se volvió lenta.

- **Se trabaja en:** [052 — Planes de ejecución: leer EXPLAIN y refutar una hipótesis](classes/part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md) (parte 09)
- **Ver también:** [estimación de cardinalidad](#estimación-de-cardinalidad), [autovacuum](#autovacuum), [optimizador por costos](#optimizador-por-costos)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)

### estampida de caché

Cuando una clave muy consultada expira y miles de peticiones van a la vez a la base de datos a recalcularla. Se mitiga con expiraciones escalonadas, recálculo anticipado o un cerrojo que deja pasar a uno solo.

- **Se trabaja en:** [037 — Clave-valor, caché y expiración: qué se pierde exactamente](classes/part-06-documentos-y-clave-valor/037-clave-valor-cache-y-expiracion/README.md) (parte 06)
- **Ver también:** [TTL](#ttl), [punto caliente](#punto-caliente), [saturación](#saturación)
- **Fuente:** Redis Ltd. (2026), [Redis Documentation](https://redis.io/docs/latest/)

### estimación de cardinalidad

Cuántas filas cree el planificador que devolverá cada paso. Es la entrada de la que depende todo lo demás, y también la parte más frágil: los errores se multiplican al reunir tablas, y una estimación de 1 fila que en realidad son 100 000 explica casi cualquier plan absurdo.

- **Se trabaja en:** [052 — Planes de ejecución: leer EXPLAIN y refutar una hipótesis](classes/part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md) (parte 09)
- **Ver también:** [estadística](#estadística), [selectividad](#selectividad), [costo frente a tiempo](#costo-frente-a-tiempo)
- **Fuente:** P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie, T. G. Price (1979), [Access Path Selection in a Relational Database Management System](https://dl.acm.org/doi/10.1145/582095.582099)

### ETL

Extraer, transformar y luego cargar: la transformación ocurre fuera del destino. Tiene sentido cuando el destino es caro o rígido, o cuando hay que limpiar datos personales antes de que entren.

- **Se trabaja en:** [066 — Integración: ETL, ELT, captura de cambios y el registro como nexo](classes/part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md) (parte 12)
- **Ver también:** [ELT](#elt), [CDC](#cdc), [minimización](#minimización)
- **Fuente:** Joe Reis, Matt Housley (2022), [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)

### evidencia

La salida real de un comando, con su versión y sus parámetros, que respalda una afirmación. Una captura sin comando no es evidencia, porque no se puede repetir.

- **Se trabaja en:** [014 — Entorno reproducible y evidencia comprobable](classes/part-01-fundamentos-datos-sistemas-y-metodo/014-entorno-reproducible-y-evidencia/README.md) (parte 01)
- **Ver también:** [reproducibilidad](#reproducibilidad), [semilla](#semilla), [prueba de restauración](#prueba-de-restauración)
- **Fuente:** Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (2016), [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)

### evidencia reproducible

Mediciones que otra persona puede repetir: comando, versión, datos, semilla y salida. Sin ellas, un número de rendimiento en una defensa es una afirmación, y se le puede oponer cualquier otra.

- **Se trabaja en:** [074 — Proyecto final: diseñar, medir y defender](classes/part-14-arquitectura-y-proyecto-final/074-proyecto-final-disenar-medir-y-defender/README.md) (parte 14)
- **Ver también:** [evidencia](#evidencia), [reproducibilidad](#reproducibilidad), [defensa técnica](#defensa-técnica)
- **Fuente:** Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (2016), [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)

### expandir y contraer

Patrón de migración en tres tiempos: primero se añade lo nuevo sin quitar lo viejo, después se traslada el tráfico y se rellena, y solo cuando nadie usa lo antiguo se elimina. Es lo que permite desplegar esquema y código por separado sin ventana de caída.

- **Se trabaja en:** [059 — Migraciones evolutivas sin ventana de caída](classes/part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md) (parte 11)
- **Ver también:** [doble escritura](#doble-escritura), [relleno](#relleno), [compatibilidad hacia atras](#compatibilidad-hacia-atras)
- **Fuente:** Scott W. Ambler, Pramod J. Sadalage (2006), [Refactoring Databases: Evolutionary Database Design](https://databaserefactoring.com/)

### extensión

Módulo cargable que añade tipos, operadores, índices o funciones a PostgreSQL sin tocar su núcleo: `pgvector`, `PostGIS`, `pg_stat_statements`. Es el mecanismo por el que un motor relacional cubre familias enteras —vectores, geometría, series— sin dejar de ser el mismo motor.

- **Se trabaja en:** [031 — PostgreSQL: tipos, extensiones y modelo de procesos](classes/part-05-motores-relacionales-y-dialectos/031-postgresql-tipos-extensiones-y-procesos/README.md) (parte 05)
- **Ver también:** [multimodelo](#multimodelo), [extensión propietaria](#extensión-propietaria), [tipo compuesto](#tipo-compuesto)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

### extensión propietaria

Sintaxis o función que solo existe en un motor: `LIMIT` frente a `FETCH FIRST`, `ON CONFLICT` frente a `MERGE`, tipos de arreglo, `RETURNING`. Usarlas es legítimo y a menudo correcto; lo que no lo es, es usarlas sin saber que se está atando el proyecto a ese producto.

- **Se trabaja en:** [030 — Portabilidad: qué exige la norma y qué añade cada motor](classes/part-05-motores-relacionales-y-dialectos/030-portabilidad-y-matriz-de-dialectos/README.md) (parte 05)
- **Ver también:** [norma frente a producto](#norma-frente-a-producto), [extensión](#extensión), [matriz de portabilidad](#matriz-de-portabilidad)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

## F

### factor de bloque

Cuántas filas caben en una página. Depende del ancho de la fila, así que columnas anchas que nadie consulta encarecen todas las lecturas de esa tabla, incluidas las que no las piden.

- **Se trabaja en:** [048 — Páginas, filas y buffer: por qué la entrada y salida manda](classes/part-09-almacenamiento-indices-y-planes/048-paginas-filas-y-buffer-pool/README.md) (parte 09)
- **Ver también:** [pagina](#pagina), [localidad](#localidad), [almacenamiento columnar](#almacenamiento-columnar)
- **Fuente:** Alex Petrov (2019), [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/)

### familias de motores

Las formas de organizar datos que estructuran este programa: relacional, documental, clave-valor, grafo, columnas anchas y series temporales, más los índices de búsqueda y los vectoriales como casos especializados. Cada familia optimiza un patrón de acceso y paga en los demás.

- **Se trabaja en:** [010 — El mapa de los motores: seis familias y un criterio](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/010-el-mapa-de-los-motores/README.md) (parte 00)
- **Ver también:** [modelo de agregado](#modelo-de-agregado), [patrón de acceso](#patrón-de-acceso), [multimodelo](#multimodelo)
- **Fuente:** Pramod J. Sadalage, Martin Fowler (2012), [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html)

### fantasma

Repetir una consulta por rango y encontrar filas nuevas que otra transacción insertó. No es un cambio de valor sino de pertenencia al conjunto, y por eso exige bloquear el rango —o usar instantáneas— y no solo las filas leídas.

- **Se trabaja en:** [044 — Anomalías de aislamiento y la crítica a los niveles ANSI](classes/part-08-transacciones-concurrencia-y-recuperacion/044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) (parte 08)
- **Ver también:** [lectura no repetible](#lectura-no-repetible), [2PL](#2pl), [snapshot isolation](#snapshot-isolation)
- **Fuente:** Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil, Patrick O'Neil (1995), [A Critique of ANSI SQL Isolation Levels](https://arxiv.org/abs/cs/0701157)

### fecha ISO-8601

El formato `AAAA-MM-DD` —y `AAAA-MM-DDTHH:MM:SSZ` con hora— que ordena alfabéticamente igual que cronológicamente y no es ambiguo entre día y mes. Guardar fechas como texto libre es la vía directa a datos que no se pueden comparar.

- **Se trabaja en:** [006 — Tipos de datos: por qué un número no es un texto](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/006-tipos-de-datos-un-numero-no-es-un-texto/README.md) (parte 00)
- **Ver también:** [tipo de dato](#tipo-de-dato), [tiempo de evento](#tiempo-de-evento)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### filas afectadas

El número que el motor devuelve tras una escritura. Es la evidencia de que el cambio alcanzó lo previsto: si esperabas una fila y salieron cuatro mil, el `WHERE` estaba mal.

- **Se trabaja en:** [005 — Cambiar datos: INSERT, UPDATE, DELETE y el WHERE que salva](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/005-cambiar-datos-insert-update-delete/README.md) (parte 00)
- **Ver también:** [alcance del cambio](#alcance-del-cambio), [evidencia](#evidencia)
- **Fuente:** SQLite Consortium (2026), [SQLite Documentation](https://sqlite.org/docs.html)

### filtrado

Quedarse con las filas que cumplen un predicado (`WHERE`). En álgebra relacional es la selección: reduce el número de filas, nunca el de columnas.

- **Se trabaja en:** [004 — Leer datos: SELECT, WHERE y ORDER BY](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/004-leer-datos-select-where-y-order-by/README.md) (parte 00)
- **Ver también:** [selección](#selección), [predicado](#predicado), [proyección](#proyección)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### filtro de Bloom

Estructura probabilística compacta que responde «seguro que no está» o «puede que esté». Ahorra abrir SSTables que no contienen la clave; nunca produce falsos negativos, así que es seguro usarla para descartar.

- **Se trabaja en:** [050 — LSM-Tree, compactación y amplificación de escritura](classes/part-09-almacenamiento-indices-y-planes/050-lsm-tree-compactacion-y-amplificacion/README.md) (parte 09)
- **Ver también:** [SSTable](#sstable), [compactación](#compactación), [cuantización](#cuantización)
- **Fuente:** Burton H. Bloom (1970), [Space/Time Trade-offs in Hash Coding with Allowable Errors](https://dl.acm.org/doi/10.1145/362686.362692)

### filtro posterior

Buscar primero y filtrar después. Es simple y tiene un fallo característico: si de los K vecinos ninguno cumple el filtro, la respuesta llega vacía aunque existieran resultados válidos algo más lejos.

- **Se trabaja en:** [070 — Búsqueda híbrida: léxica más vectorial y filtrado por metadatos](classes/part-13-vectores-recuperacion-y-rag/070-busqueda-hibrida-y-filtrado/README.md) (parte 13)
- **Ver también:** [filtro previo](#filtro-previo), [recall](#recall), [búsqueda aproximada](#búsqueda-aproximada)
- **Fuente:** Qdrant (2026), [Qdrant Documentation](https://qdrant.tech/documentation/)

### filtro previo

Aplicar el filtro de metadatos antes de la búsqueda vectorial, de modo que solo se exploren los candidatos admisibles. Conserva el número de resultados pedido, pero puede degradar la navegación del grafo si el filtro es muy selectivo.

- **Se trabaja en:** [070 — Búsqueda híbrida: léxica más vectorial y filtrado por metadatos](classes/part-13-vectores-recuperacion-y-rag/070-busqueda-hibrida-y-filtrado/README.md) (parte 13)
- **Ver también:** [filtro posterior](#filtro-posterior), [HNSW](#hnsw), [selectividad](#selectividad)
- **Fuente:** Qdrant (2026), [Qdrant Documentation](https://qdrant.tech/documentation/)

### formato de almacenamiento

Cómo se disponen los bytes en disco: por filas o por columnas, comprimidos o no, con o sin estadísticas por bloque. Es la decisión que explica la mayor parte de la diferencia de rendimiento entre OLTP y OLAP, muy por encima del lenguaje de consulta.

- **Se trabaja en:** [064 — OLTP frente a OLAP: por qué se separan](classes/part-12-analitica-integracion-y-streaming/064-oltp-frente-a-olap/README.md) (parte 12)
- **Ver también:** [almacenamiento columnar](#almacenamiento-columnar), [compresión](#compresión), [poda de particiones](#poda-de-particiones)
- **Fuente:** DuckDB Foundation (2026), [DuckDB Documentation](https://duckdb.org/docs/)

### fragmentación

Cómo se parte el documento antes de vectorizarlo: por tamaño, por párrafo, por sección, con o sin solape. Es la decisión que más mueve la calidad de un RAG y la que más se toma por defecto sin medirla.

- **Se trabaja en:** [071 — RAG evaluable: medir la recuperación antes que la generación](classes/part-13-vectores-recuperacion-y-rag/071-rag-evaluable/README.md) (parte 13)
- **Ver también:** [recall@k](#recallk), [espacio vectorial](#espacio-vectorial), [trazabilidad de la cita](#trazabilidad-de-la-cita)
- **Fuente:** Patrick Lewis, Ethan Perez, Aleksandra Piktus (2020), [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)

### frontera transaccional

El límite dentro del cual el motor garantiza atomicidad y aislamiento. En los motores de agregado coincide con el agregado: una escritura sobre un documento es atómica, dos sobre documentos distintos ya no. Diseñar el agregado es, por tanto, diseñar dónde termina la garantía.

- **Se trabaja en:** [034 — El agregado como unidad de consistencia](classes/part-06-documentos-y-clave-valor/034-el-agregado-como-unidad-de-consistencia/README.md) (parte 06)
- **Ver también:** [agregado](#agregado), [atomicidad](#atomicidad), [saga](#saga)
- **Fuente:** Pat Helland (2007), [Life beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf)

### fusión de rangos

Combinar dos listas ordenadas —la léxica y la vectorial— en una sola. La fusión recíproca de rangos suma el inverso de la posición en cada lista, y funciona bien precisamente porque no exige que las puntuaciones de ambos sistemas sean comparables entre sí.

- **Se trabaja en:** [070 — Búsqueda híbrida: léxica más vectorial y filtrado por metadatos](classes/part-13-vectores-recuperacion-y-rag/070-busqueda-hibrida-y-filtrado/README.md) (parte 13)
- **Ver también:** [BM25](#bm25), [filtro previo](#filtro-previo), [recall@k](#recallk)
- **Fuente:** OpenSearch Project (2026), [OpenSearch Documentation](https://docs.opensearch.org/latest/)

## G

### gestor de almacenamiento

La capa que traduce filas a páginas en disco y de vuelta, y que sostiene el registro, el buffer y las estructuras de índice. Es donde se decide si el motor es B-Tree o LSM, y con ello su perfil de lectura y escritura.

- **Se trabaja en:** [012 — Arquitectura interna de un gestor, del cliente al disco](classes/part-01-fundamentos-datos-sistemas-y-metodo/012-arquitectura-interna-de-un-gestor/README.md) (parte 01)
- **Ver también:** [pagina](#pagina), [buffer pool](#buffer-pool), [B-Tree](#b-tree), [memtable](#memtable)
- **Fuente:** Alex Petrov (2019), [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/)

### GIN

Índice invertido generalizado de PostgreSQL: indexa los elementos de un valor compuesto —palabras de un texto, claves de un JSONB, elementos de un arreglo—. Es rápido buscando y caro escribiendo, y por eso admite una cola de actualizaciones diferida.

- **Se trabaja en:** [051 — Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes](classes/part-09-almacenamiento-indices-y-planes/051-indices-especializados/README.md) (parte 09)
- **Ver también:** [índice invertido](#índice-invertido), [índice multiclave](#índice-multiclave), [BRIN](#brin)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Indexes](https://www.postgresql.org/docs/current/indexes.html)

### grano

Qué representa exactamente una fila de la tabla de hechos: ¿una venta, una línea de venta, un resumen diario? Es la primera decisión del modelo dimensional y la que no se puede corregir después sin rehacerlo todo.

- **Se trabaja en:** [065 — Modelado dimensional: hechos, dimensiones y cambios lentos](classes/part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) (parte 12)
- **Ver también:** [tabla de hechos](#tabla-de-hechos), [doble conteo](#doble-conteo), [dimensión](#dimensión)
- **Fuente:** Ralph Kimball, Margy Ross (2013), [The Data Warehouse Toolkit](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

## H

### hash consistente

Reparto de claves sobre un anillo de posiciones de modo que añadir o quitar un nodo mueva solo una fracción de los datos, y no obligue a redistribuirlo todo como haría un `hash mod N`. Es la base del rebalanceo en Dynamo y Cassandra.

- **Se trabaja en:** [054 — Particionado, rebalanceo y claves calientes](classes/part-10-distribucion-replica-y-consistencia/054-particionado-rebalanceo-y-claves-calientes/README.md) (parte 10)
- **Ver también:** [partición por rango](#partición-por-rango), [reequilibrio](#reequilibrio), [clave de partición](#clave-de-partición)
- **Fuente:** Giuseppe DeCandia, Deniz Hastorun, Madan Jampani (2007), [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

### HAVING

Filtro que se aplica a los grupos ya formados, después de agregar. `WHERE` descarta filas antes de agrupar y por eso es más barato: la regla es filtrar en `WHERE` todo lo que no dependa del agregado.

- **Se trabaja en:** [027 — Agregación, GROUP BY y HAVING sin duplicar filas](classes/part-04-sql-en-profundidad/027-agregacion-group-by-y-having/README.md) (parte 04)
- **Ver también:** [agrupación](#agrupación), [orden de evaluación](#orden-de-evaluación), [predicado](#predicado)
- **Fuente:** Joe Celko (2014), [Joe Celko's SQL for Smarties: Advanced SQL Programming](https://www.sciencedirect.com/book/9780128007617/joe-celkos-sql-for-smarties)

### HNSW

Grafo navegable de mundo pequeño por capas: las capas altas dan saltos largos y las bajas afinan. Da el mejor compromiso entre recall y latencia de los índices actuales, a costa de un uso de memoria alto y una construcción lenta.

- **Se trabaja en:** [069 — Índices vectoriales aproximados: HNSW, IVF y el recall](classes/part-13-vectores-recuperacion-y-rag/069-indices-vectoriales-aproximados/README.md) (parte 13)
- **Ver también:** [búsqueda aproximada](#búsqueda-aproximada), [cuantización](#cuantización), [recorrido de profundidad variable](#recorrido-de-profundidad-variable)
- **Fuente:** Yu A. Malkov, D. A. Yashunin (2020), [Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs](https://arxiv.org/abs/1603.09320)

## I

### idempotencia

Propiedad de una operación que, repetida con la misma entrada, deja el mismo estado que ejecutarla una vez. Es la única defensa realista contra las redes: en un sistema distribuido no se puede distinguir «no llegó» de «llegó y se perdió la respuesta».

- **Se trabaja en:** [047 — Concurrencia en la aplicación: idempotencia, reintentos y bloqueo optimista](classes/part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md) (parte 08)
- **Ver también:** [clave de idempotencia](#clave-de-idempotencia), [reintento con retroceso](#reintento-con-retroceso), [entrega al menos una vez](#entrega-al-menos-una-vez)
- **Fuente:** Pat Helland (2007), [Life beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf)

### idempotencia de carga

Que reprocesar el mismo lote no duplique ni corrompa el destino, gracias a una clave de negocio y a una operación de fusión. Es la condición para poder relanzar una carga fallida sin auditar a mano lo que había entrado.

- **Se trabaja en:** [066 — Integración: ETL, ELT, captura de cambios y el registro como nexo](classes/part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md) (parte 12)
- **Ver también:** [idempotencia](#idempotencia), [entrega al menos una vez](#entrega-al-menos-una-vez), [relleno](#relleno)
- **Fuente:** dbt Labs (2026), [dbt Documentation](https://docs.getdbt.com/)

### identidad estable

La propiedad de que el identificador de una fila no cambie mientras la fila represente la misma cosa. Es el criterio real del debate entre clave natural y sustituta: no cuál es más elegante, sino cuál sobrevive a los cambios del mundo.

- **Se trabaja en:** [017 — Claves, identidad y el debate natural frente a sustituta](classes/part-02-modelado-conceptual-y-requisitos/017-claves-identidad-natural-y-sustituta/README.md) (parte 02)
- **Ver también:** [clave natural](#clave-natural), [clave sustituta](#clave-sustituta), [reversibilidad](#reversibilidad)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### identificador citado

Nombre de objeto entre comillas dobles —o entre acentos graves en MySQL, entre corchetes en SQL Server—. Al citarlo se vuelve sensible a mayúsculas y se congela tal cual; sin citar, cada motor lo pliega a un caso distinto, y ahí nacen los «la tabla no existe» al cambiar de producto.

- **Se trabaja en:** [032 — MySQL, MariaDB, SQL Server y Oracle: divergencias que rompen código](classes/part-05-motores-relacionales-y-dialectos/032-mysql-sqlserver-y-oracle-divergencias/README.md) (parte 05)
- **Ver también:** [colación](#colación), [matriz de portabilidad](#matriz-de-portabilidad), [norma frente a producto](#norma-frente-a-producto)
- **Fuente:** Oracle (2026), [MySQL Reference Manual](https://dev.mysql.com/doc/)

### identificador dinamico

El caso que los parámetros no cubren: nombres de tabla, de columna o la dirección de un `ORDER BY` no se pueden enviar como valor. La única solución correcta es validarlos contra una lista blanca cerrada, nunca escaparlos a mano.

- **Se trabaja en:** [061 — Inyección SQL y el contrato de parametrización](classes/part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md) (parte 11)
- **Ver también:** [lista blanca](#lista-blanca), [consulta parametrizada](#consulta-parametrizada)
- **Fuente:** OWASP (2026), [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

### incrustación

Guardar los datos relacionados dentro del propio documento. Una sola lectura devuelve todo y la escritura es atómica, a cambio de duplicar el dato si otro documento también lo necesita y de arriesgar un documento que crece sin techo.

- **Se trabaja en:** [035 — Modelado documental: incrustar o referenciar](classes/part-06-documentos-y-clave-valor/035-modelado-documental-incrustar-o-referenciar/README.md) (parte 06)
- **Ver también:** [referencia](#referencia), [crecimiento no acotado](#crecimiento-no-acotado), [agregado](#agregado)
- **Fuente:** MongoDB, Inc. (2026), [MongoDB: Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/)

### independencia de datos

Poder cambiar cómo se guardan los datos sin reescribir las aplicaciones que los consultan. Es la idea central del artículo de Codd de 1970 y la razón de que exista un nivel lógico separado del físico.

- **Se trabaja en:** [011 — Qué resuelve un sistema de bases de datos y qué no](classes/part-01-fundamentos-datos-sistemas-y-metodo/011-que-resuelve-un-sistema-de-bases-de-datos/README.md) (parte 01)
- **Ver también:** [independencia lógica](#independencia-lógica), [esquema físico](#esquema-físico), [vista externa](#vista-externa)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

### independencia lógica

Poder cambiar el esquema conceptual —dividir una tabla, renombrar una columna— sin romper las aplicaciones, apoyándose en vistas que preservan el contrato anterior. Es más difícil de lograr que la independencia física y es la base técnica de las migraciones sin caída.

- **Se trabaja en:** [013 — Independencia de datos y los tres niveles de esquema](classes/part-01-fundamentos-datos-sistemas-y-metodo/013-independencia-de-datos-y-niveles-de-esquema/README.md) (parte 01)
- **Ver también:** [independencia de datos](#independencia-de-datos), [expandir y contraer](#expandir-y-contraer), [vista externa](#vista-externa)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

### índice compuesto

Índice sobre varias claves en un orden concreto. Sirve para las consultas que filtran por un prefijo de esa lista, no para cualquier subconjunto: `(a, b, c)` acelera filtrar por `a` o por `a, b`, pero no por `b` a secas.

- **Se trabaja en:** [036 — Consultas, índices y agregación sobre documentos](classes/part-06-documentos-y-clave-valor/036-consultas-e-indices-sobre-documentos/README.md) (parte 06)
- **Ver también:** [prefijo más a la izquierda](#prefijo-más-a-la-izquierda), [cobertura](#cobertura), [B-Tree](#b-tree)
- **Fuente:** Markus Winand (2012), [SQL Performance Explained](https://use-the-index-luke.com/)

### índice cubriente

Índice que incluye todas las columnas que la consulta necesita, así que el motor responde sin volver a la tabla. En PostgreSQL se construye con `INCLUDE`; su costo es un índice más ancho y más caro de mantener en cada escritura.

- **Se trabaja en:** [049 — B-Tree: estructura, orden de columnas y selectividad](classes/part-09-almacenamiento-indices-y-planes/049-b-tree-orden-de-columnas-y-selectividad/README.md) (parte 09)
- **Ver también:** [cobertura](#cobertura), [costo de mantenimiento](#costo-de-mantenimiento), [índice compuesto](#índice-compuesto)
- **Fuente:** Markus Winand (2012), [SQL Performance Explained](https://use-the-index-luke.com/)

### índice de expresión

Índice sobre el resultado de una función, como `lower(correo)`. Es lo que permite que una búsqueda insensible a mayúsculas use índice, siempre que la consulta escriba la expresión exactamente igual que el índice.

- **Se trabaja en:** [051 — Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes](classes/part-09-almacenamiento-indices-y-planes/051-indices-especializados/README.md) (parte 09)
- **Ver también:** [índice parcial](#índice-parcial), [colación](#colación), [B-Tree](#b-tree)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Indexes](https://www.postgresql.org/docs/current/indexes.html)

### índice invertido

Estructura que va de cada término al listado de documentos que lo contienen —lo contrario de recorrer los documentos buscando el término—. Es la base de todo buscador de texto y la razón de que `LIKE '%algo%'` no sea comparable a una búsqueda de verdad.

- **Se trabaja en:** [041 — Búsqueda de texto: índice invertido, análisis y relevancia](classes/part-07-grafos-columnas-tiempo-y-busqueda/041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) (parte 07)
- **Ver también:** [analizador](#analizador), [BM25](#bm25), [TF-IDF](#tf-idf)
- **Fuente:** OpenSearch Project (2026), [OpenSearch Documentation](https://docs.opensearch.org/latest/)

### índice multiclave

Índice sobre un campo que contiene un arreglo: MongoDB crea una entrada por elemento. Permite buscar dentro del arreglo, y explica por qué el índice de una colección puede tener muchas más entradas que documentos.

- **Se trabaja en:** [036 — Consultas, índices y agregación sobre documentos](classes/part-06-documentos-y-clave-valor/036-consultas-e-indices-sobre-documentos/README.md) (parte 06)
- **Ver también:** [índice compuesto](#índice-compuesto), [GIN](#gin), [incrustación](#incrustación)
- **Fuente:** MongoDB, Inc. (2026), [MongoDB Manual](https://www.mongodb.com/docs/manual/)

### índice parcial

Índice que solo cubre las filas que cumplen un predicado (`WHERE activo`). Ocupa una fracción del total y se mantiene más barato, y encaja perfectamente cuando las consultas siempre filtran por ese mismo estado.

- **Se trabaja en:** [051 — Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes](classes/part-09-almacenamiento-indices-y-planes/051-indices-especializados/README.md) (parte 09)
- **Ver también:** [índice de expresión](#índice-de-expresión), [costo de mantenimiento](#costo-de-mantenimiento), [selectividad](#selectividad)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Indexes](https://www.postgresql.org/docs/current/indexes.html)

### información

El dato más el contexto que fija su significado: de qué es, de cuándo y de quién. «38» es un dato; «la temperatura del sensor 3 a las 10:15 fue 38 °C» es información. Diseñar un esquema es, literalmente, decidir qué contexto se guarda y cuál se pierde para siempre.

- **Se trabaja en:** [001 — Qué es un dato, un registro y una tabla](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md) (parte 00)
- **Ver también:** [dato](#dato), [esquema conceptual](#esquema-conceptual), [alcance](#alcance)
- **Fuente:** William Kent (2012), [Data and Reality](https://technicspub.com/data-and-reality/)

### INSERT

La orden que añade filas. Falla —y debe fallar— si la fila viola una restricción declarada: es el momento en que la integridad declarada demuestra que sirve para algo.

- **Se trabaja en:** [003 — Tu primera base de datos: crear, insertar y leer](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/003-tu-primera-base-de-datos/README.md) (parte 00)
- **Ver también:** [UPDATE](#update), [DELETE](#delete), [integridad declarada](#integridad-declarada)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### instantánea

El conjunto de versiones visibles para una transacción, fijado en un instante. Permite que las lecturas no bloqueen y que dos consultas de la misma transacción vean exactamente lo mismo aunque el mundo cambie alrededor.

- **Se trabaja en:** [045 — Bloqueo en dos fases, MVCC e instantáneas](classes/part-08-transacciones-concurrencia-y-recuperacion/045-bloqueo-en-dos-fases-y-mvcc/README.md) (parte 08)
- **Ver también:** [versión de fila](#versión-de-fila), [snapshot isolation](#snapshot-isolation), [lectura no repetible](#lectura-no-repetible)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html)

### integridad

Que los datos cumplan siempre las reglas del dominio, incluidas las que ninguna aplicación recordó comprobar. El gestor la sostiene con restricciones declaradas y con transacciones.

- **Se trabaja en:** [011 — Qué resuelve un sistema de bases de datos y qué no](classes/part-01-fundamentos-datos-sistemas-y-metodo/011-que-resuelve-un-sistema-de-bases-de-datos/README.md) (parte 01)
- **Ver también:** [integridad declarada](#integridad-declarada), [invariante](#invariante), [consistencia](#consistencia)
- **Fuente:** Abraham Silberschatz, Henry F. Korth, S. Sudarshan (2019), [Database System Concepts](https://db-book.com/)

### integridad de entidad

Regla que exige que ninguna columna de la clave primaria sea nula. Su fundamento no es estético: un identificador desconocido no identifica, y la fila deja de ser referenciable.

- **Se trabaja en:** [023 — Integridad: restricciones, claves foraneas y acciones referenciales](classes/part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md) (parte 03)
- **Ver también:** [clave primaria](#clave-primaria), [NULL](#null), [integridad referencial](#integridad-referencial)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

### integridad declarada

Las reglas del dominio escritas en el esquema —`NOT NULL`, `UNIQUE`, `CHECK`, clave foránea— para que el gestor las imponga a toda aplicación que escriba, no solo a la que recordó comprobarlas. Es la diferencia entre una regla y una esperanza.

- **Se trabaja en:** [002 — Del archivo y la hoja de cálculo a la base de datos](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) (parte 00)
- **Ver también:** [restricción](#restricción), [integridad referencial](#integridad-referencial), [CHECK](#check)
- **Fuente:** Abraham Silberschatz, Henry F. Korth, S. Sudarshan (2019), [Database System Concepts](https://db-book.com/)

### integridad referencial

Regla que exige que todo valor de clave foránea apunte a una fila existente o sea nulo. El gestor la comprueba en cada escritura, lo que la hace inmune a la aplicación que se olvidó de validar.

- **Se trabaja en:** [023 — Integridad: restricciones, claves foraneas y acciones referenciales](classes/part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md) (parte 03)
- **Ver también:** [clave foránea](#clave-foránea), [ON DELETE](#on-delete), [aplazamiento](#aplazamiento)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### interbloqueo

Dos transacciones que se esperan mutuamente porque cada una tiene el cerrojo que la otra necesita. El motor lo detecta y aborta a una; la aplicación debe estar preparada para reintentar, y ordenar siempre los accesos igual reduce la frecuencia.

- **Se trabaja en:** [045 — Bloqueo en dos fases, MVCC e instantáneas](classes/part-08-transacciones-concurrencia-y-recuperacion/045-bloqueo-en-dos-fases-y-mvcc/README.md) (parte 08)
- **Ver también:** [2PL](#2pl), [reintento con retroceso](#reintento-con-retroceso), [bloqueo optimista](#bloqueo-optimista)
- **Fuente:** Jim Gray, Andreas Reuter (1992), [Transaction Processing: Concepts and Techniques](https://www.sciencedirect.com/book/9781558601901/transaction-processing)

### invalidación

Borrar o marcar como obsoleta una entrada de caché cuando cambia el dato de origen. Es el problema difícil de las cachés porque exige que quien escribe en la base sepa qué claves quedaron mentirosas —y normalmente no lo sabe.

- **Se trabaja en:** [037 — Clave-valor, caché y expiración: qué se pierde exactamente](classes/part-06-documentos-y-clave-valor/037-clave-valor-cache-y-expiracion/README.md) (parte 06)
- **Ver también:** [TTL](#ttl), [estampida de caché](#estampida-de-caché), [escritura dual](#escritura-dual)
- **Fuente:** Redis Ltd. (2026), [Redis Documentation](https://redis.io/docs/latest/)

### invariante

Algo que tiene que ser verdad siempre en el sistema: «ningún pedido sin cliente», «el saldo nunca es negativo». Un invariante que no está comprobado por una restricción o una prueba es un deseo.

- **Se trabaja en:** [014 — Entorno reproducible y evidencia comprobable](classes/part-01-fundamentos-datos-sistemas-y-metodo/014-entorno-reproducible-y-evidencia/README.md) (parte 01)
- **Ver también:** [integridad declarada](#integridad-declarada), [CHECK](#check), [evidencia](#evidencia)
- **Fuente:** Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (2016), [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)

### IS DISTINCT FROM

Comparación que trata el nulo como un valor más: dos nulos son iguales y un nulo es distinto de cualquier valor, sin producir `UNKNOWN`. Es la forma correcta de comparar columnas opcionales, por ejemplo al detectar cambios en una migración.

- **Se trabaja en:** [029 — Nulos y lógica de tres valores](classes/part-04-sql-en-profundidad/029-nulos-y-logica-de-tres-valores/README.md) (parte 04)
- **Ver también:** [UNKNOWN](#unknown), [NULL](#null), [IS NULL](#is-null)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

### IS NULL

El único predicado que comprueba ausencia de valor. `= NULL` nunca es cierto —da `UNKNOWN`— porque nada, ni siquiera otro nulo, es igual a lo desconocido.

- **Se trabaja en:** [004 — Leer datos: SELECT, WHERE y ORDER BY](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/004-leer-datos-select-where-y-order-by/README.md) (parte 00)
- **Ver también:** [NULL](#null), [UNKNOWN](#unknown), [IS DISTINCT FROM](#is-distinct-from)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

## L

### latencia frente a consistencia

La mitad de PACELC que CAP ignora: incluso sin particiones hay que elegir entre responder rápido desde una réplica cercana o esperar la coordinación que garantiza el dato más reciente. Es el compromiso que se paga todos los días, no solo el día de la avería.

- **Se trabaja en:** [055 — CAP, PACELC y lo que realmente se elige](classes/part-10-distribucion-replica-y-consistencia/055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) (parte 10)
- **Ver también:** [partición de red](#partición-de-red), [linealizabilidad](#linealizabilidad), [percentil](#percentil)
- **Fuente:** Daniel J. Abadi (2012), [Consistency Tradeoffs in Modern Distributed Database System Design](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf)

### latencia frente a exactitud

El compromiso que gobiernan los parámetros del índice (`ef_search`, `nprobe`): explorar más nodos sube el recall y el tiempo de respuesta. No hay valor correcto universal; se elige midiendo con los datos y las consultas reales.

- **Se trabaja en:** [069 — Índices vectoriales aproximados: HNSW, IVF y el recall](classes/part-13-vectores-recuperacion-y-rag/069-indices-vectoriales-aproximados/README.md) (parte 13)
- **Ver también:** [recall](#recall), [búsqueda aproximada](#búsqueda-aproximada), [percentil](#percentil)
- **Fuente:** Yu A. Malkov, D. A. Yashunin (2020), [Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs](https://arxiv.org/abs/1603.09320)

### lectura de tu propia escritura

Garantía de sesión que asegura que quien acaba de escribir verá su propio cambio, aunque otros aún no. Se implementa dirigiendo al líder las lecturas recientes de ese usuario, o esperando a que la réplica alcance el LSN de su escritura.

- **Se trabaja en:** [053 — Réplica: líder único, multilíder y sin líder](classes/part-10-distribucion-replica-y-consistencia/053-replica-lider-unico-multilider-y-sin-lider/README.md) (parte 10)
- **Ver también:** [retraso de réplica](#retraso-de-réplica), [lectura monotona](#lectura-monotona), [consistencia causal](#consistencia-causal)
- **Fuente:** Werner Vogels (2009), [Eventually Consistent](https://dl.acm.org/doi/10.1145/1435417.1435432)

### lectura monotona

Garantía de sesión que impide retroceder en el tiempo: si ya viste un valor, no volverás a ver uno anterior. Sin ella, alternar entre réplicas con distinto retraso hace que un dato aparezca y desaparezca al recargar.

- **Se trabaja en:** [056 — Modelos de consistencia y garantías de sesión](classes/part-10-distribucion-replica-y-consistencia/056-modelos-de-consistencia-y-garantias-de-sesion/README.md) (parte 10)
- **Ver también:** [lectura de tu propia escritura](#lectura-de-tu-propia-escritura), [retraso de réplica](#retraso-de-réplica), [consistencia causal](#consistencia-causal)
- **Fuente:** Werner Vogels (2009), [Eventually Consistent](https://dl.acm.org/doi/10.1145/1435417.1435432)

### lectura no repetible

Leer la misma fila dos veces dentro de una transacción y obtener valores distintos, porque otra confirmó un cambio en medio. Es lo que `READ COMMITTED` permite y `REPEATABLE READ` impide.

- **Se trabaja en:** [044 — Anomalías de aislamiento y la crítica a los niveles ANSI](classes/part-08-transacciones-concurrencia-y-recuperacion/044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) (parte 08)
- **Ver también:** [fantasma](#fantasma), [instantánea](#instantánea), [aislamiento](#aislamiento)
- **Fuente:** Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil, Patrick O'Neil (1995), [A Critique of ANSI SQL Isolation Levels](https://arxiv.org/abs/cs/0701157)

### lectura secuencial

Leer páginas contiguas, que es órdenes de magnitud más barato por fila que saltar de una a otra. Por eso un recorrido completo puede ganarle a un índice cuando la consulta devuelve una fracción grande de la tabla.

- **Se trabaja en:** [048 — Páginas, filas y buffer: por qué la entrada y salida manda](classes/part-09-almacenamiento-indices-y-planes/048-paginas-filas-y-buffer-pool/README.md) (parte 09)
- **Ver también:** [selectividad](#selectividad), [localidad](#localidad), [poda de particiones](#poda-de-particiones)
- **Fuente:** Alex Petrov (2019), [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/)

### lectura sucia

Leer un dato que otra transacción escribió y todavía no confirmó —y que puede acabar deshaciéndose—. Solo la permite el nivel `READ UNCOMMITTED`, que casi ningún motor usa por defecto.

- **Se trabaja en:** [044 — Anomalías de aislamiento y la crítica a los niveles ANSI](classes/part-08-transacciones-concurrencia-y-recuperacion/044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) (parte 08)
- **Ver también:** [lectura no repetible](#lectura-no-repetible), [aislamiento](#aislamiento), [snapshot isolation](#snapshot-isolation)
- **Fuente:** Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil, Patrick O'Neil (1995), [A Critique of ANSI SQL Isolation Levels](https://arxiv.org/abs/cs/0701157)

### LIMIT

Corta el resultado a las primeras N filas. Sin `ORDER BY` no significa nada estable: «las primeras N» sin criterio de orden es «N cualesquiera».

- **Se trabaja en:** [004 — Leer datos: SELECT, WHERE y ORDER BY](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/004-leer-datos-select-where-y-order-by/README.md) (parte 00)
- **Ver también:** [orden](#orden), [determinismo de orden](#determinismo-de-orden)
- **Fuente:** SQLite Consortium (2026), [SQLite Documentation](https://sqlite.org/docs.html)

### limitación de finalidad

Los datos recogidos para un fin no pueden reutilizarse para otro incompatible sin nueva base legal. Es lo que impide que un correo pedido para la facturación acabe alimentando un modelo de recomendación.

- **Se trabaja en:** [063 — Privacidad, retención y gobierno del dato](classes/part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) (parte 11)
- **Ver también:** [minimización](#minimización), [retención](#retención), [derecho de supresión](#derecho-de-supresión)
- **Fuente:** Union Europea (2016), [Reglamento (UE) 2016/679 - Proteccion de datos personales](https://eur-lex.europa.eu/eli/reg/2016/679/oj)

### límite declarado

Lo que el trabajo explícitamente no demuestra: escala no probada, fallos no simulados, supuestos del entorno. Declararlo aumenta la credibilidad en lugar de restarla, porque distingue lo medido de lo esperado.

- **Se trabaja en:** [074 — Proyecto final: diseñar, medir y defender](classes/part-14-arquitectura-y-proyecto-final/074-proyecto-final-disenar-medir-y-defender/README.md) (parte 14)
- **Ver también:** [alcance](#alcance), [consecuencia](#consecuencia), [evidencia reproducible](#evidencia-reproducible)
- **Fuente:** William Kent (2012), [Data and Reality](https://technicspub.com/data-and-reality/)

### linealizabilidad

La garantía más fuerte para un objeto: el sistema se comporta como si hubiera una sola copia y cada operación ocurriera en un instante entre su inicio y su fin. Es cara porque exige coordinación, y casi ninguna aplicación la necesita para todo.

- **Se trabaja en:** [056 — Modelos de consistencia y garantías de sesión](classes/part-10-distribucion-replica-y-consistencia/056-modelos-de-consistencia-y-garantias-de-sesion/README.md) (parte 10)
- **Ver también:** [consenso](#consenso), [consistencia causal](#consistencia-causal), [disponibilidad](#disponibilidad)
- **Fuente:** Kyle Kingsbury (2026), [Jepsen: Consistency Models](https://jepsen.io/consistency)

### lista blanca

Permitir solo lo que está explícitamente enumerado y rechazar todo lo demás. Se prefiere a la lista negra porque no hay que anticipar todas las formas de atacar, solo todas las formas válidas de usar.

- **Se trabaja en:** [061 — Inyección SQL y el contrato de parametrización](classes/part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md) (parte 11)
- **Ver también:** [identificador dinamico](#identificador-dinamico), [defensa en profundidad](#defensa-en-profundidad), [CHECK](#check)
- **Fuente:** OWASP (2021), [OWASP Top 10](https://owasp.org/Top10/)

### localidad

Que los datos que se usan juntos estén guardados juntos. Es la propiedad que convierte muchas lecturas lógicas en pocas lecturas físicas, y el motivo por el que el orden físico de una tabla —y la clave de agrupamiento— importa tanto.

- **Se trabaja en:** [048 — Páginas, filas y buffer: por qué la entrada y salida manda](classes/part-09-almacenamiento-indices-y-planes/048-paginas-filas-y-buffer-pool/README.md) (parte 09)
- **Ver también:** [pagina](#pagina), [lectura secuencial](#lectura-secuencial), [clave de agrupamiento](#clave-de-agrupamiento)
- **Fuente:** Joseph M. Hellerstein, Michael Stonebraker, James Hamilton (2007), [Architecture of a Database System](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf)

### LSN

Número de secuencia del registro: identifica cada entrada del WAL en orden y se estampa en la página que modifica. Permite saber, página por página, si un cambio ya está aplicado —y por eso rehacer se puede repetir sin efectos secundarios.

- **Se trabaja en:** [046 — Registro anticipado y recuperación: WAL y ARIES](classes/part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md) (parte 08)
- **Ver también:** [WAL](#wal), [rehacer](#rehacer), [retraso de réplica](#retraso-de-réplica)
- **Fuente:** C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz (1992), [ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging](https://dl.acm.org/doi/10.1145/128765.128770)

## M

### marca de agua

Estimación del sistema sobre hasta qué tiempo de evento ya llegó todo. Es lo que permite cerrar una ventana y emitir el resultado; siempre es una apuesta, y por eso hay que decidir explícitamente qué se hace con lo que llega tarde.

- **Se trabaja en:** [067 — Streaming: tiempo de evento, ventanas y semántica de entrega](classes/part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md) (parte 12)
- **Ver también:** [tiempo de evento](#tiempo-de-evento), [ventana](#ventana), [entrega al menos una vez](#entrega-al-menos-una-vez)
- **Fuente:** Tyler Akidau, Slava Chernyak, Reuven Lax (2018), [Streaming Systems](https://www.oreilly.com/library/view/streaming-systems/9781491983867/)

### marco

El `ROWS`/`RANGE BETWEEN` que define qué filas de la partición entran en el cálculo de cada fila. Su valor por defecto no es «toda la partición» cuando hay `ORDER BY`, y esa sutileza cambia el resultado de una suma acumulada.

- **Se trabaja en:** [028 — CTE, subconsultas y funciones de ventana](classes/part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md) (parte 04)
- **Ver también:** [partición de ventana](#partición-de-ventana), [determinismo de orden](#determinismo-de-orden)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### matriz de portabilidad

Tabla que registra, para cada construcción usada, si es de norma y cómo la escribe cada motor del proyecto. Convierte la portabilidad en un artefacto revisable en lugar de en una intención declarada en la primera reunión.

- **Se trabaja en:** [030 — Portabilidad: qué exige la norma y qué añade cada motor](classes/part-05-motores-relacionales-y-dialectos/030-portabilidad-y-matriz-de-dialectos/README.md) (parte 05)
- **Ver también:** [norma frente a producto](#norma-frente-a-producto), [extensión propietaria](#extensión-propietaria), [identificador citado](#identificador-citado)
- **Fuente:** Anthony Molinaro, Robert de Graaf (2020), [SQL Cookbook](https://www.oreilly.com/library/view/sql-cookbook-2nd/9781492077435/)

### memtable

Estructura ordenada en memoria donde un motor LSM acumula las escrituras antes de volcarlas a disco. Convierte escrituras aleatorias en secuenciales, que es la razón de que los LSM absorban mucha más carga de escritura que un B-Tree.

- **Se trabaja en:** [050 — LSM-Tree, compactación y amplificación de escritura](classes/part-09-almacenamiento-indices-y-planes/050-lsm-tree-compactacion-y-amplificacion/README.md) (parte 09)
- **Ver también:** [SSTable](#sstable), [compactación](#compactación), [WAL](#wal)
- **Fuente:** Patrick O'Neil, Edward Cheng, Dieter Gawlick, Elizabeth O'Neil (1996), [The Log-Structured Merge-Tree (LSM-Tree)](https://link.springer.com/article/10.1007/s002360050048)

### minimización

Recoger solo los datos personales necesarios para la finalidad declarada. Es la medida de protección más eficaz que existe, porque el dato que no se guarda no se filtra, no hay que cifrarlo ni hay que borrarlo después.

- **Se trabaja en:** [063 — Privacidad, retención y gobierno del dato](classes/part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) (parte 11)
- **Ver también:** [limitación de finalidad](#limitación-de-finalidad), [seudonimización](#seudonimización), [alcance](#alcance)
- **Fuente:** Union Europea (2016), [Reglamento (UE) 2016/679 - Proteccion de datos personales](https://eur-lex.europa.eu/eli/reg/2016/679/oj)

### modelo de agregado

Cómo agrupa el motor los datos que lee y escribe de una vez. El relacional trabaja con filas que se recomponen por reunión; los motores de agregado guardan la unidad completa junta y evitan la reunión, a cambio de duplicar.

- **Se trabaja en:** [010 — El mapa de los motores: seis familias y un criterio](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/010-el-mapa-de-los-motores/README.md) (parte 00)
- **Ver también:** [agregado](#agregado), [frontera transaccional](#frontera-transaccional), [incrustación](#incrustación)
- **Fuente:** Pramod J. Sadalage, Martin Fowler (2012), [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html)

### modo estricto

Ajuste que decide si el motor rechaza un dato inválido o lo convierte en silencio. MySQL sin modo estricto trunca cadenas y transforma fechas imposibles en ceros; el mismo `INSERT` que en PostgreSQL falla, allí «funciona» y corrompe.

- **Se trabaja en:** [032 — MySQL, MariaDB, SQL Server y Oracle: divergencias que rompen código](classes/part-05-motores-relacionales-y-dialectos/032-mysql-sqlserver-y-oracle-divergencias/README.md) (parte 05)
- **Ver también:** [afinidad de tipos](#afinidad-de-tipos), [cadena vacia frente a nulo](#cadena-vacia-frente-a-nulo), [integridad declarada](#integridad-declarada)
- **Fuente:** Oracle (2026), [MySQL Reference Manual](https://dev.mysql.com/doc/)

### motor embebido

Base de datos que corre dentro del proceso de la aplicación, sin servidor ni puerto: SQLite, DuckDB. Elimina el costo de operación y la latencia de red, a cambio de no poder servir a varias máquinas.

- **Se trabaja en:** [009 — Cuándo NO necesitas una base de datos](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/009-cuando-no-necesitas-una-base-de-datos/README.md) (parte 00)
- **Ver también:** [costo de operación](#costo-de-operación), [tipado dinamico](#tipado-dinamico), [almacenamiento columnar](#almacenamiento-columnar)
- **Fuente:** SQLite Consortium (2026), [SQLite Documentation](https://sqlite.org/docs.html)

### MRR

Rango recíproco medio: la media de 1 dividido por la posición del primer resultado relevante. Premia colocar arriba la respuesta correcta, que es justo lo que importa cuando solo se van a leer los tres primeros fragmentos.

- **Se trabaja en:** [071 — RAG evaluable: medir la recuperación antes que la generación](classes/part-13-vectores-recuperacion-y-rag/071-rag-evaluable/README.md) (parte 13)
- **Ver también:** [recall@k](#recallk), [precisión@k](#precisiónk), [fusión de rangos](#fusión-de-rangos)
- **Fuente:** Vladimir Karpukhin, Barlas Oguz, Sewon Min (2020), [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)

### multimodelo

Motor que soporta varias familias a la vez —PostgreSQL con JSONB, vectores y búsqueda de texto—. Reduce el número de sistemas que hay que operar; el riesgo es dar por hecho que hacer varias cosas equivale a hacerlas todas bien.

- **Se trabaja en:** [010 — El mapa de los motores: seis familias y un criterio](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/010-el-mapa-de-los-motores/README.md) (parte 00)
- **Ver también:** [familias de motores](#familias-de-motores), [complejidad añadida](#complejidad-añadida)
- **Fuente:** solid IT gmbh (2026), [DB-Engines Ranking](https://db-engines.com/en/ranking)

### multiplicación de filas

Efecto de reunir con una tabla que tiene varias filas por clave: cada fila del lado uno aparece repetida. Es la causa del doble conteo cuando después se suma, y la razón de que agregar antes de reunir sea a menudo la corrección.

- **Se trabaja en:** [026 — Reuniones: interna, externa, semi y anti](classes/part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md) (parte 04)
- **Ver también:** [doble conteo](#doble-conteo), [semirreunion](#semirreunion), [agrupación](#agrupación)
- **Fuente:** Markus Winand (2012), [SQL Performance Explained](https://use-the-index-luke.com/)

## N

### nodo

Vértice del grafo de propiedades: una cosa con etiquetas y con pares clave-valor propios. Equivale a una fila, con la diferencia de que sus conexiones son parte de la estructura y no se recomponen por reunión.

- **Se trabaja en:** [038 — Grafos de propiedades y los recorridos que SQL hace mal](classes/part-07-grafos-columnas-tiempo-y-busqueda/038-grafos-de-propiedades-y-recorridos/README.md) (parte 07)
- **Ver también:** [arista](#arista), [recorrido de profundidad variable](#recorrido-de-profundidad-variable), [entidad](#entidad)
- **Fuente:** Ian Robinson, Jim Webber, Emil Eifrem (2015), [Graph Databases](https://neo4j.com/graph-databases-book/)

### norma frente a producto

La distinción entre lo que exige ISO/IEC 9075 y lo que cada motor añade por su cuenta. Ningún producto implementa la norma entera y todos la extienden; saber en qué lado está cada línea de tu código es lo que decide si una migración de motor cuesta un día o un trimestre.

- **Se trabaja en:** [030 — Portabilidad: qué exige la norma y qué añade cada motor](classes/part-05-motores-relacionales-y-dialectos/030-portabilidad-y-matriz-de-dialectos/README.md) (parte 05)
- **Ver también:** [matriz de portabilidad](#matriz-de-portabilidad), [extensión propietaria](#extensión-propietaria)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### normalización

Escalar cada vector a longitud 1. Hace equivalentes coseno y producto interno y permite usar el índice más rápido sin cambiar el orden de los resultados; es un paso rutinario que conviene declarar, porque mezclar vectores normalizados y sin normalizar arruina la búsqueda.

- **Se trabaja en:** [068 — Embeddings y métricas de distancia: qué significa parecido](classes/part-13-vectores-recuperacion-y-rag/068-embeddings-y-metricas-de-distancia/README.md) (parte 13)
- **Ver también:** [coseno](#coseno), [producto interno](#producto-interno), [cuantización](#cuantización)
- **Fuente:** Andrew Kane (2026), [pgvector](https://github.com/pgvector/pgvector)

### NOT IN con nulos

Trampa clásica: si la lista o la subconsulta de un `NOT IN` contiene un solo nulo, el predicado nunca es verdadero y el resultado es vacío. `NOT EXISTS` no tiene ese problema y es la sustitución recomendada.

- **Se trabaja en:** [029 — Nulos y lógica de tres valores](classes/part-04-sql-en-profundidad/029-nulos-y-logica-de-tres-valores/README.md) (parte 04)
- **Ver también:** [antirreunion](#antirreunion), [UNKNOWN](#unknown), [NULL](#null)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### NULL

Marca de ausencia de valor: no es cero, ni cadena vacía, ni «desconocido» codificado a mano. Introduce una lógica de tres valores que cambia el resultado de comparaciones, agregados y `NOT IN`.

- **Se trabaja en:** [003 — Tu primera base de datos: crear, insertar y leer](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/003-tu-primera-base-de-datos/README.md) (parte 00)
- **Ver también:** [UNKNOWN](#unknown), [IS NULL](#is-null), [IS DISTINCT FROM](#is-distinct-from)
- **Fuente:** E. F. Codd (1979), [Extending the Database Relational Model to Capture More Meaning](https://dl.acm.org/doi/10.1145/320107.320109)

## O

### ON DELETE

Acción referencial que declara qué pasa con las filas hijas cuando se borra la padre: `RESTRICT` lo impide, `CASCADE` las borra, `SET NULL` las desvincula. Es una decisión de dominio, no técnica: `CASCADE` sobre datos contables borra historia.

- **Se trabaja en:** [023 — Integridad: restricciones, claves foraneas y acciones referenciales](classes/part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md) (parte 03)
- **Ver también:** [clave foránea](#clave-foránea), [integridad referencial](#integridad-referencial), [entidad débil](#entidad-débil)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### optimizador por costos

Componente que enumera planes equivalentes y elige el de menor costo estimado a partir de estadísticas. Desde el artículo de Selinger de 1979 el principio no ha cambiado: el motor no ejecuta lo que escribiste, ejecuta lo que calculó que es más barato.

- **Se trabaja en:** [052 — Planes de ejecución: leer EXPLAIN y refutar una hipótesis](classes/part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md) (parte 09)
- **Ver también:** [estadística](#estadística), [estimación de cardinalidad](#estimación-de-cardinalidad), [equivalencia](#equivalencia)
- **Fuente:** P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie, T. G. Price (1979), [Access Path Selection in a Relational Database Management System](https://dl.acm.org/doi/10.1145/582095.582099)

### orden

El resultado de una consulta es un conjunto: no tiene orden hasta que se declara `ORDER BY`. Confiar en el orden «que salió» es un error que sobrevive en pruebas y falla en producción el día que cambia el plan.

- **Se trabaja en:** [004 — Leer datos: SELECT, WHERE y ORDER BY](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/004-leer-datos-select-where-y-order-by/README.md) (parte 00)
- **Ver también:** [determinismo de orden](#determinismo-de-orden), [colación](#colación), [LIMIT](#limit)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### orden de evaluación

El orden lógico en que SQL procesa una consulta: `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY`, `LIMIT`. Explica por qué no se puede usar un alias del `SELECT` en el `WHERE` y por qué `HAVING` filtra grupos y `WHERE` filtra filas.

- **Se trabaja en:** [025 — SELECT: filtrado, proyección y orden con semántica precisa](classes/part-04-sql-en-profundidad/025-select-filtrado-proyeccion-y-orden/README.md) (parte 04)
- **Ver también:** [HAVING](#having), [agrupación](#agrupación), [predicado](#predicado)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

## P

### pagina

La unidad mínima de lectura y escritura en disco, típicamente de 4 a 16 KB. El motor nunca lee «una fila»: lee la página que la contiene, y de ahí que quepan más filas por página sea una optimización real.

- **Se trabaja en:** [048 — Páginas, filas y buffer: por qué la entrada y salida manda](classes/part-09-almacenamiento-indices-y-planes/048-paginas-filas-y-buffer-pool/README.md) (parte 09)
- **Ver también:** [factor de bloque](#factor-de-bloque), [buffer pool](#buffer-pool), [localidad](#localidad)
- **Fuente:** Alex Petrov (2019), [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/)

### partición de red

Situación en la que dos grupos de nodos siguen vivos pero no pueden comunicarse. No es un fallo hipotético: es lo que ocurre con un cable, un cortafuegos mal aplicado o una latencia lo bastante alta como para que los tiempos de espera venzan.

- **Se trabaja en:** [055 — CAP, PACELC y lo que realmente se elige](classes/part-10-distribucion-replica-y-consistencia/055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) (parte 10)
- **Ver también:** [disponibilidad](#disponibilidad), [consenso](#consenso), [latencia frente a consistencia](#latencia-frente-a-consistencia)
- **Fuente:** Seth Gilbert, Nancy Lynch (2002), [Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services](https://dl.acm.org/doi/10.1145/564585.564601)

### partición de ventana

El `PARTITION BY` de una función de ventana: divide las filas en grupos para calcular el agregado dentro de cada uno, pero sin colapsarlas. Es la diferencia esencial con `GROUP BY`: la ventana conserva el detalle y añade el cálculo al lado.

- **Se trabaja en:** [028 — CTE, subconsultas y funciones de ventana](classes/part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md) (parte 04)
- **Ver también:** [marco](#marco), [agrupación](#agrupación), [CTE](#cte)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

### partición por rango

Repartir por intervalos ordenados de la clave. Permite consultas por rango eficientes, a costa de generar puntos calientes cuando las escrituras se concentran al final del rango —el caso típico de una clave temporal.

- **Se trabaja en:** [054 — Particionado, rebalanceo y claves calientes](classes/part-10-distribucion-replica-y-consistencia/054-particionado-rebalanceo-y-claves-calientes/README.md) (parte 10)
- **Ver también:** [hash consistente](#hash-consistente), [punto caliente](#punto-caliente), [poda de particiones](#poda-de-particiones)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### participación total

Cuando toda instancia de una entidad debe participar obligatoriamente en la relación —todo pedido tiene un cliente—. Se traduce en `NOT NULL` sobre la clave foránea; la participación parcial admite el nulo.

- **Se trabaja en:** [016 — Entidad-relación, cardinalidad y participación](classes/part-02-modelado-conceptual-y-requisitos/016-entidad-relacion-cardinalidad-y-participacion/README.md) (parte 02)
- **Ver también:** [cardinalidad](#cardinalidad), [NULL](#null), [integridad referencial](#integridad-referencial)
- **Fuente:** Ramez Elmasri, Shamkant B. Navathe (2015), [Fundamentals of Database Systems](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003546)

### patrón de acceso

La lista concreta de consultas y escrituras que el sistema tendrá que servir, con su frecuencia y su latencia aceptable. Es el dato de entrada del diseño: sin él, elegir modelo o índice es adivinar.

- **Se trabaja en:** [010 — El mapa de los motores: seis familias y un criterio](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/010-el-mapa-de-los-motores/README.md) (parte 00)
- **Ver también:** [carga de trabajo](#carga-de-trabajo), [patrón de lectura](#patrón-de-lectura), [desnormalización por consulta](#desnormalización-por-consulta)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### patrón de extensión

Familia de soluciones para el crecimiento no acotado: partir el arreglo en cubos de tamaño fijo, guardar solo los N últimos elementos incrustados y el resto en otra colección, o separar los campos grandes en un documento satélite.

- **Se trabaja en:** [035 — Modelado documental: incrustar o referenciar](classes/part-06-documentos-y-clave-valor/035-modelado-documental-incrustar-o-referenciar/README.md) (parte 06)
- **Ver también:** [crecimiento no acotado](#crecimiento-no-acotado), [incrustación](#incrustación), [submuestreo](#submuestreo)
- **Fuente:** MongoDB, Inc. (2026), [MongoDB: Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/)

### patrón de lectura

Qué se consulta, con qué filtros y con qué frecuencia. Es el argumento que justifica desnormalizar: sin una lectura dominante medida, duplicar datos es solo asumir el costo sin cobrar el beneficio.

- **Se trabaja en:** [019 — Desnormalización deliberada y patrones de acceso](classes/part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md) (parte 02)
- **Ver también:** [patrón de acceso](#patrón-de-acceso), [desnormalización por consulta](#desnormalización-por-consulta), [redundancia controlada](#redundancia-controlada)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### percentil

El valor por debajo del cual queda un porcentaje de las observaciones. La media oculta el problema; el p99 lo enseña. Y si una petición de usuario abre veinte consultas, casi todos los usuarios tocarán al menos una de la cola lenta.

- **Se trabaja en:** [062 — Observabilidad, objetivos de servicio y capacidad](classes/part-11-operacion-seguridad-y-gobierno/062-observabilidad-slo-y-capacidad/README.md) (parte 11)
- **Ver también:** [presupuesto de error](#presupuesto-de-error), [consulta lenta](#consulta-lenta), [latencia frente a consistencia](#latencia-frente-a-consistencia)
- **Fuente:** Jeffrey Dean, Luiz Andre Barroso (2013), [The Tail at Scale](https://dl.acm.org/doi/10.1145/2408776.2408794)

### persistencia

Que el dato siga existiendo cuando el proceso que lo escribió ya no está. Es el requisito mínimo de una base de datos y la única de sus funciones que un archivo también cumple.

- **Se trabaja en:** [011 — Qué resuelve un sistema de bases de datos y qué no](classes/part-01-fundamentos-datos-sistemas-y-metodo/011-que-resuelve-un-sistema-de-bases-de-datos/README.md) (parte 01)
- **Ver también:** [durabilidad](#durabilidad), [WAL](#wal)
- **Fuente:** Abraham Silberschatz, Henry F. Korth, S. Sudarshan (2019), [Database System Concepts](https://db-book.com/)

### plan de evolución

Qué se haría al multiplicar por diez el volumen, y qué señal indicaría que ha llegado el momento. Convierte una arquitectura en una decisión con fecha de revisión en lugar de en una apuesta permanente.

- **Se trabaja en:** [074 — Proyecto final: diseñar, medir y defender](classes/part-14-arquitectura-y-proyecto-final/074-proyecto-final-disenar-medir-y-defender/README.md) (parte 14)
- **Ver también:** [reversibilidad](#reversibilidad), [ADR](#adr), [carga de trabajo](#carga-de-trabajo)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### planificador

Decide *cómo* ejecutar la consulta: qué índice usar, en qué orden reunir las tablas, con qué algoritmo. Elige por costo estimado a partir de estadísticas, no por el orden en que está escrita la consulta.

- **Se trabaja en:** [012 — Arquitectura interna de un gestor, del cliente al disco](classes/part-01-fundamentos-datos-sistemas-y-metodo/012-arquitectura-interna-de-un-gestor/README.md) (parte 01)
- **Ver también:** [optimizador por costos](#optimizador-por-costos), [estadística](#estadística), [estimación de cardinalidad](#estimación-de-cardinalidad)
- **Fuente:** P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie, T. G. Price (1979), [Access Path Selection in a Relational Database Management System](https://dl.acm.org/doi/10.1145/582095.582099)

### poda de particiones

Descartar ficheros o bloques enteros sin abrirlos, gracias a los mínimos y máximos guardados en sus metadatos. Es lo que hace que consultar un día concreto sobre un histórico de diez años cueste casi lo mismo que consultar ese día solo.

- **Se trabaja en:** [042 — Analítica columnar: por qué el formato cambia el orden de magnitud](classes/part-07-grafos-columnas-tiempo-y-busqueda/042-analitica-columnar-y-vectorizacion/README.md) (parte 07)
- **Ver también:** [BRIN](#brin), [partición por rango](#partición-por-rango), [compresión](#compresión)
- **Fuente:** DuckDB Foundation (2026), [DuckDB Documentation](https://duckdb.org/docs/)

### precisión y exhaustividad

Precisión: qué proporción de lo devuelto era relevante. Exhaustividad (o *recall*): qué proporción de lo relevante se devolvió. Casi siempre se compensan entre sí, y por eso una búsqueda solo puede evaluarse fijando cuál de las dos importa en ese caso.

- **Se trabaja en:** [041 — Búsqueda de texto: índice invertido, análisis y relevancia](classes/part-07-grafos-columnas-tiempo-y-busqueda/041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) (parte 07)
- **Ver también:** [recall](#recall), [recall@k](#recallk), [precisión@k](#precisiónk)
- **Fuente:** Stephen Robertson, Hugo Zaragoza (2009), [The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)

### precisión@k

Qué proporción de los K devueltos era relevante. Importa porque el contexto es finito y caro: llenar la ventana de ruido desplaza a los fragmentos que sí servían.

- **Se trabaja en:** [071 — RAG evaluable: medir la recuperación antes que la generación](classes/part-13-vectores-recuperacion-y-rag/071-rag-evaluable/README.md) (parte 13)
- **Ver también:** [recall@k](#recallk), [MRR](#mrr), [precisión y exhaustividad](#precisión-y-exhaustividad)
- **Fuente:** Stephen Robertson, Hugo Zaragoza (2009), [The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)

### predicado

Expresión lógica que se evalúa a verdadero, falso o desconocido para cada fila. En SQL solo pasan el filtro las filas cuyo predicado es verdadero: `UNKNOWN` se descarta igual que `FALSE`, y ahí empiezan los resultados sorprendentes con nulos.

- **Se trabaja en:** [025 — SELECT: filtrado, proyección y orden con semántica precisa](classes/part-04-sql-en-profundidad/025-select-filtrado-proyeccion-y-orden/README.md) (parte 04)
- **Ver también:** [UNKNOWN](#unknown), [filtrado](#filtrado), [selección](#selección)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### prefijo más a la izquierda

Un índice sobre `(a, b, c)` solo sirve para filtros que fijan `a`, o `a` y `b`, o los tres —nunca para `b` solo—. Es la regla que decide el orden de las columnas de un índice compuesto y la que explica por qué «tengo el índice y no lo usa».

- **Se trabaja en:** [049 — B-Tree: estructura, orden de columnas y selectividad](classes/part-09-almacenamiento-indices-y-planes/049-b-tree-orden-de-columnas-y-selectividad/README.md) (parte 09)
- **Ver también:** [índice compuesto](#índice-compuesto), [B-Tree](#b-tree), [clave compuesta](#clave-compuesta)
- **Fuente:** Markus Winand (2012), [SQL Performance Explained](https://use-the-index-luke.com/)

### presupuesto de error

Lo que resta entre el objetivo de servicio y el 100 %: con un SLO de 99,9 % se dispone de unos 43 minutos de fallo al mes. Convierte la fiabilidad en una cantidad que se gasta, y da una regla objetiva para decidir si se despliega o se estabiliza.

- **Se trabaja en:** [062 — Observabilidad, objetivos de servicio y capacidad](classes/part-11-operacion-seguridad-y-gobierno/062-observabilidad-slo-y-capacidad/README.md) (parte 11)
- **Ver también:** [percentil](#percentil), [RTO](#rto), [disponibilidad](#disponibilidad)
- **Fuente:** Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (2016), [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)

### privilegio mínimo

Cada identidad recibe exactamente los permisos que necesita para su función y ninguno más. La comprobación práctica es incómoda y reveladora: si la aplicación se conecta como propietaria del esquema, no hay privilegio mínimo.

- **Se trabaja en:** [060 — Control de acceso: privilegio mínimo, roles y seguridad por fila](classes/part-11-operacion-seguridad-y-gobierno/060-control-de-acceso-y-seguridad-por-fila/README.md) (parte 11)
- **Ver también:** [rol](#rol), [separación de funciones](#separación-de-funciones), [defensa en profundidad](#defensa-en-profundidad)
- **Fuente:** NIST (2020), [NIST SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)

### proceso por conexión

Modelo de PostgreSQL: cada conexión es un proceso del sistema operativo con su propia memoria. Es robusto —una caída no arrastra a las demás— y caro: por eso un agrupador de conexiones deja de ser un lujo a partir de unos cientos de clientes.

- **Se trabaja en:** [031 — PostgreSQL: tipos, extensiones y modelo de procesos](classes/part-05-motores-relacionales-y-dialectos/031-postgresql-tipos-extensiones-y-procesos/README.md) (parte 05)
- **Ver también:** [autovacuum](#autovacuum), [saturación](#saturación), [buffer pool](#buffer-pool)
- **Fuente:** Egor Rogov (2022), [PostgreSQL 14 Internals](https://postgrespro.com/community/books/internals)

### producto cartesiano

Operador × que combina cada tupla de una relación con todas las de otra. Casi nunca se quiere: aparecer en un plan de ejecución suele indicar una condición de reunión olvidada y una explosión de filas.

- **Se trabaja en:** [021 — Álgebra relacional: selección, proyección, producto y reunión](classes/part-03-modelo-relacional-y-algebra/021-algebra-relacional-operadores/README.md) (parte 03)
- **Ver también:** [reunión natural](#reunión-natural), [multiplicación de filas](#multiplicación-de-filas), [reunión interna](#reunión-interna)
- **Fuente:** Raghu Ramakrishnan, Johannes Gehrke (2002), [Database Management Systems](https://pages.cs.wisc.edu/~dbbook/)

### producto interno

Métrica que sí tiene en cuenta la magnitud, útil cuando el modelo codifica intensidad en la norma del vector. Sobre vectores normalizados es equivalente al coseno, y de ahí que normalizar simplifique la elección.

- **Se trabaja en:** [068 — Embeddings y métricas de distancia: qué significa parecido](classes/part-13-vectores-recuperacion-y-rag/068-embeddings-y-metricas-de-distancia/README.md) (parte 13)
- **Ver también:** [coseno](#coseno), [normalización](#normalización), [espacio vectorial](#espacio-vectorial)
- **Fuente:** Jeff Johnson, Matthijs Douze, Herve Jegou (2019), [Billion-scale Similarity Search with GPUs](https://arxiv.org/abs/1702.08734)

### proyección

Quedarse con un subconjunto de columnas. Reduce el ancho de la fila, no su cantidad —salvo que se eliminen los duplicados resultantes con `DISTINCT`, cosa que SQL no hace por defecto y el álgebra sí.

- **Se trabaja en:** [004 — Leer datos: SELECT, WHERE y ORDER BY](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/004-leer-datos-select-where-y-order-by/README.md) (parte 00)
- **Ver también:** [selección](#selección), [relación](#relación), [cierre](#cierre)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### prueba de restauración

Restaurar la copia en un entorno limpio, comprobar la integridad de los datos y medir cuánto tardó. Un respaldo que nunca se ha restaurado no es un respaldo: es un fichero con nombre esperanzador.

- **Se trabaja en:** [058 — Respaldo y restauración: solo cuenta lo que se ha restaurado](classes/part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md) (parte 11)
- **Ver también:** [RTO](#rto), [evidencia](#evidencia), [recuperación a un punto en el tiempo](#recuperación-a-un-punto-en-el-tiempo)
- **Fuente:** Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (2016), [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)

### punto caliente

Partición que recibe una parte desproporcionada del tráfico: la celebridad con millones de seguidores, la fecha de hoy, el cliente que factura el 40 %. Ninguna cantidad de nodos ayuda mientras el reparto siga concentrando ahí.

- **Se trabaja en:** [054 — Particionado, rebalanceo y claves calientes](classes/part-10-distribucion-replica-y-consistencia/054-particionado-rebalanceo-y-claves-calientes/README.md) (parte 10)
- **Ver también:** [clave de partición](#clave-de-partición), [reequilibrio](#reequilibrio), [cardinalidad de etiquetas](#cardinalidad-de-etiquetas)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### punto de control

Marca periódica que fija hasta dónde están ya volcadas a disco las páginas modificadas. Acorta la recuperación, porque tras una caída solo hay que releer el registro desde el último punto de control y no desde el principio de los tiempos.

- **Se trabaja en:** [046 — Registro anticipado y recuperación: WAL y ARIES](classes/part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md) (parte 08)
- **Ver también:** [WAL](#wal), [rehacer](#rehacer), [recuperación](#recuperación)
- **Fuente:** C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz (1992), [ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging](https://dl.acm.org/doi/10.1145/128765.128770)

## Q

### quórum

Regla de los sistemas sin líder: si las escrituras van a W réplicas, las lecturas consultan R, y `W + R > N`, entonces toda lectura toca al menos una réplica con el último valor. Permite ajustar el compromiso entre latencia y frescura por operación.

- **Se trabaja en:** [053 — Réplica: líder único, multilíder y sin líder](classes/part-10-distribucion-replica-y-consistencia/053-replica-lider-unico-multilider-y-sin-lider/README.md) (parte 10)
- **Ver también:** [replicación sincrónica](#replicación-sincrónica), [convergencia](#convergencia), [consenso](#consenso)
- **Fuente:** Giuseppe DeCandia, Deniz Hastorun, Madan Jampani (2007), [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

## R

### recall

Qué proporción de los verdaderos K vecinos devolvió el índice aproximado. Es la métrica que hay que medir contra una búsqueda exhaustiva antes de dar por buena una configuración; sin ese número, «funciona» significa «devolvió algo».

- **Se trabaja en:** [069 — Índices vectoriales aproximados: HNSW, IVF y el recall](classes/part-13-vectores-recuperacion-y-rag/069-indices-vectoriales-aproximados/README.md) (parte 13)
- **Ver también:** [búsqueda aproximada](#búsqueda-aproximada), [recall@k](#recallk), [precisión y exhaustividad](#precisión-y-exhaustividad)
- **Fuente:** Jeff Johnson, Matthijs Douze, Herve Jegou (2019), [Billion-scale Similarity Search with GPUs](https://arxiv.org/abs/1702.08734)

### recall@k

Qué proporción de los documentos relevantes aparece entre los K primeros resultados. Es la métrica que gobierna un sistema RAG: si el fragmento correcto no entra en el contexto, ningún modelo de lenguaje podrá responder bien.

- **Se trabaja en:** [071 — RAG evaluable: medir la recuperación antes que la generación](classes/part-13-vectores-recuperacion-y-rag/071-rag-evaluable/README.md) (parte 13)
- **Ver también:** [precisión@k](#precisiónk), [MRR](#mrr), [recall](#recall)
- **Fuente:** Patrick Lewis, Ethan Perez, Aleksandra Piktus (2020), [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)

### recorrido de profundidad variable

Consulta del tipo «amigos de amigos hasta cinco saltos» o «cualquier camino entre A y B». En SQL exige una CTE recursiva y una reunión por nivel; en un motor de grafos el costo depende del subgrafo recorrido, no del tamaño total del grafo.

- **Se trabaja en:** [038 — Grafos de propiedades y los recorridos que SQL hace mal](classes/part-07-grafos-columnas-tiempo-y-busqueda/038-grafos-de-propiedades-y-recorridos/README.md) (parte 07)
- **Ver también:** [recursión](#recursión), [reunión sin índice](#reunión-sin-índice), [arista](#arista)
- **Fuente:** Neo4j, Inc. (2026), [Neo4j Documentation](https://neo4j.com/docs/)

### recuperación

Volver a un estado correcto después de una caída, descartando lo no confirmado y rehaciendo lo confirmado. Es lo que distingue una base de datos de un archivo que se corrompió a medio escribir.

- **Se trabaja en:** [011 — Qué resuelve un sistema de bases de datos y qué no](classes/part-01-fundamentos-datos-sistemas-y-metodo/011-que-resuelve-un-sistema-de-bases-de-datos/README.md) (parte 01)
- **Ver también:** [WAL](#wal), [rehacer](#rehacer), [deshacer](#deshacer), [punto de control](#punto-de-control)
- **Fuente:** Jim Gray, Andreas Reuter (1992), [Transaction Processing: Concepts and Techniques](https://www.sciencedirect.com/book/9781558601901/transaction-processing)

### recuperación a un punto en el tiempo

Restaurar una copia base y reaplicar el registro archivado hasta un instante concreto, justo antes del `DELETE` sin `WHERE`. Exige que el archivado del registro esté activo y verificado desde antes del incidente.

- **Se trabaja en:** [058 — Respaldo y restauración: solo cuenta lo que se ha restaurado](classes/part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md) (parte 11)
- **Ver también:** [WAL](#wal), [RPO](#rpo), [prueba de restauración](#prueba-de-restauración)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Backup and Restore](https://www.postgresql.org/docs/current/backup.html)

### recursión

`WITH RECURSIVE`: una CTE que se referencia a sí misma para recorrer jerarquías y grafos —organigramas, listas de materiales, caminos—. Necesita siempre una condición de parada; sin ella el motor recorre hasta agotar la memoria.

- **Se trabaja en:** [028 — CTE, subconsultas y funciones de ventana](classes/part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md) (parte 04)
- **Ver también:** [CTE](#cte), [recorrido de profundidad variable](#recorrido-de-profundidad-variable), [división](#división)
- **Fuente:** Joe Celko (2014), [Joe Celko's SQL for Smarties: Advanced SQL Programming](https://www.sciencedirect.com/book/9780128007617/joe-celkos-sql-for-smarties)

### redundancia controlada

Duplicar un dato a propósito, sabiendo dónde está la copia y quién la mantiene al día. Se distingue de la redundancia accidental en que existe un mecanismo declarado de sincronización y un costo de escritura aceptado.

- **Se trabaja en:** [019 — Desnormalización deliberada y patrones de acceso](classes/part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md) (parte 02)
- **Ver también:** [costo de escritura](#costo-de-escritura), [desnormalización por consulta](#desnormalización-por-consulta), [anomalía de actualización](#anomalía-de-actualización)
- **Fuente:** Pramod J. Sadalage, Martin Fowler (2012), [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html)

### reequilibrio

Mover particiones entre nodos al cambiar la capacidad del clúster. La práctica recomendada es fijar de antemano muchas más particiones que nodos y mover particiones enteras, en lugar de recalcular la asignación de cada clave.

- **Se trabaja en:** [054 — Particionado, rebalanceo y claves calientes](classes/part-10-distribucion-replica-y-consistencia/054-particionado-rebalanceo-y-claves-calientes/README.md) (parte 10)
- **Ver también:** [hash consistente](#hash-consistente), [punto caliente](#punto-caliente), [clave de partición](#clave-de-partición)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### referencia

Guardar el identificador del documento relacionado en lugar de su contenido. Evita la duplicación y el crecimiento no acotado, a cambio de una segunda consulta —o de un `$lookup`— que el motor no optimiza como un `JOIN` relacional.

- **Se trabaja en:** [035 — Modelado documental: incrustar o referenciar](classes/part-06-documentos-y-clave-valor/035-modelado-documental-incrustar-o-referenciar/README.md) (parte 06)
- **Ver también:** [incrustación](#incrustación), [clave foránea](#clave-foránea), [canalización de agregación](#canalización-de-agregación)
- **Fuente:** MongoDB, Inc. (2026), [MongoDB: Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/)

### registro

Una fila: un hecho completo sobre una cosa, ni medio hecho ni dos. La regla práctica para detectar el error más común: si para leer un campo hay que partirlo por comas, ese registro esconde varios hechos y viola la primera forma normal.

- **Se trabaja en:** [001 — Qué es un dato, un registro y una tabla](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md) (parte 00)
- **Ver también:** [campo](#campo), [tabla](#tabla), [dependencia funcional](#dependencia-funcional)
- **Fuente:** Michael J. Hernandez (2020), [Database Design for Mere Mortals](https://www.informit.com/store/database-design-for-mere-mortals-a-hands-on-guide-to-9780136788041)

### regla de negocio

Una afirmación del dominio que el sistema debe respetar: «un estudiante no puede inscribirse dos veces en el mismo curso». Cada regla acaba en una restricción, en un índice único o en una prueba; la que no acaba en ninguna de las tres es solo una frase en un documento.

- **Se trabaja en:** [015 — De requisitos ambiguos a entidades defendibles](classes/part-02-modelado-conceptual-y-requisitos/015-de-requisitos-a-entidades/README.md) (parte 02)
- **Ver también:** [invariante](#invariante), [integridad declarada](#integridad-declarada), [diccionario de datos](#diccionario-de-datos)
- **Fuente:** Michael J. Hernandez (2020), [Database Design for Mere Mortals](https://www.informit.com/store/database-design-for-mere-mortals-a-hands-on-guide-to-9780136788041)

### rehacer

Fase de la recuperación que reaplica desde el registro todo lo confirmado que aún no había llegado a las páginas de datos. ARIES la ejecuta antes de deshacer y de forma que repetirla sea inofensiva, lo que permite recuperarse de una caída ocurrida durante la recuperación.

- **Se trabaja en:** [046 — Registro anticipado y recuperación: WAL y ARIES](classes/part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md) (parte 08)
- **Ver también:** [deshacer](#deshacer), [WAL](#wal), [punto de control](#punto-de-control), [idempotencia](#idempotencia)
- **Fuente:** C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz (1992), [ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging](https://dl.acm.org/doi/10.1145/128765.128770)

### reintento con retroceso

Reintentar tras un fallo esperando cada vez más tiempo, con una componente aleatoria. El retroceso evita hundir un sistema que ya está en apuros y la aleatoriedad evita que todos los clientes vuelvan sincronizados a la vez.

- **Se trabaja en:** [047 — Concurrencia en la aplicación: idempotencia, reintentos y bloqueo optimista](classes/part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md) (parte 08)
- **Ver también:** [idempotencia](#idempotencia), [interbloqueo](#interbloqueo), [saturación](#saturación), [estampida de caché](#estampida-de-caché)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### relación

En el modelo de Codd, un conjunto de tuplas sobre unos dominios dados. Al ser conjunto no tiene orden ni duplicados —dos propiedades que SQL no respeta, y de ahí nacen la mitad de las sorpresas del lenguaje.

- **Se trabaja en:** [020 — La relación como conjunto: tuplas, dominios y acceso por valor](classes/part-03-modelo-relacional-y-algebra/020-la-relacion-como-conjunto/README.md) (parte 03)
- **Ver también:** [tupla](#tupla), [dominio](#dominio), [cierre](#cierre)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

### relleno

Copiar el histórico a la estructura nueva, por lotes y de forma reanudable, para no bloquear la tabla ni saturar el registro. Debe ser idempotente: se va a interrumpir y habrá que relanzarlo.

- **Se trabaja en:** [059 — Migraciones evolutivas sin ventana de caída](classes/part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md) (parte 11)
- **Ver también:** [doble escritura](#doble-escritura), [idempotencia](#idempotencia), [expandir y contraer](#expandir-y-contraer)
- **Fuente:** Scott W. Ambler, Pramod J. Sadalage (2006), [Refactoring Databases: Evolutionary Database Design](https://databaserefactoring.com/)

### replicación sincrónica

El líder no confirma la escritura hasta que al menos una réplica la ha recibido. Garantiza que no se pierda al caer el líder, a cambio de que la latencia del cliente incluya la de la réplica más lenta y de que una réplica caída pueda detener las escrituras.

- **Se trabaja en:** [053 — Réplica: líder único, multilíder y sin líder](classes/part-10-distribucion-replica-y-consistencia/053-replica-lider-unico-multilider-y-sin-lider/README.md) (parte 10)
- **Ver también:** [retraso de réplica](#retraso-de-réplica), [quórum](#quórum), [RPO](#rpo)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### reproducibilidad

Que otra persona, en otra máquina, obtenga el mismo resultado con las instrucciones dadas. Exige fijar versión del motor, datos de partida y semilla; sin eso, una medición es una anécdota.

- **Se trabaja en:** [014 — Entorno reproducible y evidencia comprobable](classes/part-01-fundamentos-datos-sistemas-y-metodo/014-entorno-reproducible-y-evidencia/README.md) (parte 01)
- **Ver también:** [semilla](#semilla), [contenedor](#contenedor), [evidencia](#evidencia)
- **Fuente:** Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (2016), [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)

### restricción

Regla declarada en el esquema que el motor impone siempre: `NOT NULL`, `UNIQUE`, `CHECK`, `PRIMARY KEY`, `FOREIGN KEY`. Su ventaja sobre la validación en la aplicación es que no depende de que alguien se acuerde.

- **Se trabaja en:** [024 — DDL: el esquema como contrato ejecutable](classes/part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md) (parte 04)
- **Ver también:** [integridad declarada](#integridad-declarada), [CHECK](#check), [invariante](#invariante)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### retención

Cuánto tiempo se conservan los datos antes de borrarlos automáticamente. En series temporales es una decisión de capacidad; en datos personales es además una obligación legal, y las dos deben coincidir en la misma política escrita.

- **Se trabaja en:** [040 — Series temporales: cardinalidad, retención y agregados continuos](classes/part-07-grafos-columnas-tiempo-y-busqueda/040-series-temporales-cardinalidad-y-retencion/README.md) (parte 07)
- **Ver también:** [submuestreo](#submuestreo), [limitación de finalidad](#limitación-de-finalidad), [derecho de supresión](#derecho-de-supresión)
- **Fuente:** Timescale, Inc. (2026), [TimescaleDB Documentation](https://docs.timescale.com/)

### retraso de réplica

La distancia temporal entre lo que ya está en el líder y lo que la réplica ha aplicado. Con replicación asíncrona es inevitable, y es la causa directa de que un usuario guarde algo y al recargar no lo vea.

- **Se trabaja en:** [053 — Réplica: líder único, multilíder y sin líder](classes/part-10-distribucion-replica-y-consistencia/053-replica-lider-unico-multilider-y-sin-lider/README.md) (parte 10)
- **Ver también:** [lectura de tu propia escritura](#lectura-de-tu-propia-escritura), [LSN](#lsn), [lectura monotona](#lectura-monotona)
- **Fuente:** Martin Kleppmann (2017), [Designing Data-Intensive Applications](https://dataintensive.net/)

### reunión

Combinar filas de dos tablas emparejándolas por un valor común, normalmente clave foránea contra clave primaria. Es la operación que permite normalizar sin perder la capacidad de ver el hecho completo.

- **Se trabaja en:** [008 — Dos tablas y una relación: la clave foránea](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/008-dos-tablas-y-una-relacion/README.md) (parte 00)
- **Ver también:** [reunión interna](#reunión-interna), [reunión natural](#reunión-natural), [clave foránea](#clave-foránea)
- **Fuente:** Raghu Ramakrishnan, Johannes Gehrke (2002), [Database Management Systems](https://pages.cs.wisc.edu/~dbbook/)

### reunión externa

`LEFT`, `RIGHT` o `FULL OUTER JOIN`: conserva las filas sin pareja y rellena con nulos. Cuidado con poner en el `WHERE` una condición sobre la tabla externa: la convierte de nuevo en interna.

- **Se trabaja en:** [026 — Reuniones: interna, externa, semi y anti](classes/part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md) (parte 04)
- **Ver también:** [reunión interna](#reunión-interna), [NULL](#null), [antirreunion](#antirreunion)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### reunión interna

`INNER JOIN`: devuelve solo los pares que casan. Las filas sin pareja desaparecen, y ese descarte silencioso es la causa más frecuente de informes con menos filas de las esperadas.

- **Se trabaja en:** [026 — Reuniones: interna, externa, semi y anti](classes/part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md) (parte 04)
- **Ver también:** [reunión externa](#reunión-externa), [reunión](#reunión), [multiplicación de filas](#multiplicación-de-filas)
- **Fuente:** Markus Winand (2012), [SQL Performance Explained](https://use-the-index-luke.com/)

### reunión natural

Reunión que empareja por todos los atributos con el mismo nombre y deja una sola copia de cada uno. Elegante en el álgebra y peligrosa en SQL: si alguien añade una columna homónima, la consulta cambia de significado sin avisar.

- **Se trabaja en:** [021 — Álgebra relacional: selección, proyección, producto y reunión](classes/part-03-modelo-relacional-y-algebra/021-algebra-relacional-operadores/README.md) (parte 03)
- **Ver también:** [reunión interna](#reunión-interna), [producto cartesiano](#producto-cartesiano), [descomposición sin pérdida](#descomposición-sin-pérdida)
- **Fuente:** Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom (2008), [Database Systems: The Complete Book](http://infolab.stanford.edu/~ullman/dscb.html)

### reunión sin índice

Propiedad de los motores de grafos nativos: cada nodo guarda las direcciones físicas de sus vecinos, así que pasar de uno a otro no consulta ningún índice. Es la razón técnica de que el recorrido profundo escale donde el `JOIN` repetido se degrada.

- **Se trabaja en:** [038 — Grafos de propiedades y los recorridos que SQL hace mal](classes/part-07-grafos-columnas-tiempo-y-busqueda/038-grafos-de-propiedades-y-recorridos/README.md) (parte 07)
- **Ver también:** [arista](#arista), [recorrido de profundidad variable](#recorrido-de-profundidad-variable), [B-Tree](#b-tree)
- **Fuente:** Ian Robinson, Jim Webber, Emil Eifrem (2015), [Graph Databases](https://neo4j.com/graph-databases-book/)

### reversibilidad

Cuánto cuesta deshacer la decisión si resulta equivocada. Es el criterio que decide cuánto análisis merece: una decisión barata de revertir se prueba, una cara se estudia antes.

- **Se trabaja en:** [073 — Registro de decisiones de arquitectura y costo total](classes/part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md) (parte 14)
- **Ver también:** [ADR](#adr), [costo total de propiedad](#costo-total-de-propiedad), [compatibilidad hacia atras](#compatibilidad-hacia-atras)
- **Fuente:** Joe Reis, Matt Housley (2022), [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)

### rol

Agrupación de privilegios que se concede a personas o a aplicaciones. Permite razonar sobre permisos por función en lugar de por individuo, y revocar el acceso de alguien sin tener que auditar cada objeto.

- **Se trabaja en:** [060 — Control de acceso: privilegio mínimo, roles y seguridad por fila](classes/part-11-operacion-seguridad-y-gobierno/060-control-de-acceso-y-seguridad-por-fila/README.md) (parte 11)
- **Ver también:** [privilegio mínimo](#privilegio-mínimo), [separación de funciones](#separación-de-funciones), [vista externa](#vista-externa)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)

### RPO

Objetivo de punto de recuperación: cuántos datos se acepta perder, medido en tiempo. Un RPO de cinco minutos obliga a archivar el registro al menos cada cinco minutos; si no está escrito y probado, el RPO real es «el que salga».

- **Se trabaja en:** [058 — Respaldo y restauración: solo cuenta lo que se ha restaurado](classes/part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md) (parte 11)
- **Ver también:** [RTO](#rto), [recuperación a un punto en el tiempo](#recuperación-a-un-punto-en-el-tiempo), [durabilidad configurable](#durabilidad-configurable)
- **Fuente:** Laine Campbell, Charity Majors (2017), [Database Reliability Engineering](https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/)

### RTO

Objetivo de tiempo de recuperación: cuánto se acepta estar caído. Se mide restaurando de verdad y cronometrando, no estimando; casi siempre resulta ser varias veces mayor de lo que el equipo suponía.

- **Se trabaja en:** [058 — Respaldo y restauración: solo cuenta lo que se ha restaurado](classes/part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md) (parte 11)
- **Ver también:** [RPO](#rpo), [prueba de restauración](#prueba-de-restauración), [presupuesto de error](#presupuesto-de-error)
- **Fuente:** Laine Campbell, Charity Majors (2017), [Database Reliability Engineering](https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/)

## S

### saga

Secuencia de transacciones locales, cada una con su compensación, que sustituye a una transacción distribuida. Renuncia al aislamiento —los estados intermedios se ven— a cambio de no bloquear recursos entre servicios.

- **Se trabaja en:** [057 — Consenso y transacciones distribuidas: Raft, 2PC y sagas](classes/part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) (parte 10)
- **Ver también:** [compensación](#compensación), [commit en dos fases](#commit-en-dos-fases), [frontera transaccional](#frontera-transaccional)
- **Fuente:** Pat Helland (2007), [Life beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf)

### saturación

Cuán lleno está el recurso más escaso: conexiones, entrada y salida, memoria, CPU. Es la señal que anticipa el incidente, porque la latencia se dispara de forma no lineal justo antes de que el recurso se agote.

- **Se trabaja en:** [062 — Observabilidad, objetivos de servicio y capacidad](classes/part-11-operacion-seguridad-y-gobierno/062-observabilidad-slo-y-capacidad/README.md) (parte 11)
- **Ver también:** [percentil](#percentil), [proceso por conexión](#proceso-por-conexión), [estampida de caché](#estampida-de-caché)
- **Fuente:** Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (2016), [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)

### seguridad de expresión

Condición que garantiza que una fórmula del cálculo devuelve un resultado finito. `{t | ¬P(t)}` no es segura: «todo lo que no cumple P» incluye el universo entero. Es la razón de que SQL obligue a nombrar siempre un `FROM`.

- **Se trabaja en:** [022 — Cálculo relacional y su equivalencia con el álgebra](classes/part-03-modelo-relacional-y-algebra/022-calculo-relacional-y-equivalencia/README.md) (parte 03)
- **Ver también:** [cálculo de tuplas](#cálculo-de-tuplas), [dominio](#dominio)
- **Fuente:** Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom (2008), [Database Systems: The Complete Book](http://infolab.stanford.edu/~ullman/dscb.html)

### seguridad por fila

Políticas que el motor añade automáticamente a cada consulta para que un usuario solo vea las filas que le corresponden. La ventaja sobre filtrar en la aplicación es que no hay consulta que se pueda olvidar del filtro.

- **Se trabaja en:** [060 — Control de acceso: privilegio mínimo, roles y seguridad por fila](classes/part-11-operacion-seguridad-y-gobierno/060-control-de-acceso-y-seguridad-por-fila/README.md) (parte 11)
- **Ver también:** [vista externa](#vista-externa), [privilegio mínimo](#privilegio-mínimo), [seudonimización](#seudonimización)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)

### selección

Operador σ del álgebra: se queda con las tuplas que cumplen un predicado. Es el `WHERE` de SQL y el primero que el optimizador intenta empujar hacia abajo en el plan, para descartar filas antes de reunirlas.

- **Se trabaja en:** [021 — Álgebra relacional: selección, proyección, producto y reunión](classes/part-03-modelo-relacional-y-algebra/021-algebra-relacional-operadores/README.md) (parte 03)
- **Ver también:** [filtrado](#filtrado), [proyección](#proyección), [predicado](#predicado)
- **Fuente:** Raghu Ramakrishnan, Johannes Gehrke (2002), [Database Management Systems](https://pages.cs.wisc.edu/~dbbook/)

### SELECT

La orden de lectura. Nunca modifica datos; describe el conjunto que se quiere y deja al motor la estrategia para producirlo.

- **Se trabaja en:** [003 — Tu primera base de datos: crear, insertar y leer](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/003-tu-primera-base-de-datos/README.md) (parte 00)
- **Ver también:** [filtrado](#filtrado), [proyección](#proyección), [consulta declarativa](#consulta-declarativa)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### selectividad

Qué fracción de la tabla devuelve un predicado. Un índice compensa cuando la selectividad es alta —pocas filas—; con predicados poco selectivos, el recorrido secuencial gana y el planificador lo elige a propósito.

- **Se trabaja en:** [049 — B-Tree: estructura, orden de columnas y selectividad](classes/part-09-almacenamiento-indices-y-planes/049-b-tree-orden-de-columnas-y-selectividad/README.md) (parte 09)
- **Ver también:** [estimación de cardinalidad](#estimación-de-cardinalidad), [lectura secuencial](#lectura-secuencial), [estadística](#estadística)
- **Fuente:** Markus Winand (2012), [SQL Performance Explained](https://use-the-index-luke.com/)

### semilla

El número que fija la secuencia de un generador pseudoaleatorio. Declararla convierte un conjunto de datos «aleatorio» en uno reproducible, que es la condición para poder comparar dos ejecuciones.

- **Se trabaja en:** [014 — Entorno reproducible y evidencia comprobable](classes/part-01-fundamentos-datos-sistemas-y-metodo/014-entorno-reproducible-y-evidencia/README.md) (parte 01)
- **Ver también:** [reproducibilidad](#reproducibilidad), [evidencia](#evidencia)
- **Fuente:** Python Software Foundation (2026), [Python: sqlite3](https://docs.python.org/3/library/sqlite3.html)

### semirreunion

Filtrar una tabla por la existencia de una pareja, sin traer columnas de la otra ni multiplicar filas: `WHERE EXISTS (…)` o `IN (…)`. Es lo que casi siempre se quería cuando se escribió un `JOIN` seguido de `DISTINCT`.

- **Se trabaja en:** [026 — Reuniones: interna, externa, semi y anti](classes/part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md) (parte 04)
- **Ver también:** [antirreunion](#antirreunion), [multiplicación de filas](#multiplicación-de-filas), [reunión interna](#reunión-interna)
- **Fuente:** Anthony Molinaro, Robert de Graaf (2020), [SQL Cookbook](https://www.oreilly.com/library/view/sql-cookbook-2nd/9781492077435/)

### separación de funciones

Que quien desarrolla no sea quien despliega en producción, y que quien opera no pueda borrar sus propias huellas de auditoría. Es un control organizativo antes que técnico, y sin él el registro de auditoría no prueba nada.

- **Se trabaja en:** [060 — Control de acceso: privilegio mínimo, roles y seguridad por fila](classes/part-11-operacion-seguridad-y-gobierno/060-control-de-acceso-y-seguridad-por-fila/README.md) (parte 11)
- **Ver también:** [privilegio mínimo](#privilegio-mínimo), [rol](#rol), [defensa en profundidad](#defensa-en-profundidad)
- **Fuente:** NIST (2020), [NIST SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)

### sesgo de escritura

Dos transacciones leen el mismo conjunto, cada una decide que puede escribir, y juntas rompen un invariante que ninguna rompía por separado —los dos médicos de guardia que se dan de baja a la vez—. Snapshot isolation lo permite; hace falta serializable o un bloqueo explícito.

- **Se trabaja en:** [044 — Anomalías de aislamiento y la crítica a los niveles ANSI](classes/part-08-transacciones-concurrencia-y-recuperacion/044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) (parte 08)
- **Ver también:** [snapshot isolation](#snapshot-isolation), [invariante](#invariante), [bloqueo optimista](#bloqueo-optimista)
- **Fuente:** Atul Adya (1999), [Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions](http://pmg.csail.mit.edu/papers/adya-phd.pdf)

### seudonimización

Sustituir los identificadores directos por referencias, guardando por separado la tabla que permite revertirlo. Reduce el riesgo pero no convierte el dato en anónimo: mientras exista la clave, sigue siendo dato personal.

- **Se trabaja en:** [063 — Privacidad, retención y gobierno del dato](classes/part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) (parte 11)
- **Ver también:** [minimización](#minimización), [seguridad por fila](#seguridad-por-fila), [derecho de supresión](#derecho-de-supresión)
- **Fuente:** Union Europea (2016), [Reglamento (UE) 2016/679 - Proteccion de datos personales](https://eur-lex.europa.eu/eli/reg/2016/679/oj)

### snapshot isolation

Cada transacción ve una fotografía coherente de la base tomada al empezar. Elimina lecturas sucias, no repetibles y fantasmas, pero no el sesgo de escritura; es el nivel que PostgreSQL llama `REPEATABLE READ`.

- **Se trabaja en:** [044 — Anomalías de aislamiento y la crítica a los niveles ANSI](classes/part-08-transacciones-concurrencia-y-recuperacion/044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) (parte 08)
- **Ver también:** [instantánea](#instantánea), [versión de fila](#versión-de-fila), [sesgo de escritura](#sesgo-de-escritura)
- **Fuente:** Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil, Patrick O'Neil (1995), [A Critique of ANSI SQL Isolation Levels](https://arxiv.org/abs/cs/0701157)

### SSTable

Fichero ordenado e inmutable resultante de volcar una memtable. Al ser inmutable no se actualiza: los cambios posteriores viven en ficheros más nuevos, y por eso una lectura puede tener que consultar varios niveles.

- **Se trabaja en:** [050 — LSM-Tree, compactación y amplificación de escritura](classes/part-09-almacenamiento-indices-y-planes/050-lsm-tree-compactacion-y-amplificacion/README.md) (parte 09)
- **Ver también:** [memtable](#memtable), [compactación](#compactación), [filtro de Bloom](#filtro-de-bloom)
- **Fuente:** Patrick O'Neil, Edward Cheng, Dieter Gawlick, Elizabeth O'Neil (1996), [The Log-Structured Merge-Tree (LSM-Tree)](https://link.springer.com/article/10.1007/s002360050048)

### subconsulta correlacionada

Subconsulta que referencia una columna de la consulta externa y por tanto se evalúa en función de cada fila. Conceptualmente es un bucle; los optimizadores modernos suelen convertirla en una reunión, pero conviene comprobarlo en el plan y no suponerlo.

- **Se trabaja en:** [028 — CTE, subconsultas y funciones de ventana](classes/part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md) (parte 04)
- **Ver también:** [CTE](#cte), [semirreunion](#semirreunion), [optimizador por costos](#optimizador-por-costos)
- **Fuente:** Anthony Molinaro, Robert de Graaf (2020), [SQL Cookbook](https://www.oreilly.com/library/view/sql-cookbook-2nd/9781492077435/)

### submuestreo

Reducir la resolución de los datos antiguos: guardar cada segundo la última hora, cada minuto la última semana, cada hora el último año. Es cómo se sostiene un histórico largo sin que el tamaño crezca de forma lineal para siempre.

- **Se trabaja en:** [040 — Series temporales: cardinalidad, retención y agregados continuos](classes/part-07-grafos-columnas-tiempo-y-busqueda/040-series-temporales-cardinalidad-y-retencion/README.md) (parte 07)
- **Ver también:** [agregado continuo](#agregado-continuo), [retención](#retención), [compresión](#compresión)
- **Fuente:** Timescale, Inc. (2026), [TimescaleDB Documentation](https://docs.timescale.com/)

## T

### tabla

Un conjunto de registros con exactamente la misma forma: mismas columnas, mismos tipos, mismo significado por columna. Esa uniformidad es lo que permite consultar sin saber de antemano qué hay dentro.

- **Se trabaja en:** [001 — Qué es un dato, un registro y una tabla](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md) (parte 00)
- **Ver también:** [relación](#relación), [registro](#registro), [esquema conceptual](#esquema-conceptual)
- **Fuente:** Ramez Elmasri, Shamkant B. Navathe (2015), [Fundamentals of Database Systems](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003546)

### tabla de hechos

Tabla central del modelo dimensional: una fila por evento medible, con sus métricas numéricas y sus claves a las dimensiones. Crece indefinidamente y se consulta siempre agregando.

- **Se trabaja en:** [065 — Modelado dimensional: hechos, dimensiones y cambios lentos](classes/part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) (parte 12)
- **Ver también:** [dimensión](#dimensión), [grano](#grano), [actividad](#actividad)
- **Fuente:** Ralph Kimball, Margy Ross (2013), [The Data Warehouse Toolkit](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

### tabla de relación

Tabla intermedia que resuelve una relación muchos-a-muchos guardando pares de claves foráneas. Deja de ser «solo técnica» en cuanto la relación tiene atributos propios —fecha de inscripción, nota— y pasa a ser una entidad de pleno derecho.

- **Se trabaja en:** [008 — Dos tablas y una relación: la clave foránea](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/008-dos-tablas-y-una-relacion/README.md) (parte 00)
- **Ver también:** [clave compuesta](#clave-compuesta), [atributo de relación](#atributo-de-relación), [cardinalidad](#cardinalidad)
- **Fuente:** Ramez Elmasri, Shamkant B. Navathe (2015), [Fundamentals of Database Systems](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003546)

### TF-IDF

Peso clásico de un término: crece con su frecuencia en el documento (TF) y decrece con el número de documentos en que aparece (IDF). Formaliza la intuición de que «el» no distingue nada y «hipervisor» distingue mucho.

- **Se trabaja en:** [041 — Búsqueda de texto: índice invertido, análisis y relevancia](classes/part-07-grafos-columnas-tiempo-y-busqueda/041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) (parte 07)
- **Ver también:** [BM25](#bm25), [índice invertido](#índice-invertido), [precisión y exhaustividad](#precisión-y-exhaustividad)
- **Fuente:** Stephen Robertson, Hugo Zaragoza (2009), [The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)

### tiempo de evento

El instante en que el hecho ocurrió, frente al de proceso, que es cuando el sistema lo vio. Son distintos —un móvil sin cobertura envía tres horas después— y agrupar por el segundo cuando se quería el primero produce informes silenciosamente falsos.

- **Se trabaja en:** [067 — Streaming: tiempo de evento, ventanas y semántica de entrega](classes/part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md) (parte 12)
- **Ver también:** [marca de agua](#marca-de-agua), [ventana](#ventana), [fecha ISO-8601](#fecha-iso-8601)
- **Fuente:** Tyler Akidau, Slava Chernyak, Reuven Lax (2018), [Streaming Systems](https://www.oreilly.com/library/view/streaming-systems/9781491983867/)

### tipado dinamico

En SQLite el tipo pertenece al valor, no a la columna: la declaración es una sugerencia (afinidad) y no una barrera. Cómodo para prototipar, peligroso para datos que otro sistema leerá; desde la versión 3.37 existen las tablas `STRICT` para recuperar el rigor.

- **Se trabaja en:** [033 — SQLite y DuckDB: motores embebidos, transaccional frente a analítico](classes/part-05-motores-relacionales-y-dialectos/033-sqlite-y-duckdb-motores-embebidos/README.md) (parte 05)
- **Ver también:** [afinidad de tipos](#afinidad-de-tipos), [modo estricto](#modo-estricto), [motor embebido](#motor-embebido)
- **Fuente:** SQLite Consortium (2026), [SQLite Documentation](https://sqlite.org/docs.html)

### tipo

El conjunto de valores posibles de un campo más las operaciones válidas sobre ellos. Declarar el tipo correcto delega en el motor la mitad de las validaciones que, si no, hay que escribir a mano en cada aplicación.

- **Se trabaja en:** [006 — Tipos de datos: por qué un número no es un texto](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/006-tipos-de-datos-un-numero-no-es-un-texto/README.md) (parte 00)
- **Ver también:** [dominio](#dominio), [tipo de dato](#tipo-de-dato), [afinidad de tipos](#afinidad-de-tipos)
- **Fuente:** C. J. Date (2015), [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/)

### tipo compuesto

Tipo de dato definido por el usuario con varios campos, o los tipos estructurados que PostgreSQL trae de fábrica: arreglos, rangos, `JSONB`, tipos enumerados. Permiten modelar sin salir del relacional lo que en otros motores obligaría a una tabla más o a un documento.

- **Se trabaja en:** [031 — PostgreSQL: tipos, extensiones y modelo de procesos](classes/part-05-motores-relacionales-y-dialectos/031-postgresql-tipos-extensiones-y-procesos/README.md) (parte 05)
- **Ver también:** [tipo de dato](#tipo-de-dato), [extensión](#extensión), [incrustación](#incrustación)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

### tipo de dato

La declaración que fija qué valores acepta una columna y qué operaciones tienen sentido sobre ella. Es la primera línea de defensa del esquema y la más barata: lo que el tipo rechaza no hay que validarlo en ningún lenguaje de aplicación.

- **Se trabaja en:** [024 — DDL: el esquema como contrato ejecutable](classes/part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md) (parte 04)
- **Ver también:** [tipo](#tipo), [dominio](#dominio), [restricción](#restricción)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### transacción como red

Envolver un cambio en `BEGIN` … `ROLLBACK` permite ver su efecto y deshacerlo. Es la red de seguridad más barata que existe y la razón práctica de que un `UPDATE` sin transacción sea una apuesta.

- **Se trabaja en:** [005 — Cambiar datos: INSERT, UPDATE, DELETE y el WHERE que salva](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/005-cambiar-datos-insert-update-delete/README.md) (parte 00)
- **Ver también:** [atomicidad](#atomicidad), [unidad de recuperación](#unidad-de-recuperación), [deshacer](#deshacer)
- **Fuente:** SQLite Consortium (2026), [SQLite Documentation](https://sqlite.org/docs.html)

### trazabilidad de la cita

Que cada afirmación de la respuesta pueda seguirse hasta el fragmento y el documento del que salió. Es lo que permite auditar el sistema y detectar la alucinación; sin ella no hay forma de distinguir una respuesta correcta de una convincente.

- **Se trabaja en:** [071 — RAG evaluable: medir la recuperación antes que la generación](classes/part-13-vectores-recuperacion-y-rag/071-rag-evaluable/README.md) (parte 13)
- **Ver también:** [fragmentación](#fragmentación), [evidencia](#evidencia), [defensa técnica](#defensa-técnica)
- **Fuente:** Patrick Lewis, Ethan Perez, Aleksandra Piktus (2020), [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)

### TTL

Tiempo de vida tras el cual la clave expira y desaparece. Es la política de retención más simple que existe y la que convierte a una caché en caché: sin TTL, un almacén clave-valor es solo una base de datos en memoria que crece hasta llenarla.

- **Se trabaja en:** [037 — Clave-valor, caché y expiración: qué se pierde exactamente](classes/part-06-documentos-y-clave-valor/037-clave-valor-cache-y-expiracion/README.md) (parte 06)
- **Ver también:** [invalidación](#invalidación), [retención](#retención), [durabilidad configurable](#durabilidad-configurable)
- **Fuente:** Redis Ltd. (2026), [Redis Documentation](https://redis.io/docs/latest/)

### tupla

Un elemento de la relación: una asignación de un valor a cada atributo. No es «una fila en una posición», porque en un conjunto no hay posiciones; se identifica por sus valores, no por dónde está.

- **Se trabaja en:** [020 — La relación como conjunto: tuplas, dominios y acceso por valor](classes/part-03-modelo-relacional-y-algebra/020-la-relacion-como-conjunto/README.md) (parte 03)
- **Ver también:** [relación](#relación), [acceso por valor](#acceso-por-valor), [registro](#registro)
- **Fuente:** E. F. Codd (1970), [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685)

## U

### unidad de recuperación

La transacción como frontera de lo que se rehace o se deshace tras una caída. Es lo que conecta ACID con el registro anticipado: sin transacción no hay nada que delimite qué debe sobrevivir.

- **Se trabaja en:** [043 — ACID: qué garantiza cada letra y quién la implementa](classes/part-08-transacciones-concurrencia-y-recuperacion/043-acid-que-garantiza-cada-letra/README.md) (parte 08)
- **Ver también:** [atomicidad](#atomicidad), [WAL](#wal), [rehacer](#rehacer), [deshacer](#deshacer)
- **Fuente:** Jim Gray (1981), [The Transaction Concept: Virtues and Limitations](https://jimgray.azurewebsites.net/papers/thetransactionconcept.pdf)

### UNIQUE

Restricción que prohíbe valores repetidos en una columna o combinación de columnas. A diferencia de la clave primaria admite nulos —y cuántos admite depende del motor, que es una de las divergencias clásicas entre dialectos.

- **Se trabaja en:** [007 — La clave primaria: cómo se distingue una fila de otra](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/007-la-clave-primaria/README.md) (parte 00)
- **Ver también:** [restricción](#restricción), [clave candidata](#clave-candidata), [integridad declarada](#integridad-declarada)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

### UNKNOWN

El tercer valor de verdad de SQL, resultado de comparar con un nulo. No es verdadero ni falso: `NOT UNKNOWN` sigue siendo `UNKNOWN`, y un `WHERE` que se evalúa a `UNKNOWN` descarta la fila igual que si fuera falso.

- **Se trabaja en:** [029 — Nulos y lógica de tres valores](classes/part-04-sql-en-profundidad/029-nulos-y-logica-de-tres-valores/README.md) (parte 04)
- **Ver también:** [NULL](#null), [predicado](#predicado), [IS DISTINCT FROM](#is-distinct-from)
- **Fuente:** E. F. Codd (1979), [Extending the Database Relational Model to Capture More Meaning](https://dl.acm.org/doi/10.1145/320107.320109)

### UPDATE

Cambia valores de las filas que cumplen el `WHERE`. Sin `WHERE` cambia todas: es la orden que más datos ha destruido en la historia de las bases de datos.

- **Se trabaja en:** [005 — Cambiar datos: INSERT, UPDATE, DELETE y el WHERE que salva](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/005-cambiar-datos-insert-update-delete/README.md) (parte 00)
- **Ver también:** [alcance del cambio](#alcance-del-cambio), [filas afectadas](#filas-afectadas), [transacción como red](#transacción-como-red)
- **Fuente:** ISO/IEC JTC 1/SC 32 (2023), [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html)

## V

### vacuum

Proceso que recupera el espacio de las versiones de fila que ya nadie puede ver y actualiza los mapas de visibilidad. Sin él, MVCC crece sin límite: es el mantenimiento invisible que explica por qué una tabla ocupa el triple de lo que debería.

- **Se trabaja en:** [045 — Bloqueo en dos fases, MVCC e instantáneas](classes/part-08-transacciones-concurrencia-y-recuperacion/045-bloqueo-en-dos-fases-y-mvcc/README.md) (parte 08)
- **Ver también:** [autovacuum](#autovacuum), [versión de fila](#versión-de-fila), [costo de mantenimiento](#costo-de-mantenimiento)
- **Fuente:** Egor Rogov (2022), [PostgreSQL 14 Internals](https://postgrespro.com/community/books/internals)

### valor por defecto

Valor que el motor asigna cuando el `INSERT` no menciona la columna. Bien usado evita nulos accidentales; mal usado enmascara datos que faltaban de verdad y que convenía detectar.

- **Se trabaja en:** [024 — DDL: el esquema como contrato ejecutable](classes/part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md) (parte 04)
- **Ver también:** [NULL](#null), [restricción](#restricción), [tipo de dato](#tipo-de-dato)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)

### vectorización

Procesar lotes de miles de valores por llamada en lugar de una fila cada vez. Amortiza el costo de interpretación del plan y aprovecha las instrucciones SIMD del procesador; es la segunda mitad —junto al formato columnar— de la ventaja analítica de DuckDB o ClickHouse.

- **Se trabaja en:** [033 — SQLite y DuckDB: motores embebidos, transaccional frente a analítico](classes/part-05-motores-relacionales-y-dialectos/033-sqlite-y-duckdb-motores-embebidos/README.md) (parte 05)
- **Ver también:** [ejecución vectorizada](#ejecución-vectorizada), [almacenamiento columnar](#almacenamiento-columnar), [ejecutor](#ejecutor)
- **Fuente:** DuckDB Foundation (2026), [DuckDB Documentation](https://duckdb.org/docs/)

### ventana

Recorte temporal sobre el que se agrega un flujo: fija, deslizante o de sesión. Es lo que convierte un flujo infinito en resultados finitos que se pueden emitir.

- **Se trabaja en:** [067 — Streaming: tiempo de evento, ventanas y semántica de entrega](classes/part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md) (parte 12)
- **Ver también:** [marca de agua](#marca-de-agua), [agregado continuo](#agregado-continuo), [marco](#marco)
- **Fuente:** Tyler Akidau, Slava Chernyak, Reuven Lax (2018), [Streaming Systems](https://www.oreilly.com/library/view/streaming-systems/9781491983867/)

### versión de fila

Copia de una fila con el rango de transacciones para las que es visible. Con MVCC un `UPDATE` no sobrescribe: crea una versión nueva, de modo que quien está leyendo la anterior no se detiene. El precio es el espacio y el trabajo de limpiarlo.

- **Se trabaja en:** [045 — Bloqueo en dos fases, MVCC e instantáneas](classes/part-08-transacciones-concurrencia-y-recuperacion/045-bloqueo-en-dos-fases-y-mvcc/README.md) (parte 08)
- **Ver también:** [instantánea](#instantánea), [vacuum](#vacuum), [snapshot isolation](#snapshot-isolation)
- **Fuente:** PostgreSQL Global Development Group (2026), [PostgreSQL: Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html)

### vista externa

La porción del esquema que ve cada aplicación o cada rol, normalmente mediante vistas. Permite dar acceso a lo necesario y solo a eso, y absorber cambios del esquema sin romper a quien consulta.

- **Se trabaja en:** [013 — Independencia de datos y los tres niveles de esquema](classes/part-01-fundamentos-datos-sistemas-y-metodo/013-independencia-de-datos-y-niveles-de-esquema/README.md) (parte 01)
- **Ver también:** [independencia lógica](#independencia-lógica), [seguridad por fila](#seguridad-por-fila), [privilegio mínimo](#privilegio-mínimo)
- **Fuente:** Abraham Silberschatz, Henry F. Korth, S. Sudarshan (2019), [Database System Concepts](https://db-book.com/)

## W

### WAL

Registro anticipado: antes de tocar la página de datos se escribe en un registro secuencial qué se va a cambiar, y ese registro se fuerza al disco antes de confirmar. Es lo que hace posible la durabilidad sin escribir cada página en cada `COMMIT`.

- **Se trabaja en:** [046 — Registro anticipado y recuperación: WAL y ARIES](classes/part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md) (parte 08)
- **Ver también:** [punto de control](#punto-de-control), [rehacer](#rehacer), [deshacer](#deshacer), [LSN](#lsn)
- **Fuente:** C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz (1992), [ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging](https://dl.acm.org/doi/10.1145/128765.128770)
