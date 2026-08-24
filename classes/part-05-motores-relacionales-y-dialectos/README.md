# Parte 05 — Motores relacionales y dialectos

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

Que exige la norma, que añade cada producto y como se escribe código que sobrevive a un cambio de motor.

**4 clases · 12 horas · 15 conceptos · 12 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 04 — SQL en profundidad](../part-04-sql-en-profundidad/README.md)

## De qué trata esta parte

SQL no es un lenguaje, son varios que se parecen. Esta parte separa lo que exige la norma ISO/IEC 9075 de lo que cada producto añade por su cuenta, y produce un artefacto revisable en lugar de una intención: una matriz que registra, construcción por construcción, si es de norma y cómo la escribe cada motor del proyecto.

Después de la matriz vienen tres estudios de caso elegidos por contraste. PostgreSQL, como ejemplo de motor extensible que absorbe familias enteras —vectores, geometría, series— sin dejar de ser relacional. El bloque MySQL, MariaDB, SQL Server y Oracle, centrado exclusivamente en las divergencias que rompen código: modo estricto, cadena vacía tratada como nulo, plegado de identificadores. Y los dos motores embebidos, SQLite y DuckDB, cuya comparación deja ver el efecto del formato de almacenamiento con la menor cantidad posible de ruido operativo.

El objetivo no es ser portable a toda costa. Es saber, línea a línea, cuándo estás atando el proyecto a un producto —lo que muchas veces es la decisión correcta— y cuándo lo estás haciendo sin darte cuenta.

## Al terminar esta parte podrás

1. Distinguir qué construcciones de una consulta son de norma y cuáles son extensiones del producto.
2. Mantener una matriz de portabilidad de las construcciones que el proyecto realmente usa.
3. Explicar tres divergencias entre motores que rompen código y demostrar cada una con un ejemplo ejecutable.
4. Elegir entre motor embebido y motor servidor, y entre orientación a filas y a columnas, con un argumento de carga de trabajo.

## Mapa de la parte

