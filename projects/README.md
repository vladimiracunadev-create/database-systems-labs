# 🏗️ Proyectos

Las clases explican mecanismos y los [laboratorios](../labs/README.md) los demuestran de uno en
uno. Los proyectos son donde todo eso se junta y aparece la parte difícil: **decidir con
información incompleta y sostener la decisión ante alguien que pregunta**.

## Qué hay aquí

| Documento | Para qué |
|---|---|
| [Dominios canónicos](canonical-domains.md) | Los cinco dominios del programa, con su invariante, su patrón de acceso y la forma concreta en que cada uno rompe |
| [Proyecto final](capstone.md) | El encargo integrador: nueve fases, sus entregables, la defensa y la lista de comprobación previa |
| [Portafolio verificable](portafolio.md) | Cómo convertir la evidencia acumulada en algo que se pueda enseñar |

Se evalúan con la [rúbrica](../assessments/rubric.md), y valen el **25 %** de la nota del
programa; las decisiones de arquitectura, otro 15 %.

## Cómo se trabaja

1. **Elige un dominio y no lo cambies.** Los cinco están descritos con su dificultad central;
   elige por la dificultad que quieras aprender, no por la que te resulte cómoda.
2. **Empieza por la alternativa más simple.** Diseña primero el sistema con un solo motor. En la
   mayoría de los casos basta, y descubrirlo a tiempo vale más que cualquier arquitectura
   elegante.
3. **Provoca los problemas.** Nadie aprende recuperación esperando a que falle algo: se borra a
   propósito y se restaura. Lo mismo con la concurrencia y con la carga.
4. **Deja rastro de cada fase.** Si una fase no produce un archivo, no ocurrió.
5. **Prepara la defensa desde el principio.** Las preguntas están publicadas en el
   [proyecto final](capstone.md#la-defensa): no hay sorpresa, solo trabajo.

## Lo que distingue un buen proyecto

No es el número de motores ni el tamaño del diagrama. Es esto:

- una **medición propia** que respalde la decisión principal;
- una **anomalía reproducida** y corregida, con la traza de las dos;
- una **restauración ejecutada** y cronometrada, no una política escrita;
- un **ADR** que otra persona pueda usar para revisar la decisión dentro de dos años;
- y una frase que casi nadie escribe: **qué no demuestra este trabajo**.

## El error más común

Construir la arquitectura políglota que se tenía en la cabeza antes de leer los requisitos.
El programa entero está diseñado para hacer visible ese sesgo: por eso la fase 3 del proyecto
final obliga a diseñar la alternativa de un solo motor **antes** de justificar cualquier otra
cosa, y por eso la rúbrica premia la decisión revertible por encima de la ambiciosa.
