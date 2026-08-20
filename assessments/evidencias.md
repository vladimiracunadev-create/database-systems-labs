# Evidencias de laboratorio

Las evidencias de laboratorio son el **40 %** de la nota: el bloque más pesado del programa.
No porque ejecutar sea difícil —ocho comandos y ya está—, sino porque lo que se evalúa es lo
que rodea a la ejecución.

> Una captura sin comando no es evidencia: no se puede repetir.

## Qué cuenta como evidencia

Cinco piezas por cada laboratorio. Faltar una baja el nivel; faltar la quinta lo baja mucho.

| Pieza | Qué es | Por qué se pide |
| --- | --- | --- |
| **Hipótesis** | Qué esperabas, escrito antes de ejecutar | Sin predicción, ejecutar es un trámite y no se aprende nada |
| **Comando** | Lo que ejecutaste, literal, con su ruta | Es lo que permite repetirlo |
| **Entorno** | Versión del motor, del sistema y de Python | Sin esto, un número no significa nada |
| **Salida** | Completa, sin recortar lo que no encaja | La parte recortada suele ser la interesante |
| **Explicación y límite** | Por qué salió eso, y qué **no** demuestra | Es donde se ve quién entendió el mecanismo |

## Plantilla

```markdown
# Evidencia — Laboratorio 04 (índices y planes)

## Hipótesis
Espero que la consulta por (course_id, student_id) pase de recorrer la tabla a
buscar por índice, y que insertar 5000 filas cueste más con dos índices.

## Entorno
Python 3.12.3 · SQLite 3.45.1 · Windows 11 · commit a1b2c3d

## Comando
python labs/04-indexing/run_indexing_lab.py

## Salida
(la salida completa, tal cual)

## Explicación
El plan pasa de SCAN a SEARCH porque el índice cubre las dos columnas del filtro...
El trabajo baja de 60 810 a 20 pasos porque...

## Qué NO demuestra
No mide latencia real ni concurrencia; el planificador de SQLite es más simple
que el de PostgreSQL, así que la forma se transfiere pero los costes no.
```

## Qué se espera de cada laboratorio

| Laboratorio | La afirmación que tu evidencia debe sostener | Lo que casi nadie declara |
| --- | --- | --- |
| [01 SQL foundations](../labs/01-sql-foundations/README.md) | Predijiste el resultado de las tres consultas antes de ejecutar | Que el promedio con `NULL` no es el promedio con cero |
| [02 Polyglot modeling](../labs/02-polyglot-modeling/README.md) | Los tres modelos con lo que gana y pierde cada uno | Bajo qué carga cambiarías de opinión |
| [03 Transactions](../labs/03-transactions/README.md) | Reprodujiste la actualización perdida y la corregiste | Qué corrección elegirías en tu sistema y por qué |
| [04 Indexing](../labs/04-indexing/README.md) | El plan cambió y la escritura se encareció | Que el skip-scan depende de las estadísticas y de la versión |
| [05 NoSQL workloads](../labs/05-nosql-workloads/README.md) | La conclusión se invierte al cambiar la carga | Que los números modelan, no miden un motor real |
| [06 Vector search](../labs/06-vector-search/README.md) | Calculaste `recall@k` y sabes qué cambia con `k` | Que sin declarar `k` la métrica no significa nada |
| [07 Replication](../labs/07-replication/README.md) | Contaste las lecturas que no ven la escritura propia | Qué cuesta cada corrección: carga, latencia o peticiones |
| [08 Recovery](../labs/08-recovery/README.md) | Restauraste y verificaste el contenido | Tu RPO y tu RTO, en números, no en adjetivos |

## Cómo se puntúa

| Nivel | Qué se observa |
| --- | --- |
| 1 · Inicial | Está la salida, sin comando ni entorno |
| 2 · Funcional | Comando, entorno y salida; la explicación repite lo que se ve |
| 3 · Sólido | La explicación cuenta el mecanismo y hay una hipótesis previa |
| 4 · Profesional | Además, el límite está declarado y hay una extensión propia ejecutada |

El salto de 3 a 4 es barato en tiempo y caro en honestidad: exige decir qué no probaste.

## Errores que hacen perder la evidencia

- **Recortar la salida** para que se lea mejor. Si sobra, se explica; no se borra.
- **Ejecutar y después escribir la hipótesis.** Se nota siempre: la predicción coincide
  demasiado.
- **Copiar la explicación de la guía del laboratorio.** La guía dice qué pasa; tu evidencia
  tiene que decir por qué pasó **en tu ejecución**.
- **Medir tiempos y presentarlos como conclusión.** Ningún laboratorio de este programa afirma
  nada en milisegundos, y tu evidencia tampoco debería.
- **Guardar credenciales o datos reales** en la evidencia. Es una
  [falta crítica](rubric.md#faltas-críticas).

## Dónde guardarla

En tu propio repositorio, con una carpeta por laboratorio y el formato de la plantilla. Al
terminar el programa, esa carpeta **es** tu portafolio: ocho experimentos con hipótesis,
resultado y límite. Vale más en una entrevista que cualquier certificado, y se explica en
[`projects/portafolio.md`](../projects/portafolio.md).
