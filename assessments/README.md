# 📝 Evaluación

Este programa no evalúa memoria. La regla que ordena todo lo que hay en esta carpeta es la
misma que aparece en cada clase:

> **Un resultado correcto sin explicación no demuestra transferencia.**

De ahí salen dos consecuencias prácticas. La primera: casi todo lo evaluable es **evidencia
reproducible** —un comando, su salida y una explicación—, no una respuesta marcada. La segunda:
la rúbrica está escrita para que la aplique alguien que no conoce el programa, porque una
evaluación que solo entiende su autor no es una evaluación.

## Las cinco piezas

| Pieza | Peso | Qué evalúa | Dónde está |
| --- | ---: | --- | --- |
| Diagnóstico inicial | 0 % | Por dónde empezar, no cuánto sabes | [`diagnostic.md`](diagnostic.md) |
| Evidencias de laboratorio | 40 % | Que ejecutaste, entendiste y declaraste límites | [`evidencias.md`](evidencias.md) |
| Retos de transferencia | 20 % | Que lo aplicaste a tu propio contexto | Al final de cada clase |
| Decisiones de arquitectura | 15 % | Que puedes justificar y revertir una elección | [`../projects/capstone.md`](../projects/capstone.md) |
| Proyecto final | 25 % | Todo junto, defendido ante preguntas | [`rubric.md`](rubric.md) |

**Aprobación: 80 sobre 100**, y además los mínimos por dimensión de la rúbrica. Los pesos viven
en [`curriculum.yaml`](../curriculum.yaml), no aquí: esta tabla se compara con ellos en las
pruebas del repositorio.

## Los tres documentos que se generan

- **[Rúbrica del proyecto final](rubric.md)** — diez dimensiones, cuatro niveles descritos en
  cada una, el mínimo exigido y la evidencia que hay que ver. Generada desde el currículo.
- **[Examen final por rol](examen-por-rol.md)** — teoría, práctica y defensa para cada una de
  las siete [rutas](../rutas/README.md), con sus laboratorios y clases clave. Generado.
- **[Banco de autoevaluación](https://vladimiracunadev-create.github.io/database-systems-labs/autoevaluacion.html)**
  — las 256 preguntas de evaluación del programa, reunidas y enlazadas a su clase. Generado
  desde las lecciones.

Que sean generados no es un detalle técnico: significa que **no pueden contradecir al
programa**. Si una clase cambia de laboratorio o una parte cambia de horas, la evaluación
cambia con ella o la integración continua falla.

## Cómo se evalúa una evidencia de laboratorio

Cada laboratorio produce una salida. Lo que se corrige no es la salida —esa la produce el
ordenador— sino lo que la acompaña:

1. **Hipótesis previa.** Qué esperabas que pasara, escrito **antes** de ejecutar. Sin esto, la
   ejecución es un trámite.
2. **Comando y entorno.** Lo que ejecutaste, literal, y dónde. Una captura sin comando no es
   evidencia: no se puede repetir.
3. **Salida completa.** Sin recortar la parte que no encaja.
4. **Explicación del mecanismo.** Por qué el resultado es el que es. Aquí se ve quién entendió.
5. **Límite declarado.** Qué **no** demuestra este experimento. Es la parte que distingue una
   entrega de nivel 4 de una de nivel 2.

El punto 5 se puntúa igual que los demás. Un trabajo que cree haberlo demostrado todo es un
trabajo que todavía no sabe lo que hizo.

## Para quien corrige

- Empieza por reproducir **una** afirmación del trabajo. Si no puedes con las instrucciones
  entregadas, ninguna dimensión de esa parte pasa de nivel 2.
- Pregunta siempre «¿y qué pasaría si…?». La respuesta separa a quien copió un procedimiento de
  quien entendió el mecanismo.
- Usa la rúbrica dimensión a dimensión y anota una frase por cada una. La nota sin la frase no
  enseña nada.
- Revisa las [faltas críticas](rubric.md#faltas-críticas) antes de poner la nota: suspenden con
  independencia de ella.

## Para quien estudia

- Haz el [diagnóstico](diagnostic.md) sin buscar nada: sirve para elegir por dónde entrar, no
  para juzgarte.
- Guarda la evidencia **mientras** trabajas, no al final. El «yo me acuerdo» no sobrevive a la
  redacción del informe tres días después.
- Cuando termines una parte, responde sus preguntas de autoevaluación **por escrito**. Explicar
  en voz alta se siente más fácil de lo que es.
- Prepara la defensa asumiendo que quien pregunta va a buscar el límite de lo que afirmas.
