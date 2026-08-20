# Diagnóstico inicial

**No tiene calificación y no sirve para juzgarte: sirve para elegir por dónde entrar.** Un
programa de 210 horas empezado en el punto equivocado se abandona; empezado en el correcto, se
termina.

Respóndelo **sin buscar nada** y por escrito. Si una respuesta te sale en dos líneas, está
bien; si te sale «depende», escribe de qué depende, que es la respuesta que importa.

## Parte 1 — Diez preguntas

Para cada una: responde, y marca si has dudado.

1. ¿Qué diferencia hay entre una base de datos y un gestor de bases de datos?
2. ¿Qué protege una clave foránea, y qué **no** protege?
3. ¿Por qué `NULL = NULL` no se comporta como una igualdad ordinaria en SQL?
4. ¿Qué problema resuelve una transacción que no resolvería escribir con cuidado?
5. ¿Cuándo un índice empeora el sistema?
6. ¿Qué diferencia hay entre un respaldo y una réplica?
7. ¿Qué significa que una operación sea idempotente, y por qué importa al reintentar?
8. En una base documental, ¿dónde se valida el esquema?
9. ¿Qué es una partición de red y por qué obliga a elegir?
10. ¿Qué mide `recall@k` en un sistema de recuperación?

### Clave de corrección

No hay respuestas «correctas» de una palabra. Esto es lo que distingue una respuesta sólida:

| # | Una respuesta sólida menciona | Señal de alarma |
|---|---|---|
| 1 | Que el gestor aporta concurrencia, integridad, recuperación e independencia de datos | «Es lo mismo» |
| 2 | Que garantiza que la referencia existe, pero no que el dato sea correcto | «Que no se borren datos» |
| 3 | Que `NULL` es «desconocido» y la comparación devuelve desconocido, no falso | «Es un cero» o «es vacío» |
| 4 | Atomicidad y aislamiento frente a fallo y frente a concurrencia | «Para poder deshacer» |
| 5 | El costo en cada escritura y el espacio; que un índice no usado solo cuesta | «Nunca empeora» |
| 6 | Que la réplica copia también el error, y el respaldo permite volver atrás en el tiempo | «Son lo mismo con otro nombre» |
| 7 | Que repetirla deja el mismo estado, y que sin eso los reintentos duplican | Confundirla con «sin efectos» |
| 8 | Que se valida en la aplicación salvo que se declare validación en el motor | «No hay esquema» |
| 9 | Que los nodos siguen vivos pero incomunicados, y hay que elegir qué sacrificar | «Que se cae la base» |
| 10 | Qué proporción de lo relevante aparece entre los `k` primeros, y que sin `k` no significa nada | Confundirlo con precisión |

## Parte 2 — Una práctica de quince minutos

Diseña tres tablas para estudiantes, cursos y matrículas. Después:

1. Escribe la consulta que lista los estudiantes de cada curso.
2. Explica **con qué restricción** impides que un estudiante se matricule dos veces en el mismo
   curso, y por qué esa restricción va en el motor y no en la aplicación.
3. Di qué devuelve tu consulta para un curso sin estudiantes, y si eso es lo que quieres.

La tercera pregunta es la que más información da sobre tu nivel real.

## Cómo usar el resultado

Cuenta las respuestas que has escrito **sin dudar** y que mencionan lo que pide la clave:

| Respuestas sólidas | Por dónde empezar |
|---|---|
| 0–3 | [Parte 00](../classes/part-00-fundamentos-datos-sistemas-y-metodo/README.md) completa, sin saltarte nada. Es el cimiento y se nota en todo lo demás. |
| 4–6 | [Parte 00](../classes/part-00-fundamentos-datos-sistemas-y-metodo/README.md) en lectura rápida y [Parte 01](../classes/part-01-modelado-conceptual-y-requisitos/README.md) completa; refuerza [SQL](../classes/part-03-sql-en-profundidad/README.md) con el [laboratorio 01](../labs/01-sql-foundations/README.md). |
| 7–8 | Empieza por la [Parte 03](../classes/part-03-sql-en-profundidad/README.md) y haz los [laboratorios 03 y 04](../labs/README.md) pronto: ahí suele estar la brecha de quien ya escribe SQL. |
| 9–10 | Elige tu [ruta por rol](../rutas/README.md) y ve a las partes avanzadas, **sin saltarte** transacciones, seguridad ni recuperación. Son las que más gente da por sabidas. |

Si has fallado la 6 o la 7 —respaldo frente a réplica, idempotencia—, no importa cuánto sepas
de SQL: empieza por las Partes 07 y 10. Son los dos errores que más caros salen en producción.

## Y después

El diagnóstico no se repite al final. Lo que cierra el programa es el
[examen por rol](examen-por-rol.md) y el
[proyecto final](../projects/capstone.md), evaluados con la [rúbrica](rubric.md).
