# Parte 06 — Documentos y clave-valor

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

Modelos sin reunión en el servidor: el agregado como frontera de consistencia, cuando incrustar y que se pierde en una caché.

**4 clases · 13 horas · 16 conceptos · 9 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 02 — Modelado conceptual y requisitos](../part-02-modelado-conceptual-y-requisitos/README.md)
- [Parte 04 — SQL en profundidad](../part-04-sql-en-profundidad/README.md)

## De qué trata esta parte

La primera salida del relacional, y se hace por la puerta correcta: no por la moda, sino por una idea con nombre propio. El agregado es el conjunto de datos que se lee, se escribe y se mantiene consistente como una unidad, y en los motores documentales la frontera transaccional coincide con él. Diseñar el agregado es, por tanto, decidir dónde termina la garantía del motor y empieza el trabajo de tu aplicación.

Las cuatro clases desarrollan esa idea. La primera la establece. La segunda la aplica a la decisión central del modelado documental —incrustar o referenciar— con sus dos criterios: si el dato se lee siempre junto, y si puede crecer sin techo. La tercera enseña a consultar e indexar lo modelado, con la regla que más rendimiento decide en una canalización de agregación. La cuarta trata el clave- valor y la caché diciendo con precisión qué se pierde: la consulta por contenido, la integridad declarada y, según la configuración, parte de la durabilidad.

Nada aquí sugiere abandonar el relacional. Sugiere saber qué se está comprando y con qué moneda se paga.

## Al terminar esta parte podrás

1. Identificar los agregados de un dominio y justificar dónde se pone la frontera transaccional.
2. Decidir entre incrustar y referenciar con criterios de patrón de lectura y crecimiento acotado.
3. Diseñar índices y canalizaciones de agregación que usen el índice en lugar de recorrer la colección.
4. Declarar la política de caché —TTL, invalidación y durabilidad— en términos de pérdida aceptable.

## Mapa de la parte

