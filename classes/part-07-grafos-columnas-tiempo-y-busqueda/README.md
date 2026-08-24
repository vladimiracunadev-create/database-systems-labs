# Parte 07 — Grafos, columnas, tiempo y búsqueda

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

Modelos especializados y el criterio para saber cuando la carga de trabajo justifica salir del relacional.

**5 clases · 15 horas · 20 conceptos · 16 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 06 — Documentos y clave-valor](../part-06-documentos-y-clave-valor/README.md)

## De qué trata esta parte

Cinco familias especializadas y un mismo criterio para todas: qué carga de trabajo justifica salir del relacional, y qué se paga por hacerlo. La estructura de la parte es deliberadamente comparativa, porque el error habitual no es elegir mal el motor especializado, sino adoptarlo sin haber comprobado que el relacional ya no daba más.

Grafos, para los recorridos de profundidad variable que SQL resuelve mal —con la aclaración honesta de cuándo una CTE recursiva sobre PostgreSQL es suficiente—. Columnas anchas, con su método de diseño invertido: primero la lista de consultas, después una tabla por consulta. Series temporales, con sus tres restricciones propias: cardinalidad de etiquetas, retención y submuestreo. Búsqueda de texto, con el índice invertido y la relevancia de TF-IDF a BM25. Y analítica columnar, donde se miden las cuatro contribuciones que producen los dos órdenes de magnitud, en lugar de atribuirlos al producto.

Las clases 041 y 042 son además preparación directa de la parte 13: BM25 vuelve como componente léxico de la búsqueda híbrida, y precisión y exhaustividad vuelven como métricas de un sistema RAG.

## Al terminar esta parte podrás

1. Decidir si un recorrido justifica un motor de grafos o si una CTE recursiva es suficiente.
2. Diseñar tablas de columnas anchas partiendo de la lista de consultas y no del modelo conceptual.
3. Controlar la cardinalidad, la retención y el submuestreo de una serie temporal.
4. Explicar cómo se construye un índice invertido y cómo BM25 ordena los resultados.
5. Medir de dónde sale la ventaja de un motor columnar en lugar de atribuirla al producto.

## Mapa de la parte

