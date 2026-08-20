# 🤖 Ingeniero de IA aplicada y recuperación

> Construyes la parte del sistema que decide **qué texto ve el modelo** antes de que responda.
> Si esa parte falla, el modelo inventa con seguridad y elocuencia, y la culpa parecerá suya
> cuando en realidad fue de tu recuperación.
>
> **Nivel de entrada:** avanzado (requiere SQL, modelado e índices) · **Foco:** embeddings,
> índices aproximados, búsqueda híbrida y evaluación de la recuperación · **Cargos
> habituales:** ingeniero de IA aplicada, ingeniero de búsqueda y recuperación, ML engineer de
> producto.

## 🧭 Qué es y por qué importa

La mayoría de los sistemas de IA que llegan a producción no entrenan modelos: los usan, y
gastan su esfuerzo en decidir con qué contexto los alimentan. Ese trabajo —fragmentar, indexar,
buscar, filtrar por permisos, ordenar y medir— es ingeniería de datos y de recuperación, no
aprendizaje automático. De ahí que este rol viva en un programa de bases de datos.

Importa porque **la calidad de la respuesta está acotada por la calidad de la recuperación**.
Si el fragmento correcto no está entre los que recuperaste, ningún modelo lo va a adivinar; y
si recuperaste basura plausible, la generará con la misma confianza. Medir la recuperación
—recall@k y compañía— antes de tocar el prompt es lo que separa un sistema evaluable de una
demostración con suerte.

Es un rol joven y con mucho ruido comercial. Cada semana aparece una base vectorial nueva y un
patrón con nombre propio. Lo que no cambia: un índice aproximado intercambia exactitud por
velocidad, un filtro por permisos aplicado después del ranking es una fuga de datos, y sin un
conjunto de evaluación no puedes decir si tu cambio mejoró algo.

Lo que este programa **no** cubre: entrenar o afinar modelos, ni la ingeniería de prompts. Sí
cubre lo que se rompe primero en producción.

## 🗓️ Un día en el puesto

- **Una queja: «el asistente se inventó una política».** Antes de tocar el prompt, compruebas
  si el documento correcto estaba entre los recuperados. Casi siempre no estaba.
- **Revisar la fragmentación.** Fragmentos demasiado grandes diluyen; demasiado pequeños
  pierden el contexto. Se ajusta midiendo, no por intuición.
- **Ajustar el índice aproximado.** Parámetros que cambian el recall y la latencia; hay que
  elegir el punto y **declararlo**.
- **Añadir búsqueda léxica** junto a la vectorial porque los identificadores, códigos y nombres
  propios se recuperan mal por similitud semántica.
- **Filtrado por permisos.** Que un usuario no reciba un fragmento que no puede leer. Se
  resuelve en la consulta, no después.
- **Evaluar.** Un conjunto de preguntas con su respuesta esperada, y una métrica que se
  compara entre versiones. Sin eso, cada cambio es una opinión.
- **Borrar.** Cuando el documento original desaparece, sus vectores también deben irse; si no,
  el sistema responde con lo que ya no existe.

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **Embeddings y métricas de distancia:** qué significa «parecido» y por qué la métrica debe
  coincidir con la que usó el modelo al entrenar.
- **Índices vectoriales aproximados:** HNSW, IVF y el compromiso entre recall, latencia y
  memoria.
- **Búsqueda léxica:** índice invertido, análisis de texto y relevancia (BM25). La mitad de los
  fallos de un RAG se arreglan volviendo a lo léxico.
- **Búsqueda híbrida y filtrado:** combinar señales y aplicar filtros de permisos **dentro** de
  la consulta.
- **Evaluación:** recall@k, precisión@k, MRR, conjuntos de prueba y trazabilidad de la cita.
- **Fundamentos de bases de datos:** índices, planes, transacciones y consistencia. Un almacén
  vectorial sigue siendo un almacén: se llena, se actualiza, se borra y se opera.
- **Modelado del documento:** qué guardas junto al vector —metadatos, permisos, versión,
  origen— y por qué eso decide qué filtros puedes hacer.

### Herramientas del oficio

- PostgreSQL con `pgvector` para empezar sin infraestructura nueva, y un motor vectorial
  dedicado (Qdrant, Milvus) cuando el volumen lo justifique.