```mermaid
flowchart LR
    C034["034<br/>El agregado como unidad de consistencia"]
    C035["035<br/>Modelado documental: incrustar o referenciar"]
    C036["036<br/>Consultas, índices y agregación sobre doc…"]
    C037["037<br/>Clave-valor, caché y expiración: qué se p…"]
    C034 --> C035
    C035 --> C036
    C036 --> C037
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C034 inter
    class C035 inter
    class C036 inter
    class C037 inter
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [034](034-el-agregado-como-unidad-de-consistencia/README.md) | [El agregado como unidad de consistencia](034-el-agregado-como-unidad-de-consistencia/README.md) | Intermedio | 3 | 3 |
| [035](035-modelado-documental-incrustar-o-referenciar/README.md) | [Modelado documental: incrustar o referenciar](035-modelado-documental-incrustar-o-referenciar/README.md) | Intermedio | 4 | 3 |
| [036](036-consultas-e-indices-sobre-documentos/README.md) | [Consultas, índices y agregación sobre documentos](036-consultas-e-indices-sobre-documentos/README.md) | Intermedio | 3 | 3 |
| [037](037-clave-valor-cache-y-expiracion/README.md) | [Clave-valor, caché y expiración: qué se pierde exactamente](037-clave-valor-cache-y-expiracion/README.md) | Intermedio | 3 | 3 |

## Las clases, una por una

### [034 — El agregado como unidad de consistencia](034-el-agregado-como-unidad-de-consistencia/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [019](../part-02-modelado-conceptual-y-requisitos/019-desnormalizacion-deliberada/README.md), [023](../part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md)*

El agregado como unidad de lectura, escritura y consistencia, y la consecuencia que ordena toda la parte: en los motores documentales la frontera transaccional coincide con el agregado. Diseñar el agregado es, por tanto, decidir dónde termina la garantía del motor y empieza el trabajo de la aplicación.

**Conceptos que introduce:** `agregado` · `frontera transaccional` · `entidad` · `actividad`

[Ir a la clase →](034-el-agregado-como-unidad-de-consistencia/README.md)

### [035 — Modelado documental: incrustar o referenciar](035-modelado-documental-incrustar-o-referenciar/README.md)

*Intermedio · 4 h · 3 fuentes · requiere [034](034-el-agregado-como-unidad-de-consistencia/README.md)*

La decisión central del modelado documental —incrustar o referenciar— con sus dos criterios: si el dato se lee siempre junto y si puede crecer sin techo. Presenta el crecimiento no acotado como el fallo característico del modelo documental y los patrones de extensión que lo evitan.

**Conceptos que introduce:** `incrustación` · `referencia` · `crecimiento no acotado` · `patrón de extensión`

[Ir a la clase →](035-modelado-documental-incrustar-o-referenciar/README.md)

### [036 — Consultas, índices y agregación sobre documentos](036-consultas-e-indices-sobre-documentos/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [035](035-modelado-documental-incrustar-o-referenciar/README.md)*

Cómo se consulta e indexa lo que se modeló en la clase anterior: índices compuestos y multiclave, cobertura, y la canalización de agregación con la regla que más rendimiento decide —poner `$match` al principio para que el índice sirva, no después.

**Conceptos que introduce:** `índice compuesto` · `canalización de agregación` · `índice multiclave` · `cobertura`

[Ir a la clase →](036-consultas-e-indices-sobre-documentos/README.md)

### [037 — Clave-valor, caché y expiración: qué se pierde exactamente](037-clave-valor-cache-y-expiracion/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [034](034-el-agregado-como-unidad-de-consistencia/README.md)*

Qué se gana y qué se pierde exactamente al poner una caché delante. Trata el TTL como política de retención, la invalidación como el problema difícil que es, la estampida como fallo predecible, y la durabilidad configurable de Redis como una decisión de negocio que hay que escribir en segundos de pérdida aceptable.

**Conceptos que introduce:** `TTL` · `invalidación` · `estampida de caché` · `durabilidad configurable`

[Ir a la clase →](037-clave-valor-cache-y-expiracion/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «En documentales no hay esquema.» Hay esquema; lo que no hay es quien lo imponga. Se traslada de la base a la aplicación, donde nadie lo comprueba en cada escritura.
- «Incrustar es más rápido siempre.» Hasta que el arreglo incrustado crece sin techo y cada lectura arrastra megabytes que nadie pidió.
- «Redis es una base de datos.» Puede serlo con la configuración adecuada, pero por defecto es una caché: si no declaraste la durabilidad, aceptaste perder datos.
- «El `$lookup` es como un `JOIN`.» Existe, pero no está optimizado como una reunión relacional; si tu modelo lo necesita en cada consulta, el modelo probablemente era relacional.

## Vocabulario de la parte

Los 16 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **actividad** | Hecho que ocurre en un instante y relaciona entidades: un pedido, un pago, una inscripción. Su volumen crece sin límite con el tiempo, lo que la convierte en la candidata natural a tabla de hechos o a flujo de eventos, y en la mala candidata a incrustarse dentro de una entidad. | [034](034-el-agregado-como-unidad-de-consistencia/README.md) |
| **agregado** | Conjunto de datos que se trata como una unidad para leer, escribir y garantizar consistencia: un pedido con sus líneas. Sadalage y Fowler lo toman del diseño dirigido por el dominio y lo convierten en el criterio que separa a los motores NoSQL del relacional. (En la clase 027 la palabra se usa en su otro sentido: el resultado de una función de agregación como `SUM` o `COUNT`.) | [034](034-el-agregado-como-unidad-de-consistencia/README.md) |
| **canalización de agregación** | Secuencia de etapas (`$match`, `$group`, `$sort`, `$lookup`) por las que pasan los documentos en MongoDB. El orden importa de verdad: poner `$match` al principio permite usar el índice, ponerlo después obliga a recorrer la colección entera. | [036](036-consultas-e-indices-sobre-documentos/README.md) |
| **cobertura** | Que el índice contenga todas las columnas que la consulta necesita, de modo que el motor responda sin tocar la tabla. Es la diferencia entre una lectura y dos, y suele ser la optimización con mejor relación entre esfuerzo y resultado. | [036](036-consultas-e-indices-sobre-documentos/README.md) |
| **crecimiento no acotado** | Un arreglo incrustado que puede crecer indefinidamente —los comentarios de una publicación viral, el histórico de un sensor—. Acaba chocando con el límite de tamaño del documento y degrada cada lectura, aunque solo se quería un campo. Es la señal de que ese arreglo debía ser una colección aparte. | [035](035-modelado-documental-incrustar-o-referenciar/README.md) |
| **durabilidad configurable** | Poder elegir cuánta pérdida se acepta a cambio de latencia: Redis ofrece desde ninguna persistencia hasta `appendfsync always`, pasando por instantáneas periódicas. La decisión es de negocio, y hay que escribirla: «se pueden perder hasta N segundos de escrituras». | [037](037-clave-valor-cache-y-expiracion/README.md) |
| **entidad** | Cosa del dominio con identidad propia que persiste a lo largo del tiempo: un cliente, un producto, una cuenta. Se distingue de la actividad en que existe aunque no pase nada, y suele ser la raíz de un agregado. | [034](034-el-agregado-como-unidad-de-consistencia/README.md) |
| **estampida de caché** | Cuando una clave muy consultada expira y miles de peticiones van a la vez a la base de datos a recalcularla. Se mitiga con expiraciones escalonadas, recálculo anticipado o un cerrojo que deja pasar a uno solo. | [037](037-clave-valor-cache-y-expiracion/README.md) |
| **frontera transaccional** | El límite dentro del cual el motor garantiza atomicidad y aislamiento. En los motores de agregado coincide con el agregado: una escritura sobre un documento es atómica, dos sobre documentos distintos ya no. Diseñar el agregado es, por tanto, diseñar dónde termina la garantía. | [034](034-el-agregado-como-unidad-de-consistencia/README.md) |
| **incrustación** | Guardar los datos relacionados dentro del propio documento. Una sola lectura devuelve todo y la escritura es atómica, a cambio de duplicar el dato si otro documento también lo necesita y de arriesgar un documento que crece sin techo. | [035](035-modelado-documental-incrustar-o-referenciar/README.md) |
| **invalidación** | Borrar o marcar como obsoleta una entrada de caché cuando cambia el dato de origen. Es el problema difícil de las cachés porque exige que quien escribe en la base sepa qué claves quedaron mentirosas —y normalmente no lo sabe. | [037](037-clave-valor-cache-y-expiracion/README.md) |
| **patrón de extensión** | Familia de soluciones para el crecimiento no acotado: partir el arreglo en cubos de tamaño fijo, guardar solo los N últimos elementos incrustados y el resto en otra colección, o separar los campos grandes en un documento satélite. | [035](035-modelado-documental-incrustar-o-referenciar/README.md) |
| **referencia** | Guardar el identificador del documento relacionado en lugar de su contenido. Evita la duplicación y el crecimiento no acotado, a cambio de una segunda consulta —o de un `$lookup`— que el motor no optimiza como un `JOIN` relacional. | [035](035-modelado-documental-incrustar-o-referenciar/README.md) |
| **TTL** | Tiempo de vida tras el cual la clave expira y desaparece. Es la política de retención más simple que existe y la que convierte a una caché en caché: sin TTL, un almacén clave-valor es solo una base de datos en memoria que crece hasta llenarla. | [037](037-clave-valor-cache-y-expiracion/README.md) |
| **índice compuesto** | Índice sobre varias claves en un orden concreto. Sirve para las consultas que filtran por un prefijo de esa lista, no para cualquier subconjunto: `(a, b, c)` acelera filtrar por `a` o por `a, b`, pero no por `b` a secas. | [036](036-consultas-e-indices-sobre-documentos/README.md) |
| **índice multiclave** | Índice sobre un campo que contiene un arreglo: MongoDB crea una entrada por elemento. Permite buscar dentro del arreglo, y explica por qué el índice de una colección puede tener muchas más entradas que documentos. | [036](036-consultas-e-indices-sobre-documentos/README.md) |

## Fuentes usadas en esta parte

9 obras distintas sostienen lo que se afirma en estas
4 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **Martin Kleppmann** (2017). [Designing Data-Intensive Applications](https://dataintensive.net/). O'Reilly. ISBN 978-1-4493-7332-0.  
  Referencia central del programa para replicación, partición, transacciones distribuidas y streaming.  
  *Se cita en las clases 034, 037.*
- **Shannon Bradshaw, Eoin Brazil, Kristina Chodorow** (2019). [MongoDB: The Definitive Guide](https://www.oreilly.com/library/view/mongodb-the-definitive/9781491954454/). 3.a ed. O'Reilly. ISBN 978-1-4919-5446-1.  
  Modelado documental, índices y canalización de agregación.  
  *Se cita en las clases 035, 036.*
- **Pramod J. Sadalage, Martin Fowler** (2012). [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html). Addison-Wesley. ISBN 978-0-321-82662-6.  
  Origen del término agregado y de la persistencia políglota que estructura este programa.  
  *Se cita en las clases 034, 035.*
- **Markus Winand** (2012). [SQL Performance Explained](https://use-the-index-luke.com/). Markus Winand. ISBN 978-3-9503078-2-5.  
  Versión web gratuita. Índices B-Tree y su relación con el orden de las columnas.  
  *Se cita en las clases 036.*
- **MongoDB, Inc.** (2026). [MongoDB Manual](https://www.mongodb.com/docs/manual/).  
  Modelo documental, índices, agregación y transacciones multi-documento.  
  *Se cita en las clases 036.*
- **MongoDB, Inc.** (2026). [MongoDB: Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/).  
  Criterio para incrustar o referenciar según patrones de acceso.  
  *Se cita en las clases 035.*
- **Redis Ltd.** (2026). [Redis Documentation](https://redis.io/docs/latest/).  
  Estructuras de datos, expiración y semántica de comandos.  
  *Se cita en las clases 037.*
- **Redis Ltd.** (2026). [Redis: Persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/).  
  RDB frente a AOF: qué se pierde exactamente en cada configuración.  
  *Se cita en las clases 037.*
- **Pat Helland** (2007). [Life beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf). CIDR.  
  Entidades, actividades y por qué las transacciones distribuidas no escalan.  
  *Se cita en las clases 034.*

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
- [Parte 07 — Grafos, columnas, tiempo y búsqueda](../part-07-grafos-columnas-tiempo-y-busqueda/README.md)
- [Parte 08 — Transacciones, concurrencia y recuperación](../part-08-transacciones-concurrencia-y-recuperacion/README.md)
- [Parte 09 — Almacenamiento, índices y planes](../part-09-almacenamiento-indices-y-planes/README.md)
- [Parte 10 — Distribución, réplica y consistencia](../part-10-distribucion-replica-y-consistencia/README.md)
- [Parte 11 — Operación, seguridad y gobierno](../part-11-operacion-seguridad-y-gobierno/README.md)
- [Parte 12 — Analítica, integración y streaming](../part-12-analitica-integracion-y-streaming/README.md)
- [Parte 13 — Vectores, recuperación y RAG](../part-13-vectores-recuperacion-y-rag/README.md)
- [Parte 14 — Arquitectura y proyecto final](../part-14-arquitectura-y-proyecto-final/README.md)
