# Parte 01 — Fundamentos, sistemas y método

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

Qué problema resuelve un gestor de bases de datos, qué hay dentro de él y cómo se monta un entorno donde cada afirmación pueda comprobarse.

**4 clases · 12 horas · 19 conceptos · 11 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 00 — Primeros pasos: del archivo a la base de datos](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/README.md)

## De qué trata esta parte

La parte 00 mostró qué se hace con una base de datos. Esta pregunta por qué existe y qué hay dentro. Es la transición de usuario a persona que puede razonar sobre el sistema, y sin ella las partes 08 y 09 —transacciones y planes de ejecución— son magia con nombres técnicos.

Las cuatro clases responden a cuatro preguntas encadenadas. Qué garantiza un gestor y qué no, para no atribuirle poderes que no tiene. Qué componentes lo forman, del analizador al gestor de almacenamiento, para saber después en cuál vive cada problema. Por qué se separan tres niveles de esquema, que es la idea de Codd de la que depende toda la evolución del esquema sin caída. Y cómo se monta un entorno donde cada afirmación se pueda comprobar, que es el método de trabajo del resto del programa.

La clase 014 no es un anexo técnico: es la que define qué cuenta como evidencia en este programa. A partir de ella, ninguna afirmación de rendimiento se acepta sin comando, versión, semilla y salida.

## Al terminar esta parte podrás

1. Enumerar las garantías que aporta un gestor y nombrar al menos tres cosas que explícitamente no resuelve.
2. Trazar el recorrido de una consulta desde el cliente hasta el disco nombrando cada componente.
3. Distinguir esquema externo, conceptual y físico, y dar un ejemplo de cambio que cada nivel absorbe.
4. Montar un entorno reproducible con versión fijada, datos con semilla y evidencia repetible.

## Mapa de la parte

