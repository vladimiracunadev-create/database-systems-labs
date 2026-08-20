# 📊 Analytics engineer / BI

> Estás entre el dato crudo y la persona que decide. Traduces «cuánto vendimos» a un modelo que
> siempre da el mismo número, y defiendes ese número cuando dos áreas traen dos cifras
> distintas para la misma pregunta.
>
> **Nivel de entrada:** intermedio · **Foco:** SQL analítico, modelado dimensional,
> transformaciones versionadas y la frontera OLTP/OLAP · **Cargos habituales:** analytics
> engineer, ingeniero de BI, analista de datos sénior.

## 🧭 Qué es y por qué importa

Este rol apareció cuando quedó claro que el problema del análisis no era la herramienta de
visualización, sino la capa intermedia: nadie sabía qué significaba exactamente cada métrica ni
de dónde salía. El analytics engineer construye esa capa —modelos, definiciones, pruebas de
datos— con prácticas de ingeniería: versionado, revisión y pruebas automáticas.

Importa porque **una organización no puede decidir sobre números que no se sostienen**. Si
finanzas y operaciones traen dos cifras de ingresos, la reunión se convierte en una discusión
sobre datos en lugar de una decisión. Tu trabajo es que exista una definición, esté escrita,
esté probada y se pueda rastrear hasta el origen.

Es también el puesto donde más se nota la diferencia entre saber SQL y saber modelar. Escribir
una consulta que devuelva el número correcto hoy es fácil. Diseñar un modelo donde ese número
siga siendo correcto cuando cambien las jerarquías, se corrijan datos históricos o aparezca una
línea de negocio nueva, no lo es.

Lo que este programa **no** cubre: la parte de comunicación visual y de producto —qué gráfico
usar, cómo contar una historia con datos— ni la herramienta de BI concreta de tu empresa.

## 🗓️ Un día en el puesto

- **«Este número no cuadra».** La mitad del trabajo empieza así. Rastreas la métrica hasta el
  origen y descubres una definición implícita que nadie escribió.
- **Modelar un hecho nuevo.** Decidir el grano, las dimensiones, y qué hacer cuando un atributo
  cambia con el tiempo.
- **Escribir transformaciones versionadas** con sus pruebas: unicidad de la clave, no nulos,
  totales que deben cuadrar contra el origen.
- **Optimizar una consulta que se ejecuta cien veces al día** desde un panel: mirar el plan,
  el formato y la partición antes de pedir más máquina.
- **Depurar la carga incremental** que dejó fuera un día por un cambio de zona horaria.
- **Documentar definiciones** para que la próxima persona no reinvente «cliente activo».

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **SQL analítico de verdad:** agregación sin duplicar, `HAVING`, CTE, subconsultas
  correlacionadas y funciones de ventana —la herramienta que separa a un analista de un
  analytics engineer—.
- **Modelado dimensional:** hechos, dimensiones, grano, esquema en estrella y dimensiones que
  cambian lentamente.
- **OLTP frente a OLAP:** por qué la misma consulta cuesta órdenes de magnitud distintos según
  el formato de almacenamiento.
- **Analítica columnar y vectorización:** qué hace que un motor analítico sea rápido, para
  poder elegir y para no pedir imposibles a uno transaccional.
- **Integración y cargas incrementales:** ETL/ELT, captura de cambios, idempotencia y marcas de
  agua.
- **Índices y planes**, lo suficiente para diagnosticar un panel lento sin adivinar.
- **Calidad de datos:** pruebas automáticas sobre unicidad, integridad y frescura.

### Herramientas del oficio

- Un motor analítico para practicar en local: DuckDB es suficiente y no necesita servidor.
- Transformaciones versionadas con dbt o equivalente, con pruebas en el repositorio.
- Un motor relacional serio como origen (PostgreSQL) y su `EXPLAIN`.
- Control de versiones y revisión de código: tus modelos son código, no consultas sueltas.