- Un motor de búsqueda léxica (OpenSearch) o las capacidades de texto del propio motor
  relacional.
- Un conjunto de evaluación propio, versionado junto al código.
- Contenedores para reproducir el conjunto entero en local.

### Habilidades no técnicas

- **Resistir la presión de demostrar rápido.** Una demostración impresionante sin evaluación es
  deuda con intereses.
- **Explicar el límite del sistema** a quien lo va a vender: qué preguntas responde y cuáles
  no.
- **Declarar la incertidumbre:** de dónde salió la cita y con qué confianza.

## 📚 Tu ruta en el programa

9 partes, 131 horas estimadas.

1. 📚 [**Parte 00 — Fundamentos**](../classes/part-00-fundamentos-datos-sistemas-y-metodo/README.md)
   (4 clases · 12 h).
2. 📚 [**Parte 01 — Modelado conceptual**](../classes/part-01-modelado-conceptual-y-requisitos/README.md)
   (5 clases · 16 h).
3. 📚 [**Parte 02 — Modelo relacional y álgebra**](../classes/part-02-modelo-relacional-y-algebra/README.md)
   (4 clases · 13 h).
4. 📚 [**Parte 03 — SQL en profundidad**](../classes/part-03-sql-en-profundidad/README.md)
   (6 clases · 20 h). Los filtros y las reuniones que acompañan a cada búsqueda.
5. 📚 [**Parte 05 — Documentos y clave-valor**](../classes/part-05-documentos-y-clave-valor/README.md)
   (4 clases · 13 h). El agregado, la caché y su expiración.
6. 📚 [**Parte 06 — Grafos, columnas, tiempo y búsqueda**](../classes/part-06-grafos-columnas-tiempo-y-busqueda/README.md)
   (5 clases · 15 h). Especialmente
   [031 — Búsqueda de texto: índice invertido y relevancia](../classes/part-06-grafos-columnas-tiempo-y-busqueda/031-busqueda-de-texto-indice-invertido-y-relevancia/README.md).
7. 📚 [**Parte 08 — Almacenamiento, índices y planes**](../classes/part-08-almacenamiento-indices-y-planes/README.md)
   (5 clases · 17 h). Con
   [041 — Índices especializados](../classes/part-08-almacenamiento-indices-y-planes/041-indices-especializados/README.md).
8. 📚 [**Parte 12 — Vectores, recuperación y RAG**](../classes/part-12-vectores-recuperacion-y-rag/README.md)
   (4 clases · 13 h). El núcleo:
   [058 — Embeddings y métricas de distancia](../classes/part-12-vectores-recuperacion-y-rag/058-embeddings-y-metricas-de-distancia/README.md),
   [059 — Índices vectoriales aproximados](../classes/part-12-vectores-recuperacion-y-rag/059-indices-vectoriales-aproximados/README.md),
   [060 — Búsqueda híbrida y filtrado](../classes/part-12-vectores-recuperacion-y-rag/060-busqueda-hibrida-y-filtrado/README.md)
   y [061 — RAG evaluable](../classes/part-12-vectores-recuperacion-y-rag/061-rag-evaluable/README.md).
9. 📚 [**Parte 13 — Arquitectura y proyecto final**](../classes/part-13-arquitectura-y-proyecto-final/README.md)
   (3 clases · 12 h).

Laboratorios de la ruta:

- 🧪 [`06-vector-search`](../labs/06-vector-search/README.md) — similitud coseno y recall@k
  sobre vectores deterministas: la métrica antes que el modelo.
- 🧪 [`05-nosql-workloads`](../labs/05-nosql-workloads/README.md) — expiración, incrustar
  frente a referenciar y claves calientes; decisiones que reaparecen en el almacén de
  fragmentos.
- 🧪 [`01-sql-foundations`](../labs/01-sql-foundations/README.md) — porque el filtrado por
  permisos se escribe en SQL.

## 🧪 Qué tienes que poder demostrar

- calcular **recall@k** sobre un conjunto de evaluación propio y usarlo para decidir un cambio;
- explicar qué pierdes al pasar de búsqueda exacta a un índice aproximado, y con qué parámetro
  se recupera;
- justificar por qué añadir búsqueda léxica mejora los casos con códigos y nombres propios;
- aplicar filtros de permisos **antes** de que el ranking decida, y demostrar que un usuario no
  recupera lo que no puede leer;
