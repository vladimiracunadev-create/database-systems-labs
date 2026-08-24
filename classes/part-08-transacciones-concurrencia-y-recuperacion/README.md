# Parte 08 — Transacciones, concurrencia y recuperación

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

Que garantiza realmente ACID, que anomalías sobreviven en cada nivel de aislamiento y como se vuelve de una caída.

**5 clases · 18 horas · 24 conceptos · 15 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 04 — SQL en profundidad](../part-04-sql-en-profundidad/README.md)

## De qué trata esta parte

La parte donde el programa se pone serio con la corrección. Todo lo anterior asume implícitamente que las operaciones ocurren una detrás de otra y que la máquina no se apaga. Las cinco clases de aquí retiran esas dos suposiciones y muestran qué hace falta para que el sistema siga siendo correcto sin ellas.

ACID primero, con cuidado especial en la letra que más se malinterpreta: la consistencia es respetar las restricciones declaradas, así que lo que el motor no sabe no lo protege. Después las anomalías reales y la crítica de Berenson y otros, que demuestra que los niveles de la norma no las definen sin ambigüedad —de ahí que el nivel por defecto de tu motor no sea el que crees y haya que comprobarlo experimentalmente—. Luego los dos mecanismos que sostienen el aislamiento: bloqueo, que hace esperar, y versiones, que hacen copias. Después la recuperación, con el registro anticipado y ARIES. Y al final la parte que el motor no resuelve por ti: idempotencia, reintentos y bloqueo optimista en la aplicación.

Es la parte con más laboratorio por clase del programa, y no por casualidad: las anomalías de aislamiento se creen cuando se ven ocurrir en dos sesiones abiertas al mismo tiempo.

## Al terminar esta parte podrás

1. Explicar qué garantiza cada letra de ACID y quién implementa cada garantía.
2. Reproducir experimentalmente una lectura no repetible, un fantasma y un sesgo de escritura.
3. Explicar por qué con MVCC las lecturas no bloquean y qué costo de mantenimiento genera.
4. Describir la recuperación tras una caída en términos de registro, punto de control, rehacer y deshacer.
5. Diseñar una operación idempotente con clave de idempotencia y reintento con retroceso.

## Mapa de la parte

