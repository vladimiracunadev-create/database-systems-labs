# Laboratorio 02 — Modelado políglota del mismo dominio

> El único laboratorio del programa que no se ejecuta: se entrega escrito. Aquí lo que se
> evalúa no es un resultado, es una decisión y su justificación.

**Duración:** 120 minutos · **Dependencias:** un editor de texto (contenedores, opcionales)
· **Entrega:** documento con los tres modelos y la decisión razonada
· **Partes:** [01](../../classes/part-01-modelado-conceptual-y-requisitos/README.md) ·
[05](../../classes/part-05-documentos-y-clave-valor/README.md) ·
[06](../../classes/part-06-grafos-columnas-tiempo-y-busqueda/README.md) ·
[13](../../classes/part-13-arquitectura-y-proyecto-final/README.md)

## 🎯 Qué demuestra

Que el mismo dominio admite varias representaciones correctas, y que elegir una es aceptar un
conjunto de consultas baratas y otro de consultas caras. Quien no ha modelado el mismo problema
tres veces tiende a creer que su modelo habitual es «el natural».

## 🔬 Hipótesis

1. El modelo relacional resolverá sin trabajo extra las consultas de agregación por curso y las
   restricciones de integridad; pagará en las rutas de aprendizaje de profundidad variable.
2. El modelo documental resolverá la ficha completa del curso en un acceso; pagará en
   duplicación y en actualizaciones que tocan muchos documentos.
3. El modelo de grafo resolverá los recorridos de prerrequisitos con longitud desconocida;
   pagará en operación —otro motor más que respaldar, monitorizar y actualizar—.

## ▶️ Cómo se hace

No hay guion que ejecutar. El material de partida está en la carpeta:

- [`course-document.example.json`](course-document.example.json) — la ficha de curso como
  documento agregado.
- [`learning-graph.example.cypher`](learning-graph.example.cypher) — el mismo dominio como grafo
  de propiedades.
- El modelo relacional canónico vive en
  [`reference-data/school/schema.sqlite.sql`](../../reference-data/school/schema.sqlite.sql).

Para cada uno de los tres modelos, escribe:

1. **El esquema o la forma del dato**, completo, no un esbozo.
2. **Tres consultas del negocio** resueltas en su lenguaje: agregación por curso, ficha
   completa de un curso y recorrido de prerrequisitos.
3. **Qué gana y qué pierde**: accesos por consulta, duplicación introducida, integridad que ya
   no puede garantizar el motor.
4. **La decisión**: cuál elegirías para este dominio y bajo qué carga cambiarías de opinión.

## 📊 Cómo se evalúa

| Criterio | Qué se busca |
| --- | --- |
| Completitud | Los tres modelos están, con esquema y consultas, no solo descritos |
| Costos declarados | Cada elección viene con lo que cuesta, no solo con lo que resuelve |
| Carga explícita | La decisión menciona relación lectura/escritura y volumen, no preferencias |
| Reversibilidad | Dice cómo se migraría si la decisión resulta equivocada |
| Honestidad | Declara qué no probó |

No se acepta «es más escalable» como justificación: escalable ¿en qué dimensión, con qué carga y
frente a qué alternativa?

## 🧪 Extensiones

1. Añade un requisito nuevo —«un estudiante puede repetir un curso en otro periodo»— y anota
   qué cambia en cada modelo. Normalmente uno resiste y los otros dos duelen.
2. Modela la misma ficha con incrustación y con referencia, y estima accesos y bytes con el
   método del [laboratorio 05](../05-nosql-workloads/README.md).
3. Escribe la consulta de prerrequisitos en SQL recursivo (`WITH RECURSIVE`) y compárala con la
   versión de grafo: no siempre gana el grafo, y saber cuándo es el conocimiento útil.

## 🏭 Contrastar contra los motores reales

```bash
docker compose --profile document --profile cache up -d
```

Carga tus documentos en MongoDB y comprueba si las consultas que diseñaste se pueden expresar
tal como las escribiste. La distancia entre el modelo del papel y el del motor es donde se
aprende.

## 🎓 Dónde encaja

- **Clases:** [024–027](../../classes/part-05-documentos-y-clave-valor/README.md),
  [028](../../classes/part-06-grafos-columnas-tiempo-y-busqueda/028-grafos-de-propiedades-y-recorridos/README.md),
  [062 — Persistencia políglota por evidencia](../../classes/part-13-arquitectura-y-proyecto-final/062-persistencia-poliglota-por-evidencia/README.md).
- **Rutas:** [Arquitecto de datos](../../rutas/arquitectura.md),
  [Ingeniero de datos](../../rutas/ingenieria-de-datos.md).
- **Certificaciones:** el dominio de datos no relacionales del
  [DP-900](../../certificaciones/dp-900.md) y la gestión de almacenes del
  [AWS Data Engineer Associate](../../certificaciones/aws-dea-c01.md).

## 📖 Fuentes

- **Pramod Sadalage, Martin Fowler**, *NoSQL Distilled* — el marco de familias de modelos y el
  concepto de persistencia políglota.
- **MongoDB: Data Modeling** — la guía oficial sobre incrustar frente a referenciar.
- **Neo4j Documentation** — grafos de propiedades y recorridos.
- **Ian Robinson, Jim Webber, Emil Eifrem**, *Graph Databases* — cuándo el grafo gana de verdad.

Fichas completas en el [registro de fuentes](../../catalog/sources.json).

## 🧹 Limpieza

Si levantaste contenedores: `docker compose --profile document --profile cache down -v`.