### Habilidades no técnicas

- **Preguntar la definición antes de calcular**, y escribirla donde otros la encuentren.
- **Traducir un requisito difuso** («quiero ver el rendimiento del mes») en un grano y unas
  dimensiones concretas.
- **Sostener el número** cuando a alguien no le gusta, mostrando el linaje en vez de discutir.

## 📚 Tu ruta en el programa

8 partes, 115 horas estimadas.

1. 📚 [**Parte 00 — Fundamentos**](../classes/part-00-fundamentos-datos-sistemas-y-metodo/README.md)
   (4 clases · 12 h).
2. 📚 [**Parte 01 — Modelado conceptual y requisitos**](../classes/part-01-modelado-conceptual-y-requisitos/README.md)
   (5 clases · 16 h). Aquí se aprende a convertir una frase de negocio en entidades.
3. 📚 [**Parte 02 — Modelo relacional y álgebra**](../classes/part-02-modelo-relacional-y-algebra/README.md)
   (4 clases · 13 h).
4. 📚 [**Parte 03 — SQL en profundidad**](../classes/part-03-sql-en-profundidad/README.md)
   (6 clases · 20 h). Imprescindibles:
   [017 — Agregación, GROUP BY y HAVING sin duplicar filas](../classes/part-03-sql-en-profundidad/017-agregacion-group-by-y-having/README.md)
   y [018 — CTE, subconsultas y funciones de ventana](../classes/part-03-sql-en-profundidad/018-cte-subconsultas-y-funciones-de-ventana/README.md).
5. 📚 [**Parte 04 — Motores relacionales y dialectos**](../classes/part-04-motores-relacionales-y-dialectos/README.md)
   (4 clases · 12 h). Incluye los motores embebidos y analíticos que usarás en local.
6. 📚 [**Parte 08 — Almacenamiento, índices y planes**](../classes/part-08-almacenamiento-indices-y-planes/README.md)
   (5 clases · 17 h). Lo justo para diagnosticar en vez de suponer.
7. 📚 [**Parte 11 — Analítica, integración y streaming**](../classes/part-11-analitica-integracion-y-streaming/README.md)
   (4 clases · 13 h). El núcleo del rol:
   [054 — OLTP frente a OLAP](../classes/part-11-analitica-integracion-y-streaming/054-oltp-frente-a-olap/README.md),
   [055 — Modelado dimensional](../classes/part-11-analitica-integracion-y-streaming/055-modelado-dimensional/README.md)
   y [056 — Integración: ETL, ELT y captura de cambios](../classes/part-11-analitica-integracion-y-streaming/056-integracion-etl-elt-y-captura-de-cambios/README.md).
   Complétalo con
   [032 — Analítica columnar y vectorización](../classes/part-06-grafos-columnas-tiempo-y-busqueda/032-analitica-columnar-y-vectorizacion/README.md).
8. 📚 [**Parte 13 — Arquitectura y proyecto final**](../classes/part-13-arquitectura-y-proyecto-final/README.md)
   (3 clases · 12 h).

Laboratorios de la ruta:

- 🧪 [`01-sql-foundations`](../labs/01-sql-foundations/README.md) — la base sobre la que se
  construye todo lo demás.
- 🧪 [`04-indexing`](../labs/04-indexing/README.md) — leer un plan y medir el trabajo, que es
  como se arregla un panel lento sin comprar máquina.

## 🧪 Qué tienes que poder demostrar

- escribir una consulta con funciones de ventana y **explicar por qué** no se puede hacer con
  `GROUP BY`;
- declarar el grano de una tabla de hechos y detectar cuándo una reunión lo rompe y duplica
  medidas;
- diseñar una dimensión que cambia lentamente y decir qué historia conserva;
- construir una carga incremental idempotente y probar que reprocesar no altera los totales;
- explicar con una medición por qué una consulta va mejor en un motor columnar;
- documentar una métrica de forma que otra persona obtenga el mismo número sin preguntarte.

