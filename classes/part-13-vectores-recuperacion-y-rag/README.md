# Parte 13 — Vectores, recuperación y RAG

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

La base de datos como componente de un sistema de inteligencia artificial: distancias, indices aproximados y recuperación medida.

**4 clases · 13 horas · 19 conceptos · 9 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 07 — Grafos, columnas, tiempo y búsqueda](../part-07-grafos-columnas-tiempo-y-busqueda/README.md)

## De qué trata esta parte

La base de datos como componente de un sistema de inteligencia artificial, tratada con el mismo rigor que el resto del programa: nada se da por bueno sin medirlo. Es la parte más nueva en fecha y la más expuesta a afirmaciones sin evidencia, así que es donde más se insiste en el conjunto de evaluación propio.

Primero qué significa parecido cuando lo decide un modelo: espacio vectorial, coseno, producto interno y normalización, con la advertencia que ordena toda la parte —el parecido es el que aprendió ese modelo concreto, así que cambiar de modelo cambia el significado de cerca—. Después los índices aproximados, HNSW e IVF, con la disciplina de medir el recall contra una búsqueda exhaustiva antes de dar por buena una configuración. Luego la búsqueda híbrida, porque lo léxico y lo vectorial se complementan: uno acierta con el término exacto y el otro con el significado. Y al final la evaluación de la recuperación, antes de mirar la generación.

La conexión con la parte 07 es directa: BM25 vuelve como componente léxico, y precisión y exhaustividad vuelven convertidas en recall@k y precisión@k.

## Al terminar esta parte podrás

1. Elegir la métrica de distancia adecuada y explicar el papel de la normalización.
2. Configurar un índice aproximado y medir su recall contra una búsqueda exhaustiva.
3. Combinar búsqueda léxica y vectorial con fusión de rangos y filtrado por metadatos.
4. Evaluar la recuperación de un sistema RAG con recall@k, precisión@k y MRR sobre un conjunto propio.
5. Justificar una estrategia de fragmentación con una medición y no con el valor por defecto.

## Mapa de la parte

