# 026 — Consultas, índices y agregación sobre documentos

> [Programa](../../../README.md) · [Parte 05](../README.md) · [← Anterior](../../part-05-documentos-y-clave-valor/025-modelado-documental-incrustar-o-referenciar/README.md) · [Siguiente →](../../part-05-documentos-y-clave-valor/027-clave-valor-cache-y-expiracion/README.md)

| | |
|---|---|
| **Parte** | 05 — Documentos y clave-valor |
| **Nivel** | Intermedio |
| **Horas estimadas** | 3 |
| **Motores** | `mongodb` |
| **Laboratorio** | [`labs/05-nosql-workloads`](../../../labs/05-nosql-workloads/README.md) |
| **Fuentes** | 3 |

**Conceptos centrales:** `índice compuesto` · `canalización de agregación` · `índice multiclave` · `cobertura`

---

## Propósito

Consultar documentos con la misma disciplina que se consulta SQL: sabiendo qué índice se usa, cuántos documentos se examinan y por qué una etapa de la canalización es cara.

## Resultados de aprendizaje

Al terminar podrás:

1. Leer un plan de MongoDB y distinguir `COLLSCAN` de `IXSCAN`.
2. Aplicar la regla ESR para ordenar las claves de un índice compuesto.
3. Reconocer una consulta cubierta y qué la habilita.
4. Ordenar las etapas de una canalización de agregación para reducir el trabajo.
5. Prever el efecto de los índices multiclave y parciales.

## Fundamentos

### Leer el plan

```javascript
db.enrollments.find({course_id: "curso-bd", estado: "activa"})
              .explain("executionStats")
```

Los tres números que importan:

| Campo | Significa | Objetivo |
|---|---|---|
| `nReturned` | Documentos devueltos | — |
| `totalKeysExamined` | Entradas de índice leídas | Cercano a `nReturned` |
| `totalDocsExamined` | Documentos leídos | Cercano a `nReturned`; **0** si la consulta está cubierta |

Diagnóstico rápido: si `totalDocsExamined` es mucho mayor que `nReturned`, falta índice o el que hay no sirve. Es el mismo razonamiento de selectividad de la clase 039, con otro vocabulario.

### La regla ESR

Para un índice compuesto, el orden de las claves debe ser:

1. **E**quality — campos comparados por igualdad.
2. **S**ort — campos por los que se ordena.
3. **R**ange — campos comparados por rango.

```javascript
db.enrollments.find({course_id: "curso-bd", nota: {$gte: 4.0}}).sort({registrada_en: -1})
db.enrollments.createIndex({course_id: 1, registrada_en: -1, nota: 1})
//                          E              S                  R
```

Poner el rango antes que el orden obliga al motor a ordenar en memoria el resultado del rango. Es la misma razón por la que en un B-Tree relacional el rango «rompe» el uso de las columnas siguientes (clase 039): una vez que se recorre un intervalo, las claves posteriores ya no están ordenadas globalmente.

### Consulta cubierta

Si todos los campos que la consulta necesita —filtro, orden y proyección— están en el índice, el motor no toca los documentos:

```javascript
db.enrollments.find({course_id: "curso-bd"}, {_id: 0, student_id: 1, nota: 1})
db.enrollments.createIndex({course_id: 1, student_id: 1, nota: 1})
// totalDocsExamined: 0
```

Hay que excluir `_id` explícitamente si no está en el índice, porque se devuelve por omisión.

### Tipos de índice

| Tipo | Para qué | Cuidado |
|---|---|---|
| Simple / compuesto | Lo habitual | Orden ESR |
| **Multiclave** | Campo que es un arreglo | Una entrada por elemento; solo un campo de arreglo por índice |
| **Parcial** | Subconjunto de documentos | Solo se usa si la consulta implica el filtro del índice |
| **TTL** | Expiración automática | Borra en segundo plano, con retraso |
| Texto | Búsqueda léxica básica | Uno por colección; para búsqueda seria, parte 06 |

### Canalización de agregación

El orden de las etapas determina cuánto trabajo se hace:

```javascript
// MAL: agrupa 5 millones y luego descarta
db.enrollments.aggregate([
  {$group: {_id: "$course_id", promedio: {$avg: "$nota"}}},
  {$match: {_id: "curso-bd"}}
])

// BIEN: filtra primero, con índice
db.enrollments.aggregate([
  {$match: {course_id: "curso-bd", estado: "activa"}},
  {$group: {_id: "$course_id", promedio: {$avg: "$nota"}}}
])
```

Es la equivalencia E2 de la clase 011 —empujar el filtro— aplicada a mano. El optimizador de MongoDB reordena algunos casos, pero no todos: cualquier etapa que calcule campos nuevos (`$addFields`, `$project`) bloquea el movimiento de las etapas posteriores.

Regla: **`$match` y `$limit` lo antes posible; `$lookup` y `$unwind` lo más tarde posible.**

```mermaid
flowchart LR
    M["$match<br/>usa índice"] --> S["$sort<br/>usa índice si sigue al match"]
    S --> L["$limit"]
    L --> P["$project<br/>reduce el tamaño"]
    P --> G["$group<br/>en memoria"]
    G --> LK["$lookup<br/>lo más tarde posible"]
```

## Ejemplo trabajado

Consulta: *«las 20 inscripciones activas más recientes del curso, con nota, ordenadas por fecha»*, sobre 5 millones de documentos.

**Sin índice adecuado:**

```javascript
db.enrollments.find({course_id: "curso-bd", estado: "activa"})
              .sort({registrada_en: -1}).limit(20).explain("executionStats")
```

```text
stage:                COLLSCAN
totalDocsExamined:    5 000 000
totalKeysExamined:    0
nReturned:            20
executionTimeMillis:  4 210
SORT: in-memory, 38 MB    ← cerca del límite de 100 MB
```

Cinco millones de documentos leídos para devolver 20. Además el ordenamiento se hace en memoria; superados los 100 MB, MongoDB aborta la consulta salvo que se permita el uso de disco.

**Con índice ESR:**

```javascript
db.enrollments.createIndex({course_id: 1, estado: 1, registrada_en: -1})
```

```text
stage:                IXSCAN → FETCH → LIMIT
totalKeysExamined:    20
totalDocsExamined:    20
nReturned:            20
executionTimeMillis:  1
SORT: ninguno    ← el índice ya entrega el orden
```

De 5 000 000 a 20 documentos examinados. La desaparición de la etapa `SORT` es tan importante como la reducción de lecturas: el índice ya está ordenado por `registrada_en` dentro de cada `(course_id, estado)`.

**Hacerla cubierta.** Si la interfaz solo necesita `student_id` y `nota`:

```javascript
db.enrollments.createIndex({course_id: 1, estado: 1, registrada_en: -1, student_id: 1, nota: 1})
db.enrollments.find({course_id: "curso-bd", estado: "activa"},
                    {_id: 0, student_id: 1, nota: 1, registrada_en: 1})
              .sort({registrada_en: -1}).limit(20)
// totalDocsExamined: 0
```

El índice es más ancho —más espacio y más costo por escritura— y a cambio la consulta no toca la colección. Compensa cuando esa consulta domina el tráfico; no compensa si es una de veinte.

**Índice parcial.** Si el 90 % de las inscripciones están activas, un índice parcial no aporta mucho. Si solo el 5 % está en estado `pendiente` y esa es la consulta caliente:

```javascript
db.enrollments.createIndex({course_id: 1, registrada_en: -1},
                           {partialFilterExpression: {estado: "pendiente"}})
```

El índice pasa de 5 millones de entradas a 250 000: cabe en memoria y se mantiene más barato. Requisito: la consulta debe incluir `estado: "pendiente"` explícitamente, o el motor no puede usarlo.

## Comparación

| Situación | Señal en el plan | Corrección |
|---|---|---|
| Sin índice útil | `COLLSCAN` | Crear índice siguiendo ESR |
| Índice mal ordenado | `IXSCAN` + `SORT` en memoria | Reordenar claves |
| Muchos documentos por resultado | `totalDocsExamined ≫ nReturned` | Añadir campos del filtro al índice |
| Proyección pequeña y repetida | `totalDocsExamined > 0` | Índice cubriente |
| Filtro muy selectivo y raro | Índice enorme | Índice parcial |

