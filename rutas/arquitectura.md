# 🏛️ Arquitecto de datos

> Decides qué se guarda dónde, con qué garantías y a qué costo, y después tienes que
> defenderlo delante de gente que preferiría otra cosa. Tu producto no es un diagrama: es una
> decisión con evidencia, con límites declarados y con vuelta atrás.
>
> **Nivel de entrada:** avanzado (requiere haber operado o construido sistemas reales) ·
> **Foco:** elección de motor y modelo, garantías distribuidas y costo total ·
> **Cargos habituales:** arquitecto de datos, arquitecto de soluciones, ingeniero de staff.

## 🧭 Qué es y por qué importa

Un arquitecto de datos no es «el que sabe más SQL». Es quien responde preguntas que no tienen
respuesta única: ¿un motor o cinco? ¿consistencia fuerte o disponibilidad bajo partición?
¿duplicamos el dato para servir esta consulta o pagamos la reunión cada vez? Cada respuesta
tiene un costo que alguien pagará durante años: en dinero, en complejidad operativa y en
libertad para cambiar de idea.

Importa porque estas decisiones son las más caras de revertir. Cambiar un framework web es un
trimestre incómodo; cambiar el modelo de datos de un sistema en producción es un proyecto con
riesgo de pérdida. Por eso el oficio consiste tanto en decidir como en **dejar constancia**:
qué contexto había, qué alternativas se consideraron, qué medición apoyó la elección y qué
tendría que cambiar para revisarla.

La tentación del rol es opinar sin medir. La disciplina que este programa impone —cada
afirmación con su fuente, cada conclusión con su evidencia— es exactamente el antídoto. Una
arquitectura defendida con «es lo estándar» o «lo usa Netflix» no es una arquitectura: es una
apuesta con el dinero de otro.

Lo que aquí **no** vas a aprender: la política de una organización, que es la mitad del
trabajo. Convencer a tres equipos con incentivos distintos no se estudia; se practica.

## 🗓️ Un día en el puesto

- **Una propuesta que llega con la solución ya elegida.** Tu primer trabajo es reconstruir el
  problema: patrón de acceso, volumen, latencia aceptable, consistencia necesaria.
- **Comparar dos opciones con datos.** No con tablas de marketing: con una prueba pequeña sobre
  el dominio real y una medición reproducible.
- **Escribir un registro de decisión (ADR).** Contexto, alternativas, decisión, consecuencias y
  criterio de revisión. Media página que ahorra un año de discusiones.
- **Revisar un diseño ajeno.** Buscar el punto donde la garantía prometida no se sostiene: una
  transacción que cruza dos sistemas, un identificador que no es único, una réplica leída como
  si fuera la fuente de verdad.
- **Hablar de dinero.** Licencias, almacenamiento, transferencia, personas que operarán eso.
  El costo total incluye el equipo que se levanta de madrugada.
- **Decir que no.** A un motor más «porque encaja bonito», a una consistencia más fuerte de la
  necesaria, a una migración sin plan de vuelta.

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **Todos los modelos, con criterio:** relacional, documental, clave-valor, grafo, columna
  ancha, series temporales, búsqueda y vectorial —qué problema resuelve cada uno y qué exige a
  cambio—.
- **Garantías distribuidas sin folclore:** CAP y PACELC leídos con precisión, modelos de
  consistencia, garantías de sesión, consenso y por qué las transacciones distribuidas son
  caras.
- **Transacciones y recuperación:** para saber qué prometes cuando prometes durabilidad.
- **Rendimiento con medición:** planes, índices, formatos y particionado; la diferencia entre
  una intuición y un experimento.
- **Evolución:** migraciones, compatibilidad, versionado de esquemas y el costo de cada
  acoplamiento que introduces.
- **Costo total de propiedad:** infraestructura, licencias, operación, formación y la deuda que
  dejas.

### Herramientas del oficio

- Prototipos pequeños y reproducibles: contenedores con el motor candidato y datos propios.
- Registros de decisión (ADR) versionados junto al código.
- Diagramas que expliquen el flujo del dato y las garantías, no el organigrama del sistema.
- Herramientas de medición: planes de ejecución, generadores de carga, métricas de latencia por
  percentil.

### Habilidades no técnicas

- **Escribir para que otro decida:** un documento que se entiende sin ti es la mitad del valor.
- **Escuchar la restricción real** detrás de la petición: presupuesto, plazo, equipo, miedo.
- **Sostener una decisión impopular** con evidencia, y **cambiarla en público** cuando la
  evidencia cambia.