```mermaid
flowchart LR
    C068["068<br/>Embeddings y métricas de distancia: qué s…"]
    C069["069<br/>Índices vectoriales aproximados: HNSW, IV…"]
    C070["070<br/>Búsqueda híbrida: léxica más vectorial y…"]
    C071["071<br/>RAG evaluable: medir la recuperación ante…"]
    C068 --> C069
    C069 --> C070
    C070 --> C071
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C068 inter
    class C069 avan
    class C070 avan
    class C071 avan
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [068](068-embeddings-y-metricas-de-distancia/README.md) | [Embeddings y métricas de distancia: qué significa parecido](068-embeddings-y-metricas-de-distancia/README.md) | Intermedio | 3 | 3 |
| [069](069-indices-vectoriales-aproximados/README.md) | [Índices vectoriales aproximados: HNSW, IVF y el recall](069-indices-vectoriales-aproximados/README.md) | Avanzado | 4 | 4 |
| [070](070-busqueda-hibrida-y-filtrado/README.md) | [Búsqueda híbrida: léxica más vectorial y filtrado por metadatos](070-busqueda-hibrida-y-filtrado/README.md) | Avanzado | 3 | 4 |
| [071](071-rag-evaluable/README.md) | [RAG evaluable: medir la recuperación antes que la generación](071-rag-evaluable/README.md) | Avanzado | 3 | 3 |

## Las clases, una por una

### [068 — Embeddings y métricas de distancia: qué significa parecido](068-embeddings-y-metricas-de-distancia/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [041](../part-07-grafos-columnas-tiempo-y-busqueda/041-busqueda-de-texto-indice-invertido-y-relevancia/README.md)*

Qué significa «parecido» cuando lo decide un modelo. Presenta el espacio vectorial, las métricas de coseno y producto interno, y la normalización que las vuelve equivalentes. La advertencia que ordena toda la parte: el parecido es el que aprendió ese modelo concreto, así que cambiar de modelo cambia el significado de cerca.

**Conceptos que introduce:** `espacio vectorial` · `coseno` · `producto interno` · `normalización` · `dimensión`

[Ir a la clase →](068-embeddings-y-metricas-de-distancia/README.md)

### [069 — Índices vectoriales aproximados: HNSW, IVF y el recall](069-indices-vectoriales-aproximados/README.md)

*Avanzado · 4 h · 4 fuentes · requiere [068](068-embeddings-y-metricas-de-distancia/README.md), [049](../part-09-almacenamiento-indices-y-planes/049-b-tree-orden-de-columnas-y-selectividad/README.md)*

Los índices que hacen viable la búsqueda vectorial renunciando a la exactitud. HNSW e IVF con sus parámetros, la cuantización que cambia memoria por precisión, y la disciplina que la clase impone: medir el recall contra una búsqueda exhaustiva antes de dar por buena una configuración, porque sin ese número «funciona» solo significa «devolvió algo».

**Conceptos que introduce:** `búsqueda aproximada` · `recall` · `HNSW` · `cuantización` · `latencia frente a exactitud`

[Ir a la clase →](069-indices-vectoriales-aproximados/README.md)

### [070 — Búsqueda híbrida: léxica más vectorial y filtrado por metadatos](070-busqueda-hibrida-y-filtrado/README.md)

*Avanzado · 3 h · 4 fuentes · requiere [041](../part-07-grafos-columnas-tiempo-y-busqueda/041-busqueda-de-texto-indice-invertido-y-relevancia/README.md), [069](069-indices-vectoriales-aproximados/README.md)*

Por qué lo léxico y lo vectorial se combinan en lugar de competir: uno acierta con el término exacto, el otro con el significado. La fusión recíproca de rangos los une sin exigir que sus puntuaciones sean comparables, y el filtrado por metadatos plantea la decisión entre filtro previo y posterior, cada uno con su fallo característico.

**Conceptos que introduce:** `BM25` · `fusión de rangos` · `filtro previo` · `filtro posterior`

[Ir a la clase →](070-busqueda-hibrida-y-filtrado/README.md)

### [071 — RAG evaluable: medir la recuperación antes que la generación](071-rag-evaluable/README.md)

*Avanzado · 3 h · 3 fuentes · requiere [070](070-busqueda-hibrida-y-filtrado/README.md)*

Medir la recuperación antes de mirar la generación, porque si el fragmento correcto no entra en el contexto ningún modelo de lenguaje podrá responder bien. Recall@k, precisión@k y MRR sobre un conjunto de evaluación propio, con la fragmentación como la decisión que más mueve la calidad y la que más se toma por defecto sin medirla.

**Conceptos que introduce:** `recall@k` · `precisión@k` · `MRR` · `fragmentación` · `trazabilidad de la cita`

[Ir a la clase →](071-rag-evaluable/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «La búsqueda vectorial sustituye a la de texto.» Falla justo con los términos exactos —códigos, nombres propios, referencias—, que es donde la léxica es imbatible.
- «Uso HNSW y ya es rápido y bueno.» Sin medir el recall no sabes qué estás perdiendo; «funciona» solo significa «devolvió algo».
- «Fragmento en trozos de 512 y listo.» La fragmentación es la decisión que más mueve la calidad de un RAG y la que más se toma sin medir.
- «El modelo alucinó.» A menudo el modelo no recibió el fragmento correcto: el fallo estaba en la recuperación, que es medible.

## Vocabulario de la parte

Los 19 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **BM25** | Función de relevancia que refina TF-IDF con saturación de la frecuencia y normalización por longitud del documento, gobernadas por los parámetros `k1` y `b`. Es la referencia léxica contra la que se compara cualquier buscador, incluidos los vectoriales. | [070](070-busqueda-hibrida-y-filtrado/README.md) |
| **búsqueda aproximada** | Renunciar a encontrar con certeza los K vecinos más cercanos a cambio de responder en milisegundos en lugar de en minutos. La búsqueda exacta compara contra todos los vectores; la aproximada explora solo una parte del espacio y acepta perderse algunos. | [069](069-indices-vectoriales-aproximados/README.md) |
| **coseno** | Medida de similitud basada en el ángulo entre dos vectores, que ignora su magnitud. Es la métrica habitual con embeddings de texto, donde importa la dirección del significado y no la longitud del documento. | [068](068-embeddings-y-metricas-de-distancia/README.md) |
| **cuantización** | Comprimir los vectores usando menos bits por componente —escalar, binaria o por producto—. Reduce la memoria en un orden de magnitud a cambio de precisión, y suele combinarse con un reordenamiento final sobre los vectores completos. | [069](069-indices-vectoriales-aproximados/README.md) |
| **dimensión** | Tabla que describe el contexto por el que se filtra y se agrupa: producto, cliente, tiempo, sucursal. Se desnormaliza a propósito para evitar reuniones en cada consulta, y es donde vive casi todo el significado del modelo. (En la parte 13 la misma palabra designa otra cosa: el número de componentes de un vector.) | [068](068-embeddings-y-metricas-de-distancia/README.md) |
| **espacio vectorial** | Representación de un texto, una imagen o un usuario como un punto de N coordenadas, colocado por un modelo de forma que la cercanía refleje parecido semántico. El parecido es el que aprendió ese modelo concreto: cambiar de modelo cambia el significado de «cerca». | [068](068-embeddings-y-metricas-de-distancia/README.md) |
| **filtro posterior** | Buscar primero y filtrar después. Es simple y tiene un fallo característico: si de los K vecinos ninguno cumple el filtro, la respuesta llega vacía aunque existieran resultados válidos algo más lejos. | [070](070-busqueda-hibrida-y-filtrado/README.md) |
| **filtro previo** | Aplicar el filtro de metadatos antes de la búsqueda vectorial, de modo que solo se exploren los candidatos admisibles. Conserva el número de resultados pedido, pero puede degradar la navegación del grafo si el filtro es muy selectivo. | [070](070-busqueda-hibrida-y-filtrado/README.md) |
| **fragmentación** | Cómo se parte el documento antes de vectorizarlo: por tamaño, por párrafo, por sección, con o sin solape. Es la decisión que más mueve la calidad de un RAG y la que más se toma por defecto sin medirla. | [071](071-rag-evaluable/README.md) |
| **fusión de rangos** | Combinar dos listas ordenadas —la léxica y la vectorial— en una sola. La fusión recíproca de rangos suma el inverso de la posición en cada lista, y funciona bien precisamente porque no exige que las puntuaciones de ambos sistemas sean comparables entre sí. | [070](070-busqueda-hibrida-y-filtrado/README.md) |
| **HNSW** | Grafo navegable de mundo pequeño por capas: las capas altas dan saltos largos y las bajas afinan. Da el mejor compromiso entre recall y latencia de los índices actuales, a costa de un uso de memoria alto y una construcción lenta. | [069](069-indices-vectoriales-aproximados/README.md) |
| **latencia frente a exactitud** | El compromiso que gobiernan los parámetros del índice (`ef_search`, `nprobe`): explorar más nodos sube el recall y el tiempo de respuesta. No hay valor correcto universal; se elige midiendo con los datos y las consultas reales. | [069](069-indices-vectoriales-aproximados/README.md) |
| **MRR** | Rango recíproco medio: la media de 1 dividido por la posición del primer resultado relevante. Premia colocar arriba la respuesta correcta, que es justo lo que importa cuando solo se van a leer los tres primeros fragmentos. | [071](071-rag-evaluable/README.md) |
| **normalización** | Escalar cada vector a longitud 1. Hace equivalentes coseno y producto interno y permite usar el índice más rápido sin cambiar el orden de los resultados; es un paso rutinario que conviene declarar, porque mezclar vectores normalizados y sin normalizar arruina la búsqueda. | [068](068-embeddings-y-metricas-de-distancia/README.md) |
| **precisión@k** | Qué proporción de los K devueltos era relevante. Importa porque el contexto es finito y caro: llenar la ventana de ruido desplaza a los fragmentos que sí servían. | [071](071-rag-evaluable/README.md) |
| **producto interno** | Métrica que sí tiene en cuenta la magnitud, útil cuando el modelo codifica intensidad en la norma del vector. Sobre vectores normalizados es equivalente al coseno, y de ahí que normalizar simplifique la elección. | [068](068-embeddings-y-metricas-de-distancia/README.md) |
| **recall** | Qué proporción de los verdaderos K vecinos devolvió el índice aproximado. Es la métrica que hay que medir contra una búsqueda exhaustiva antes de dar por buena una configuración; sin ese número, «funciona» significa «devolvió algo». | [069](069-indices-vectoriales-aproximados/README.md) |
| **recall@k** | Qué proporción de los documentos relevantes aparece entre los K primeros resultados. Es la métrica que gobierna un sistema RAG: si el fragmento correcto no entra en el contexto, ningún modelo de lenguaje podrá responder bien. | [071](071-rag-evaluable/README.md) |
| **trazabilidad de la cita** | Que cada afirmación de la respuesta pueda seguirse hasta el fragmento y el documento del que salió. Es lo que permite auditar el sistema y detectar la alucinación; sin ella no hay forma de distinguir una respuesta correcta de una convincente. | [071](071-rag-evaluable/README.md) |

## Fuentes usadas en esta parte

9 obras distintas sostienen lo que se afirma en estas
4 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **LF AI & Data Foundation** (2026). [Milvus Documentation](https://milvus.io/docs).  
  Índices vectoriales distribuidos y sus compromisos de exactitud.  
  *Se cita en las clases 069.*
- **OpenSearch Project** (2026). [OpenSearch Documentation](https://docs.opensearch.org/latest/).  
  Índice invertido, analizadores, relevancia y búsqueda k-NN.  
  *Se cita en las clases 070.*
- **Qdrant** (2026). [Qdrant Documentation](https://qdrant.tech/documentation/).  
  Colecciones, filtros con carga útil y parametros HNSW.  
  *Se cita en las clases 069, 070.*
- **Andrew Kane** (2026). [pgvector](https://github.com/pgvector/pgvector).  
  Búsqueda vectorial dentro de PostgreSQL: evita un sistema adicional cuando no hace falta.  
  *Se cita en las clases 068, 070.*
- **Jeff Johnson, Matthijs Douze, Herve Jegou** (2019). [Billion-scale Similarity Search with GPUs](https://arxiv.org/abs/1702.08734). IEEE Transactions on Big Data.  
  FAISS: cuantización de producto y compromiso memoria-exactitud.  
  *Se cita en las clases 068, 069.*
- **Vladimir Karpukhin, Barlas Oguz, Sewon Min** (2020). [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906). EMNLP.  
  Recuperación densa entrenada, y su comparación honesta contra BM25.  
  *Se cita en las clases 068, 071.*
- **Yu A. Malkov, D. A. Yashunin** (2020). [Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs](https://arxiv.org/abs/1603.09320). IEEE TPAMI 42(4). DOI [10.1109/TPAMI.2018.2889473](https://doi.org/10.1109/TPAMI.2018.2889473).  
  Índice HNSW: el que usan Qdrant, Weaviate, Milvus, pgvector y Lucene.  
  *Se cita en las clases 069.*
- **Patrick Lewis, Ethan Perez, Aleksandra Piktus** (2020). [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401). NeurIPS.  
  Artículo que define RAG: la base de datos es parte del sistema, no un accesorio.  
  *Se cita en las clases 071.*
- **Stephen Robertson, Hugo Zaragoza** (2009). [The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf). Foundations and Trends in Information Retrieval 3(4). DOI [10.1561/1500000019](https://doi.org/10.1561/1500000019).  
  Función de ranking léxico contra la que se compara toda búsqueda semántica.  
  *Se cita en las clases 070, 071.*

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
- [Parte 10 — Distribución, réplica y consistencia](../part-10-distribucion-replica-y-consistencia/README.md)
- [Parte 11 — Operación, seguridad y gobierno](../part-11-operacion-seguridad-y-gobierno/README.md)
- [Parte 12 — Analítica, integración y streaming](../part-12-analitica-integracion-y-streaming/README.md)
- [Parte 14 — Arquitectura y proyecto final](../part-14-arquitectura-y-proyecto-final/README.md)
