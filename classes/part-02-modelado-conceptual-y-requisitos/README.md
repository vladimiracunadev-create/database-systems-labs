# Parte 02 — Modelado conceptual y requisitos

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

Del enunciado ambiguo al esquema defendible: entidades, claves, dependencias funcionales y la decisión consciente de desnormalizar.

**5 clases · 16 horas · 20 conceptos · 12 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 00 — Primeros pasos: del archivo a la base de datos](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/README.md)
- [Parte 01 — Fundamentos, sistemas y método](../part-01-fundamentos-datos-sistemas-y-metodo/README.md)

## De qué trata esta parte

Aquí empieza el trabajo de diseño. El material de entrada es lo que suele haber en la realidad: un enunciado ambiguo escrito por alguien que no piensa en tablas. El material de salida es un esquema que se puede defender frente a preguntas, no solo dibujar.

Las cinco clases forman una secuencia que va de lo blando a lo formal y vuelve. Primero se extraen entidades, reglas de negocio y un alcance escrito de lo que el modelo decide no representar. Después el modelo entidad-relación fija cardinalidad y participación, que son las dos decisiones que determinan dónde va cada clave foránea y si admite nulos. La tercera clase resuelve el debate de las claves con un criterio y no con preferencias. La cuarta introduce el aparato formal —dependencias funcionales, formas normales, descomposición sin pérdida— que convierte «esto está mal modelado» en una demostración. Y la quinta cierra el círculo dando permiso para desnormalizar, pero solo con un patrón de lectura medido y el costo de escritura aceptado por escrito.

La tensión entre las clases 018 y 019 es intencionada y no se resuelve a favor de ninguna: normalizar es la posición por defecto, desnormalizar es una decisión que hay que ganarse con datos.

## Al terminar esta parte podrás

1. Convertir un enunciado ambiguo en entidades, atributos y reglas de negocio explícitas.
2. Dibujar un modelo entidad-relación con cardinalidad y participación justificadas.
3. Elegir entre clave natural y sustituta argumentando desde la estabilidad de la identidad.
4. Demostrar con dependencias funcionales que un esquema alcanza la forma normal de Boyce-Codd.
5. Justificar una desnormalización con un patrón de lectura medido y un mecanismo de sincronización declarado.

## Mapa de la parte