## Errores frecuentes

1. **Un índice por campo.** Los índices compuestos sirven a más consultas; el motor rara vez combina dos índices con eficacia.
2. **Ignorar el orden ESR.** Provoca ordenamientos en memoria y el límite de 100 MB.
3. **`$lookup` al principio de la canalización.** Multiplica el trabajo de todas las etapas siguientes.
4. **Índices que nadie usa.** Revisa `$indexStats`; cada índice se mantiene en cada escritura.
5. **Índice multiclave sobre arreglos largos.** Multiplica las entradas por la longitud del arreglo.
6. **Olvidar `_id: 0` en una consulta que se quiere cubierta.** Basta para que deje de serlo.

## De la clase a la operación

El síntoma habitual —«MongoDB se puso lento al crecer»— casi siempre significa que los índices dejaron de caber en memoria. Vigilar el tamaño total de los índices frente a la RAM disponible es más predictivo que cualquier métrica de CPU.

## Reto de transferencia

1. Toma la consulta más frecuente de tu dominio y captura su `explain` sin índice.
2. Diseña el índice con la regla ESR y vuelve a capturar.
3. Conviértela en consulta cubierta y compara los tres números del plan.
4. Mide el tamaño de los índices con `$indexStats` y elimina los que no se usan.

## Preguntas de evaluación

1. ¿Por qué el rango va al final en la regla ESR?
2. ¿Qué condiciones exactas debe cumplir una consulta cubierta?
3. Explica el efecto de un `$lookup` colocado antes de un `$match` selectivo.
4. Da un caso de tu dominio donde un índice parcial reduzca el tamaño más de un 80 %.

---

## Laboratorio

```bash
python scripts/validate_repository.py
python labs/05-nosql-workloads/run_lab.py
```

Guarda como evidencia la salida completa, la versión del motor y la semilla o
los parámetros usados. Una captura sin comando no es evidencia: no se puede
repetir.

## Evaluación

| Criterio | Peso | Qué se comprueba |
|---|---:|---|
| Comprensión conceptual | 25 % | Explica el mecanismo, no solo el resultado |
| Ejecución reproducible | 25 % | Otra persona obtiene lo mismo con las instrucciones dadas |
| Interpretación basada en evidencia | 25 % | Cada conclusión se apoya en una salida o una medición |
| Límites y riesgos declarados | 25 % | Dice qué no demuestra el ejercicio y qué faltaría en producción |

La clase se da por superada cuando la respuesta explica el mecanismo, muestra
la salida que la respalda y declara al menos un límite del ejercicio.

## Fuentes de esta clase

Todo lo afirmado arriba procede de estas obras. Los identificadores viven en
[`catalog/sources.json`](../../../catalog/sources.json) y el estado de los
enlaces se comprueba con `python scripts/check_external_links.py`.

- **MongoDB, Inc.** (2026). [MongoDB Manual](https://www.mongodb.com/docs/manual/).  
  Modelo documental, índices, agregación y transacciones multi-documento.
- **Shannon Bradshaw, Eoin Brazil, Kristina Chodorow** (2019). [MongoDB: The Definitive Guide](https://www.oreilly.com/library/view/mongodb-the-definitive/9781491954454/). 3.a ed. O'Reilly. ISBN 978-1-4919-5446-1.  
  Modelado documental, índices y canalización de agregación.
- **Markus Winand** (2012). [SQL Performance Explained](https://use-the-index-luke.com/). Markus Winand. ISBN 978-3-9503078-2-5.  
  Versión web gratuita. Índices B-Tree y su relación con el orden de las columnas.

---

> [Programa](../../../README.md) · [Parte 05](../README.md) · [← Anterior](../../part-05-documentos-y-clave-valor/025-modelado-documental-incrustar-o-referenciar/README.md) · [Siguiente →](../../part-05-documentos-y-clave-valor/027-clave-valor-cache-y-expiracion/README.md)