```mermaid
flowchart LR
    C011["011<br/>Qué resuelve un sistema de bases de datos…"]
    C012["012<br/>Arquitectura interna de un gestor, del cl…"]
    C013["013<br/>Independencia de datos y los tres niveles…"]
    C014["014<br/>Entorno reproducible y evidencia comprobable"]
    C011 --> C012
    C012 --> C013
    C013 --> C014
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C011 fund
    class C012 fund
    class C013 fund
    class C014 fund
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [011](011-que-resuelve-un-sistema-de-bases-de-datos/README.md) | [Qué resuelve un sistema de bases de datos y qué no](011-que-resuelve-un-sistema-de-bases-de-datos/README.md) | Fundamentos | 3 | 4 |
| [012](012-arquitectura-interna-de-un-gestor/README.md) | [Arquitectura interna de un gestor, del cliente al disco](012-arquitectura-interna-de-un-gestor/README.md) | Fundamentos | 3 | 3 |
| [013](013-independencia-de-datos-y-niveles-de-esquema/README.md) | [Independencia de datos y los tres niveles de esquema](013-independencia-de-datos-y-niveles-de-esquema/README.md) | Fundamentos | 3 | 3 |
| [014](014-entorno-reproducible-y-evidencia/README.md) | [Entorno reproducible y evidencia comprobable](014-entorno-reproducible-y-evidencia/README.md) | Fundamentos | 3 | 4 |

## Las clases, una por una

### [011 — Qué resuelve un sistema de bases de datos y qué no](011-que-resuelve-un-sistema-de-bases-de-datos/README.md)

*Fundamentos · 3 h · 4 fuentes · requiere [002](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md), [010](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/010-el-mapa-de-los-motores/README.md)*

La misma pregunta de la clase 002, ahora con el vocabulario de sistemas: qué garantiza un gestor —persistencia, concurrencia, integridad, recuperación— y, con la misma seriedad, qué no garantiza. La independencia de datos aparece aquí como la idea de Codd que ordena todo lo demás.

**Conceptos que introduce:** `persistencia` · `concurrencia` · `integridad` · `recuperación` · `independencia de datos`

[Ir a la clase →](011-que-resuelve-un-sistema-de-bases-de-datos/README.md)

### [012 — Arquitectura interna de un gestor, del cliente al disco](012-arquitectura-interna-de-un-gestor/README.md)

*Fundamentos · 3 h · 3 fuentes · requiere [011](011-que-resuelve-un-sistema-de-bases-de-datos/README.md)*

El recorrido completo de una consulta desde el cliente hasta el disco: analizador, planificador, ejecutor, gestor de almacenamiento y buffer. Es el mapa mental que después permite leer un plan de ejecución sin adivinar, y saber en qué componente vive cada problema de rendimiento.

**Conceptos que introduce:** `analizador` · `planificador` · `ejecutor` · `gestor de almacenamiento` · `buffer pool`

[Ir a la clase →](012-arquitectura-interna-de-un-gestor/README.md)

### [013 — Independencia de datos y los tres niveles de esquema](013-independencia-de-datos-y-niveles-de-esquema/README.md)

*Fundamentos · 3 h · 3 fuentes · requiere [011](011-que-resuelve-un-sistema-de-bases-de-datos/README.md)*

Los tres niveles de esquema —externo, conceptual y físico— y por qué separarlos es lo que permite añadir un índice, particionar una tabla o dividir una entidad sin reescribir las aplicaciones. La independencia lógica que se define aquí es el fundamento técnico de las migraciones sin caída de la parte 11.

**Conceptos que introduce:** `esquema conceptual` · `esquema físico` · `vista externa` · `independencia lógica`

[Ir a la clase →](013-independencia-de-datos-y-niveles-de-esquema/README.md)

### [014 — Entorno reproducible y evidencia comprobable](014-entorno-reproducible-y-evidencia/README.md)

*Fundamentos · 3 h · 4 fuentes · requiere [011](011-que-resuelve-un-sistema-de-bases-de-datos/README.md)*

El método de trabajo del resto del programa: entorno en contenedor con la versión fijada, datos generados con semilla declarada, invariantes escritos y evidencia que otra persona pueda reproducir. Es la clase que convierte «me funcionó» en un resultado defendible.

**Conceptos que introduce:** `reproducibilidad` · `semilla` · `contenedor` · `invariante` · `evidencia`

[Ir a la clase →](014-entorno-reproducible-y-evidencia/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «El motor garantiza que mis datos sean correctos.» Solo garantiza lo que le declaraste. Lo que no está en una restricción no está protegido.
- «El motor ejecuta la consulta como la escribí.» Ejecuta el plan que su optimizador estimó más barato; el orden del texto es casi irrelevante.
- «Independencia de datos es que la aplicación no vea el motor.» No: es poder cambiar cómo se guardan los datos sin reescribir lo que los consulta.
- «Lo medí y va rápido.» Sin versión, datos y semilla declarados, eso no es una medición, es una anécdota.

## Vocabulario de la parte

Los 19 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **analizador** | Primer componente del gestor: convierte el texto SQL en un árbol sintáctico y comprueba que los objetos citados existen y que los tipos encajan. Aquí mueren los errores de sintaxis, antes de tocar un solo dato. (En la clase 041 la misma palabra nombra otra cosa: el analizador de texto que parte un documento en términos indexables.) | [012](012-arquitectura-interna-de-un-gestor/README.md) |
| **buffer pool** | La memoria donde el motor mantiene las páginas leídas para no volver a pedirlas al disco. Su tasa de acierto explica la mayor parte de la diferencia entre una consulta de 2 ms y la misma consulta de 200 ms. | [012](012-arquitectura-interna-de-un-gestor/README.md) |
| **concurrencia** | Varias sesiones leyendo y escribiendo a la vez sobre los mismos datos. Un archivo compartido no la resuelve: el último en guardar pisa al anterior. Un gestor la resuelve con transacciones, bloqueo o versiones. | [011](011-que-resuelve-un-sistema-de-bases-de-datos/README.md) |
| **contenedor** | Entorno de ejecución aislado con el motor y su versión congelados. Elimina el «en mi máquina funciona» y convierte la versión del motor en parte de la evidencia, no en un detalle olvidado. | [014](014-entorno-reproducible-y-evidencia/README.md) |
| **ejecutor** | Recorre el plan elegido operador a operador y produce las filas. Es donde `EXPLAIN ANALYZE` muestra los tiempos reales frente a los que el planificador había estimado. | [012](012-arquitectura-interna-de-un-gestor/README.md) |
| **esquema conceptual** | La descripción del qué: entidades, atributos y relaciones del dominio, sin decir cómo se guardan. Es el nivel en el que se discute con quien conoce el negocio. | [013](013-independencia-de-datos-y-niveles-de-esquema/README.md) |
| **esquema físico** | Cómo se materializan realmente los datos: ficheros, páginas, índices, particiones, compresión. Debe poder cambiar —añadir un índice, particionar una tabla— sin que ninguna consulta se reescriba. | [013](013-independencia-de-datos-y-niveles-de-esquema/README.md) |
| **evidencia** | La salida real de un comando, con su versión y sus parámetros, que respalda una afirmación. Una captura sin comando no es evidencia, porque no se puede repetir. | [014](014-entorno-reproducible-y-evidencia/README.md) |
| **gestor de almacenamiento** | La capa que traduce filas a páginas en disco y de vuelta, y que sostiene el registro, el buffer y las estructuras de índice. Es donde se decide si el motor es B-Tree o LSM, y con ello su perfil de lectura y escritura. | [012](012-arquitectura-interna-de-un-gestor/README.md) |
| **independencia de datos** | Poder cambiar cómo se guardan los datos sin reescribir las aplicaciones que los consultan. Es la idea central del artículo de Codd de 1970 y la razón de que exista un nivel lógico separado del físico. | [011](011-que-resuelve-un-sistema-de-bases-de-datos/README.md) |
| **independencia lógica** | Poder cambiar el esquema conceptual —dividir una tabla, renombrar una columna— sin romper las aplicaciones, apoyándose en vistas que preservan el contrato anterior. Es más difícil de lograr que la independencia física y es la base técnica de las migraciones sin caída. | [013](013-independencia-de-datos-y-niveles-de-esquema/README.md) |
| **integridad** | Que los datos cumplan siempre las reglas del dominio, incluidas las que ninguna aplicación recordó comprobar. El gestor la sostiene con restricciones declaradas y con transacciones. | [011](011-que-resuelve-un-sistema-de-bases-de-datos/README.md) |
| **invariante** | Algo que tiene que ser verdad siempre en el sistema: «ningún pedido sin cliente», «el saldo nunca es negativo». Un invariante que no está comprobado por una restricción o una prueba es un deseo. | [014](014-entorno-reproducible-y-evidencia/README.md) |
| **persistencia** | Que el dato siga existiendo cuando el proceso que lo escribió ya no está. Es el requisito mínimo de una base de datos y la única de sus funciones que un archivo también cumple. | [011](011-que-resuelve-un-sistema-de-bases-de-datos/README.md) |
| **planificador** | Decide *cómo* ejecutar la consulta: qué índice usar, en qué orden reunir las tablas, con qué algoritmo. Elige por costo estimado a partir de estadísticas, no por el orden en que está escrita la consulta. | [012](012-arquitectura-interna-de-un-gestor/README.md) |
| **recuperación** | Volver a un estado correcto después de una caída, descartando lo no confirmado y rehaciendo lo confirmado. Es lo que distingue una base de datos de un archivo que se corrompió a medio escribir. | [011](011-que-resuelve-un-sistema-de-bases-de-datos/README.md) |
| **reproducibilidad** | Que otra persona, en otra máquina, obtenga el mismo resultado con las instrucciones dadas. Exige fijar versión del motor, datos de partida y semilla; sin eso, una medición es una anécdota. | [014](014-entorno-reproducible-y-evidencia/README.md) |
| **semilla** | El número que fija la secuencia de un generador pseudoaleatorio. Declararla convierte un conjunto de datos «aleatorio» en uno reproducible, que es la condición para poder comparar dos ejecuciones. | [014](014-entorno-reproducible-y-evidencia/README.md) |
| **vista externa** | La porción del esquema que ve cada aplicación o cada rol, normalmente mediante vistas. Permite dar acceso a lo necesario y solo a eso, y absorber cambios del esquema sin romper a quien consulta. | [013](013-independencia-de-datos-y-niveles-de-esquema/README.md) |

## Fuentes usadas en esta parte

11 obras distintas sostienen lo que se afirma en estas
4 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **William Kent** (2012). [Data and Reality](https://technicspub.com/data-and-reality/). 3.a ed. Technics Publications. ISBN 978-1-935504-21-4.  
  Por qué ningún modelo captura el mundo: fuente del criterio de alcance del programa.  
  *Se cita en las clases 011.*
- **Alex Petrov** (2019). [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/). O'Reilly. ISBN 978-1-4920-4034-7.  
  Motor de almacenamiento (B-Tree y LSM) y consenso explicados con detalle de implementación.  
  *Se cita en las clases 012.*
- **Abraham Silberschatz, Henry F. Korth, S. Sudarshan** (2019). [Database System Concepts](https://db-book.com/). 7.a ed. McGraw-Hill. ISBN 978-0-07-802215-9.  
  Texto de referencia universitario. El sitio oficial publica diapositivas y capítulos de muestra.  
  *Se cita en las clases 011, 013.*
- **Egor Rogov** (2022). [PostgreSQL 14 Internals](https://postgrespro.com/community/books/internals). Postgres Professional. ISBN 978-5-6041193-2-8.  
  PDF gratuito. MVCC, vacuum, buffers, índices y planificador sobre el código real.  
  *Se cita en las clases 012.*
- **C. J. Date** (2015). [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/). 3.a ed. O'Reilly. ISBN 978-1-4919-4117-1.  
  Separa el modelo relacional de lo que SQL realmente implementa, incluidos los nulos.  
  *Se cita en las clases 013.*
- **Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy** (2016). [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/). O'Reilly. ISBN 978-1-4919-2912-4.  
  Lectura libre. Objetivos de nivel de servicio y presupuesto de error.  
  *Se cita en las clases 014.*
- **Docker, Inc.** (2026). [Docker Compose Documentation](https://docs.docker.com/compose/).  
  Perfiles y comprobaciones de salud usados por los laboratorios con contenedores.  
  *Se cita en las clases 014.*
- **Python Software Foundation** (2026). [Python: sqlite3](https://docs.python.org/3/library/sqlite3.html).  
  API DB-API 2.0 usada por los laboratorios ejecutables del repositorio.  
  *Se cita en las clases 014.*
- **SQLite Consortium** (2026). [SQLite Documentation](https://sqlite.org/docs.html).  
  Motor embebido usado por los laboratorios sin dependencias del programa.  
  *Se cita en las clases 014.*
- **E. F. Codd** (1970). [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685). Communications of the ACM 13(6). DOI [10.1145/362384.362685](https://doi.org/10.1145/362384.362685).  
  Artículo fundacional del modelo relacional y de la independencia de datos.  
  *Se cita en las clases 011, 013.*
- **Joseph M. Hellerstein, Michael Stonebraker, James Hamilton** (2007). [Architecture of a Database System](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf). Foundations and Trends in Databases 1(2). DOI [10.1561/1900000002](https://doi.org/10.1561/1900000002).  
  Descripción completa de los componentes internos de un SGBD relacional.  
  *Se cita en las clases 011, 012.*

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
- [Parte 02 — Modelado conceptual y requisitos](../part-02-modelado-conceptual-y-requisitos/README.md)
- [Parte 03 — Modelo relacional y álgebra](../part-03-modelo-relacional-y-algebra/README.md)
- [Parte 04 — SQL en profundidad](../part-04-sql-en-profundidad/README.md)
- [Parte 05 — Motores relacionales y dialectos](../part-05-motores-relacionales-y-dialectos/README.md)
- [Parte 06 — Documentos y clave-valor](../part-06-documentos-y-clave-valor/README.md)
- [Parte 07 — Grafos, columnas, tiempo y búsqueda](../part-07-grafos-columnas-tiempo-y-busqueda/README.md)
- [Parte 08 — Transacciones, concurrencia y recuperación](../part-08-transacciones-concurrencia-y-recuperacion/README.md)
- [Parte 09 — Almacenamiento, índices y planes](../part-09-almacenamiento-indices-y-planes/README.md)
- [Parte 10 — Distribución, réplica y consistencia](../part-10-distribucion-replica-y-consistencia/README.md)
- [Parte 11 — Operación, seguridad y gobierno](../part-11-operacion-seguridad-y-gobierno/README.md)
- [Parte 12 — Analítica, integración y streaming](../part-12-analitica-integracion-y-streaming/README.md)
- [Parte 13 — Vectores, recuperación y RAG](../part-13-vectores-recuperacion-y-rag/README.md)
- [Parte 14 — Arquitectura y proyecto final](../part-14-arquitectura-y-proyecto-final/README.md)