- diseñar el borrado: cuando desaparece el documento, desaparecen sus vectores;
- declarar qué preguntas **no** responde tu sistema, con evidencia de la evaluación.

## 🎓 Credenciales

No hay credencial reconocida para este rol —es demasiado nuevo— y desconfía de las que
aparezcan atadas a un producto vectorial concreto. Lo que se valora es un proyecto donde se vea
el conjunto de evaluación, las métricas antes y después de cada cambio y el tratamiento de
permisos y borrado.

Si necesitas una credencial de contexto por la nube que uses, la
[Professional Data Engineer de Google Cloud](https://cloud.google.com/learn/certification/data-engineer)
cubre el lado de ingesta y almacenamiento; no evalúa recuperación.

## 📈 Progresión y mercado

1. **Desarrollador backend o ingeniero de datos** con curiosidad por la recuperación.
2. **Ingeniero de IA aplicada** — construyes recuperación y evaluación para un producto.
3. **Especialista en búsqueda y relevancia** — el perfil clásico de *search engineer*, hoy con
   señal semántica añadida.
4. **Bifurcación:** [arquitectura](arquitectura.md) de sistemas de datos, o aprendizaje
   automático propiamente dicho si te atrae entrenar y no recuperar.

Sobre cifras: no hay una fuente oficial equivalente al
[Occupational Outlook Handbook](https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm)
para este puesto —es demasiado reciente para tener epígrafe propio—, así que este repositorio
no publica rangos. Desconfía de las cifras que circulan en redes sobre sueldos de «ingeniero de
IA»: casi ninguna declara muestra ni método.

## ⚠️ Mitos y errores comunes

- **«El problema es el prompt.»** Casi nunca. Si el fragmento correcto no fue recuperado,
  ningún prompt lo arregla.
- **«Base vectorial nueva, problema resuelto.»** El almacén es la parte fácil. La fragmentación,
  los permisos, la evaluación y el borrado son el trabajo.
- **«Similitud alta significa verdad.»** Significa parecido en el espacio del modelo. Puede ser
  parecido y falso.
- **«Ya filtro los resultados después.»** Filtrar después del ranking sirve resultados que el
  usuario no debía ver y estropea el orden. El filtro va dentro de la consulta.
- **«No hace falta búsqueda léxica.»** Hasta que alguien busca un número de factura o un
  apellido poco común y el sistema devuelve poesía.
- **«Evaluamos con un par de preguntas.»** Sin un conjunto estable y versionado, no puedes
  distinguir una mejora de una casualidad.
- **«Los vectores no envejecen.»** Cambias de modelo de embeddings y todo el índice queda
  inconsistente: hay que reindexar y planificarlo.

## 🚀 Siguientes pasos

1. No empieces por la Parte 12: haz antes 00 → 03 y la 08. Un almacén vectorial mal indexado se
   diagnostica con las mismas herramientas que cualquier otro.
2. Ejecuta [`06-vector-search`](../labs/06-vector-search/README.md) y añade dos documentos
   propios; observa cómo cambia el recall.
3. Monta un conjunto de evaluación de 30 preguntas sobre tu propio corpus. Es tedioso y es lo
   que más valor te va a dar.
4. Implementa la búsqueda híbrida y compara métricas contra la puramente vectorial.
5. Diseña el borrado y la reindexación antes de que sean urgentes.
6. Cierra con el [proyecto final](../projects/capstone.md), midiendo la recuperación y no la
   elocuencia.

## 📖 De dónde sale esto

- **Patrick Lewis y otros**, *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
  — el artículo que da nombre al patrón.
- **Yu. A. Malkov, D. A. Yashunin**, *Efficient and Robust Approximate Nearest Neighbor Search
  Using HNSW* — el índice aproximado que usa casi todo el ecosistema.
- **Stephen Robertson, Hugo Zaragoza**, *The Probabilistic Relevance Framework: BM25 and
  Beyond* — la relevancia léxica que sigue siendo necesaria.
- **pgvector** — extensión que permite empezar sin añadir un motor nuevo.

Fichas completas en el [registro de fuentes](../catalog/sources.json).

---

- ⬅️ [Volver al índice de rutas](README.md)
- 🏠 [Inicio del programa](../README.md)
