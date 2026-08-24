# Guía de estudio

Cómo recorrer las 74 clases de principio a fin: en qué orden, con qué método,
cuánto tiempo, y cómo saber en cada punto si puedes seguir o tienes que volver.

Esta guía es la pauta; el [modelo de aprendizaje](LEARNING-MODEL.md) explica por
qué está construida así, y el [glosario](../GLOSARIO.md) define los 306 términos
que se usan a lo largo del camino.

---

## 1. Cómo está construido el programa

El material tiene cuatro niveles y conviene saber qué se busca en cada uno,
porque están pensados para leerse en este orden y no en otro.

| Nivel | Dónde | Qué contiene | Cuándo se lee |
|---|---|---|---|
| Programa | [`README.md`](../README.md) | Qué es esto, la regla de las fuentes, el mapa de las 15 partes | Una vez, al empezar |
| Parte | `classes/part-NN/README.md` | Introducción, prerrequisitos, resultados, una ficha por clase, errores frecuentes, vocabulario y bibliografía de la parte | **Siempre antes de la primera clase de la parte** |
| Clase | `classes/part-NN/NNN-*/README.md` | De qué trata, qué se da por sabido, vocabulario, materia, ejemplo trabajado, comparación entre motores, laboratorio y fuentes | Una por sesión |
| Término | [`GLOSARIO.md`](../GLOSARIO.md) | Definición única, clase donde se trabaja, términos relacionados y fuente | Cada vez que una palabra no está clara |

El error más común de quien viene de otros repositorios es saltar directamente
al README de una clase. La portada de la parte existe precisamente para que no
haya que deducir del contexto ni por qué está esa clase ahí ni qué se supone que
ya sabes.

## 2. El método de una clase

El mismo en las 74, y el orden importa:

1. **Lee la ficha de la clase en la portada de su parte.** Dos minutos. Te dice
   para qué está esa clase y qué exige.
2. **Comprueba los prerrequisitos.** Cada clase abre con una tabla de lo que da
   por sabido. Si algo de la última columna no te suena, vuelve a esa clase:
   aquí se usará sin volver a explicarlo.
3. **Lee el vocabulario antes que la materia.** Está arriba a propósito. Cada
   término aparece definido antes de que el texto lo use.
4. **Ejecuta el ejemplo trabajado mientras lees**, no después. La mitad de lo
   que se aprende solo aparece cuando la salida no es la que esperabas.
5. **Lee la comparación entre motores completa**, incluidas las filas de los
   motores que *no* resuelven el caso. Descartar con un argumento escrito es la
   habilidad que se evalúa en el proyecto final.
6. **Responde por escrito las preguntas de evaluación.** Una respuesta que no
   cabe en tres líneas todavía no está entendida.
7. **Haz el reto de transferencia.** Es el único ejercicio que comprueba si el
   concepto se aplica a un caso que la clase no mostró.
8. **Guarda la evidencia:** comando, versión del motor, semilla y salida
   completa. Una captura sin comando no es evidencia, porque no se puede
   repetir.

Los pasos 6, 7 y 8 son los que se corrigen. Los cinco primeros son los que hacen
que valgan la pena.

## 3. El orden

**El orden por defecto es el numérico, del 001 al 074.** Cada clase declara sus
prerrequisitos explícitamente, y todos apuntan siempre hacia atrás: el
validador del repositorio rechaza cualquier prerrequisito que no preceda a su
clase, así que seguir la numeración nunca te deja con un hueco.

Tres atajos legítimos, y lo que cuesta cada uno:

- **Ya sabes SQL y quieres empezar por lo formal.** Empieza en la parte 01, pero
  no te saltes las clases 006, 009 y 010 —tipos, criterio de decisión y mapa de
  familias—: son las tres que más se dan por sabidas y menos se dominan.
- **Vas a por un rol concreto.** Las [rutas por rol](../rutas/README.md) declaran
  qué partes hacer y en qué orden, y qué clases no se saltan.
