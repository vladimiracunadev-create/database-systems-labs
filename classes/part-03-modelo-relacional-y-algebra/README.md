# Parte 03 — Modelo relacional y álgebra

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

La teoría que SQL implementa a medias: relaciones como conjuntos, operadores del álgebra, cálculo relacional e integridad declarada.

**4 clases · 13 horas · 19 conceptos · 8 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 02 — Modelado conceptual y requisitos](../part-02-modelado-conceptual-y-requisitos/README.md)

## De qué trata esta parte

Esta parte da la teoría que SQL implementa a medias, y lo hace precisamente para que las diferencias entre teoría y lenguaje dejen de ser sorpresas. La relación de Codd es un conjunto: no tiene orden y no tiene duplicados. SQL trabaja con multiconjuntos ordenables. Conocer esa brecha explica de antemano por qué hace falta `DISTINCT`, por qué no se puede confiar en el orden y por qué `NOT IN` se comporta como se comporta.

Las cuatro clases van de la definición al operador y del operador a la garantía. La relación como conjunto; los operadores del álgebra, que son el lenguaje en el que el optimizador piensa; el cálculo relacional y el teorema de equivalencia, que es literalmente el permiso que tiene el motor para reescribir tu consulta; y la integridad declarada en su forma completa, incluidas las acciones referenciales.

Es la parte más formal del programa y la que más rendimiento da a largo plazo: quien la trabaja lee después un plan de ejecución sin adivinar.

## Al terminar esta parte podrás

1. Explicar las dos propiedades de la relación que SQL no respeta y sus consecuencias prácticas.
2. Traducir una consulta SQL a una expresión del álgebra relacional y viceversa.
3. Argumentar por qué el optimizador puede reordenar una consulta sin cambiar su resultado.
4. Declarar integridad de entidad, referencial y de dominio, eligiendo la acción referencial adecuada.

## Mapa de la parte