## 📚 Tu ruta en el programa

Las 14 partes, 210 horas. Es la única ruta completa, y con razón: no puedes elegir entre
modelos que no conoces.

- 📚 [Parte 00 — Fundamentos](../classes/part-00-fundamentos-datos-sistemas-y-metodo/README.md) ·
  [01 — Modelado](../classes/part-01-modelado-conceptual-y-requisitos/README.md) ·
  [02 — Modelo relacional](../classes/part-02-modelo-relacional-y-algebra/README.md) ·
  [03 — SQL](../classes/part-03-sql-en-profundidad/README.md) ·
  [04 — Motores y dialectos](../classes/part-04-motores-relacionales-y-dialectos/README.md).
- 📚 [05 — Documentos y clave-valor](../classes/part-05-documentos-y-clave-valor/README.md) ·
  [06 — Grafos, columnas, tiempo y búsqueda](../classes/part-06-grafos-columnas-tiempo-y-busqueda/README.md).
  Aquí se construye el criterio para no elegir por moda.
- 📚 [07 — Transacciones](../classes/part-07-transacciones-concurrencia-y-recuperacion/README.md) ·
  [08 — Almacenamiento, índices y planes](../classes/part-08-almacenamiento-indices-y-planes/README.md).
- 📚 [09 — Distribución, réplica y consistencia](../classes/part-09-distribucion-replica-y-consistencia/README.md).
  El corazón del rol:
  [045 — CAP, PACELC y lo que realmente se elige](../classes/part-09-distribucion-replica-y-consistencia/045-cap-pacelc-y-lo-que-realmente-se-elige/README.md),
  [046 — Modelos de consistencia y garantías de sesión](../classes/part-09-distribucion-replica-y-consistencia/046-modelos-de-consistencia-y-garantias-de-sesion/README.md)
  y [047 — Consenso y transacciones distribuidas](../classes/part-09-distribucion-replica-y-consistencia/047-consenso-y-transacciones-distribuidas/README.md).
- 📚 [10 — Operación, seguridad y gobierno](../classes/part-10-operacion-seguridad-y-gobierno/README.md) ·
  [11 — Analítica, integración y streaming](../classes/part-11-analitica-integracion-y-streaming/README.md) ·
  [12 — Vectores, recuperación y RAG](../classes/part-12-vectores-recuperacion-y-rag/README.md).
- 📚 [13 — Arquitectura y proyecto final](../classes/part-13-arquitectura-y-proyecto-final/README.md).
  Donde se cierra todo:
  [062 — Persistencia políglota por evidencia](../classes/part-13-arquitectura-y-proyecto-final/062-persistencia-poliglota-por-evidencia/README.md),
  [063 — Registro de decisiones y costo total](../classes/part-13-arquitectura-y-proyecto-final/063-registro-de-decisiones-y-costo-total/README.md)
  y [064 — Proyecto final: diseñar, medir y defender](../classes/part-13-arquitectura-y-proyecto-final/064-proyecto-final-disenar-medir-y-defender/README.md).

Laboratorios de la ruta:

- 🧪 [`02-polyglot-modeling`](../labs/02-polyglot-modeling/README.md) — el mismo dominio en tres
  modelos, con lo que gana y pierde cada uno declarado.
- 🧪 [`04-indexing`](../labs/04-indexing/README.md) — cómo se mide una hipótesis de rendimiento
  sin caer en el cronómetro.
- 🧪 [`06-vector-search`](../labs/06-vector-search/README.md) — recuperación medible, antes de
  aprobar un proyecto de IA con recuperación.

## 🧪 Qué tienes que poder demostrar

- **elegir un motor para un caso concreto y defender la elección** con una medición propia y
  un límite declarado;
- explicar qué garantía pierdes exactamente al distribuir, en el vocabulario de los modelos de
  consistencia y no en el de los eslóganes;
- escribir un ADR que otra persona pueda usar para revisar la decisión dentro de dos años;
- estimar el costo total de una opción, incluida la operación y la formación del equipo;
- diseñar la evolución: cómo se migra hacia esa arquitectura y cómo se vuelve atrás;
- decir en qué condiciones tu propia decisión sería equivocada.

## 🎓 Credenciales