```mermaid
flowchart LR
    C015["015<br/>De requisitos ambiguos a entidades defend…"]
    C016["016<br/>Entidad-relación, cardinalidad y particip…"]
    C017["017<br/>Claves, identidad y el debate natural fre…"]
    C018["018<br/>Normalización de 1FN a BCFN con dependenc…"]
    C019["019<br/>Desnormalización deliberada y patrones de…"]
    C015 --> C016
    C016 --> C017
    C017 --> C018
    C018 --> C019
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C015 fund
    class C016 fund
    class C017 fund
    class C018 inter
    class C019 inter
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [015](015-de-requisitos-a-entidades/README.md) | [De requisitos ambiguos a entidades defendibles](015-de-requisitos-a-entidades/README.md) | Fundamentos | 3 | 3 |
| [016](016-entidad-relacion-cardinalidad-y-participacion/README.md) | [Entidad-relación, cardinalidad y participación](016-entidad-relacion-cardinalidad-y-participacion/README.md) | Fundamentos | 3 | 3 |
| [017](017-claves-identidad-natural-y-sustituta/README.md) | [Claves, identidad y el debate natural frente a sustituta](017-claves-identidad-natural-y-sustituta/README.md) | Fundamentos | 3 | 3 |
| [018](018-normalizacion-y-dependencias-funcionales/README.md) | [Normalización de 1FN a BCFN con dependencias funcionales](018-normalizacion-y-dependencias-funcionales/README.md) | Intermedio | 4 | 4 |
| [019](019-desnormalizacion-deliberada/README.md) | [Desnormalización deliberada y patrones de acceso](019-desnormalizacion-deliberada/README.md) | Intermedio | 3 | 3 |

## Las clases, una por una

### [015 — De requisitos ambiguos a entidades defendibles](015-de-requisitos-a-entidades/README.md)

*Fundamentos · 3 h · 3 fuentes · requiere [001](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md), [008](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/008-dos-tablas-y-una-relacion/README.md)*

El paso del enunciado ambiguo a un conjunto de entidades que se puede defender. Trabaja tres herramientas: las reglas de negocio que acabarán siendo restricciones, el diccionario de datos que impide que dos equipos llamen igual a cosas distintas, y el alcance escrito de lo que el modelo decide no representar.

**Conceptos que introduce:** `regla de negocio` · `diccionario de datos` · `alcance` · `patrón de acceso`

[Ir a la clase →](015-de-requisitos-a-entidades/README.md)

### [016 — Entidad-relación, cardinalidad y participación](016-entidad-relacion-cardinalidad-y-participacion/README.md)

*Fundamentos · 3 h · 3 fuentes · requiere [015](015-de-requisitos-a-entidades/README.md)*

El modelo entidad-relación de Chen con las dos decisiones que más consecuencias tienen: la cardinalidad, que determina dónde va la clave foránea, y la participación, que determina si esa columna admite nulos. Introduce la entidad débil y el atributo que pertenece a la relación y no a ninguna de las dos entidades.

**Conceptos que introduce:** `entidad débil` · `cardinalidad` · `participación total` · `atributo de relación`

[Ir a la clase →](016-entidad-relacion-cardinalidad-y-participacion/README.md)

### [017 — Claves, identidad y el debate natural frente a sustituta](017-claves-identidad-natural-y-sustituta/README.md)

*Fundamentos · 3 h · 3 fuentes · requiere [007](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/007-la-clave-primaria/README.md), [016](016-entidad-relacion-cardinalidad-y-participacion/README.md)*

El debate entre clave natural y clave sustituta resuelto por un criterio y no por preferencia: cuál de las dos mantiene la identidad estable cuando el mundo cambia. La conclusión práctica —usar sustituta y proteger además la natural con `UNIQUE`— se aplica al resto del programa.

**Conceptos que introduce:** `clave candidata` · `clave primaria` · `clave sustituta` · `identidad estable`

[Ir a la clase →](017-claves-identidad-natural-y-sustituta/README.md)

### [018 — Normalización de 1FN a BCFN con dependencias funcionales](018-normalizacion-y-dependencias-funcionales/README.md)

*Intermedio · 4 h · 4 fuentes · requiere [008](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/008-dos-tablas-y-una-relacion/README.md), [016](016-entidad-relacion-cardinalidad-y-participacion/README.md)*

La normalización explicada como lo que es: una demostración a partir de dependencias funcionales, no una intuición sobre qué pertenece a qué. Recorre de la primera forma normal a la de Boyce-Codd y exige que cada descomposición sea sin pérdida, es decir, que reunir las tablas devuelva exactamente la original.

**Conceptos que introduce:** `dependencia funcional` · `anomalía de actualización` · `BCFN` · `descomposición sin pérdida`

[Ir a la clase →](018-normalizacion-y-dependencias-funcionales/README.md)

### [019 — Desnormalización deliberada y patrones de acceso](019-desnormalizacion-deliberada/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [018](018-normalizacion-y-dependencias-funcionales/README.md)*

El contrapeso de la clase anterior: cuándo duplicar a propósito. Exige tres cosas antes de desnormalizar —un patrón de lectura medido, un mecanismo declarado que mantenga las copias al día y el costo de escritura aceptado por escrito—, y así separa la redundancia controlada de la accidental.

**Conceptos que introduce:** `redundancia controlada` · `costo de escritura` · `agregado` · `patrón de lectura`

[Ir a la clase →](019-desnormalizacion-deliberada/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «Normalizar hasta la tercera forma normal y ya está.» La tercera forma normal deja pasar anomalías que BCFN elimina; el listón práctico de este programa es BCFN.
- «La normalización hace las consultas lentas.» La normalización cambia dónde está el costo. Sin medir el patrón de lectura, esa frase es una creencia.
- «El diagrama entidad-relación es documentación bonita.» Es donde se deciden cardinalidad y participación, que se traducen directamente en columnas, claves y nulos.
- «Uso UUID como clave primaria, así no hay debate.» Sigue habiendo debate: falta el `UNIQUE` sobre la clave natural, sin el cual el sistema admitirá duplicados del mundo real.

## Vocabulario de la parte

Los 20 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **agregado** | Conjunto de datos que se trata como una unidad para leer, escribir y garantizar consistencia: un pedido con sus líneas. Sadalage y Fowler lo toman del diseño dirigido por el dominio y lo convierten en el criterio que separa a los motores NoSQL del relacional. (En la clase 027 la palabra se usa en su otro sentido: el resultado de una función de agregación como `SUM` o `COUNT`.) | [019](019-desnormalizacion-deliberada/README.md) |
| **alcance** | Lo que el modelo decide representar y lo que decide ignorar. Kent lo formula sin rodeos: ningún modelo captura el mundo, siempre hay un recorte, y ese recorte es una decisión humana que conviene escribir en lugar de sufrir después. | [015](015-de-requisitos-a-entidades/README.md) |
| **anomalía de actualización** | Consecuencia de guardar un hecho en varias filas: corregirlo exige tocarlas todas, y la que se olvida deja la base contradiciéndose a sí misma. Junto con las anomalías de inserción y borrado, es lo que la normalización elimina. | [018](018-normalizacion-y-dependencias-funcionales/README.md) |
| **atributo de relación** | Dato que no pertenece a ninguna de las dos entidades sino al hecho de que estén relacionadas: la fecha de inscripción no es del estudiante ni del curso, es de la inscripción. Es la señal de que la tabla intermedia es una entidad de pleno derecho. | [016](016-entidad-relacion-cardinalidad-y-participacion/README.md) |
| **BCFN** | Forma normal de Boyce-Codd: toda dependencia funcional no trivial tiene como determinante una clave candidata. Es más estricta que la tercera forma normal y es el listón práctico de este programa para un esquema transaccional. | [018](018-normalizacion-y-dependencias-funcionales/README.md) |
| **cardinalidad** | Cuántas instancias de una entidad pueden relacionarse con cuántas de la otra: uno a uno, uno a muchos, muchos a muchos. Determina directamente dónde va la clave foránea y si hace falta una tabla intermedia. | [016](016-entidad-relacion-cardinalidad-y-participacion/README.md) |
| **clave candidata** | Cualquier conjunto mínimo de atributos que identifica unívocamente una fila. Una tabla puede tener varias; elegir una como primaria no anula a las demás, que deben seguir protegidas con `UNIQUE`. | [017](017-claves-identidad-natural-y-sustituta/README.md) |
| **clave primaria** | La clave candidata elegida para identificar cada fila: única, no nula y estable en el tiempo. Es la dirección por la que el resto del esquema se referirá a esa fila. | [017](017-claves-identidad-natural-y-sustituta/README.md) |
| **clave sustituta** | Identificador inventado por el sistema y sin significado externo: entero autoincremental, UUID. No cambia nunca porque no depende del mundo, a costa de necesitar además una restricción `UNIQUE` sobre la clave natural real. | [017](017-claves-identidad-natural-y-sustituta/README.md) |
| **costo de escritura** | Lo que se paga en cada `INSERT` o `UPDATE` por las copias, los índices y los agregados que hay que mantener coherentes. Toda aceleración de lectura por duplicación se cobra aquí; el diseño consiste en decidir de qué lado se quiere el dolor. | [019](019-desnormalizacion-deliberada/README.md) |
| **dependencia funcional** | Relación `X → Y`: conocido el valor de X queda determinado el de Y. Es la herramienta formal con la que se demuestra que una tabla está mal descompuesta, y no una intuición sobre qué «pertenece» a qué. | [018](018-normalizacion-y-dependencias-funcionales/README.md) |
| **descomposición sin pérdida** | Partir una tabla en dos de modo que reunirlas devuelva exactamente la original, ni una fila más ni una menos. Se garantiza cuando el atributo común es clave en al menos una de las dos; sin esa condición la normalización inventa datos. | [018](018-normalizacion-y-dependencias-funcionales/README.md) |
| **diccionario de datos** | La lista de cada atributo con su significado exacto, su tipo, su unidad y su origen. Es lo que impide que «fecha» signifique alta para un equipo y último acceso para otro. | [015](015-de-requisitos-a-entidades/README.md) |
| **entidad débil** | Entidad que no puede identificarse sin la entidad de la que depende: una línea de pedido existe solo dentro de su pedido. Su clave incluye la del padre, y su ciclo de vida termina cuando termina el del padre. | [016](016-entidad-relacion-cardinalidad-y-participacion/README.md) |
| **identidad estable** | La propiedad de que el identificador de una fila no cambie mientras la fila represente la misma cosa. Es el criterio real del debate entre clave natural y sustituta: no cuál es más elegante, sino cuál sobrevive a los cambios del mundo. | [017](017-claves-identidad-natural-y-sustituta/README.md) |
| **participación total** | Cuando toda instancia de una entidad debe participar obligatoriamente en la relación —todo pedido tiene un cliente—. Se traduce en `NOT NULL` sobre la clave foránea; la participación parcial admite el nulo. | [016](016-entidad-relacion-cardinalidad-y-participacion/README.md) |
| **patrón de acceso** | La lista concreta de consultas y escrituras que el sistema tendrá que servir, con su frecuencia y su latencia aceptable. Es el dato de entrada del diseño: sin él, elegir modelo o índice es adivinar. | [015](015-de-requisitos-a-entidades/README.md) |
| **patrón de lectura** | Qué se consulta, con qué filtros y con qué frecuencia. Es el argumento que justifica desnormalizar: sin una lectura dominante medida, duplicar datos es solo asumir el costo sin cobrar el beneficio. | [019](019-desnormalizacion-deliberada/README.md) |
| **redundancia controlada** | Duplicar un dato a propósito, sabiendo dónde está la copia y quién la mantiene al día. Se distingue de la redundancia accidental en que existe un mecanismo declarado de sincronización y un costo de escritura aceptado. | [019](019-desnormalizacion-deliberada/README.md) |
| **regla de negocio** | Una afirmación del dominio que el sistema debe respetar: «un estudiante no puede inscribirse dos veces en el mismo curso». Cada regla acaba en una restricción, en un índice único o en una prueba; la que no acaba en ninguna de las tres es solo una frase en un documento. | [015](015-de-requisitos-a-entidades/README.md) |

## Fuentes usadas en esta parte

12 obras distintas sostienen lo que se afirma en estas
5 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **William Kent** (2012). [Data and Reality](https://technicspub.com/data-and-reality/). 3.a ed. Technics Publications. ISBN 978-1-935504-21-4.  
  Por qué ningún modelo captura el mundo: fuente del criterio de alcance del programa.  
  *Se cita en las clases 015.*
- **Michael J. Hernandez** (2020). [Database Design for Mere Mortals](https://www.informit.com/store/database-design-for-mere-mortals-a-hands-on-guide-to-9780136788041). 4.a ed. Addison-Wesley. ISBN 978-0-13-678804-1.  
  Método de diseño paso a paso, independiente de producto.  
  *Se cita en las clases 015.*
- **Raghu Ramakrishnan, Johannes Gehrke** (2002). [Database Management Systems](https://pages.cs.wisc.edu/~dbbook/). 3.a ed. McGraw-Hill. ISBN 978-0-07-246563-1.  
  Fuerte en álgebra relacional, evaluación de consultas y estructuras de almacenamiento.  
  *Se cita en las clases 018.*
- **Abraham Silberschatz, Henry F. Korth, S. Sudarshan** (2019). [Database System Concepts](https://db-book.com/). 7.a ed. McGraw-Hill. ISBN 978-0-07-802215-9.  
  Texto de referencia universitario. El sitio oficial publica diapositivas y capítulos de muestra.  
  *Se cita en las clases 016, 017, 018.*
- **Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom** (2008). [Database Systems: The Complete Book](http://infolab.stanford.edu/~ullman/dscb.html). 2.a ed. Pearson. ISBN 978-0-13-187325-4.  
  Tratamiento formal de dependencias funcionales, normalización y optimización.  
  *Se cita en las clases 018.*
- **Martin Kleppmann** (2017). [Designing Data-Intensive Applications](https://dataintensive.net/). O'Reilly. ISBN 978-1-4493-7332-0.  
  Referencia central del programa para replicación, partición, transacciones distribuidas y streaming.  
  *Se cita en las clases 019.*
- **Ramez Elmasri, Shamkant B. Navathe** (2015). [Fundamentals of Database Systems](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003546). 7.a ed. Pearson. ISBN 978-0-13-397077-7.  
  Modelado entidad-relación tratado con más detalle que en otros manuales.  
  *Se cita en las clases 015, 016.*
- **Pramod J. Sadalage, Martin Fowler** (2012). [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html). Addison-Wesley. ISBN 978-0-321-82662-6.  
  Origen del término agregado y de la persistencia políglota que estructura este programa.  
  *Se cita en las clases 019.*
- **Bill Karwin** (2010). [SQL Antipatterns: Avoiding the Pitfalls of Database Programming](https://pragprog.com/titles/bksqla/sql-antipatterns/). Pragmatic Bookshelf. ISBN 978-1-934356-55-5.  
  Catálogo de errores de modelado con su corrección y cuando el antipatron es aceptable.  
  *Se cita en las clases 017, 019.*
- **C. J. Date** (2015). [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/). 3.a ed. O'Reilly. ISBN 978-1-4919-4117-1.  
  Separa el modelo relacional de lo que SQL realmente implementa, incluidos los nulos.  
  *Se cita en las clases 017.*
- **E. F. Codd** (1970). [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685). Communications of the ACM 13(6). DOI [10.1145/362384.362685](https://doi.org/10.1145/362384.362685).  
  Artículo fundacional del modelo relacional y de la independencia de datos.  
  *Se cita en las clases 018.*
- **Peter Pin-Shan Chen** (1976). [The Entity-Relationship Model - Toward a Unified View of Data](https://dl.acm.org/doi/10.1145/320434.320440). ACM TODS 1(1). DOI [10.1145/320434.320440](https://doi.org/10.1145/320434.320440).  
  Origen del diagrama entidad-relación.  
  *Se cita en las clases 016.*

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