```mermaid
flowchart LR
    C020["020<br/>La relación como conjunto: tuplas, domini…"]
    C021["021<br/>Álgebra relacional: selección, proyección…"]
    C022["022<br/>Cálculo relacional y su equivalencia con…"]
    C023["023<br/>Integridad: restricciones, claves foranea…"]
    C020 --> C021
    C021 --> C022
    C022 --> C023
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C020 fund
    class C021 fund
    class C022 inter
    class C023 inter
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [020](020-la-relacion-como-conjunto/README.md) | [La relación como conjunto: tuplas, dominios y acceso por valor](020-la-relacion-como-conjunto/README.md) | Fundamentos | 3 | 3 |
| [021](021-algebra-relacional-operadores/README.md) | [Álgebra relacional: selección, proyección, producto y reunión](021-algebra-relacional-operadores/README.md) | Fundamentos | 4 | 3 |
| [022](022-calculo-relacional-y-equivalencia/README.md) | [Cálculo relacional y su equivalencia con el álgebra](022-calculo-relacional-y-equivalencia/README.md) | Intermedio | 3 | 3 |
| [023](023-integridad-restricciones-y-acciones-referenciales/README.md) | [Integridad: restricciones, claves foraneas y acciones referenciales](023-integridad-restricciones-y-acciones-referenciales/README.md) | Intermedio | 3 | 4 |

## Las clases, una por una

### [020 — La relación como conjunto: tuplas, dominios y acceso por valor](020-la-relacion-como-conjunto/README.md)

*Fundamentos · 3 h · 3 fuentes · requiere [001](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md), [004](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/004-leer-datos-select-where-y-order-by/README.md)*

La relación como conjunto de tuplas sobre dominios, con dos propiedades que SQL no respeta: no hay orden y no hay duplicados. Entender esa brecha explica de antemano la mitad de las sorpresas del lenguaje, del `DISTINCT` que hace falta al `ORDER BY` que no se puede dar por supuesto.

**Conceptos que introduce:** `relación` · `tupla` · `dominio` · `acceso por valor` · `cierre`

[Ir a la clase →](020-la-relacion-como-conjunto/README.md)

### [021 — Álgebra relacional: selección, proyección, producto y reunión](021-algebra-relacional-operadores/README.md)

*Fundamentos · 4 h · 3 fuentes · requiere [020](020-la-relacion-como-conjunto/README.md)*

Los operadores del álgebra relacional —selección, proyección, producto, reunión y división— como el lenguaje en el que el optimizador piensa. Ver una consulta como una expresión algebraica es lo que después permite entender por qué el motor la reordena y por qué eso es legítimo.

**Conceptos que introduce:** `selección` · `proyección` · `producto cartesiano` · `reunión natural` · `división`

[Ir a la clase →](021-algebra-relacional-operadores/README.md)

### [022 — Cálculo relacional y su equivalencia con el álgebra](022-calculo-relacional-y-equivalencia/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [021](021-algebra-relacional-operadores/README.md)*

El cálculo relacional y el teorema que lo hace equivalente al álgebra. No es formalismo por gusto: esa equivalencia es exactamente el permiso que tiene el optimizador para reescribir tu consulta, y la razón de que SQL pueda ser declarativo.

**Conceptos que introduce:** `cálculo de tuplas` · `seguridad de expresión` · `equivalencia` · `declaratividad`

[Ir a la clase →](022-calculo-relacional-y-equivalencia/README.md)

### [023 — Integridad: restricciones, claves foraneas y acciones referenciales](023-integridad-restricciones-y-acciones-referenciales/README.md)

*Intermedio · 3 h · 4 fuentes · requiere [008](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/008-dos-tablas-y-una-relacion/README.md), [016](../part-02-modelado-conceptual-y-requisitos/016-entidad-relacion-cardinalidad-y-participacion/README.md)*

La integridad declarada en su forma completa: integridad de entidad, integridad referencial, `CHECK` y las acciones referenciales. Insiste en que `ON DELETE CASCADE` es una decisión de dominio y no técnica, y presenta el aplazamiento para los casos en que el estado intermedio tiene que ser inválido.

**Conceptos que introduce:** `integridad de entidad` · `integridad referencial` · `CHECK` · `ON DELETE` · `aplazamiento`

[Ir a la clase →](023-integridad-restricciones-y-acciones-referenciales/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «Álgebra relacional es teoría que no se usa.» Es exactamente lo que muestra un plan de ejecución: selecciones, proyecciones y reuniones reordenadas.
- «`SELECT` devuelve un conjunto.» Devuelve un multiconjunto: los duplicados sobreviven salvo que se pidan `DISTINCT` o se agrupen.
- «`ON DELETE CASCADE` es lo cómodo.» Es una decisión de dominio: sobre datos contables o de auditoría, borra historia que había obligación de conservar.
- «La reunión natural es más limpia.» Y más frágil: empareja por todos los nombres coincidentes, así que añadir una columna homónima cambia el significado de la consulta sin avisar.

## Vocabulario de la parte

Los 19 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **acceso por valor** | En el modelo relacional se llega a un dato por lo que vale, nunca por un puntero o una posición física. Es lo que hace posible la independencia de datos: el motor puede reorganizar el almacenamiento sin invalidar ninguna referencia. | [020](020-la-relacion-como-conjunto/README.md) |
| **aplazamiento** | Postergar la comprobación de una restricción hasta el `COMMIT` (`DEFERRABLE INITIALLY DEFERRED`). Permite estados intermedios inválidos dentro de la transacción —como insertar dos filas que se referencian mutuamente— sin renunciar a la garantía final. | [023](023-integridad-restricciones-y-acciones-referenciales/README.md) |
| **CHECK** | Restricción que exige que una expresión sea verdadera en cada fila: `CHECK (precio >= 0)`. Convierte una regla de negocio en algo que el motor impone; cuidado con los nulos, porque `UNKNOWN` no viola un `CHECK`. | [023](023-integridad-restricciones-y-acciones-referenciales/README.md) |
| **cierre** | Propiedad por la que toda operación del álgebra relacional sobre relaciones devuelve una relación. Es lo que permite anidar y componer consultas indefinidamente, y lo que sostiene las vistas y las CTE. | [020](020-la-relacion-como-conjunto/README.md) |
| **cálculo de tuplas** | Formalismo que describe el resultado con una fórmula lógica —«las tuplas t tales que…»— en lugar de con una secuencia de operadores. Es el antepasado directo de SQL y la razón formal de que SQL sea declarativo. | [022](022-calculo-relacional-y-equivalencia/README.md) |
| **declaratividad** | Decir qué se quiere, no cómo obtenerlo. Su valor práctico es que el motor puede cambiar de estrategia —de recorrido completo a índice, de reunión anidada a hash— cuando cambian los datos, sin que nadie toque el código. | [022](022-calculo-relacional-y-equivalencia/README.md) |
| **división** | Operador que responde a las preguntas de tipo «para todos»: qué estudiantes están inscritos en *todos* los cursos obligatorios. SQL no tiene un operador equivalente y se resuelve con doble negación (`NOT EXISTS` anidado) o contando. | [021](021-algebra-relacional-operadores/README.md) |
| **dominio** | El conjunto de valores admisibles de un atributo, con sus operaciones. Es el concepto del que los tipos de SQL son una aproximación pobre: SQL permite comparar un número de teléfono con un código postal si ambos son enteros. | [020](020-la-relacion-como-conjunto/README.md) |
| **equivalencia** | Dos expresiones son equivalentes si devuelven la misma relación para toda base de datos posible. Codd demostró que álgebra y cálculo tienen el mismo poder expresivo; sobre ese teorema descansa la libertad del optimizador para reescribir consultas. | [022](022-calculo-relacional-y-equivalencia/README.md) |
| **integridad de entidad** | Regla que exige que ninguna columna de la clave primaria sea nula. Su fundamento no es estético: un identificador desconocido no identifica, y la fila deja de ser referenciable. | [023](023-integridad-restricciones-y-acciones-referenciales/README.md) |
| **integridad referencial** | Regla que exige que todo valor de clave foránea apunte a una fila existente o sea nulo. El gestor la comprueba en cada escritura, lo que la hace inmune a la aplicación que se olvidó de validar. | [023](023-integridad-restricciones-y-acciones-referenciales/README.md) |
| **ON DELETE** | Acción referencial que declara qué pasa con las filas hijas cuando se borra la padre: `RESTRICT` lo impide, `CASCADE` las borra, `SET NULL` las desvincula. Es una decisión de dominio, no técnica: `CASCADE` sobre datos contables borra historia. | [023](023-integridad-restricciones-y-acciones-referenciales/README.md) |
| **producto cartesiano** | Operador × que combina cada tupla de una relación con todas las de otra. Casi nunca se quiere: aparecer en un plan de ejecución suele indicar una condición de reunión olvidada y una explosión de filas. | [021](021-algebra-relacional-operadores/README.md) |
| **proyección** | Quedarse con un subconjunto de columnas. Reduce el ancho de la fila, no su cantidad —salvo que se eliminen los duplicados resultantes con `DISTINCT`, cosa que SQL no hace por defecto y el álgebra sí. | [021](021-algebra-relacional-operadores/README.md) |
| **relación** | En el modelo de Codd, un conjunto de tuplas sobre unos dominios dados. Al ser conjunto no tiene orden ni duplicados —dos propiedades que SQL no respeta, y de ahí nacen la mitad de las sorpresas del lenguaje. | [020](020-la-relacion-como-conjunto/README.md) |
| **reunión natural** | Reunión que empareja por todos los atributos con el mismo nombre y deja una sola copia de cada uno. Elegante en el álgebra y peligrosa en SQL: si alguien añade una columna homónima, la consulta cambia de significado sin avisar. | [021](021-algebra-relacional-operadores/README.md) |
| **seguridad de expresión** | Condición que garantiza que una fórmula del cálculo devuelve un resultado finito. `{t \| ¬P(t)}` no es segura: «todo lo que no cumple P» incluye el universo entero. Es la razón de que SQL obligue a nombrar siempre un `FROM`. | [022](022-calculo-relacional-y-equivalencia/README.md) |
| **selección** | Operador σ del álgebra: se queda con las tuplas que cumplen un predicado. Es el `WHERE` de SQL y el primero que el optimizador intenta empujar hacia abajo en el plan, para descartar filas antes de reunirlas. | [021](021-algebra-relacional-operadores/README.md) |
| **tupla** | Un elemento de la relación: una asignación de un valor a cada atributo. No es «una fila en una posición», porque en un conjunto no hay posiciones; se identifica por sus valores, no por dónde está. | [020](020-la-relacion-como-conjunto/README.md) |

## Fuentes usadas en esta parte

8 obras distintas sostienen lo que se afirma en estas
4 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **Raghu Ramakrishnan, Johannes Gehrke** (2002). [Database Management Systems](https://pages.cs.wisc.edu/~dbbook/). 3.a ed. McGraw-Hill. ISBN 978-0-07-246563-1.  
  Fuerte en álgebra relacional, evaluación de consultas y estructuras de almacenamiento.  
  *Se cita en las clases 020, 021, 022.*
- **Abraham Silberschatz, Henry F. Korth, S. Sudarshan** (2019). [Database System Concepts](https://db-book.com/). 7.a ed. McGraw-Hill. ISBN 978-0-07-802215-9.  
  Texto de referencia universitario. El sitio oficial publica diapositivas y capítulos de muestra.  
  *Se cita en las clases 021.*
- **Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom** (2008). [Database Systems: The Complete Book](http://infolab.stanford.edu/~ullman/dscb.html). 2.a ed. Pearson. ISBN 978-0-13-187325-4.  
  Tratamiento formal de dependencias funcionales, normalización y optimización.  
  *Se cita en las clases 021, 022.*
- **C. J. Date** (2015). [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/). 3.a ed. O'Reilly. ISBN 978-1-4919-4117-1.  
  Separa el modelo relacional de lo que SQL realmente implementa, incluidos los nulos.  
  *Se cita en las clases 020, 022, 023.*
- **PostgreSQL Global Development Group** (2026). [PostgreSQL Documentation](https://www.postgresql.org/docs/current/).  
  Documentación de referencia del motor relacional principal del programa.  
  *Se cita en las clases 023.*
- **E. F. Codd** (1970). [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685). Communications of the ACM 13(6). DOI [10.1145/362384.362685](https://doi.org/10.1145/362384.362685).  
  Artículo fundacional del modelo relacional y de la independencia de datos.  
  *Se cita en las clases 020.*
- **E. F. Codd** (1979). [Extending the Database Relational Model to Capture More Meaning](https://dl.acm.org/doi/10.1145/320107.320109). ACM TODS 4(4). DOI [10.1145/320107.320109](https://doi.org/10.1145/320107.320109).  
  Introduce los valores nulos y la semántica de información faltante.  
  *Se cita en las clases 023.*
- **ISO/IEC JTC 1/SC 32** (2023). [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html).  
  Norma del lenguaje SQL. Ningún motor la implementa por completo.  
  *Se cita en las clases 023.*

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