- **Necesitas una parte suelta.** Léela igualmente desde su portada: la sección
  «Antes de esta parte» te dice qué vocabulario mínimo hace falta, y el glosario
  cubre lo que falte.

Lo que no es un atajo legítimo: saltarse la parte 08. Transacciones y
aislamiento sostienen las partes 09, 10 y 12, y sin ellas el resto se lee como
una lista de nombres.

## 4. Ritmo y tiempo

230 horas estimadas de trabajo real: lectura, ejecución de los laboratorios,
respuestas escritas y evidencia. No incluye el proyecto final más allá de sus
6 horas nominales, que en la práctica se quedan cortas.

| Ritmo | Dedicación | Duración | Para quién |
|---|---|---|---|
| Intensivo | 20 h/semana | ~12 semanas | Dedicación completa o bootcamp |
| Sostenido | 10 h/semana | ~23 semanas | Compaginado con trabajo |
| De fondo | 5 h/semana | ~46 semanas | Estudio de mantenimiento |

Recomendación práctica: una clase por sesión, sin partirla. Las clases de 3 y
4 horas están dimensionadas para una sesión larga, y partir el laboratorio a la
mitad obliga a rehacer el montaje del entorno.

## 5. Cómo saber si puedes seguir

Al final de cada parte, antes de pasar a la siguiente:

- ¿Puedes responder de memoria los **resultados de aprendizaje** que la portada
  de la parte declaró? Están escritos como verbos comprobables a propósito.
- ¿Reconoces los **errores frecuentes** de la parte y sabes por qué son falsos?
  Si alguno te sonaba propio, esa es la clase a la que hay que volver.
- ¿Puedes explicar cada término del **vocabulario de la parte** sin releerlo?
- ¿Tienes **evidencia guardada** de los laboratorios, con comando y versión?

Si fallan los dos primeros, vuelve. Si falla el tercero, el glosario está para
eso. Si falla el cuarto, no hay nota que dar: no hay nada que revisar.

Para una comprobación externa, el [diagnóstico inicial](../assessments/diagnostic.md)
sitúa el punto de partida y el [examen por rol](../assessments/examen-por-rol.md)
comprueba el de llegada.

## 6. Qué hacer cuando algo no sale

- **No entiendo un término.** Búscalo en el [glosario](../GLOSARIO.md). Cada
  entrada dice en qué clase se trabaja y con qué otros términos se relaciona.
- **El ejemplo no da el resultado del texto.** Comprueba primero la versión del
  motor: cada comparación declara qué se ejecutó y contra qué. Las diferencias
  entre dialectos están documentadas en la parte 05.
- **El laboratorio falla.** Ejecuta `python scripts/validate_repository.py`
  antes que nada; comprueba después el entorno con
  [`docs/ENVIRONMENTS.md`](ENVIRONMENTS.md).
- **Entiendo la clase pero no el reto de transferencia.** Es la señal esperada
  de que el concepto todavía está atado al ejemplo. Vuelve a los fundamentos de
  la clase y busca qué parte del mecanismo no se movió contigo.
- **Voy demasiado lento.** Lo normal. Las horas estimadas suponen ejecutar todo,
  no solo leer.

## 7. Qué produce este programa

Al terminar deberías tener tres cosas, y las tres son revisables por otra
persona:

1. **Un cuaderno de evidencia** con la salida de los laboratorios, cada una con
   su comando, su versión y su semilla.
2. **Un conjunto de registros de decisión** que expliquen por qué elegiste cada
   motor y cada modelo, con las alternativas descartadas.
3. **Un proyecto final defendible**: diseñado, medido y con sus límites
   declarados por escrito.

Lo que se evalúa no es que el sistema funcione, sino que puedas decir qué
mediste, qué descartaste y con qué dato. El detalle está en la
[rúbrica](../assessments/rubric.md).

---

> [Programa](../README.md) · [Índice de clases](../classes/README.md) ·
> [Glosario](../GLOSARIO.md) · [Modelo de aprendizaje](LEARNING-MODEL.md) ·
> [Rutas por rol](../rutas/README.md) · [Evaluación](../assessments/README.md)
