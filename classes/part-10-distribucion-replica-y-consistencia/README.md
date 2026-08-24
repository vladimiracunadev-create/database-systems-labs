# Parte 10 — Distribución, réplica y consistencia

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

Qué se gana y qué se paga al repartir los datos: replicación, partición, los teoremas que acotan lo posible y el consenso.

**5 clases · 17 horas · 20 conceptos · 17 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 08 — Transacciones, concurrencia y recuperación](../part-08-transacciones-concurrencia-y-recuperacion/README.md)

## De qué trata esta parte

Repartir los datos entre máquinas resuelve problemas de capacidad y de disponibilidad, y crea una clase entera de problemas nuevos que no existían en una sola máquina. Esta parte los nombra con precisión y acota lo que es teóricamente posible, para que las decisiones de arquitectura dejen de apoyarse en eslóganes.

Réplica primero, con las tres arquitecturas y la consecuencia que el usuario nota: guardar algo y al recargar no verlo. Después particionado, con los dos esquemas de reparto y el punto caliente que cada uno genera. Luego CAP dicho con precisión —la disponibilidad del teorema es mucho más estricta que el noventa y nueve coma nueve del lenguaje operativo— y PACELC, que añade lo que CAP calla: el compromiso entre latencia y consistencia existe también los días en que no hay avería. Después el espectro de modelos de consistencia con las garantías de sesión que resuelven en la práctica la mayoría de los síntomas. Y al final consenso, commit en dos fases y sagas.

Es la parte más citada del programa en fuentes primarias: Gilbert y Lynch, Brewer, Abadi, Lamport, Ongaro, DeCandia y Corbett. Merece leerse con los artículos abiertos al lado.

## Al terminar esta parte podrás

1. Elegir entre líder único, multilíder y sin líder según el patrón de escritura y la tolerancia a conflictos.
2. Diseñar un esquema de particionado que evite puntos calientes y permita rebalancear.
3. Enunciar CAP con precisión y explicar por qué «elegir dos de tres» es una simplificación errónea.
4. Elegir el modelo de consistencia y las garantías de sesión que el caso realmente necesita.
5. Comparar consenso, commit en dos fases y saga por lo que cada uno bloquea y garantiza.

## Mapa de la parte