```mermaid
flowchart LR
    C038["038<br/>Grafos de propiedades y los recorridos qu…"]
    C039["039<br/>Columnas anchas: modelar desde la consulta"]
    C040["040<br/>Series temporales: cardinalidad, retenció…"]
    C041["041<br/>Búsqueda de texto: índice invertido, anál…"]
    C042["042<br/>Analítica columnar: por qué el formato ca…"]
    C038 --> C039
    C039 --> C040
    C040 --> C041
    C041 --> C042
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C038 inter
    class C039 avan
    class C040 inter
    class C041 inter
    class C042 avan
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [038](038-grafos-de-propiedades-y-recorridos/README.md) | [Grafos de propiedades y los recorridos que SQL hace mal](038-grafos-de-propiedades-y-recorridos/README.md) | Intermedio | 3 | 3 |
| [039](039-columnas-anchas-modelar-desde-la-consulta/README.md) | [Columnas anchas: modelar desde la consulta](039-columnas-anchas-modelar-desde-la-consulta/README.md) | Avanzado | 3 | 3 |
| [040](040-series-temporales-cardinalidad-y-retencion/README.md) | [Series temporales: cardinalidad, retención y agregados continuos](040-series-temporales-cardinalidad-y-retencion/README.md) | Intermedio | 3 | 3 |
| [041](041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) | [Búsqueda de texto: índice invertido, análisis y relevancia](041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) | Intermedio | 3 | 3 |
| [042](042-analitica-columnar-y-vectorizacion/README.md) | [Analítica columnar: por qué el formato cambia el orden de magnitud](042-analitica-columnar-y-vectorizacion/README.md) | Avanzado | 3 | 4 |

## Las clases, una por una

### [038 — Grafos de propiedades y los recorridos que SQL hace mal](038-grafos-de-propiedades-y-recorridos/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [026](../part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md), [028](../part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md)*

Los recorridos que SQL hace mal: profundidad variable, caminos y vecindarios. Explica la ventaja estructural del motor de grafos —la reunión sin índice, porque cada nodo guarda las direcciones de sus vecinos— y también cuándo una CTE recursiva sobre PostgreSQL es suficiente y no hace falta otro sistema.

**Conceptos que introduce:** `nodo` · `arista` · `recorrido de profundidad variable` · `reunión sin índice`

[Ir a la clase →](038-grafos-de-propiedades-y-recorridos/README.md)

### [039 — Columnas anchas: modelar desde la consulta](039-columnas-anchas-modelar-desde-la-consulta/README.md)

*Avanzado · 3 h · 3 fuentes · requiere [019](../part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md), [034](../part-06-documentos-y-clave-valor/034-el-agregado-como-unidad-de-consistencia/README.md)*

El método de diseño invertido de las columnas anchas: primero se escribe la lista de consultas y después una tabla por consulta, aunque los mismos datos queden repetidos cinco veces. La clave de partición decide en qué nodo vive la fila y la de agrupamiento el orden dentro de ella; equivocarse en la primera es el error de diseño más caro de esta familia.

**Conceptos que introduce:** `clave de partición` · `clave de agrupamiento` · `desnormalización por consulta`

[Ir a la clase →](039-columnas-anchas-modelar-desde-la-consulta/README.md)

### [040 — Series temporales: cardinalidad, retención y agregados continuos](040-series-temporales-cardinalidad-y-retencion/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [006](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/006-tipos-de-datos-un-numero-no-es-un-texto/README.md), [019](../part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md)*

Las series temporales y sus tres restricciones propias: la cardinalidad de etiquetas, que explota si se usa un identificador como etiqueta; la retención, que hay que decidir antes de acumular; y el submuestreo con agregados continuos, que es cómo se sostiene un histórico largo sin crecimiento lineal.

**Conceptos que introduce:** `cardinalidad de etiquetas` · `submuestreo` · `retención` · `agregado continuo`

[Ir a la clase →](040-series-temporales-cardinalidad-y-retencion/README.md)

### [041 — Búsqueda de texto: índice invertido, análisis y relevancia](041-busqueda-de-texto-indice-invertido-y-relevancia/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [004](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/004-leer-datos-select-where-y-order-by/README.md), [025](../part-04-sql-en-profundidad/025-select-filtrado-proyeccion-y-orden/README.md)*

Por qué `LIKE '%algo%'` no es buscar. Presenta el índice invertido, el analizador que decide qué es un término, y la relevancia de TF-IDF a BM25. Cierra con precisión y exhaustividad, el par de métricas que hace que una búsqueda se pueda evaluar en lugar de opinar sobre ella; ambas reaparecen en la parte 13.

**Conceptos que introduce:** `índice invertido` · `analizador` · `TF-IDF` · `BM25` · `precisión y exhaustividad`

[Ir a la clase →](041-busqueda-de-texto-indice-invertido-y-relevancia/README.md)

### [042 — Analítica columnar: por qué el formato cambia el orden de magnitud](042-analitica-columnar-y-vectorizacion/README.md)

*Avanzado · 3 h · 4 fuentes · requiere [033](../part-05-motores-relacionales-y-dialectos/033-sqlite-y-duckdb-motores-embebidos/README.md)*

De dónde salen realmente los dos órdenes de magnitud de la analítica: leer solo las columnas necesarias, comprimirlas mejor porque los valores contiguos se parecen, procesarlas en lotes vectorizados y podar bloques enteros por sus estadísticas. La clase mide las cuatro contribuciones en lugar de atribuirlas al producto.

**Conceptos que introduce:** `almacenamiento columnar` · `compresión` · `ejecución vectorizada` · `poda de particiones`

[Ir a la clase →](042-analitica-columnar-y-vectorizacion/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «Mis datos son un grafo, necesito un motor de grafos.» Casi todo es un grafo. Lo que justifica el motor es el recorrido de profundidad variable, no la forma de los datos.
- «En Cassandra modelo como en SQL y ya.» Una consulta que no fija la clave de partición obliga a preguntar a todo el anillo; es el error de diseño número uno de esa familia.
- «Pongo el identificador de usuario como etiqueta para poder filtrar.» Eso multiplica la cardinalidad de series y tumba el motor de series temporales.
- «Con `LIKE '%texto%'` ya busco.» Eso recorre la tabla y no ordena por relevancia. Buscar es índice invertido más una función de puntuación.

## Vocabulario de la parte

Los 20 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **agregado continuo** | Vista materializada que se actualiza de forma incremental según llegan datos nuevos, típicamente con medias u otros resúmenes por intervalo. Permite responder «el promedio por hora del último año» sin recorrer mil millones de puntos en cada consulta. | [040](040-series-temporales-cardinalidad-y-retencion/README.md) |
| **almacenamiento columnar** | Guardar juntos todos los valores de una misma columna en lugar de todas las columnas de una misma fila. Una consulta analítica lee solo las columnas que necesita y comprime mucho mejor, porque los valores contiguos se parecen entre sí. | [042](042-analitica-columnar-y-vectorizacion/README.md) |
| **analizador** | Primer componente del gestor: convierte el texto SQL en un árbol sintáctico y comprueba que los objetos citados existen y que los tipos encajan. Aquí mueren los errores de sintaxis, antes de tocar un solo dato. (En la clase 041 la misma palabra nombra otra cosa: el analizador de texto que parte un documento en términos indexables.) | [041](041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) |
| **arista** | Relación dirigida y con tipo entre dos nodos, que puede llevar sus propias propiedades. En un motor de grafos es un puntero real, no una clave foránea que haya que buscar en un índice, y de ahí viene su ventaja al recorrer. | [038](038-grafos-de-propiedades-y-recorridos/README.md) |
| **BM25** | Función de relevancia que refina TF-IDF con saturación de la frecuencia y normalización por longitud del documento, gobernadas por los parámetros `k1` y `b`. Es la referencia léxica contra la que se compara cualquier buscador, incluidos los vectoriales. | [041](041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) |
| **cardinalidad de etiquetas** | Número de combinaciones distintas de etiquetas en una base de series temporales; cada combinación es una serie con su índice y su memoria. Meter un identificador de usuario o de petición como etiqueta produce una explosión de cardinalidad que tumba el motor. | [040](040-series-temporales-cardinalidad-y-retencion/README.md) |
| **clave de agrupamiento** | La parte de la clave primaria que ordena las filas dentro de una partición. Es lo que permite leer rangos —«los últimos 20 mensajes de este chat»— con una sola lectura secuencial, y por eso el orden se decide al crear la tabla, no al consultar. | [039](039-columnas-anchas-modelar-desde-la-consulta/README.md) |
| **clave de partición** | La parte de la clave primaria que decide en qué nodo vive la fila. Toda consulta eficiente debe fijarla; una consulta sin ella obliga a preguntar a todo el anillo, y es el error de diseño número uno en columnas anchas. | [039](039-columnas-anchas-modelar-desde-la-consulta/README.md) |
| **compresión** | En un formato columnar, los valores contiguos se parecen, así que técnicas como el diccionario, la codificación por carrera o el delta reducen el tamaño en un orden de magnitud. Menos bytes leídos es menos entrada y salida, que es de donde sale casi toda la ventaja analítica. | [042](042-analitica-columnar-y-vectorizacion/README.md) |
| **desnormalización por consulta** | Método de diseño de columnas anchas: se escribe primero la lista de consultas y luego una tabla por consulta, aunque los mismos datos queden repetidos en cinco tablas. La coherencia entre copias pasa a ser responsabilidad de la aplicación. | [039](039-columnas-anchas-modelar-desde-la-consulta/README.md) |
| **ejecución vectorizada** | El ejecutor procesa lotes de valores por operador en lugar de fila a fila. Reduce el costo por fila del intérprete y permite usar instrucciones SIMD; combinada con el formato columnar, es la explicación de las diferencias de dos órdenes de magnitud frente a un motor de filas. | [042](042-analitica-columnar-y-vectorizacion/README.md) |
| **nodo** | Vértice del grafo de propiedades: una cosa con etiquetas y con pares clave-valor propios. Equivale a una fila, con la diferencia de que sus conexiones son parte de la estructura y no se recomponen por reunión. | [038](038-grafos-de-propiedades-y-recorridos/README.md) |
| **poda de particiones** | Descartar ficheros o bloques enteros sin abrirlos, gracias a los mínimos y máximos guardados en sus metadatos. Es lo que hace que consultar un día concreto sobre un histórico de diez años cueste casi lo mismo que consultar ese día solo. | [042](042-analitica-columnar-y-vectorizacion/README.md) |
| **precisión y exhaustividad** | Precisión: qué proporción de lo devuelto era relevante. Exhaustividad (o *recall*): qué proporción de lo relevante se devolvió. Casi siempre se compensan entre sí, y por eso una búsqueda solo puede evaluarse fijando cuál de las dos importa en ese caso. | [041](041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) |
| **recorrido de profundidad variable** | Consulta del tipo «amigos de amigos hasta cinco saltos» o «cualquier camino entre A y B». En SQL exige una CTE recursiva y una reunión por nivel; en un motor de grafos el costo depende del subgrafo recorrido, no del tamaño total del grafo. | [038](038-grafos-de-propiedades-y-recorridos/README.md) |
| **retención** | Cuánto tiempo se conservan los datos antes de borrarlos automáticamente. En series temporales es una decisión de capacidad; en datos personales es además una obligación legal, y las dos deben coincidir en la misma política escrita. | [040](040-series-temporales-cardinalidad-y-retencion/README.md) |
| **reunión sin índice** | Propiedad de los motores de grafos nativos: cada nodo guarda las direcciones físicas de sus vecinos, así que pasar de uno a otro no consulta ningún índice. Es la razón técnica de que el recorrido profundo escale donde el `JOIN` repetido se degrada. | [038](038-grafos-de-propiedades-y-recorridos/README.md) |
| **submuestreo** | Reducir la resolución de los datos antiguos: guardar cada segundo la última hora, cada minuto la última semana, cada hora el último año. Es cómo se sostiene un histórico largo sin que el tamaño crezca de forma lineal para siempre. | [040](040-series-temporales-cardinalidad-y-retencion/README.md) |
| **TF-IDF** | Peso clásico de un término: crece con su frecuencia en el documento (TF) y decrece con el número de documentos en que aparece (IDF). Formaliza la intuición de que «el» no distingue nada y «hipervisor» distingue mucho. | [041](041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) |
| **índice invertido** | Estructura que va de cada término al listado de documentos que lo contienen —lo contrario de recorrer los documentos buscando el término—. Es la base de todo buscador de texto y la razón de que `LIKE '%algo%'` no sea comparable a una búsqueda de verdad. | [041](041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) |

## Fuentes usadas en esta parte

16 obras distintas sostienen lo que se afirma en estas
5 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **Jeff Carpenter, Eben Hewitt** (2020). [Cassandra: The Definitive Guide](https://www.oreilly.com/library/view/cassandra-the-definitive/9781098115159/). 3.a ed. O'Reilly. ISBN 978-1-0981-1516-3.  
  Modelado dirigido por consultas en un motor de columnas anchas.  
  *Se cita en las clases 039.*
- **Martin Kleppmann** (2017). [Designing Data-Intensive Applications](https://dataintensive.net/). O'Reilly. ISBN 978-1-4493-7332-0.  
  Referencia central del programa para replicación, partición, transacciones distribuidas y streaming.  
  *Se cita en las clases 040.*
- **Ian Robinson, Jim Webber, Emil Eifrem** (2015). [Graph Databases](https://neo4j.com/graph-databases-book/). 2.a ed. O'Reilly. ISBN 978-1-4919-3089-2.  
  Descarga gratuita. Modelado de grafos de propiedades y recorridos.  
  *Se cita en las clases 038.*
- **Joe Celko** (2014). [Joe Celko's SQL for Smarties: Advanced SQL Programming](https://www.sciencedirect.com/book/9780128007617/joe-celkos-sql-for-smarties). 5.a ed. Morgan Kaufmann. ISBN 978-0-12-800761-7.  
  Modelado de jerarquias, conjuntos anidados y SQL declarativo avanzado.  
  *Se cita en las clases 038.*
- **Apache Software Foundation** (2026). [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/).  
  CQL, claves de partición y niveles de consistencia ajustables.  
  *Se cita en las clases 039.*
- **ClickHouse, Inc.** (2026). [ClickHouse Documentation](https://clickhouse.com/docs/).  
  Motores de tabla, claves de ordenamiento y vistas materializadas.  
  *Se cita en las clases 042.*
- **DuckDB Foundation** (2026). [DuckDB Documentation](https://duckdb.org/docs/).  
  Motor analítico embebido: OLAP columnar sin servidor.  
  *Se cita en las clases 042.*
- **InfluxData** (2026). [InfluxDB Documentation](https://docs.influxdata.com/).  
  Modelo de medición, etiquetas y campos para series temporales.  
  *Se cita en las clases 040.*
- **Neo4j, Inc.** (2026). [Neo4j Documentation](https://neo4j.com/docs/).  
  Cypher y modelo de grafo de propiedades.  
  *Se cita en las clases 038.*
- **OpenSearch Project** (2026). [OpenSearch Documentation](https://docs.opensearch.org/latest/).  
  Índice invertido, analizadores, relevancia y búsqueda k-NN.  
  *Se cita en las clases 041.*
- **PostgreSQL Global Development Group** (2026). [PostgreSQL Documentation](https://www.postgresql.org/docs/current/).  
  Documentación de referencia del motor relacional principal del programa.  
  *Se cita en las clases 041.*
- **Timescale, Inc.** (2026). [TimescaleDB Documentation](https://docs.timescale.com/).  
  Hipertablas, compresión y agregados continuos sobre PostgreSQL.  
  *Se cita en las clases 040.*
- **Fay Chang, Jeffrey Dean, Sanjay Ghemawat** (2006). [Bigtable: A Distributed Storage System for Structured Data](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/). USENIX OSDI.  
  Origen del modelo de familias de columnas que adoptaron HBase y Cassandra.  
  *Se cita en las clases 039.*
- **Philippe Flajolet, Eric Fusy, Olivier Gandouet, Frederic Meunier** (2007). [HyperLogLog: The Analysis of a Near-Optimal Cardinality Estimation Algorithm](http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf). Analysis of Algorithms (AofA).  
  Conteo aproximado de distintos con memoria prácticamente constante.  
  *Se cita en las clases 042.*
- **Michael Stonebraker, Samuel Madden, Daniel J. Abadi, Stavros Harizopoulos, Nabil Hachem, Pat Helland** (2007). [The End of an Architectural Era (It's Time for a Complete Rewrite)](https://cs.brown.edu/courses/cs227/archives/2008/Papers/OLTP/hstore.pdf). VLDB.  
  Mide en qué gasta el tiempo realmente un motor OLTP tradicional.  
  *Se cita en las clases 042.*
- **Stephen Robertson, Hugo Zaragoza** (2009). [The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf). Foundations and Trends in Information Retrieval 3(4). DOI [10.1561/1500000019](https://doi.org/10.1561/1500000019).  
  Función de ranking léxico contra la que se compara toda búsqueda semántica.  
  *Se cita en las clases 041.*

## Cómo estudiar esta parte

El mismo método en las 74 clases, y conviene respetar el orden:

1. **Lee el vocabulario antes que la materia.** Cada clase define sus términos
   arriba precisamente para que no haya que deducirlos del contexto.
2. **Ejecuta el ejemplo trabajado mientras lees**, no después. La mitad de lo
   que se aprende aquí solo aparece cuando la salida no es la esperada.
3. **Compara los motores.** La sección comparada muestra el mismo problema
   resuelto —o descartado con argumento— en varios sistemas. Lee también las
   filas de los que no lo resuelven: descartar con motivo es la habilidad que
   se evalúa en el proyecto final.
4. **Responde las preguntas de evaluación por escrito.** Una respuesta que no
   se puede escribir en tres líneas todavía no está entendida.
5. **Haz el reto de transferencia.** Es el único ejercicio que comprueba si el
   concepto se puede aplicar a un caso que la clase no mostró.
6. **Guarda la evidencia**: comando, versión del motor, semilla y salida
   completa. Sin eso no hay nota, porque no hay nada que revisar.

## Otras partes

- [Parte 00 — Primeros pasos: del archivo a la base de datos](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/README.md)
- [Parte 01 — Fundamentos, sistemas y método](../part-01-fundamentos-datos-sistemas-y-metodo/README.md)
- [Parte 02 — Modelado conceptual y requisitos](../part-02-modelado-conceptual-y-requisitos/README.md)
- [Parte 03 — Modelo relacional y álgebra](../part-03-modelo-relacional-y-algebra/README.md)
- [Parte 04 — SQL en profundidad](../part-04-sql-en-profundidad/README.md)
- [Parte 05 — Motores relacionales y dialectos](../part-05-motores-relacionales-y-dialectos/README.md)
- [Parte 06 — Documentos y clave-valor](../part-06-documentos-y-clave-valor/README.md)
- [Parte 08 — Transacciones, concurrencia y recuperación](../part-08-transacciones-concurrencia-y-recuperacion/README.md)
- [Parte 09 — Almacenamiento, índices y planes](../part-09-almacenamiento-indices-y-planes/README.md)
- [Parte 10 — Distribución, réplica y consistencia](../part-10-distribucion-replica-y-consistencia/README.md)
- [Parte 11 — Operación, seguridad y gobierno](../part-11-operacion-seguridad-y-gobierno/README.md)
- [Parte 12 — Analítica, integración y streaming](../part-12-analitica-integracion-y-streaming/README.md)
- [Parte 13 — Vectores, recuperación y RAG](../part-13-vectores-recuperacion-y-rag/README.md)
- [Parte 14 — Arquitectura y proyecto final](../part-14-arquitectura-y-proyecto-final/README.md)