```mermaid
flowchart LR
    C043["043<br/>ACID: qué garantiza cada letra y quién la…"]
    C044["044<br/>Anomalías de aislamiento y la crítica a l…"]
    C045["045<br/>Bloqueo en dos fases, MVCC e instantáneas"]
    C046["046<br/>Registro anticipado y recuperación: WAL y…"]
    C047["047<br/>Concurrencia en la aplicación: idempotenc…"]
    C043 --> C044
    C044 --> C045
    C045 --> C046
    C046 --> C047
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C043 inter
    class C044 avan
    class C045 avan
    class C046 avan
    class C047 avan
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [043](043-acid-que-garantiza-cada-letra/README.md) | [ACID: qué garantiza cada letra y quién la implementa](043-acid-que-garantiza-cada-letra/README.md) | Intermedio | 3 | 3 |
| [044](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) | [Anomalías de aislamiento y la crítica a los niveles ANSI](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) | Avanzado | 4 | 5 |
| [045](045-bloqueo-en-dos-fases-y-mvcc/README.md) | [Bloqueo en dos fases, MVCC e instantáneas](045-bloqueo-en-dos-fases-y-mvcc/README.md) | Avanzado | 4 | 3 |
| [046](046-registro-anticipado-y-recuperacion/README.md) | [Registro anticipado y recuperación: WAL y ARIES](046-registro-anticipado-y-recuperacion/README.md) | Avanzado | 4 | 3 |
| [047](047-concurrencia-en-la-aplicacion/README.md) | [Concurrencia en la aplicación: idempotencia, reintentos y bloqueo optimista](047-concurrencia-en-la-aplicacion/README.md) | Avanzado | 3 | 3 |

## Las clases, una por una

### [043 — ACID: qué garantiza cada letra y quién la implementa](043-acid-que-garantiza-cada-letra/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [005](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/005-cambiar-datos-insert-update-delete/README.md), [023](../part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md)*

Qué garantiza cada letra de ACID y quién la implementa, con especial cuidado en la que más se malinterpreta: la consistencia es respetar las restricciones declaradas, así que lo que el motor no sabe no lo protege. Deja planteado que el aislamiento es la única letra que se vende por niveles.

**Conceptos que introduce:** `atomicidad` · `consistencia` · `aislamiento` · `durabilidad` · `unidad de recuperación`

[Ir a la clase →](043-acid-que-garantiza-cada-letra/README.md)

### [044 — Anomalías de aislamiento y la crítica a los niveles ANSI](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md)

*Avanzado · 4 h · 5 fuentes · requiere [043](043-acid-que-garantiza-cada-letra/README.md)*

Las anomalías reales —lectura sucia, no repetible, fantasma y sesgo de escritura— y la crítica de Berenson y otros que demuestra que los niveles de la norma no las definen sin ambigüedad. La consecuencia práctica es que el nivel por defecto de tu motor no es el que crees y hay que comprobarlo experimentalmente.

**Conceptos que introduce:** `lectura sucia` · `lectura no repetible` · `fantasma` · `sesgo de escritura` · `snapshot isolation`

[Ir a la clase →](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md)

### [045 — Bloqueo en dos fases, MVCC e instantáneas](045-bloqueo-en-dos-fases-y-mvcc/README.md)

*Avanzado · 4 h · 3 fuentes · requiere [044](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md)*

Las dos formas de sostener el aislamiento: bloqueo en dos fases, que hace esperar, y control de versiones, que hace copias. Explica por qué con MVCC las lecturas no bloquean, y también su factura escondida: las versiones muertas que el vacuum tiene que recoger.

**Conceptos que introduce:** `2PL` · `versión de fila` · `instantánea` · `interbloqueo` · `vacuum`

[Ir a la clase →](045-bloqueo-en-dos-fases-y-mvcc/README.md)

### [046 — Registro anticipado y recuperación: WAL y ARIES](046-registro-anticipado-y-recuperacion/README.md)

*Avanzado · 4 h · 3 fuentes · requiere [043](043-acid-que-garantiza-cada-letra/README.md)*

Cómo se vuelve de una caída. El registro anticipado escribe la intención antes que el dato, el punto de control acorta la recuperación y ARIES ordena las fases de rehacer y deshacer de modo que repetirlas sea inofensivo —lo que permite recuperarse de una caída ocurrida durante la recuperación.

**Conceptos que introduce:** `WAL` · `punto de control` · `rehacer` · `deshacer` · `LSN`

[Ir a la clase →](046-registro-anticipado-y-recuperacion/README.md)

### [047 — Concurrencia en la aplicación: idempotencia, reintentos y bloqueo optimista](047-concurrencia-en-la-aplicacion/README.md)

*Avanzado · 3 h · 3 fuentes · requiere [045](045-bloqueo-en-dos-fases-y-mvcc/README.md)*

La parte de la concurrencia que el motor no resuelve por ti. Trata la idempotencia como la única defensa realista frente a una red que no distingue «no llegó» de «se perdió la respuesta», y el bloqueo optimista y el reintento con retroceso como los dos patrones que toda aplicación con transacciones acaba necesitando.

**Conceptos que introduce:** `idempotencia` · `clave de idempotencia` · `bloqueo optimista` · `reintento con retroceso`

[Ir a la clase →](047-concurrencia-en-la-aplicacion/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «Mi motor es ACID, entonces mis transacciones son serializables.» El nivel por defecto casi nunca es serializable: suele ser `READ COMMITTED` o snapshot.
- «Snapshot isolation elimina todas las anomalías.» Deja pasar el sesgo de escritura, que es justo el que rompe invariantes de negocio.
- «MVCC no tiene costo.» Cada versión muerta hay que recogerla; cuando el vacuum se queda atrás, la tabla se hincha y los planes se degradan.
- «Si la transacción falla, reintento y ya.» Solo si la operación es idempotente. Si no, el reintento cobra dos veces.

## Vocabulario de la parte

Los 24 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **2PL** | Bloqueo en dos fases: una fase en la que la transacción solo adquiere cerrojos y otra en la que solo los libera. Es la técnica clásica que garantiza serializabilidad, al precio de que los lectores bloqueen a los escritores. | [045](045-bloqueo-en-dos-fases-y-mvcc/README.md) |
| **aislamiento** | Grado en que una transacción concurrente no ve los pasos intermedios de otra. Es la única letra de ACID que se vende por niveles, y el nivel por defecto de casi todos los motores no es el más fuerte. | [043](043-acid-que-garantiza-cada-letra/README.md) |
| **atomicidad** | Todo o nada: la transacción se aplica entera o no deja rastro. No promete que sea correcta ni que sea rápida, solo que no habrá estados a medias visibles para nadie. | [043](043-acid-que-garantiza-cada-letra/README.md) |
| **bloqueo optimista** | En lugar de bloquear, se lee una versión y al escribir se comprueba que no haya cambiado (`WHERE version = ?`). Si cambió, se reintenta. Rinde mejor que el bloqueo cuando los conflictos son raros, y peor cuando son frecuentes. | [047](047-concurrencia-en-la-aplicacion/README.md) |
| **clave de idempotencia** | Identificador que el cliente genera y envía con la petición para que el servidor reconozca un reintento y devuelva el resultado anterior en lugar de ejecutar dos veces. Es cómo se cobra una tarjeta una sola vez aunque el navegador reenvíe. | [047](047-concurrencia-en-la-aplicacion/README.md) |
| **consistencia** | La letra tramposa de ACID: significa que la transacción lleva la base de un estado válido a otro *según las restricciones declaradas*. Lo que el motor no sabe, no lo protege; la consistencia de negocio la pone quien declara las reglas, no el gestor. | [043](043-acid-que-garantiza-cada-letra/README.md) |
| **deshacer** | Fase que revierte las transacciones que estaban a medias en el momento de la caída, usando la información de deshacer del registro. Es la implementación concreta de la atomicidad. | [046](046-registro-anticipado-y-recuperacion/README.md) |
| **durabilidad** | Una vez confirmada la transacción, su efecto sobrevive a un corte de luz. Se consigue escribiendo el cambio en un registro secuencial y forzándolo al disco antes de responder «hecho». | [043](043-acid-que-garantiza-cada-letra/README.md) |
| **fantasma** | Repetir una consulta por rango y encontrar filas nuevas que otra transacción insertó. No es un cambio de valor sino de pertenencia al conjunto, y por eso exige bloquear el rango —o usar instantáneas— y no solo las filas leídas. | [044](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) |
| **idempotencia** | Propiedad de una operación que, repetida con la misma entrada, deja el mismo estado que ejecutarla una vez. Es la única defensa realista contra las redes: en un sistema distribuido no se puede distinguir «no llegó» de «llegó y se perdió la respuesta». | [047](047-concurrencia-en-la-aplicacion/README.md) |
| **instantánea** | El conjunto de versiones visibles para una transacción, fijado en un instante. Permite que las lecturas no bloqueen y que dos consultas de la misma transacción vean exactamente lo mismo aunque el mundo cambie alrededor. | [045](045-bloqueo-en-dos-fases-y-mvcc/README.md) |
| **interbloqueo** | Dos transacciones que se esperan mutuamente porque cada una tiene el cerrojo que la otra necesita. El motor lo detecta y aborta a una; la aplicación debe estar preparada para reintentar, y ordenar siempre los accesos igual reduce la frecuencia. | [045](045-bloqueo-en-dos-fases-y-mvcc/README.md) |
| **lectura no repetible** | Leer la misma fila dos veces dentro de una transacción y obtener valores distintos, porque otra confirmó un cambio en medio. Es lo que `READ COMMITTED` permite y `REPEATABLE READ` impide. | [044](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) |
| **lectura sucia** | Leer un dato que otra transacción escribió y todavía no confirmó —y que puede acabar deshaciéndose—. Solo la permite el nivel `READ UNCOMMITTED`, que casi ningún motor usa por defecto. | [044](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) |
| **LSN** | Número de secuencia del registro: identifica cada entrada del WAL en orden y se estampa en la página que modifica. Permite saber, página por página, si un cambio ya está aplicado —y por eso rehacer se puede repetir sin efectos secundarios. | [046](046-registro-anticipado-y-recuperacion/README.md) |
| **punto de control** | Marca periódica que fija hasta dónde están ya volcadas a disco las páginas modificadas. Acorta la recuperación, porque tras una caída solo hay que releer el registro desde el último punto de control y no desde el principio de los tiempos. | [046](046-registro-anticipado-y-recuperacion/README.md) |
| **rehacer** | Fase de la recuperación que reaplica desde el registro todo lo confirmado que aún no había llegado a las páginas de datos. ARIES la ejecuta antes de deshacer y de forma que repetirla sea inofensiva, lo que permite recuperarse de una caída ocurrida durante la recuperación. | [046](046-registro-anticipado-y-recuperacion/README.md) |
| **reintento con retroceso** | Reintentar tras un fallo esperando cada vez más tiempo, con una componente aleatoria. El retroceso evita hundir un sistema que ya está en apuros y la aleatoriedad evita que todos los clientes vuelvan sincronizados a la vez. | [047](047-concurrencia-en-la-aplicacion/README.md) |
| **sesgo de escritura** | Dos transacciones leen el mismo conjunto, cada una decide que puede escribir, y juntas rompen un invariante que ninguna rompía por separado —los dos médicos de guardia que se dan de baja a la vez—. Snapshot isolation lo permite; hace falta serializable o un bloqueo explícito. | [044](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) |
| **snapshot isolation** | Cada transacción ve una fotografía coherente de la base tomada al empezar. Elimina lecturas sucias, no repetibles y fantasmas, pero no el sesgo de escritura; es el nivel que PostgreSQL llama `REPEATABLE READ`. | [044](044-anomalias-de-aislamiento-y-la-critica-ansi/README.md) |
| **unidad de recuperación** | La transacción como frontera de lo que se rehace o se deshace tras una caída. Es lo que conecta ACID con el registro anticipado: sin transacción no hay nada que delimite qué debe sobrevivir. | [043](043-acid-que-garantiza-cada-letra/README.md) |
| **vacuum** | Proceso que recupera el espacio de las versiones de fila que ya nadie puede ver y actualiza los mapas de visibilidad. Sin él, MVCC crece sin límite: es el mantenimiento invisible que explica por qué una tabla ocupa el triple de lo que debería. | [045](045-bloqueo-en-dos-fases-y-mvcc/README.md) |
| **versión de fila** | Copia de una fila con el rango de transacciones para las que es visible. Con MVCC un `UPDATE` no sobrescribe: crea una versión nueva, de modo que quien está leyendo la anterior no se detiene. El precio es el espacio y el trabajo de limpiarlo. | [045](045-bloqueo-en-dos-fases-y-mvcc/README.md) |
| **WAL** | Registro anticipado: antes de tocar la página de datos se escribe en un registro secuencial qué se va a cambiar, y ese registro se fuerza al disco antes de confirmar. Es lo que hace posible la durabilidad sin escribir cada página en cada `COMMIT`. | [046](046-registro-anticipado-y-recuperacion/README.md) |

## Fuentes usadas en esta parte

15 obras distintas sostienen lo que se afirma en estas
5 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **Alex Petrov** (2019). [Database Internals: A Deep Dive into How Distributed Data Systems Work](https://www.databass.dev/). O'Reilly. ISBN 978-1-4920-4034-7.  
  Motor de almacenamiento (B-Tree y LSM) y consenso explicados con detalle de implementación.  
  *Se cita en las clases 046.*
- **Abraham Silberschatz, Henry F. Korth, S. Sudarshan** (2019). [Database System Concepts](https://db-book.com/). 7.a ed. McGraw-Hill. ISBN 978-0-07-802215-9.  
  Texto de referencia universitario. El sitio oficial publica diapositivas y capítulos de muestra.  
  *Se cita en las clases 043.*
- **Martin Kleppmann** (2017). [Designing Data-Intensive Applications](https://dataintensive.net/). O'Reilly. ISBN 978-1-4493-7332-0.  
  Referencia central del programa para replicación, partición, transacciones distribuidas y streaming.  
  *Se cita en las clases 047.*
- **Egor Rogov** (2022). [PostgreSQL 14 Internals](https://postgrespro.com/community/books/internals). Postgres Professional. ISBN 978-5-6041193-2-8.  
  PDF gratuito. MVCC, vacuum, buffers, índices y planificador sobre el código real.  
  *Se cita en las clases 045.*
- **Philip A. Bernstein, Eric Newcomer** (2009). [Principles of Transaction Processing](https://www.sciencedirect.com/book/9781558606234/principles-of-transaction-processing). 2.a ed. Morgan Kaufmann. ISBN 978-1-55860-623-4.  
  Enfoque de sistemas: monitores transaccionales, colas y commit en dos fases.  
  *Se cita en las clases 047.*
- **Jim Gray, Andreas Reuter** (1992). [Transaction Processing: Concepts and Techniques](https://www.sciencedirect.com/book/9781558601901/transaction-processing). Morgan Kaufmann. ISBN 978-1-55860-190-1.  
  Obra canónica sobre ACID, bloqueo, registro y recuperación.  
  *Se cita en las clases 043, 045.*
- **Martin Kleppmann** (2014). [Hermitage: Testing Transaction Isolation Levels](https://github.com/ept/hermitage).  
  Guion reproducible que muestra que anomalías permite cada motor en cada nivel.  
  *Se cita en las clases 044.*
- **PostgreSQL Global Development Group** (2026). [PostgreSQL: Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html).  
  Niveles de aislamiento tal como los implementa PostgreSQL, no como los define la norma.  
  *Se cita en las clases 044, 045.*
- **SQLite Consortium** (2026). [SQLite: Isolation](https://sqlite.org/isolation.html).  
  Que garantiza y que no garantiza SQLite entre conexiones.  
  *Se cita en las clases 044.*
- **SQLite Consortium** (2026). [SQLite: Write-Ahead Logging](https://sqlite.org/wal.html).  
  Registro anticipado explicado en un motor lo bastante pequeno para leerlo entero.  
  *Se cita en las clases 046.*
- **Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil, Patrick O'Neil** (1995). [A Critique of ANSI SQL Isolation Levels](https://arxiv.org/abs/cs/0701157). ACM SIGMOD. DOI [10.1145/223784.223785](https://doi.org/10.1145/223784.223785).  
  Demuestra que los niveles de la norma no definen sin ambigüedad las anomalías e introduce snapshot isolation.  
  *Se cita en las clases 044.*
- **C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz** (1992). [ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging](https://dl.acm.org/doi/10.1145/128765.128770). ACM TODS 17(1). DOI [10.1145/128765.128770](https://doi.org/10.1145/128765.128770).  
  Algoritmo de recuperación con registro anticipado que implementan casi todos los motores.  
  *Se cita en las clases 046.*
- **Pat Helland** (2007). [Life beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf). CIDR.  
  Entidades, actividades y por qué las transacciones distribuidas no escalan.  
  *Se cita en las clases 047.*
- **Jim Gray** (1981). [The Transaction Concept: Virtues and Limitations](https://jimgray.azurewebsites.net/papers/thetransactionconcept.pdf). VLDB.  
  Define la transacción como unidad de consistencia y recuperación.  
  *Se cita en las clases 043.*
- **Atul Adya** (1999). [Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions](http://pmg.csail.mit.edu/papers/adya-phd.pdf). Tesis doctoral, MIT.  
  Definición de los fenomenos de aislamiento independiente de la implementación.  
  *Se cita en las clases 044.*

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
- [Parte 09 — Almacenamiento, índices y planes](../part-09-almacenamiento-indices-y-planes/README.md)
- [Parte 10 — Distribución, réplica y consistencia](../part-10-distribucion-replica-y-consistencia/README.md)
- [Parte 11 — Operación, seguridad y gobierno](../part-11-operacion-seguridad-y-gobierno/README.md)
- [Parte 12 — Analítica, integración y streaming](../part-12-analitica-integracion-y-streaming/README.md)
- [Parte 13 — Vectores, recuperación y RAG](../part-13-vectores-recuperacion-y-rag/README.md)
- [Parte 14 — Arquitectura y proyecto final](../part-14-arquitectura-y-proyecto-final/README.md)