## 🎓 Credenciales

En este rol pesa más el portafolio que la credencial: un repositorio con modelos versionados,
pruebas de datos y documentación de métricas dice más que cualquier examen. Si tu equipo
trabaja sobre una nube, la credencial de esa nube ayuda en filtros de RR. HH.; la más cercana
a esta ruta es la
[Professional Data Engineer de Google Cloud](https://cloud.google.com/learn/certification/data-engineer),
aunque su foco es más de ingeniería que de modelado analítico.

Un apunte de contexto con fuente: en la
[Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/technology),
PostgreSQL (55,6 %) y MySQL (40,5 %) siguen encabezando el uso declarado, muy por delante de
cualquier motor analítico especializado. Traducción práctica: la mayor parte de tu SQL diario
será estándar y transferible, y la especialización columnar llega después.

## 📈 Progresión y mercado

1. **Analista de datos** con SQL y una herramienta de BI.
2. **Analytics engineer** — modelas, versionas y pruebas; el salto real es dejar de escribir
   consultas sueltas y empezar a construir modelos.
3. **Sénior / líder de analítica** — defines la capa semántica de la empresa y sus
   definiciones.
4. **Bifurcación:** [ingeniería de datos](ingenieria-de-datos.md) si te atrae la tubería y la
   escala, o producto/negocio si te atrae la decisión.

Este repositorio no publica rangos salariales para el rol: no existe una fuente pública
comparable a la del [Occupational Outlook Handbook](https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm)
para *analytics engineer* en español, y dar un número sin respaldo sería exactamente lo que las
clases prohíben.

## ⚠️ Mitos y errores comunes

- **«Lo arreglo en la herramienta de BI.»** Una métrica calculada dentro del panel no se puede
  probar, ni reutilizar, ni auditar. La lógica va al modelo.
- **«Un `SELECT DISTINCT` y listo.»** El `DISTINCT` casi siempre tapa un grano mal definido o
  una reunión que duplica. Arregla la causa.
- **«Si el total cuadra, el modelo está bien.»** Cuadra hasta que alguien filtra por una
  dimensión y aparece el doble conteo.
- **«El histórico no cambia.»** Cambia: correcciones, reclasificaciones, jerarquías que se
  reorganizan. Por eso existen las dimensiones que cambian lentamente.
- **«Necesitamos un motor analítico ya.»** A menudo un índice, una materialización y un grano
  correcto resuelven el problema por dos órdenes de magnitud menos de costo.
- **«La documentación la hago al final.»** La definición de la métrica *es* el entregable; sin
  ella entregas un número sin significado.

## 🚀 Siguientes pasos

1. Haz las Partes 01 → 03 completas; las funciones de ventana son el punto de inflexión del
   rol.
2. Modela un dominio propio en estrella y escribe el grano de cada hecho **en una frase**.
3. Ejecuta [`04-indexing`](../labs/04-indexing/README.md) y aplica el método —plan y trabajo, no
   cronómetro— al panel más lento que tengas.
4. Convierte tres consultas sueltas de tu trabajo en modelos versionados con pruebas.
5. Escribe la definición de las cinco métricas que más se discuten en tu empresa.
6. Cierra con el [proyecto final](../projects/capstone.md).

## 📖 De dónde sale esto

- **Ralph Kimball, Margy Ross**, *The Data Warehouse Toolkit* — la referencia del modelado
  dimensional.
- **dbt Labs**, *dbt Documentation* — transformaciones versionadas y pruebas de datos en el
  almacén.
- **DuckDB**, *DuckDB Documentation* — motor analítico embebido para practicar sin
  infraestructura.
- **Stack Overflow**, *Developer Survey 2025* — uso declarado de motores, con su sesgo de
  muestra.

Fichas completas en el [registro de fuentes](../catalog/sources.json).

---

- ⬅️ [Volver al índice de rutas](README.md)
- 🏠 [Inicio del programa](../README.md)
