# Parte 09 — Almacenamiento, índices y planes

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

Por qué una consulta tarda: páginas, estructuras de índice, estadísticas y la lectura honesta de un plan de ejecución.

**5 clases · 17 horas · 23 conceptos · 12 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 01 — Fundamentos, sistemas y método](../part-01-fundamentos-datos-sistemas-y-metodo/README.md)
- [Parte 04 — SQL en profundidad](../part-04-sql-en-profundidad/README.md)

## De qué trata esta parte

Por qué una consulta tarda, respondido desde el disco hacia arriba. La parte empieza donde de verdad empieza el costo —la página, no la fila— y termina en la única herramienta que convierte el rendimiento en un asunto de evidencia: el plan de ejecución.

Primero páginas, factor de bloque, buffer y localidad, que explican por qué a veces recorrer la tabla entera le gana a usar el índice. Después las dos grandes familias de estructuras: B-Tree, con la regla del prefijo más a la izquierda que decide el orden de las columnas de un índice compuesto, y LSM-Tree, con su compactación y su amplificación de escritura. Luego los índices especializados, cada uno con el caso concreto en que gana y con el costo de mantenimiento que hace que un índice inútil sea una penalización permanente. Y al final leer `EXPLAIN` para refutar una hipótesis, comparando filas estimadas contra reales nodo a nodo.

La clase 052 es la que cambia la forma de trabajar: después de ella, «creo que va lento por el índice» deja de ser una frase aceptable sin un plan al lado.

## Al terminar esta parte podrás

1. Explicar por qué la unidad de costo es la página y qué consecuencias tiene para el diseño de la fila.
2. Elegir el orden de las columnas de un índice compuesto y justificarlo con las consultas que debe servir.
3. Comparar B-Tree y LSM-Tree en términos de amplificación de lectura y de escritura.
4. Elegir el índice especializado adecuado y contar su costo de mantenimiento.
5. Leer un plan de ejecución y refutar una hipótesis de rendimiento con filas estimadas frente a reales.

## Mapa de la parte

