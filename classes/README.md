# Clases

74 clases repartidas en 15 partes, 230 horas
estimadas y 306 conceptos definidos en el
[glosario del programa](../GLOSARIO.md).

## Cómo se lee este índice

Cada parte tiene su **portada**, y ahí es donde empieza el trabajo: explica de
qué trata la parte, qué hay que traer sabido, qué sabrás hacer al terminar, una
ficha por clase, los errores frecuentes que desmonta, su vocabulario y la
bibliografía completa. Este índice es solo el mapa para llegar hasta allí.

La columna «en una línea» resume cada clase; la explicación completa está en la
portada de su parte y, con todo el detalle, en el README de la clase.

Cada clase declara sus fuentes al final y ninguna se publica sin al menos tres.
Este índice, los README de clase y el glosario se generan con
`python scripts/build_classes.py`; la materia se edita en el `lesson.md` de cada
carpeta y la pauta pedagógica en [`curriculum.yaml`](../curriculum.yaml).

## [Parte 00 — Primeros pasos: del archivo a la base de datos](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/README.md)

La rampa de entrada. Qué es un dato, por qué una hoja de cálculo deja de servir, y las primeras órdenes de SQL —crear, insertar, leer, cambiar— hasta llegar a dos tablas relacionadas. Termina con las dos preguntas que hay que saber contestar antes de seguir: cuándo NO hace falta una base de datos y qué familias de motores existen.

Esta parte existe porque el resto del programa da por sabidas cosas que casi nadie aprendió de forma ordenada. Antes de discutir normalización, aislamiento o consenso hay que poder decir sin dudar qué es un dato, qué es una fila, qué garantiza una clave y por qué una hoja de cálculo deja de servir. Diez clases, veinte horas, y ninguna teoría que no se pueda ejecutar en la misma sesión en que se lee.