```mermaid
flowchart LR
    C030["030<br/>Portabilidad: qué exige la norma y qué añ…"]
    C031["031<br/>PostgreSQL: tipos, extensiones y modelo d…"]
    C032["032<br/>MySQL, MariaDB, SQL Server y Oracle: dive…"]
    C033["033<br/>SQLite y DuckDB: motores embebidos, trans…"]
    C030 --> C031
    C031 --> C032
    C032 --> C033
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C030 inter
    class C031 inter
    class C032 inter
    class C033 inter
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [030](030-portabilidad-y-matriz-de-dialectos/README.md) | [Portabilidad: qué exige la norma y qué añade cada motor](030-portabilidad-y-matriz-de-dialectos/README.md) | Intermedio | 3 | 4 |
| [031](031-postgresql-tipos-extensiones-y-procesos/README.md) | [PostgreSQL: tipos, extensiones y modelo de procesos](031-postgresql-tipos-extensiones-y-procesos/README.md) | Intermedio | 3 | 3 |
| [032](032-mysql-sqlserver-y-oracle-divergencias/README.md) | [MySQL, MariaDB, SQL Server y Oracle: divergencias que rompen código](032-mysql-sqlserver-y-oracle-divergencias/README.md) | Intermedio | 3 | 4 |
| [033](033-sqlite-y-duckdb-motores-embebidos/README.md) | [SQLite y DuckDB: motores embebidos, transaccional frente a analítico](033-sqlite-y-duckdb-motores-embebidos/README.md) | Intermedio | 3 | 3 |

## Las clases, una por una

### [030 — Portabilidad: qué exige la norma y qué añade cada motor](030-portabilidad-y-matriz-de-dialectos/README.md)

*Intermedio · 3 h · 4 fuentes · requiere [024](../part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md), [029](../part-04-sql-en-profundidad/029-nulos-y-logica-de-tres-valores/README.md)*

Qué exige la norma ISO/IEC 9075 y qué añade cada producto por su cuenta. El resultado de la clase no es una opinión sobre portabilidad sino un artefacto: una matriz que registra, construcción por construcción, si es de norma y cómo la escribe cada motor del proyecto.

**Conceptos que introduce:** `norma frente a producto` · `matriz de portabilidad` · `extensión propietaria`

[Ir a la clase →](030-portabilidad-y-matriz-de-dialectos/README.md)

### [031 — PostgreSQL: tipos, extensiones y modelo de procesos](031-postgresql-tipos-extensiones-y-procesos/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [012](../part-01-fundamentos-datos-sistemas-y-metodo/012-arquitectura-interna-de-un-gestor/README.md), [024](../part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md)*

PostgreSQL como caso de estudio de motor extensible: tipos compuestos, arreglos, rangos y JSONB de fábrica, extensiones que añaden vectores o geometría sin tocar el núcleo, y un modelo de proceso por conexión que explica por qué el agrupador de conexiones deja de ser opcional. Incluye autovacuum, que reaparece en la parte 08.

**Conceptos que introduce:** `extensión` · `tipo compuesto` · `proceso por conexión` · `autovacuum`

[Ir a la clase →](031-postgresql-tipos-extensiones-y-procesos/README.md)

### [032 — MySQL, MariaDB, SQL Server y Oracle: divergencias que rompen código](032-mysql-sqlserver-y-oracle-divergencias/README.md)

*Intermedio · 3 h · 4 fuentes · requiere [030](030-portabilidad-y-matriz-de-dialectos/README.md)*

Las divergencias concretas que rompen código al cambiar de motor: el modo estricto de MySQL que convierte datos inválidos en silencio, la cadena vacía que Oracle trata como nulo, y el plegado de mayúsculas de los identificadores sin citar. Cada una se demuestra con el `INSERT` que en un motor falla y en otro «funciona».

**Conceptos que introduce:** `colación` · `modo estricto` · `cadena vacia frente a nulo` · `identificador citado`

[Ir a la clase →](032-mysql-sqlserver-y-oracle-divergencias/README.md)

### [033 — SQLite y DuckDB: motores embebidos, transaccional frente a analítico](033-sqlite-y-duckdb-motores-embebidos/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [009](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/009-cuando-no-necesitas-una-base-de-datos/README.md), [031](031-postgresql-tipos-extensiones-y-procesos/README.md)*

Los dos motores embebidos del programa y por qué no compiten entre sí: SQLite es transaccional y por filas, DuckDB es analítico, columnar y vectorizado. La comparación deja ver, con la menor cantidad posible de ruido operativo, cómo el formato de almacenamiento decide el perfil de rendimiento.

**Conceptos que introduce:** `motor embebido` · `tipado dinamico` · `almacenamiento columnar` · `vectorización`

[Ir a la clase →](033-sqlite-y-duckdb-motores-embebidos/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «SQL es SQL.» Paginación, concatenación, tipos de fecha, `UPSERT` y comillas de identificadores divergen en todos los motores relevantes.
- «Usar una extensión propietaria es mala práctica.» A menudo es la decisión correcta. Lo malo es usarla sin saber que se está usando.
- «SQLite es una base de datos de juguete.» Es una de las piezas de software más desplegadas del planeta; su límite es la concurrencia de escritura y el servicio en red, no la seriedad.
- «DuckDB es SQLite para datos grandes.» Son motores con propósitos distintos: uno transaccional y por filas, otro analítico y columnar.

## Vocabulario de la parte

Los 15 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **almacenamiento columnar** | Guardar juntos todos los valores de una misma columna en lugar de todas las columnas de una misma fila. Una consulta analítica lee solo las columnas que necesita y comprime mucho mejor, porque los valores contiguos se parecen entre sí. | [033](033-sqlite-y-duckdb-motores-embebidos/README.md) |
| **autovacuum** | Proceso que recupera el espacio de las versiones de fila muertas que deja MVCC y actualiza las estadísticas del planificador. Cuando se queda atrás, la tabla se hincha y los planes se degradan: dos síntomas que se ven antes en el monitor que en el error. | [031](031-postgresql-tipos-extensiones-y-procesos/README.md) |
| **cadena vacia frente a nulo** | Divergencia que rompe código al migrar: Oracle trata la cadena vacía `''` como `NULL`, y el resto de motores la distingue. Una condición `= ''` cambia de significado según el producto, y un `NOT NULL` deja de proteger lo que se creía. | [032](032-mysql-sqlserver-y-oracle-divergencias/README.md) |
| **colación** | El conjunto de reglas que decide cómo se comparan y ordenan los textos: si `a` = `A`, dónde va la `ñ`, si los acentos cuentan. Cambia el resultado de `ORDER BY`, de `=` y de un `UNIQUE`, y es distinta por defecto en cada motor. | [032](032-mysql-sqlserver-y-oracle-divergencias/README.md) |
| **extensión** | Módulo cargable que añade tipos, operadores, índices o funciones a PostgreSQL sin tocar su núcleo: `pgvector`, `PostGIS`, `pg_stat_statements`. Es el mecanismo por el que un motor relacional cubre familias enteras —vectores, geometría, series— sin dejar de ser el mismo motor. | [031](031-postgresql-tipos-extensiones-y-procesos/README.md) |
| **extensión propietaria** | Sintaxis o función que solo existe en un motor: `LIMIT` frente a `FETCH FIRST`, `ON CONFLICT` frente a `MERGE`, tipos de arreglo, `RETURNING`. Usarlas es legítimo y a menudo correcto; lo que no lo es, es usarlas sin saber que se está atando el proyecto a ese producto. | [030](030-portabilidad-y-matriz-de-dialectos/README.md) |
| **identificador citado** | Nombre de objeto entre comillas dobles —o entre acentos graves en MySQL, entre corchetes en SQL Server—. Al citarlo se vuelve sensible a mayúsculas y se congela tal cual; sin citar, cada motor lo pliega a un caso distinto, y ahí nacen los «la tabla no existe» al cambiar de producto. | [032](032-mysql-sqlserver-y-oracle-divergencias/README.md) |
| **matriz de portabilidad** | Tabla que registra, para cada construcción usada, si es de norma y cómo la escribe cada motor del proyecto. Convierte la portabilidad en un artefacto revisable en lugar de en una intención declarada en la primera reunión. | [030](030-portabilidad-y-matriz-de-dialectos/README.md) |
| **modo estricto** | Ajuste que decide si el motor rechaza un dato inválido o lo convierte en silencio. MySQL sin modo estricto trunca cadenas y transforma fechas imposibles en ceros; el mismo `INSERT` que en PostgreSQL falla, allí «funciona» y corrompe. | [032](032-mysql-sqlserver-y-oracle-divergencias/README.md) |
| **motor embebido** | Base de datos que corre dentro del proceso de la aplicación, sin servidor ni puerto: SQLite, DuckDB. Elimina el costo de operación y la latencia de red, a cambio de no poder servir a varias máquinas. | [033](033-sqlite-y-duckdb-motores-embebidos/README.md) |
| **norma frente a producto** | La distinción entre lo que exige ISO/IEC 9075 y lo que cada motor añade por su cuenta. Ningún producto implementa la norma entera y todos la extienden; saber en qué lado está cada línea de tu código es lo que decide si una migración de motor cuesta un día o un trimestre. | [030](030-portabilidad-y-matriz-de-dialectos/README.md) |
| **proceso por conexión** | Modelo de PostgreSQL: cada conexión es un proceso del sistema operativo con su propia memoria. Es robusto —una caída no arrastra a las demás— y caro: por eso un agrupador de conexiones deja de ser un lujo a partir de unos cientos de clientes. | [031](031-postgresql-tipos-extensiones-y-procesos/README.md) |
| **tipado dinamico** | En SQLite el tipo pertenece al valor, no a la columna: la declaración es una sugerencia (afinidad) y no una barrera. Cómodo para prototipar, peligroso para datos que otro sistema leerá; desde la versión 3.37 existen las tablas `STRICT` para recuperar el rigor. | [033](033-sqlite-y-duckdb-motores-embebidos/README.md) |
| **tipo compuesto** | Tipo de dato definido por el usuario con varios campos, o los tipos estructurados que PostgreSQL trae de fábrica: arreglos, rangos, `JSONB`, tipos enumerados. Permiten modelar sin salir del relacional lo que en otros motores obligaría a una tabla más o a un documento. | [031](031-postgresql-tipos-extensiones-y-procesos/README.md) |
| **vectorización** | Procesar lotes de miles de valores por llamada en lugar de una fila cada vez. Amortiza el costo de interpretación del plan y aprovecha las instrucciones SIMD del procesador; es la segunda mitad —junto al formato columnar— de la ventaja analítica de DuckDB o ClickHouse. | [033](033-sqlite-y-duckdb-motores-embebidos/README.md) |

## Fuentes usadas en esta parte

12 obras distintas sostienen lo que se afirma en estas
4 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **Egor Rogov** (2022). [PostgreSQL 14 Internals](https://postgrespro.com/community/books/internals). Postgres Professional. ISBN 978-5-6041193-2-8.  
  PDF gratuito. MVCC, vacuum, buffers, índices y planificador sobre el código real.  
  *Se cita en las clases 031.*
- **Anthony Molinaro, Robert de Graaf** (2020). [SQL Cookbook](https://www.oreilly.com/library/view/sql-cookbook-2nd/9781492077435/). 2.a ed. O'Reilly. ISBN 978-1-4920-7744-2.  
  Recetas comparadas entre dialectos, útil para la matriz de portabilidad.  
  *Se cita en las clases 030.*
- **DuckDB Foundation** (2026). [DuckDB Documentation](https://duckdb.org/docs/).  
  Motor analítico embebido: OLAP columnar sin servidor.  
  *Se cita en las clases 033.*
- **MariaDB Foundation** (2026). [MariaDB Documentation](https://mariadb.com/docs/).  
  Divergencias respecto de MySQL relevantes para la portabilidad.  
  *Se cita en las clases 032.*
- **Oracle** (2026). [MySQL Reference Manual](https://dev.mysql.com/doc/).  
  Dialecto y comportamiento del motor InnoDB.  
  *Se cita en las clases 030, 032.*
- **Oracle** (2026). [Oracle Database Documentation](https://docs.oracle.com/en/database/).  
  PL/SQL y modelo de consistencia de lectura de Oracle.  
  *Se cita en las clases 032.*
- **PostgreSQL Global Development Group** (2026). [PostgreSQL Documentation](https://www.postgresql.org/docs/current/).  
  Documentación de referencia del motor relacional principal del programa.  
  *Se cita en las clases 030, 031.*
- **Microsoft** (2026). [SQL Server Documentation](https://learn.microsoft.com/sql/sql-server/).  
  T-SQL, niveles de aislamiento y almacen de consultas.  
  *Se cita en las clases 032.*
- **SQLite Consortium** (2026). [SQLite Documentation](https://sqlite.org/docs.html).  
  Motor embebido usado por los laboratorios sin dependencias del programa.  
  *Se cita en las clases 033.*
- **SQLite Consortium** (2026). [SQLite: Query Optimizer Overview](https://sqlite.org/optoverview.html).  
  Como decide SQLite usar un índice; útil para leer EXPLAIN QUERY PLAN.  
  *Se cita en las clases 033.*
- **Joseph M. Hellerstein, Michael Stonebraker, James Hamilton** (2007). [Architecture of a Database System](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf). Foundations and Trends in Databases 1(2). DOI [10.1561/1900000002](https://doi.org/10.1561/1900000002).  
  Descripción completa de los componentes internos de un SGBD relacional.  
  *Se cita en las clases 031.*
- **ISO/IEC JTC 1/SC 32** (2023). [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html).  
  Norma del lenguaje SQL. Ningún motor la implementa por completo.  
  *Se cita en las clases 030.*

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
- [Parte 06 — Documentos y clave-valor](../part-06-documentos-y-clave-valor/README.md)
- [Parte 07 — Grafos, columnas, tiempo y búsqueda](../part-07-grafos-columnas-tiempo-y-busqueda/README.md)
- [Parte 08 — Transacciones, concurrencia y recuperación](../part-08-transacciones-concurrencia-y-recuperacion/README.md)
- [Parte 09 — Almacenamiento, índices y planes](../part-09-almacenamiento-indices-y-planes/README.md)
- [Parte 10 — Distribución, réplica y consistencia](../part-10-distribucion-replica-y-consistencia/README.md)
- [Parte 11 — Operación, seguridad y gobierno](../part-11-operacion-seguridad-y-gobierno/README.md)
- [Parte 12 — Analítica, integración y streaming](../part-12-analitica-integracion-y-streaming/README.md)
- [Parte 13 — Vectores, recuperación y RAG](../part-13-vectores-recuperacion-y-rag/README.md)
- [Parte 14 — Arquitectura y proyecto final](../part-14-arquitectura-y-proyecto-final/README.md)