No existe una credencial que acredite «arquitecto de datos» de forma reconocida y neutral. Las
que hay son de proveedor —de nube, sobre todo— y validan su catálogo, no el criterio. Sirven
para pasar filtros, no para demostrar arquitectura.

Lo que sí se reconoce en este rol: decisiones documentadas que otros pueden auditar. El
[registro de decisiones](../classes/part-13-arquitectura-y-proyecto-final/063-registro-de-decisiones-y-costo-total/README.md)
y el [proyecto final](../projects/capstone.md) de este programa producen justamente ese
material.

Como referencia de contexto —no de calidad—, el
[DB-Engines Ranking](https://db-engines.com/en/ranking) publica cada mes la popularidad de más
de 400 gestores a partir de menciones, ofertas de empleo y perfiles profesionales. Es útil para
saber qué vas a encontrar en el mercado y qué te costará contratar; no dice nada sobre si un
motor es adecuado para tu problema.

## 📈 Progresión y mercado

Casi nadie llega aquí de entrada. Los caminos habituales:

1. **Desarrollo o ingeniería de datos con años de sistemas reales** — es donde se forma el
   criterio.
2. **Referente técnico de un dominio** — decides el modelo de una parte del producto.
3. **Arquitecto de datos / de soluciones** — decides entre sistemas y equipos.
4. **Bifurcación:** ingeniero de staff o principal (influencia técnica sin gestión), o
   dirección técnica (con gestión).

Sobre cifras: el [Occupational Outlook Handbook](https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm)
del U.S. Bureau of Labor Statistics agrupa administradores y **arquitectos** de bases de datos,
y publica para estos últimos una mediana claramente superior a la del administrador —datos de
mayo de 2024 para Estados Unidos—. Es la única referencia oficial que este repositorio cita
para el rol; para tu mercado, contrasta ofertas reales.

## ⚠️ Mitos y errores comunes

- **«Lo usa una empresa grande, luego nos sirve.»** Su escala, su equipo y su presupuesto no
  son los tuyos. La solución de otro es un dato, no un argumento.
- **«Más motores, más flexible.»** Cada motor añadido multiplica respaldo, monitorización,
  actualizaciones, seguridad y personas que deben saber operarlo.
- **«CAP dice que hay que elegir dos de tres.»** Esa lectura es folclore. La elección real
  aparece solo durante la partición, y el resto del tiempo el compromiso es entre latencia y
  consistencia.
- **«Eventualmente consistente» como respuesta.** ¿Eventualmente cuánto? ¿Qué ve una sesión que
  acaba de escribir? Sin eso, no has definido nada.
- **«El diagrama es la arquitectura.»** El diagrama es una vista. La arquitectura es el
  conjunto de decisiones y sus consecuencias, y vive en el ADR.
- **«Ya lo optimizaremos después.»** Algunas decisiones —el modelo, la clave de partición, la
  garantía prometida— no se optimizan después: se migran, y eso cuesta.

## 🚀 Siguientes pasos

1. Recorre las 14 partes; si vienes con experiencia, no te saltes la 05 y la 06: son las que
   evitan el sesgo relacional.
2. Haz la Parte 09 con lápiz y papel: escribe qué garantía necesita cada caso de uso que
   conoces.
3. Ejecuta [`02-polyglot-modeling`](../labs/02-polyglot-modeling/README.md) sobre un dominio de
   tu trabajo, no sobre el del ejemplo.
4. Escribe tres ADR de decisiones ya tomadas en tu empresa, con la información que había
   entonces. Es el mejor ejercicio de calibración que existe.
5. Cierra con el [proyecto final](../projects/capstone.md): diseñar, medir y **defender** ante
   alguien que pregunte.

## 📖 De dónde sale esto

- **Martin Kleppmann**, *Designing Data-Intensive Applications* — el marco completo de
  garantías, réplica y compromisos.
- **Peter Bailis, Joseph M. Hellerstein, Michael Stonebraker (eds.)**, *Readings in Database
  Systems* — la conversación de fondo del campo, con sus desacuerdos.
- **Pat Helland**, *Life beyond Distributed Transactions* — por qué el mundo distribuido obliga
  a rediseñar, no solo a escalar.
- **solid IT**, *DB-Engines Ranking* — visibilidad y demanda por motor, con su metodología
  declarada.

Fichas completas en el [registro de fuentes](../catalog/sources.json).

---

- ⬅️ [Volver al índice de rutas](README.md)
- 🏠 [Inicio del programa](../README.md)