```mermaid
flowchart LR
    C053["053<br/>Réplica: líder único, multilíder y sin líder"]
    C054["054<br/>Particionado, rebalanceo y claves calientes"]
    C055["055<br/>CAP, PACELC y lo que realmente se elige"]
    C056["056<br/>Modelos de consistencia y garantías de se…"]
    C057["057<br/>Consenso y transacciones distribuidas: Ra…"]
    C053 --> C054
    C054 --> C055
    C055 --> C056
    C056 --> C057
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C053 avan
    class C054 avan
    class C055 avan
    class C056 avan
    class C057 avan
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [053](053-replica-lider-unico-multilider-y-sin-lider/README.md) | [Réplica: líder único, multilíder y sin líder](053-replica-lider-unico-multilider-y-sin-lider/README.md) | Avanzado | 4 | 3 |
| [054](054-particionado-rebalanceo-y-claves-calientes/README.md) | [Particionado, rebalanceo y claves calientes](054-particionado-rebalanceo-y-claves-calientes/README.md) | Avanzado | 3 | 3 |
| [055](055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) | [CAP, PACELC y lo que realmente se elige](055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) | Avanzado | 3 | 4 |
| [056](056-modelos-de-consistencia-y-garantias-de-sesion/README.md) | [Modelos de consistencia y garantías de sesión](056-modelos-de-consistencia-y-garantias-de-sesion/README.md) | Avanzado | 3 | 5 |
| [057](057-consenso-y-transacciones-distribuidas/README.md) | [Consenso y transacciones distribuidas: Raft, 2PC y sagas](057-consenso-y-transacciones-distribuidas/README.md) | Avanzado | 4 | 4 |

## Las clases, una por una

### [053 — Réplica: líder único, multilíder y sin líder](053-replica-lider-unico-multilider-y-sin-lider/README.md)

*Avanzado · 4 h · 3 fuentes · requiere [043](../part-08-transacciones-concurrencia-y-recuperacion/043-acid-que-garantiza-cada-letra/README.md), [046](../part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md)*

Las tres arquitecturas de réplica y el compromiso que define cada una. La consecuencia visible para el usuario es el retraso de réplica: guardar algo y al recargar no verlo. Introduce las garantías de sesión que lo tapan y el quórum de los sistemas sin líder.

**Conceptos que introduce:** `replicación sincrónica` · `retraso de réplica` · `quórum` · `lectura de tu propia escritura`

[Ir a la clase →](053-replica-lider-unico-multilider-y-sin-lider/README.md)

### [054 — Particionado, rebalanceo y claves calientes](054-particionado-rebalanceo-y-claves-calientes/README.md)

*Avanzado · 3 h · 3 fuentes · requiere [039](../part-07-grafos-columnas-tiempo-y-busqueda/039-columnas-anchas-modelar-desde-la-consulta/README.md), [053](053-replica-lider-unico-multilider-y-sin-lider/README.md)*

Repartir los datos entre nodos sin crear un cuello de botella. Compara hash consistente y partición por rango por lo que cada una permite y por el punto caliente que cada una genera, y explica por qué el rebalanceo se diseña fijando muchas más particiones que nodos desde el principio.

**Conceptos que introduce:** `hash consistente` · `partición por rango` · `punto caliente` · `reequilibrio`

[Ir a la clase →](054-particionado-rebalanceo-y-claves-calientes/README.md)

### [055 — CAP, PACELC y lo que realmente se elige](055-cap-pacelc-y-lo-que-realmente-se-elige/README.md)

*Avanzado · 3 h · 4 fuentes · requiere [053](053-replica-lider-unico-multilider-y-sin-lider/README.md)*

CAP dicho con precisión y despojado de la versión de póster. La disponibilidad del teorema es mucho más estricta que el «99,9 % de tiempo activo» del lenguaje operativo, y confundirlas es el origen de casi todas las lecturas erróneas. PACELC añade lo que CAP calla: el compromiso entre latencia y consistencia existe también los días en que no hay avería.

**Conceptos que introduce:** `partición de red` · `disponibilidad` · `latencia frente a consistencia`

[Ir a la clase →](055-cap-pacelc-y-lo-que-realmente-se-elige/README.md)

### [056 — Modelos de consistencia y garantías de sesión](056-modelos-de-consistencia-y-garantias-de-sesion/README.md)

*Avanzado · 3 h · 5 fuentes · requiere [055](055-cap-pacelc-y-lo-que-realmente-se-elige/README.md)*

El espectro entre linealizabilidad y consistencia eventual, con las garantías de sesión —leer tu propia escritura, lectura monótona— que resuelven en la práctica la mayoría de los síntomas visibles. Insiste en que la consistencia eventual solo converge si existe una regla determinista de resolución de conflictos.

**Conceptos que introduce:** `linealizabilidad` · `consistencia causal` · `lectura monotona` · `convergencia`

[Ir a la clase →](056-modelos-de-consistencia-y-garantias-de-sesion/README.md)

### [057 — Consenso y transacciones distribuidas: Raft, 2PC y sagas](057-consenso-y-transacciones-distribuidas/README.md)

*Avanzado · 4 h · 4 fuentes · requiere [055](055-cap-pacelc-y-lo-que-realmente-se-elige/README.md), [047](../part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md)*

Cómo se ponen de acuerdo varios nodos y cómo se confirma algo que abarca varios sistemas. Raft para el consenso y la elección de líder, el commit en dos fases con su fragilidad conocida —el coordinador que cae dejando cerrojos tomados— y la saga con compensaciones como la alternativa que renuncia al aislamiento para no bloquear.

**Conceptos que introduce:** `consenso` · `elección de líder` · `commit en dos fases` · `saga` · `compensación`

[Ir a la clase →](057-consenso-y-transacciones-distribuidas/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «CAP dice que elijas dos de tres.» El propio Brewer lo corrigió: cuando no hay partición no hay que renunciar a nada, y cuando la hay se elige entre consistencia y disponibilidad solo durante la partición.
- «Consistencia eventual significa que al final se arregla solo.» Solo converge si existe una regla determinista de resolución de conflictos. Sin ella, diverge para siempre.
- «Añado réplicas de lectura y escalo.» Añades retraso de réplica, que es un cambio de semántica visible para el usuario, no solo un ajuste de capacidad.
- «El commit en dos fases resuelve las transacciones distribuidas.» Es correcto y es bloqueante: si el coordinador cae entre las dos fases, los participantes quedan con los cerrojos tomados.

## Vocabulario de la parte

Los 20 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **commit en dos fases** | Protocolo para confirmar una transacción que abarca varios sistemas: primero se pregunta a todos si pueden, después se les ordena confirmar. Es correcto y es frágil: si el coordinador cae entre las dos fases, los participantes quedan bloqueados con los cerrojos tomados. | [057](057-consenso-y-transacciones-distribuidas/README.md) |
| **compensación** | Operación de negocio que deshace el efecto de otra ya confirmada: reembolsar en vez de revertir, anular una reserva en vez de borrarla. No es un `ROLLBACK`, porque el estado intermedio existió y alguien pudo verlo. | [057](057-consenso-y-transacciones-distribuidas/README.md) |
| **consenso** | Que un conjunto de nodos se ponga de acuerdo en un valor y no cambie de opinión, tolerando caídas de una minoría. Es el cimiento de la elección de líder, de la pertenencia al clúster y del commit atómico; Raft y Paxos son las dos formulaciones de referencia. | [057](057-consenso-y-transacciones-distribuidas/README.md) |
| **consistencia causal** | Si un evento pudo influir en otro, todos los observadores los ven en ese orden; los eventos sin relación causal pueden verse en cualquier orden. Es el punto dulce entre lo débil y lo caro: evita el efecto «respuesta antes que la pregunta» sin exigir coordinación global. | [056](056-modelos-de-consistencia-y-garantias-de-sesion/README.md) |
| **convergencia** | Que las réplicas acaben en el mismo estado si cesan las escrituras. Es la promesa de la consistencia eventual, y solo se cumple si hay una regla determinista de resolución de conflictos, como la que dan los CRDT. | [056](056-modelos-de-consistencia-y-garantias-de-sesion/README.md) |
| **disponibilidad** | En el enunciado formal de CAP, que toda petición a un nodo no caído reciba respuesta. Es una definición mucho más estricta que el «99,9 % de tiempo activo» del lenguaje operativo, y confundirlas es el origen de casi todas las lecturas erróneas del teorema. | [055](055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) |
| **elección de líder** | Procedimiento por el que la mayoría acuerda quién ordena las escrituras durante un mandato. Que se necesite mayoría es lo que impide dos líderes simultáneos —el escenario de cerebro dividido— cuando la red se parte. | [057](057-consenso-y-transacciones-distribuidas/README.md) |
| **hash consistente** | Reparto de claves sobre un anillo de posiciones de modo que añadir o quitar un nodo mueva solo una fracción de los datos, y no obligue a redistribuirlo todo como haría un `hash mod N`. Es la base del rebalanceo en Dynamo y Cassandra. | [054](054-particionado-rebalanceo-y-claves-calientes/README.md) |
| **latencia frente a consistencia** | La mitad de PACELC que CAP ignora: incluso sin particiones hay que elegir entre responder rápido desde una réplica cercana o esperar la coordinación que garantiza el dato más reciente. Es el compromiso que se paga todos los días, no solo el día de la avería. | [055](055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) |
| **lectura de tu propia escritura** | Garantía de sesión que asegura que quien acaba de escribir verá su propio cambio, aunque otros aún no. Se implementa dirigiendo al líder las lecturas recientes de ese usuario, o esperando a que la réplica alcance el LSN de su escritura. | [053](053-replica-lider-unico-multilider-y-sin-lider/README.md) |
| **lectura monotona** | Garantía de sesión que impide retroceder en el tiempo: si ya viste un valor, no volverás a ver uno anterior. Sin ella, alternar entre réplicas con distinto retraso hace que un dato aparezca y desaparezca al recargar. | [056](056-modelos-de-consistencia-y-garantias-de-sesion/README.md) |
| **linealizabilidad** | La garantía más fuerte para un objeto: el sistema se comporta como si hubiera una sola copia y cada operación ocurriera en un instante entre su inicio y su fin. Es cara porque exige coordinación, y casi ninguna aplicación la necesita para todo. | [056](056-modelos-de-consistencia-y-garantias-de-sesion/README.md) |
| **partición de red** | Situación en la que dos grupos de nodos siguen vivos pero no pueden comunicarse. No es un fallo hipotético: es lo que ocurre con un cable, un cortafuegos mal aplicado o una latencia lo bastante alta como para que los tiempos de espera venzan. | [055](055-cap-pacelc-y-lo-que-realmente-se-elige/README.md) |
| **partición por rango** | Repartir por intervalos ordenados de la clave. Permite consultas por rango eficientes, a costa de generar puntos calientes cuando las escrituras se concentran al final del rango —el caso típico de una clave temporal. | [054](054-particionado-rebalanceo-y-claves-calientes/README.md) |
| **punto caliente** | Partición que recibe una parte desproporcionada del tráfico: la celebridad con millones de seguidores, la fecha de hoy, el cliente que factura el 40 %. Ninguna cantidad de nodos ayuda mientras el reparto siga concentrando ahí. | [054](054-particionado-rebalanceo-y-claves-calientes/README.md) |
| **quórum** | Regla de los sistemas sin líder: si las escrituras van a W réplicas, las lecturas consultan R, y `W + R > N`, entonces toda lectura toca al menos una réplica con el último valor. Permite ajustar el compromiso entre latencia y frescura por operación. | [053](053-replica-lider-unico-multilider-y-sin-lider/README.md) |
| **reequilibrio** | Mover particiones entre nodos al cambiar la capacidad del clúster. La práctica recomendada es fijar de antemano muchas más particiones que nodos y mover particiones enteras, en lugar de recalcular la asignación de cada clave. | [054](054-particionado-rebalanceo-y-claves-calientes/README.md) |
| **replicación sincrónica** | El líder no confirma la escritura hasta que al menos una réplica la ha recibido. Garantiza que no se pierda al caer el líder, a cambio de que la latencia del cliente incluya la de la réplica más lenta y de que una réplica caída pueda detener las escrituras. | [053](053-replica-lider-unico-multilider-y-sin-lider/README.md) |
| **retraso de réplica** | La distancia temporal entre lo que ya está en el líder y lo que la réplica ha aplicado. Con replicación asíncrona es inevitable, y es la causa directa de que un usuario guarde algo y al recargar no lo vea. | [053](053-replica-lider-unico-multilider-y-sin-lider/README.md) |
| **saga** | Secuencia de transacciones locales, cada una con su compensación, que sustituye a una transacción distribuida. Renuncia al aislamiento —los estados intermedios se ven— a cambio de no bloquear recursos entre servicios. | [057](057-consenso-y-transacciones-distribuidas/README.md) |

## Fuentes usadas en esta parte

17 obras distintas sostienen lo que se afirma en estas
5 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **Martin Kleppmann** (2017). [Designing Data-Intensive Applications](https://dataintensive.net/). O'Reilly. ISBN 978-1-4493-7332-0.  
  Referencia central del programa para replicación, partición, transacciones distribuidas y streaming.  
  *Se cita en las clases 053, 054.*
- **Apache Software Foundation** (2026). [Apache Cassandra Documentation](https://cassandra.apache.org/doc/latest/).  
  CQL, claves de partición y niveles de consistencia ajustables.  
  *Se cita en las clases 054.*
- **Kyle Kingsbury** (2026). [Jepsen: Analyses](https://jepsen.io/analyses).  
  Informes que verifican empiricamente las garantías que cada motor afirma.  
  *Se cita en las clases 056.*
- **Kyle Kingsbury** (2026). [Jepsen: Consistency Models](https://jepsen.io/consistency).  
  Mapa de modelos de consistencia y sus relaciones de implicación.  
  *Se cita en las clases 056.*
- **Seth Gilbert, Nancy Lynch** (2002). [Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services](https://dl.acm.org/doi/10.1145/564585.564601). ACM SIGACT News 33(2). DOI [10.1145/564585.564601](https://doi.org/10.1145/564585.564601).  
  Demostración formal del teorema CAP y de su enunciado exacto.  
  *Se cita en las clases 055.*
- **Eric Brewer** (2012). [CAP Twelve Years Later: How the Rules Have Changed](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/). IEEE Computer 45(2). DOI [10.1109/MC.2012.37](https://doi.org/10.1109/MC.2012.37).  
  El propio autor corrige la lectura simplista de elegir dos de tres.  
  *Se cita en las clases 055.*
- **Marc Shapiro, Nuno Preguica, Carlos Baquero, Marek Zawirski** (2011). [Conflict-free Replicated Data Types](https://inria.hal.science/inria-00609399/document). SSS.  
  Estructuras que convergen sin coordinación: alternativa al bloqueo distribuido.  
  *Se cita en las clases 056.*
- **Daniel J. Abadi** (2012). [Consistency Tradeoffs in Modern Distributed Database System Design](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf). IEEE Computer 45(2). DOI [10.1109/MC.2012.33](https://doi.org/10.1109/MC.2012.33).  
  PACELC: el compromiso latencia-consistencia existe también sin particiones.  
  *Se cita en las clases 055.*
- **Giuseppe DeCandia, Deniz Hastorun, Madan Jampani** (2007). [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf). ACM SOSP. DOI [10.1145/1294261.1294281](https://doi.org/10.1145/1294261.1294281).  
  Hash consistente, quorums ajustables y reconciliación en el cliente.  
  *Se cita en las clases 053, 054.*
- **Werner Vogels** (2009). [Eventually Consistent](https://dl.acm.org/doi/10.1145/1435417.1435432). Communications of the ACM 52(1). DOI [10.1145/1435417.1435432](https://doi.org/10.1145/1435417.1435432).  
  Definición operativa de consistencia eventual y de sus variantes de sesión.  
  *Se cita en las clases 056.*
- **Peter Bailis, Aaron Davidson, Alan Fekete, Ali Ghodsi, Joseph M. Hellerstein, Ion Stoica** (2014). [Highly Available Transactions: Virtues and Limitations](https://www.vldb.org/pvldb/vol7/p181-bailis.pdf). PVLDB 7(3).  
  Qué garantías transaccionales sobreviven a una partición y cuáles no.  
  *Se cita en las clases 055.*
- **Diego Ongaro, John Ousterhout** (2014). [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf). USENIX ATC.  
  Raft: consenso equivalente a Paxos con elección de líder explicita.  
  *Se cita en las clases 057.*
- **Pat Helland** (2007). [Life beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf). CIDR.  
  Entidades, actividades y por qué las transacciones distribuidas no escalan.  
  *Se cita en las clases 057.*
- **James C. Corbett, Jeffrey Dean, Michael Epstein** (2012). [Spanner: Google's Globally-Distributed Database](https://research.google/pubs/spanner-googles-globally-distributed-database-2/). USENIX OSDI.  
  Serializabilidad global usando incertidumbre de reloj acotada (TrueTime).  
  *Se cita en las clases 057.*
- **Jim Gray, Pat Helland, Patrick O'Neil, Dennis Shasha** (1996). [The Dangers of Replication and a Solution](https://dl.acm.org/doi/10.1145/233269.233330). ACM SIGMOD. DOI [10.1145/233269.233330](https://doi.org/10.1145/233269.233330).  
  Cuantifica cómo crecen los conflictos con el número de réplicas.  
  *Se cita en las clases 053.*
- **Leslie Lamport** (1998). [The Part-Time Parliament](https://dl.acm.org/doi/10.1145/279227.279229). ACM TOCS 16(2). DOI [10.1145/279227.279229](https://doi.org/10.1145/279227.279229).  
  Paxos, el primer algoritmo de consenso práctico demostrado correcto.  
  *Se cita en las clases 057.*
- **Leslie Lamport** (1978). [Time, Clocks, and the Ordering of Events in a Distributed System](https://dl.acm.org/doi/10.1145/359545.359563). Communications of the ACM 21(7). DOI [10.1145/359545.359563](https://doi.org/10.1145/359545.359563).  
  Orden causal y relojes logicos: base de la consistencia distribuida.  
  *Se cita en las clases 056.*

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
- [Parte 09 — Almacenamiento, índices y planes](../part-09-almacenamiento-indices-y-planes/README.md)
- [Parte 11 — Operación, seguridad y gobierno](../part-11-operacion-seguridad-y-gobierno/README.md)
- [Parte 12 — Analítica, integración y streaming](../part-12-analitica-integracion-y-streaming/README.md)
- [Parte 13 — Vectores, recuperación y RAG](../part-13-vectores-recuperacion-y-rag/README.md)
- [Parte 14 — Arquitectura y proyecto final](../part-14-arquitectura-y-proyecto-final/README.md)
