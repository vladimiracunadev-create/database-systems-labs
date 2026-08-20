# Laboratorio 06 — Recuperación vectorial explicable

> Antes de conectar un modelo, mide la recuperación. Si el fragmento correcto no está entre los
> recuperados, ningún prompt lo va a arreglar.

**Duración:** 60 minutos · **Dependencias:** Python 3.11+ · **Marca de éxito:** `VECTOR_LAB_OK`
· **Parte:** [12 — Vectores, recuperación y RAG](../../classes/part-12-vectores-recuperacion-y-rag/README.md)

## 🎯 Qué demuestra

Que la similitud coseno y el `recall@k` son aritmética comprensible, no magia: con cuatro
documentos y vectores de tres dimensiones se puede calcular el ranking a mano y comprobar que el
código coincide. Quien entiende el mecanismo aquí puede diagnosticar un sistema real; quien solo
ha llamado a una API, no.

## 🔬 Hipótesis

1. La consulta se parecerá más a los documentos de temática SQL que a los de grafos o RAG, y el
   orden será predecible a ojo antes de ejecutar.
2. Con `k = 2`, los dos documentos relevantes declarados estarán entre los recuperados:
   `recall@2 = 1,0`.
3. Bajar a `k = 1` reducirá el recall a la mitad aunque el sistema no haya empeorado: **la
   métrica depende de `k`, y publicar un recall sin decir su `k` no significa nada**.

## ▶️ Ejecutar

```bash
python labs/06-vector-search/run_vector_lab.py
```

## 📊 Lo que verás

```text
Ranking: [('sql-indexes', 0.9961), ('sql-basics', 0.9935), ('vector-rag', 0.3652), ('graph-paths', 0.1876)]
recall@2: 1.0
VECTOR_LAB_OK
```

Fíjate en la distancia entre el segundo y el tercero: 0,99 frente a 0,37. Un corte por umbral
—en vez de por `k`— habría funcionado aquí, y esa es una decisión de diseño que conviene tomar
con datos, no por costumbre.

## 🧠 Por qué está hecho así

- **Vectores escritos a mano**, no generados por un modelo. Así el laboratorio no depende de
  ninguna API, no cambia entre ejecuciones y permite predecir el resultado.
- **Coseno implementado a la vista**, en seis líneas: producto punto sobre el producto de las
  normas. Es el momento de entender por qué la métrica tiene que ser la misma con la que se
  entrenó el modelo de embeddings.
- **El conjunto relevante se declara** (`RELEVANT`). Sin verdad de referencia no hay métrica, y
  ese conjunto es lo que más trabajo cuesta construir en un proyecto real.

## ⚠️ Lo que este laboratorio no demuestra

- No usa embeddings reales ni mide su calidad semántica.
- No implementa un índice aproximado (HNSW o IVF): con cuatro documentos, la búsqueda exacta es
  trivial. El compromiso entre recall y latencia se estudia en la
  [clase 059](../../classes/part-12-vectores-recuperacion-y-rag/059-indices-vectoriales-aproximados/README.md).
- No cubre el filtrado por permisos ni la búsqueda híbrida, que son las dos causas más
  frecuentes de fallo en producción.
- No evalúa la generación: solo la recuperación, que es lo que la acota.

## 🧪 Extensiones

1. Cambia `k` a 1 y a 3 y anota el recall: comprueba en carne propia que la métrica sin `k` es
   un número sin significado.
2. Añade dos documentos ambiguos y observa cómo el orden se vuelve frágil. Ese es el momento en
   que hace falta añadir señal léxica.
3. Implementa `precisión@k` y `MRR` junto al recall, y decide cuál refleja mejor tu caso de uso.
4. Añade un filtro de autorización **antes** del ranking y comprueba que un usuario sin permiso
   no recupera el documento restringido. Filtrar después del ranking es una fuga.
5. Sustituye el coseno por distancia euclídea sin normalizar y explica por qué el orden cambia.

## 🏭 Llevarlo a un motor real

Con PostgreSQL y `pgvector` puedes repetir el ejercicio con los mismos vectores y comprobar que
el orden coincide; después, sube a un índice HNSW y mide cuánto recall pierdes al ganar latencia.
Ese experimento —recall frente a parámetros del índice— es el que decide una configuración de
producción.

## 🎓 Dónde encaja

- **Clases:** [058–061](../../classes/part-12-vectores-recuperacion-y-rag/README.md), en especial
  [061 — RAG evaluable](../../classes/part-12-vectores-recuperacion-y-rag/061-rag-evaluable/README.md).
- **Rutas:** [Ingeniero de IA aplicada y recuperación](../../rutas/ia-y-recuperacion.md),
  [Arquitecto de datos](../../rutas/arquitectura.md).
- **Certificaciones:** ninguna de las mapeadas evalúa recuperación vectorial todavía; es un área
  demasiado joven para tener temario estable, y conviene desconfiar de las credenciales que ya
  la venden.

## 📖 Fuentes

- **Yu. A. Malkov, D. A. Yashunin**, *Efficient and Robust Approximate Nearest Neighbor Search
  Using HNSW* — el índice aproximado que usa casi todo el ecosistema.
- **Vladimir Karpukhin y otros**, *Dense Passage Retrieval* — recuperación densa y su
  evaluación.
- **Stephen Robertson, Hugo Zaragoza**, *BM25 and Beyond* — la relevancia léxica que sigue
  haciendo falta.
- **Qdrant Documentation** — un motor vectorial real y sus parámetros de índice.

Fichas completas en el [registro de fuentes](../../catalog/sources.json).

## 🧹 Limpieza

No hace falta: todo ocurre en memoria.