```mermaid
flowchart LR
    C048["048<br/>Páginas, filas y buffer: por qué la entra…"]
    C049["049<br/>B-Tree: estructura, orden de columnas y s…"]
    C050["050<br/>LSM-Tree, compactación y amplificación de…"]
    C051["051<br/>Índices especializados: hash, GIN, GiST,…"]
    C052["052<br/>Planes de ejecución: leer EXPLAIN y refut…"]
    C048 --> C049
    C049 --> C050
    C050 --> C051
    C051 --> C052
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C048 inter
    class C049 inter
    class C050 avan
    class C051 avan
    class C052 avan
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [048](048-paginas-filas-y-buffer-pool/README.md) | [Páginas, filas y buffer: por qué la entrada y salida manda](048-paginas-filas-y-buffer-pool/README.md) | Intermedio | 3 | 3 |
| [049](049-b-tree-orden-de-columnas-y-selectividad/README.md) | [B-Tree: estructura, orden de columnas y selectividad](049-b-tree-orden-de-columnas-y-selectividad/README.md) | Intermedio | 4 | 3 |
| [050](050-lsm-tree-compactacion-y-amplificacion/README.md) | [LSM-Tree, compactación y amplificación de escritura](050-lsm-tree-compactacion-y-amplificacion/README.md) | Avanzado | 3 | 3 |
| [051](051-indices-especializados/README.md) | [Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes](051-indices-especializados/README.md) | Avanzado | 3 | 3 |
| [052](052-planes-de-ejecucion-y-refutacion/README.md) | [Planes de ejecución: leer EXPLAIN y refutar una hipótesis](052-planes-de-ejecucion-y-refutacion/README.md) | Avanzado | 4 | 3 |

## Las clases, una por una

### [048 — Páginas, filas y buffer: por qué la entrada y salida manda](048-paginas-filas-y-buffer-pool/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [012](../part-01-fundamentos-datos-sistemas-y-metodo/012-arquitectura-interna-de-un-gestor/README.md)*

Por qué la entrada y salida manda: el motor no lee filas, lee páginas. De ahí salen el factor de bloque, la localidad y la ventaja de la lectura secuencial, que explica por qué a veces recorrer la tabla entera le gana a usar el índice —y por qué el planificador lo elige a propósito.

**Conceptos que introduce:** `pagina` · `factor de bloque` · `buffer pool` · `localidad` · `lectura secuencial`

[Ir a la clase →](048-paginas-filas-y-buffer-pool/README.md)

### [049 — B-Tree: estructura, orden de columnas y selectividad](049-b-tree-orden-de-columnas-y-selectividad/README.md)

*Intermedio · 4 h · 3 fuentes · requiere [048](048-paginas-filas-y-buffer-pool/README.md)*

El B-Tree y las dos preguntas que responde en la práctica: en qué orden poner las columnas de un índice compuesto —la regla del prefijo más a la izquierda— y cuándo el índice no compensa, que es cuando la selectividad es baja. Introduce el índice cubriente, la optimización con mejor relación entre esfuerzo y resultado.

**Conceptos que introduce:** `B-Tree` · `prefijo más a la izquierda` · `selectividad` · `índice cubriente`

[Ir a la clase →](049-b-tree-orden-de-columnas-y-selectividad/README.md)

### [050 — LSM-Tree, compactación y amplificación de escritura](050-lsm-tree-compactacion-y-amplificacion/README.md)

*Avanzado · 3 h · 3 fuentes · requiere [048](048-paginas-filas-y-buffer-pool/README.md)*

La otra familia de estructuras de almacenamiento: memtable, SSTable y compactación. Explica por qué un LSM absorbe mucha más escritura que un B-Tree y qué paga a cambio —amplificación de escritura y compactaciones que consumen recursos justo cuando el sistema está cargado—, con el filtro de Bloom como pieza que salva lecturas.

**Conceptos que introduce:** `memtable` · `SSTable` · `compactación` · `amplificación de escritura` · `filtro de Bloom`

[Ir a la clase →](050-lsm-tree-compactacion-y-amplificacion/README.md)

### [051 — Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes](051-indices-especializados/README.md)

*Avanzado · 3 h · 3 fuentes · requiere [049](049-b-tree-orden-de-columnas-y-selectividad/README.md)*

Los índices que no son B-Tree y el caso concreto en que cada uno gana: hash para igualdad pura, GIN para contenido de arreglos y documentos, GiST para geometría y rangos, BRIN cuando el orden físico se correlaciona con la columna, más parciales, de expresión y cubrientes. Cierra con el costo de mantenimiento, que hace que un índice inútil no sea neutro sino una penalización permanente.

**Conceptos que introduce:** `índice parcial` · `índice de expresión` · `GIN` · `BRIN` · `costo de mantenimiento`

[Ir a la clase →](051-indices-especializados/README.md)

### [052 — Planes de ejecución: leer EXPLAIN y refutar una hipótesis](052-planes-de-ejecucion-y-refutacion/README.md)

*Avanzado · 4 h · 3 fuentes · requiere [049](049-b-tree-orden-de-columnas-y-selectividad/README.md), [051](051-indices-especializados/README.md)*

Leer un plan de ejecución para refutar una hipótesis, no para confirmarla. La técnica central es comparar filas estimadas contra reales nodo a nodo: un error de estimación explica casi cualquier plan absurdo. Insiste en que el `cost` no son milisegundos y en que solo `EXPLAIN ANALYZE` mide tiempo.

**Conceptos que introduce:** `optimizador por costos` · `estadística` · `estimación de cardinalidad` · `costo frente a tiempo`

[Ir a la clase →](052-planes-de-ejecucion-y-refutacion/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «Añadir índices siempre ayuda.» Cada índice se paga en cada escritura y ocupa espacio; el que no usa ninguna consulta es una penalización permanente.
- «Tengo el índice pero el motor no lo usa.» Casi siempre es la regla del prefijo más a la izquierda, una función aplicada a la columna, o una selectividad demasiado baja.
- «El `cost` de `EXPLAIN` son milisegundos.» Es una unidad interna comparativa. El tiempo solo aparece con `EXPLAIN ANALYZE`.
- «El recorrido secuencial siempre es malo.» Es lo correcto cuando la consulta devuelve una fracción grande de la tabla, y el planificador lo elige a propósito.

## Vocabulario de la parte

Los 23 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **amplificación de escritura** | Cuántos bytes acaba escribiendo el motor en disco por cada byte que escribió la aplicación, sumando registro y compactaciones sucesivas. Es la métrica que decide el desgaste del disco y el techo real de escritura de un motor LSM. | [050](050-lsm-tree-compactacion-y-amplificacion/README.md) |
| **B-Tree** | Árbol equilibrado de páginas ordenadas, con todos los datos en hojas enlazadas entre sí. Sirve para igualdad, para rangos y para devolver ya ordenado, con un número de accesos que crece logarítmicamente. Es la estructura por defecto de casi todos los motores relacionales. | [049](049-b-tree-orden-de-columnas-y-selectividad/README.md) |
| **BRIN** | Índice de rangos por bloque: guarda el mínimo y el máximo de cada grupo de páginas. Diminuto y utilísimo cuando el orden físico se correlaciona con la columna —una tabla de eventos por fecha—, e inútil cuando no. | [051](051-indices-especializados/README.md) |
| **buffer pool** | La memoria donde el motor mantiene las páginas leídas para no volver a pedirlas al disco. Su tasa de acierto explica la mayor parte de la diferencia entre una consulta de 2 ms y la misma consulta de 200 ms. | [048](048-paginas-filas-y-buffer-pool/README.md) |
| **compactación** | Proceso de fusionar SSTables, descartar versiones antiguas y aplicar los borrados. Es lo que impide que las lecturas se degraden sin fin, y también lo que consume entrada y salida en segundo plano justo cuando el sistema está cargado. | [050](050-lsm-tree-compactacion-y-amplificacion/README.md) |
| **costo de mantenimiento** | Lo que cada índice cobra en cada `INSERT`, `UPDATE` y `DELETE`, más el espacio que ocupa y el trabajo de reconstruirlo. Un índice que no usa ninguna consulta no es neutro: es una penalización permanente sobre todas las escrituras. | [051](051-indices-especializados/README.md) |
| **costo frente a tiempo** | El `cost` de `EXPLAIN` es una unidad interna comparativa, no milisegundos; el tiempo real solo aparece con `EXPLAIN ANALYZE`. Comparar filas estimadas contra filas reales en cada nodo es la técnica central para refutar una hipótesis de rendimiento. | [052](052-planes-de-ejecucion-y-refutacion/README.md) |
| **estadística** | Resúmenes que el motor guarda sobre los datos: número de filas, valores distintos, histogramas, valores más comunes. Cuando están obsoletas el optimizador estima mal y elige planes ruinosos, y ese es el primer sitio donde mirar ante una consulta que «de repente» se volvió lenta. | [052](052-planes-de-ejecucion-y-refutacion/README.md) |
| **estimación de cardinalidad** | Cuántas filas cree el planificador que devolverá cada paso. Es la entrada de la que depende todo lo demás, y también la parte más frágil: los errores se multiplican al reunir tablas, y una estimación de 1 fila que en realidad son 100 000 explica casi cualquier plan absurdo. | [052](052-planes-de-ejecucion-y-refutacion/README.md) |
| **factor de bloque** | Cuántas filas caben en una página. Depende del ancho de la fila, así que columnas anchas que nadie consulta encarecen todas las lecturas de esa tabla, incluidas las que no las piden. | [048](048-paginas-filas-y-buffer-pool/README.md) |
| **filtro de Bloom** | Estructura probabilística compacta que responde «seguro que no está» o «puede que esté». Ahorra abrir SSTables que no contienen la clave; nunca produce falsos negativos, así que es seguro usarla para descartar. | [050](050-lsm-tree-compactacion-y-amplificacion/README.md) |
| **GIN** | Índice invertido generalizado de PostgreSQL: indexa los elementos de un valor compuesto —palabras de un texto, claves de un JSONB, elementos de un arreglo—. Es rápido buscando y caro escribiendo, y por eso admite una cola de actualizaciones diferida. | [051](051-indices-especializados/README.md) |
| **lectura secuencial** | Leer páginas contiguas, que es órdenes de magnitud más barato por fila que saltar de una a otra. Por eso un recorrido completo puede ganarle a un índice cuando la consulta devuelve una fracción grande de la tabla. | [048](048-paginas-filas-y-buffer-pool/README.md) |
| **localidad** | Que los datos que se usan juntos estén guardados juntos. Es la propiedad que convierte muchas lecturas lógicas en pocas lecturas físicas, y el motivo por el que el orden físico de una tabla —y la clave de agrupamiento— importa tanto. | [048](048-paginas-filas-y-buffer-pool/README.md) |
| **memtable** | Estructura ordenada en memoria donde un motor LSM acumula las escrituras antes de volcarlas a disco. Convierte escrituras aleatorias en secuenciales, que es la razón de que los LSM absorban mucha más carga de escritura que un B-Tree. | [050](050-lsm-tree-compactacion-y-amplificacion/README.md) |
| **optimizador por costos** | Componente que enumera planes equivalentes y elige el de menor costo estimado a partir de estadísticas. Desde el artículo de Selinger de 1979 el principio no ha cambiado: el motor no ejecuta lo que escribiste, ejecuta lo que calculó que es más barato. | [052](052-planes-de-ejecucion-y-refutacion/README.md) |
| **pagina** | La unidad mínima de lectura y escritura en disco, típicamente de 4 a 16 KB. El motor nunca lee «una fila»: lee la página que la contiene, y de ahí que quepan más filas por página sea una optimización real. | [048](048-paginas-filas-y-buffer-pool/README.md) |
| **prefijo más a la izquierda** | Un índice sobre `(a, b, c)` solo sirve para filtros que fijan `a`, o `a` y `b`, o los tres —nunca para `b` solo—. Es la regla que decide el orden de las columnas de un índice compuesto y la que explica por qué «tengo el índice y no lo usa». | [049](049-b-tree-orden-de-columnas-y-selectividad/README.md) |
| **selectividad** | Qué fracción de la tabla devuelve un predicado. Un índice compensa cuando la selectividad es alta —pocas filas—; con predicados poco selectivos, el recorrido secuencial gana y el planificador lo elige a propósito. | [049](049-b-tree-orden-de-columnas-y-selectividad/README.md) |
| **SSTable** | Fichero ordenado e inmutable resultante de volcar una memtable. Al ser inmutable no se actualiza: los cambios posteriores viven en ficheros más nuevos, y por eso una lectura puede tener que consultar varios niveles. | [050](050-lsm-tree-compactacion-y-amplificacion/README.md) |
| **índice cubriente** | Índice que incluye todas las columnas que la consulta necesita, así que el motor responde sin volver a la tabla. En PostgreSQL se construye con `INCLUDE`; su costo es un índice más ancho y más caro de mantener en cada escritura. | [049](049-b-tree-orden-de-columnas-y-selectividad/README.md) |
| **índice de expresión** | Índice sobre el resultado de una función, como `lower(correo)`. Es lo que permite que una búsqueda insensible a mayúsculas use índice, siempre que la consulta escriba la expresión exactamente igual que el índice. | [051](051-indices-especializados/README.md) |
| **índice parcial** | Índice que solo cubre las filas que cumplen un predicado (`WHERE activo`). Ocupa una fracción del total y se mantiene más barato, y encaja perfectamente cuando las consultas siempre filtran por ese mismo estado. | [051](051-indices-especializados/README.md) |

## Fuentes usadas en esta parte

12 obras distintas sostienen lo que se afirma en estas
5 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **Alex Petrov** (2019). [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/). O'Reilly. ISBN 978-1-4920-4034-7.  
  Motor de almacenamiento (B-Tree y LSM) y consenso explicados con detalle de implementación.  
  *Se cita en las clases 048, 050.*
- **Egor Rogov** (2022). [PostgreSQL 14 Internals](https://postgrespro.com/community/books/internals). Postgres Professional. ISBN 978-5-6041193-2-8.  
  PDF gratuito. MVCC, vacuum, buffers, índices y planificador sobre el código real.  
  *Se cita en las clases 048, 051.*
- **Markus Winand** (2012). [SQL Performance Explained](https://use-the-index-luke.com/). Markus Winand. ISBN 978-3-9503078-2-5.  
  Versión web gratuita. Índices B-Tree y su relación con el orden de las columnas.  
  *Se cita en las clases 049, 051.*
- **PostgreSQL Global Development Group** (2026). [PostgreSQL: Indexes](https://www.postgresql.org/docs/current/indexes.html).  
  B-tree, hash, GiST, SP-GiST, GIN y BRIN con sus casos de uso.  
  *Se cita en las clases 051.*
- **PostgreSQL Global Development Group** (2026). [PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html).  
  Lectura de planes de ejecución y diferencia entre costo estimado y tiempo real.  
  *Se cita en las clases 052.*
- **SQLite Consortium** (2026). [SQLite: Query Optimizer Overview](https://sqlite.org/optoverview.html).  
  Como decide SQLite usar un índice; útil para leer EXPLAIN QUERY PLAN.  
  *Se cita en las clases 052.*
- **P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie, T. G. Price** (1979). [Access Path Selection in a Relational Database Management System](https://dl.acm.org/doi/10.1145/582095.582099). ACM SIGMOD. DOI [10.1145/582095.582099](https://doi.org/10.1145/582095.582099).  
  Base del optimizador por costos que siguen usando los motores actuales.  
  *Se cita en las clases 052.*
- **Joseph M. Hellerstein, Michael Stonebraker, James Hamilton** (2007). [Architecture of a Database System](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf). Foundations and Trends in Databases 1(2). DOI [10.1561/1900000002](https://doi.org/10.1561/1900000002).  
  Descripción completa de los componentes internos de un SGBD relacional.  
  *Se cita en las clases 048.*
- **Goetz Graefe** (2011). [Modern B-Tree Techniques](https://www.nowpublishers.com/article/Details/DBS-028). Foundations and Trends in Databases 3(4). DOI [10.1561/1900000028](https://doi.org/10.1561/1900000028).  
  Estado del arte del B-Tree: división, compresión y concurrencia.  
  *Se cita en las clases 049.*
- **R. Bayer, E. McCreight** (1972). [Organization and Maintenance of Large Ordered Indices](https://link.springer.com/article/10.1007/BF00288683). Acta Informatica 1(3). DOI [10.1007/BF00288683](https://doi.org/10.1007/BF00288683).  
  Artículo original del B-Tree.  
  *Se cita en las clases 049.*
- **Burton H. Bloom** (1970). [Space/Time Trade-offs in Hash Coding with Allowable Errors](https://dl.acm.org/doi/10.1145/362686.362692). Communications of the ACM 13(7). DOI [10.1145/362686.362692](https://doi.org/10.1145/362686.362692).  
  Filtro de Bloom: clave para evitar lecturas de disco en motores LSM.  
  *Se cita en las clases 050.*
- **Patrick O'Neil, Edward Cheng, Dieter Gawlick, Elizabeth O'Neil** (1996). [The Log-Structured Merge-Tree (LSM-Tree)](https://link.springer.com/article/10.1007/s002360050048). Acta Informatica 33(4). DOI [10.1007/s002360050048](https://doi.org/10.1007/s002360050048).  
  Estructura que sostiene RocksDB, Cassandra, ScyllaDB y LevelDB.  
  *Se cita en las clases 050.*

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
- [Parte 07 — Grafos, columnas, tiempo y búsqueda](../part-07-grafos-columnas-tiempo-y-busqueda/README.md)
- [Parte 08 — Transacciones, concurrencia y recuperación](../part-08-transacciones-concurrencia-y-recuperacion/README.md)
- [Parte 10 — Distribución, réplica y consistencia](../part-10-distribucion-replica-y-consistencia/README.md)
- [Parte 11 — Operación, seguridad y gobierno](../part-11-operacion-seguridad-y-gobierno/README.md)
- [Parte 12 — Analítica, integración y streaming](../part-12-analitica-integracion-y-streaming/README.md)
- [Parte 13 — Vectores, recuperación y RAG](../part-13-vectores-recuperacion-y-rag/README.md)
- [Parte 14 — Arquitectura y proyecto final](../part-14-arquitectura-y-proyecto-final/README.md)