*10 clases · 20 horas · 46 conceptos* — [portada de la parte, con la explicación de cada clase](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [001](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md) | Qué es un dato, un registro y una tabla | La clase que pone nombre a las tres piezas de las que se habla el resto del programa | Fundamentos | 2 |
| [002](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) | Del archivo y la hoja de cálculo a la base de datos | Por qué llega un momento en que la hoja de cálculo deja de servir, expresado en cuatro capacidades que un archivo no tiene: integridad declarada, c… | Fundamentos | 2 |
| [003](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/003-tu-primera-base-de-datos/README.md) | Tu primera base de datos: crear, insertar y leer | La primera base de datos real, creada, poblada y consultada en la misma sesión | Fundamentos | 2 |
| [004](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/004-leer-datos-select-where-y-order-by/README.md) | Leer datos: SELECT, WHERE y ORDER BY | Leer con precisión: filtrar filas, elegir columnas y ordenar el resultado | Fundamentos | 2 |
| [005](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/005-cambiar-datos-insert-update-delete/README.md) | Cambiar datos: INSERT, UPDATE, DELETE y el WHERE que salva | Las tres órdenes que cambian datos y la disciplina que las hace seguras: comprobar el alcance con un `SELECT` antes de escribir, leer el número de… | Fundamentos | 2 |
| [006](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/006-tipos-de-datos-un-numero-no-es-un-texto/README.md) | Tipos de datos: por qué un número no es un texto | Por qué el tipo de una columna no es burocracia: decide qué comparaciones tienen sentido, qué ordenaciones son correctas y si el dinero se calcula… | Fundamentos | 2 |
| [007](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/007-la-clave-primaria/README.md) | La clave primaria: cómo se distingue una fila de otra | Cómo se distingue una fila de otra | Fundamentos | 2 |
| [008](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/008-dos-tablas-y-una-relacion/README.md) | Dos tablas y una relación: la clave foránea | La segunda tabla y el momento en que aparece la relación | Fundamentos | 2 |
| [009](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/009-cuando-no-necesitas-una-base-de-datos/README.md) | Cuándo NO necesitas una base de datos | La clase que da permiso para no usar una base de datos | Fundamentos | 2 |
| [010](part-00-primeros-pasos-del-archivo-a-la-base-de-datos/010-el-mapa-de-los-motores/README.md) | El mapa de los motores: seis familias y un criterio | El mapa que se usará durante todo el programa: seis familias de motores, qué patrón de acceso optimiza cada una y qué paga a cambio | Fundamentos | 2 |

## [Parte 01 — Fundamentos, sistemas y método](part-01-fundamentos-datos-sistemas-y-metodo/README.md)

Qué problema resuelve un gestor de bases de datos, qué hay dentro de él y cómo se monta un entorno donde cada afirmación pueda comprobarse.

La parte 00 mostró qué se hace con una base de datos. Esta pregunta por qué existe y qué hay dentro. Es la transición de usuario a persona que puede razonar sobre el sistema, y sin ella las partes 08 y 09 —transacciones y planes de ejecución— son magia con nombres técnicos.

*4 clases · 12 horas · 19 conceptos* — [portada de la parte, con la explicación de cada clase](part-01-fundamentos-datos-sistemas-y-metodo/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [011](part-01-fundamentos-datos-sistemas-y-metodo/011-que-resuelve-un-sistema-de-bases-de-datos/README.md) | Qué resuelve un sistema de bases de datos y qué no | La misma pregunta de la clase 002, ahora con el vocabulario de sistemas: qué garantiza un gestor —persistencia, concurrencia, integridad, recuperac… | Fundamentos | 3 |
| [012](part-01-fundamentos-datos-sistemas-y-metodo/012-arquitectura-interna-de-un-gestor/README.md) | Arquitectura interna de un gestor, del cliente al disco | El recorrido completo de una consulta desde el cliente hasta el disco: analizador, planificador, ejecutor, gestor de almacenamiento y buffer | Fundamentos | 3 |
| [013](part-01-fundamentos-datos-sistemas-y-metodo/013-independencia-de-datos-y-niveles-de-esquema/README.md) | Independencia de datos y los tres niveles de esquema | Los tres niveles de esquema —externo, conceptual y físico— y por qué separarlos es lo que permite añadir un índice, particionar una tabla o dividir… | Fundamentos | 3 |
| [014](part-01-fundamentos-datos-sistemas-y-metodo/014-entorno-reproducible-y-evidencia/README.md) | Entorno reproducible y evidencia comprobable | El método de trabajo del resto del programa: entorno en contenedor con la versión fijada, datos generados con semilla declarada, invariantes escrit… | Fundamentos | 3 |

## [Parte 02 — Modelado conceptual y requisitos](part-02-modelado-conceptual-y-requisitos/README.md)

Del enunciado ambiguo al esquema defendible: entidades, claves, dependencias funcionales y la decisión consciente de desnormalizar.

Aquí empieza el trabajo de diseño. El material de entrada es lo que suele haber en la realidad: un enunciado ambiguo escrito por alguien que no piensa en tablas. El material de salida es un esquema que se puede defender frente a preguntas, no solo dibujar.

*5 clases · 16 horas · 20 conceptos* — [portada de la parte, con la explicación de cada clase](part-02-modelado-conceptual-y-requisitos/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [015](part-02-modelado-conceptual-y-requisitos/015-de-requisitos-a-entidades/README.md) | De requisitos ambiguos a entidades defendibles | El paso del enunciado ambiguo a un conjunto de entidades que se puede defender | Fundamentos | 3 |
| [016](part-02-modelado-conceptual-y-requisitos/016-entidad-relacion-cardinalidad-y-participacion/README.md) | Entidad-relación, cardinalidad y participación | El modelo entidad-relación de Chen con las dos decisiones que más consecuencias tienen: la cardinalidad, que determina dónde va la clave foránea, y… | Fundamentos | 3 |
| [017](part-02-modelado-conceptual-y-requisitos/017-claves-identidad-natural-y-sustituta/README.md) | Claves, identidad y el debate natural frente a sustituta | El debate entre clave natural y clave sustituta resuelto por un criterio y no por preferencia: cuál de las dos mantiene la identidad estable cuando… | Fundamentos | 3 |
| [018](part-02-modelado-conceptual-y-requisitos/018-normalizacion-y-dependencias-funcionales/README.md) | Normalización de 1FN a BCFN con dependencias funcionales | La normalización explicada como lo que es: una demostración a partir de dependencias funcionales, no una intuición sobre qué pertenece a qué | Intermedio | 4 |
| [019](part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md) | Desnormalización deliberada y patrones de acceso | El contrapeso de la clase anterior: cuándo duplicar a propósito | Intermedio | 3 |

## [Parte 03 — Modelo relacional y álgebra](part-03-modelo-relacional-y-algebra/README.md)

La teoría que SQL implementa a medias: relaciones como conjuntos, operadores del álgebra, cálculo relacional e integridad declarada.

Esta parte da la teoría que SQL implementa a medias, y lo hace precisamente para que las diferencias entre teoría y lenguaje dejen de ser sorpresas. La relación de Codd es un conjunto: no tiene orden y no tiene duplicados. SQL trabaja con multiconjuntos ordenables. Conocer esa brecha explica de antemano por qué hace falta `DISTINCT`, por qué no se puede confiar en el orden y por qué `NOT IN` se comporta como se comporta.

*4 clases · 13 horas · 19 conceptos* — [portada de la parte, con la explicación de cada clase](part-03-modelo-relacional-y-algebra/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [020](part-03-modelo-relacional-y-algebra/020-la-relacion-como-conjunto/README.md) | La relación como conjunto: tuplas, dominios y acceso por valor | La relación como conjunto de tuplas sobre dominios, con dos propiedades que SQL no respeta: no hay orden y no hay duplicados | Fundamentos | 3 |
| [021](part-03-modelo-relacional-y-algebra/021-algebra-relacional-operadores/README.md) | Álgebra relacional: selección, proyección, producto y reunión | Los operadores del álgebra relacional —selección, proyección, producto, reunión y división— como el lenguaje en el que el optimizador piensa | Fundamentos | 4 |
| [022](part-03-modelo-relacional-y-algebra/022-calculo-relacional-y-equivalencia/README.md) | Cálculo relacional y su equivalencia con el álgebra | El cálculo relacional y el teorema que lo hace equivalente al álgebra | Intermedio | 3 |
| [023](part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md) | Integridad: restricciones, claves foraneas y acciones referenciales | La integridad declarada en su forma completa: integridad de entidad, integridad referencial, `CHECK` y las acciones referenciales | Intermedio | 3 |

## [Parte 04 — SQL en profundidad](part-04-sql-en-profundidad/README.md)

Escribir SQL cuya semántica se pueda defender: definición del esquema, reuniones, agregación, ventanas y el comportamiento real de los nulos.

Seis clases para escribir SQL cuya semántica se pueda defender. No es un recorrido por la sintaxis: es la parte donde se cierran los huecos por los que se cuelan los resultados silenciosamente incorrectos, que son mucho peores que los errores, porque no fallan.

*6 clases · 20 horas · 27 conceptos* — [portada de la parte, con la explicación de cada clase](part-04-sql-en-profundidad/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [024](part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md) | DDL: el esquema como contrato ejecutable | El DDL leído como un contrato ejecutable: cada tipo y cada restricción es una validación que ya no hay que escribir en ninguna aplicación | Fundamentos | 3 |
| [025](part-04-sql-en-profundidad/025-select-filtrado-proyeccion-y-orden/README.md) | SELECT: filtrado, proyección y orden con semántica precisa | El `SELECT` con su semántica exacta: el orden lógico de evaluación que explica por qué un alias del `SELECT` no vale en el `WHERE`, y la colación,… | Fundamentos | 3 |
| [026](part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md) | Reuniones: interna, externa, semi y anti | Las cuatro formas de reunir y cuándo se quiere cada una | Intermedio | 4 |
| [027](part-04-sql-en-profundidad/027-agregacion-group-by-y-having/README.md) | Agregación, GROUP BY y HAVING sin duplicar filas | Agregar sin mentir | Intermedio | 3 |
| [028](part-04-sql-en-profundidad/028-cte-subconsultas-y-funciones-de-ventana/README.md) | CTE, subconsultas y funciones de ventana | Las herramientas para consultas que no caben en una sola expresión: CTE para nombrar pasos, recursión para recorrer jerarquías y funciones de venta… | Intermedio | 4 |
| [029](part-04-sql-en-profundidad/029-nulos-y-logica-de-tres-valores/README.md) | Nulos y lógica de tres valores | La lógica de tres valores y sus consecuencias prácticas: `NOT IN` que devuelve vacío por un solo nulo, agregados que ignoran ausencias y comparacio… | Intermedio | 3 |

## [Parte 05 — Motores relacionales y dialectos](part-05-motores-relacionales-y-dialectos/README.md)

Que exige la norma, que añade cada producto y como se escribe código que sobrevive a un cambio de motor.

SQL no es un lenguaje, son varios que se parecen. Esta parte separa lo que exige la norma ISO/IEC 9075 de lo que cada producto añade por su cuenta, y produce un artefacto revisable en lugar de una intención: una matriz que registra, construcción por construcción, si es de norma y cómo la escribe cada motor del proyecto.

*4 clases · 12 horas · 15 conceptos* — [portada de la parte, con la explicación de cada clase](part-05-motores-relacionales-y-dialectos/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [030](part-05-motores-relacionales-y-dialectos/030-portabilidad-y-matriz-de-dialectos/README.md) | Portabilidad: qué exige la norma y qué añade cada motor | Qué exige la norma ISO/IEC 9075 y qué añade cada producto por su cuenta | Intermedio | 3 |
| [031](part-05-motores-relacionales-y-dialectos/031-postgresql-tipos-extensiones-y-procesos/README.md) | PostgreSQL: tipos, extensiones y modelo de procesos | PostgreSQL como caso de estudio de motor extensible: tipos compuestos, arreglos, rangos y JSONB de fábrica, extensiones que añaden vectores o geome… | Intermedio | 3 |
| [032](part-05-motores-relacionales-y-dialectos/032-mysql-sqlserver-y-oracle-divergencias/README.md) | MySQL, MariaDB, SQL Server y Oracle: divergencias que rompen código | Las divergencias concretas que rompen código al cambiar de motor: el modo estricto de MySQL que convierte datos inválidos en silencio, la cadena va… | Intermedio | 3 |
| [033](part-05-motores-relacionales-y-dialectos/033-sqlite-y-duckdb-motores-embebidos/README.md) | SQLite y DuckDB: motores embebidos, transaccional frente a analítico | Los dos motores embebidos del programa y por qué no compiten entre sí: SQLite es transaccional y por filas, DuckDB es analítico, columnar y vectori… | Intermedio | 3 |

## [Parte 06 — Documentos y clave-valor](part-06-documentos-y-clave-valor/README.md)

Modelos sin reunión en el servidor: el agregado como frontera de consistencia, cuando incrustar y que se pierde en una caché.

La primera salida del relacional, y se hace por la puerta correcta: no por la moda, sino por una idea con nombre propio. El agregado es el conjunto de datos que se lee, se escribe y se mantiene consistente como una unidad, y en los motores documentales la frontera transaccional coincide con él. Diseñar el agregado es, por tanto, decidir dónde termina la garantía del motor y empieza el trabajo de tu aplicación.

*4 clases · 13 horas · 16 conceptos* — [portada de la parte, con la explicación de cada clase](part-06-documentos-y-clave-valor/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [034](part-06-documentos-y-clave-valor/034-el-agregado-como-unidad-de-consistencia/README.md) | El agregado como unidad de consistencia | El agregado como unidad de lectura, escritura y consistencia, y la consecuencia que ordena toda la parte: en los motores documentales la frontera t… | Intermedio | 3 |
| [035](part-06-documentos-y-clave-valor/035-modelado-documental-incrustar-o-referenciar/README.md) | Modelado documental: incrustar o referenciar | La decisión central del modelado documental —incrustar o referenciar— con sus dos criterios: si el dato se lee siempre junto y si puede crecer sin… | Intermedio | 4 |
| [036](part-06-documentos-y-clave-valor/036-consultas-e-indices-sobre-documentos/README.md) | Consultas, índices y agregación sobre documentos | Cómo se consulta e indexa lo que se modeló en la clase anterior: índices compuestos y multiclave, cobertura, y la canalización de agregación con la… | Intermedio | 3 |
| [037](part-06-documentos-y-clave-valor/037-clave-valor-cache-y-expiracion/README.md) | Clave-valor, caché y expiración: qué se pierde exactamente | Qué se gana y qué se pierde exactamente al poner una caché delante | Intermedio | 3 |

## [Parte 07 — Grafos, columnas, tiempo y búsqueda](part-07-grafos-columnas-tiempo-y-busqueda/README.md)

Modelos especializados y el criterio para saber cuando la carga de trabajo justifica salir del relacional.

Cinco familias especializadas y un mismo criterio para todas: qué carga de trabajo justifica salir del relacional, y qué se paga por hacerlo. La estructura de la parte es deliberadamente comparativa, porque el error habitual no es elegir mal el motor especializado, sino adoptarlo sin haber comprobado que el relacional ya no daba más.

*5 clases · 15 horas · 20 conceptos* — [portada de la parte, con la explicación de cada clase](part-07-grafos-columnas-tiempo-y-busqueda/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [038](part-07-grafos-columnas-tiempo-y-busqueda/038-grafos-de-propiedades-y-recorridos/README.md) | Grafos de propiedades y los recorridos que SQL hace mal | Los recorridos que SQL hace mal: profundidad variable, caminos y vecindarios | Intermedio | 3 |
| [039](part-07-grafos-columnas-tiempo-y-busqueda/039-columnas-anchas-modelar-desde-la-consulta/README.md) | Columnas anchas: modelar desde la consulta | El método de diseño invertido de las columnas anchas: primero se escribe la lista de consultas y después una tabla por consulta, aunque los mismos… | Avanzado | 3 |
| [040](part-07-grafos-columnas-tiempo-y-busqueda/040-series-temporales-cardinalidad-y-retencion/README.md) | Series temporales: cardinalidad, retención y agregados continuos | Las series temporales y sus tres restricciones propias: la cardinalidad de etiquetas, que explota si se usa un identificador como etiqueta; la rete… | Intermedio | 3 |
| [041](part-07-grafos-columnas-tiempo-y-busqueda/041-busqueda-de-texto-indice-invertido-y-relevancia/README.md) | Búsqueda de texto: índice invertido, análisis y relevancia | Por qué `LIKE '%algo%'` no es buscar | Intermedio | 3 |
| [042](part-07-grafos-columnas-tiempo-y-busqueda/042-analitica-columnar-y-vectorizacion/README.md) | Analítica columnar: por qué el formato cambia el orden de magnitud | De dónde salen realmente los dos órdenes de magnitud de la analítica: leer solo las columnas necesarias, comprimirlas mejor porque los valores cont… | Avanzado | 3 |

## [Parte 08 — Transacciones, concurrencia y recuperación](part-08-transacciones-concurrencia-y-recuperacion/README.md)

Que garantiza realmente ACID, que anomalías sobreviven en cada nivel de aislamiento y como se vuelve de una caída.

La parte donde el programa se pone serio con la corrección. Todo lo anterior asume implícitamente que las operaciones ocurren una detrás de otra y que la máquina no se apaga. Las cinco clases de aquí retiran esas dos suposiciones y muestran qué hace falta para que el sistema siga siendo correcto sin ellas.

*5 clases · 18 horas · 24 conceptos* — [portada de la parte, con la explicación de cada clase](part-08-transacciones-concurrencia-y-recuperacion/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [043](part-08-transacciones-concurrencia-y-recuperacion/043-acid-que-garantiza-cada-letra/README.md) | ACID: qué garantiza cada letra y quién la implementa | Qué garantiza cada letra de ACID y quién la implementa, con especial cuidado en la que más se malinterpreta: la consistencia es respetar las restri… | Intermedio | 3 |
| [044](part-08-transacciones-concurrencia-y-recuperacion/044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) | Anomalías de aislamiento y la crítica a los niveles ANSI | Las anomalías reales —lectura sucia, no repetible, fantasma y sesgo de escritura— y la crítica de Berenson y otros que demuestra que los niveles de… | Avanzado | 4 |
| [045](part-08-transacciones-concurrencia-y-recuperacion/045-bloqueo-en-dos-fases-y-mvcc/README.md) | Bloqueo en dos fases, MVCC e instantáneas | Las dos formas de sostener el aislamiento: bloqueo en dos fases, que hace esperar, y control de versiones, que hace copias | Avanzado | 4 |
| [046](part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md) | Registro anticipado y recuperación: WAL y ARIES | Cómo se vuelve de una caída | Avanzado | 4 |
| [047](part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md) | Concurrencia en la aplicación: idempotencia, reintentos y bloqueo optimista | La parte de la concurrencia que el motor no resuelve por ti | Avanzado | 3 |

## [Parte 09 — Almacenamiento, índices y planes](part-09-almacenamiento-indices-y-planes/README.md)

Por qué una consulta tarda: páginas, estructuras de índice, estadísticas y la lectura honesta de un plan de ejecución.

Por qué una consulta tarda, respondido desde el disco hacia arriba. La parte empieza donde de verdad empieza el costo —la página, no la fila— y termina en la única herramienta que convierte el rendimiento en un asunto de evidencia: el plan de ejecución.

*5 clases · 17 horas · 23 conceptos* — [portada de la parte, con la explicación de cada clase](part-09-almacenamiento-indices-y-planes/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [048](part-09-almacenamiento-indices-y-planes/048-paginas-filas-y-buffer-pool/README.md) | Páginas, filas y buffer: por qué la entrada y salida manda | Por qué la entrada y salida manda: el motor no lee filas, lee páginas | Intermedio | 3 |
| [049](part-09-almacenamiento-indices-y-planes/049-b-tree-orden-de-columnas-y-selectividad/README.md) | B-Tree: estructura, orden de columnas y selectividad | El B-Tree y las dos preguntas que responde en la práctica: en qué orden poner las columnas de un índice compuesto —la regla del prefijo más a la iz… | Intermedio | 4 |
| [050](part-09-almacenamiento-indices-y-planes/050-lsm-tree-compactacion-y-amplificacion/README.md) | LSM-Tree, compactación y amplificación de escritura | La otra familia de estructuras de almacenamiento: memtable, SSTable y compactación | Avanzado | 3 |
| [051](part-09-almacenamiento-indices-y-planes/051-indices-especializados/README.md) | Índices especializados: hash, GIN, GiST, BRIN, parciales y cubrientes | Los índices que no son B-Tree y el caso concreto en que cada uno gana: hash para igualdad pura, GIN para contenido de arreglos y documentos, GiST p… | Avanzado | 3 |
| [052](part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md) | Planes de ejecución: leer EXPLAIN y refutar una hipótesis | Leer un plan de ejecución para refutar una hipótesis, no para confirmarla | Avanzado | 4 |

## [Parte 10 — Distribución, réplica y consistencia](part-10-distribucion-replica-y-consistencia/README.md)

Qué se gana y qué se paga al repartir los datos: replicación, partición, los teoremas que acotan lo posible y el consenso.

Repartir los datos entre máquinas resuelve problemas de capacidad y de disponibilidad, y crea una clase entera de problemas nuevos que no existían en una sola máquina. Esta parte los nombra con precisión y acota lo que es teóricamente posible, para que las decisiones de arquitectura dejen de apoyarse en eslóganes.

*5 clases · 17 horas · 20 conceptos* — [portada de la parte, con la explicación de cada clase](part-10-distribucion-replica-y-consistencia/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [053](part-10-distribucion-replica-y-consistencia/053-replica-lider-unico-multilider-y-sin-lider/README.md) | Réplica: líder único, multilíder y sin líder | Las tres arquitecturas de réplica y el compromiso que define cada una | Avanzado | 4 |
| [054](part-10-distribucion-replica-y-consistencia/054-particionado-rebalanceo-y-claves-calientes/README.md) | Particionado, rebalanceo y claves calientes | Repartir los datos entre nodos sin crear un cuello de botella | Avanzado | 3 |
| [055](part-10-distribucion-replica-y-consistencia/055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) | CAP, PACELC y lo que realmente se elige | CAP dicho con precisión y despojado de la versión de póster | Avanzado | 3 |
| [056](part-10-distribucion-replica-y-consistencia/056-modelos-de-consistencia-y-garantias-de-sesion/README.md) | Modelos de consistencia y garantías de sesión | El espectro entre linealizabilidad y consistencia eventual, con las garantías de sesión —leer tu propia escritura, lectura monótona— que resuelven… | Avanzado | 3 |
| [057](part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) | Consenso y transacciones distribuidas: Raft, 2PC y sagas | Cómo se ponen de acuerdo varios nodos y cómo se confirma algo que abarca varios sistemas | Avanzado | 4 |

## [Parte 11 — Operación, seguridad y gobierno](part-11-operacion-seguridad-y-gobierno/README.md)

Lo que separa un ejercicio de un sistema: restauración probada, migraciones sin caída, control de acceso, observabilidad y privacidad.

Lo que separa un ejercicio de un sistema. Seis clases sobre las tareas que no aparecen en ningún tutorial de SQL y que son las que deciden si el sistema sobrevive a su segundo año: restaurar, migrar sin caída, controlar el acceso, no ser vulnerable, medir lo que los usuarios notan y tratar el dato personal como una obligación de diseño.

*6 clases · 19 horas · 24 conceptos* — [portada de la parte, con la explicación de cada clase](part-11-operacion-seguridad-y-gobierno/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [058](part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md) | Respaldo y restauración: solo cuenta lo que se ha restaurado | La clase que convierte una intención en una garantía medida | Intermedio | 4 |
| [059](part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md) | Migraciones evolutivas sin ventana de caída | Cambiar el esquema con el sistema en marcha, usando expandir y contraer: primero añadir sin quitar, después trasladar el tráfico y rellenar el hist… | Avanzado | 3 |
| [060](part-11-operacion-seguridad-y-gobierno/060-control-de-acceso-y-seguridad-por-fila/README.md) | Control de acceso: privilegio mínimo, roles y seguridad por fila | El control de acceso con una comprobación incómoda como punto de partida: si la aplicación se conecta como propietaria del esquema, no hay privileg… | Intermedio | 3 |
| [061](part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md) | Inyección SQL y el contrato de parametrización | La inyección SQL explicada por su causa —mezclar código y datos en la misma cadena— y su solución completa: la consulta parametrizada, que no es un… | Fundamentos | 3 |
| [062](part-11-operacion-seguridad-y-gobierno/062-observabilidad-slo-y-capacidad/README.md) | Observabilidad, objetivos de servicio y capacidad | Medir lo que los usuarios notan | Avanzado | 3 |
| [063](part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md) | Privacidad, retención y gobierno del dato | El dato personal como una obligación de diseño y no como un anexo legal | Intermedio | 3 |

## [Parte 12 — Analítica, integración y streaming](part-12-analitica-integracion-y-streaming/README.md)

Sacar los datos del sistema que los produjo sin perder su significado: almacen dimensional, captura de cambios y procesamiento continuo.

Sacar los datos del sistema que los produjo sin perder su significado. La parte parte de una pregunta operativa —por qué la analítica acaba mudándose a otro sistema— y la responde con dos argumentos independientes: el formato de almacenamiento, que decide el orden de magnitud, y la contención, que es el informe mensual compitiendo con las transacciones por el mismo buffer y el mismo disco.

*4 clases · 13 horas · 17 conceptos* — [portada de la parte, con la explicación de cada clase](part-12-analitica-integracion-y-streaming/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [064](part-12-analitica-integracion-y-streaming/064-oltp-frente-a-olap/README.md) | OLTP frente a OLAP: por qué se separan | Por qué la analítica acaba mudándose a otro sistema, con dos argumentos independientes: el formato de almacenamiento, que decide el orden de magnit… | Intermedio | 3 |
| [065](part-12-analitica-integracion-y-streaming/065-modelado-dimensional/README.md) | Modelado dimensional: hechos, dimensiones y cambios lentos | El modelo dimensional de Kimball, con el grano como primera decisión y la que no se corrige después sin rehacerlo todo | Intermedio | 4 |
| [066](part-12-analitica-integracion-y-streaming/066-integracion-etl-elt-y-captura-de-cambios/README.md) | Integración: ETL, ELT, captura de cambios y el registro como nexo | Mover datos entre sistemas sin perder cambios ni significado | Avanzado | 3 |
| [067](part-12-analitica-integracion-y-streaming/067-streaming-tiempo-de-evento-y-ventanas/README.md) | Streaming: tiempo de evento, ventanas y semántica de entrega | El procesamiento continuo y su distinción fundacional: tiempo de evento frente a tiempo de proceso | Avanzado | 3 |

## [Parte 13 — Vectores, recuperación y RAG](part-13-vectores-recuperacion-y-rag/README.md)

La base de datos como componente de un sistema de inteligencia artificial: distancias, indices aproximados y recuperación medida.

La base de datos como componente de un sistema de inteligencia artificial, tratada con el mismo rigor que el resto del programa: nada se da por bueno sin medirlo. Es la parte más nueva en fecha y la más expuesta a afirmaciones sin evidencia, así que es donde más se insiste en el conjunto de evaluación propio.

*4 clases · 13 horas · 19 conceptos* — [portada de la parte, con la explicación de cada clase](part-13-vectores-recuperacion-y-rag/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [068](part-13-vectores-recuperacion-y-rag/068-embeddings-y-metricas-de-distancia/README.md) | Embeddings y métricas de distancia: qué significa parecido | Qué significa «parecido» cuando lo decide un modelo | Intermedio | 3 |
| [069](part-13-vectores-recuperacion-y-rag/069-indices-vectoriales-aproximados/README.md) | Índices vectoriales aproximados: HNSW, IVF y el recall | Los índices que hacen viable la búsqueda vectorial renunciando a la exactitud | Avanzado | 4 |
| [070](part-13-vectores-recuperacion-y-rag/070-busqueda-hibrida-y-filtrado/README.md) | Búsqueda híbrida: léxica más vectorial y filtrado por metadatos | Por qué lo léxico y lo vectorial se combinan en lugar de competir: uno acierta con el término exacto, el otro con el significado | Avanzado | 3 |
| [071](part-13-vectores-recuperacion-y-rag/071-rag-evaluable/README.md) | RAG evaluable: medir la recuperación antes que la generación | Medir la recuperación antes de mirar la generación, porque si el fragmento correcto no entra en el contexto ningún modelo de lenguaje podrá respond… | Avanzado | 3 |

## [Parte 14 — Arquitectura y proyecto final](part-14-arquitectura-y-proyecto-final/README.md)

Cerrar el programa con una decisión defendible: comparación por evidencia, costo total y una demostración que se pueda auditar.

Tres clases para convertir catorce partes de conocimiento en una decisión que se pueda defender. No hay material nuevo de motores aquí: hay método, registro y defensa.

*3 clases · 12 horas · 13 conceptos* — [portada de la parte, con la explicación de cada clase](part-14-arquitectura-y-proyecto-final/README.md)

| # | Clase | En una línea | Nivel | Horas |
|---|---|---|---|---:|
| [072](part-14-arquitectura-y-proyecto-final/072-persistencia-poliglota-por-evidencia/README.md) | Persistencia políglota: decidir por evidencia y no por moda | La elección de motores hecha como decisión técnica: carga de trabajo cuantificada, criterio de comparación escrito antes de mirar los productos, y… | Avanzado | 3 |
| [073](part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md) | Registro de decisiones de arquitectura y costo total | Dejar constancia de por qué se decidió lo que se decidió | Avanzado | 3 |
| [074](part-14-arquitectura-y-proyecto-final/074-proyecto-final-disenar-medir-y-defender/README.md) | Proyecto final: diseñar, medir y defender | El cierre del programa: diseñar un sistema, medirlo y defenderlo ante preguntas hostiles | Avanzado | 6 |
