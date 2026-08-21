# 🧑‍💻 Desarrollador de aplicaciones

> Escribes el código que usa la base de datos todos los días. Tu trabajo no es administrarla:
> es no romperla, no corromper sus datos y no descubrir en producción que la consulta que
> funcionaba con mil filas no funciona con diez millones.
>
> **Nivel de entrada:** entrada · **Foco:** el esquema como contrato, consultas correctas,
> concurrencia y despliegues sin caída · **Cargos habituales:** desarrollador backend,
> desarrollador full-stack, ingeniero de software.

## 🧭 Qué es y por qué importa

Casi todo el software que existe guarda algo. El desarrollador de aplicaciones es quien decide
—muchas veces sin darse cuenta— qué se guarda, con qué forma, con qué garantías y qué pasa
cuando dos personas hacen lo mismo a la vez. Ese conjunto de decisiones sobrevive al código:
un endpoint se reescribe en una tarde, un esquema mal diseñado condiciona la aplicación
durante años y arrastra a cada equipo que llegue después.

Importa porque el daño de una decisión de datos es asimétrico. Una función lenta se optimiza;
un dato corrompido puede no tener vuelta atrás. Si aceptaste dos reservas para el último cupo,
si guardaste el importe como número de coma flotante, si borraste en cascada lo que debía
quedar como histórico, el problema ya no es de rendimiento: es de confianza.

Y hay una razón práctica: el motor relacional sigue siendo el sustrato del oficio. En la
[Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/technology),
PostgreSQL aparece como el sistema más usado (55,6 % de quienes respondieron a esa pregunta),
seguido de MySQL (40,5 %) y SQLite (37,5 %). La muestra es autoseleccionada y no representa a
toda la industria, pero el orden de magnitud es claro: no vas a esquivar SQL.

Lo que este programa **no** te da: la conversación con el equipo de producto para negociar un
plazo, la presión de un incidente en vivo, ni el criterio que solo aparece tras mantener el
mismo sistema durante tres años. Eso llega trabajando. Lo que sí te da es la capacidad de
justificar cada decisión de datos con un mecanismo y una medición, en vez de con una costumbre.

## 🗓️ Un día en el puesto

- **Una historia de usuario nueva.** Antes de escribir el endpoint, decides qué entidades
  toca, qué restricciones la protegen y si el esquema actual la admite sin duplicar datos.
- **Consultas.** Escribes la consulta, la lees en voz alta y compruebas qué devuelve cuando
  hay nulos, cuando no hay filas y cuando hay duplicados. Ese trío causa la mayoría de los
  errores silenciosos.
- **Revisión de código ajeno.** Alguien mete un `SELECT *` dentro de un bucle, o concatena un
  parámetro en la consulta. Tu comentario evita un incidente futuro y, en el segundo caso, una
  brecha.
- **Una migración.** Añadir una columna es fácil; añadirla con `NOT NULL` sobre una tabla de
  millones de filas y sin bloquear escrituras, no. Se hace por pasos y con vuelta atrás.
- **Un error raro en producción.** Dos usuarios, la misma fila, resultado imposible. Aquí
  empieza el trabajo de verdad: reproducir la carrera, entender el nivel de aislamiento y
  corregir con la herramienta adecuada.
- **Rendimiento.** Una pantalla tarda. Miras el plan de ejecución antes de tocar nada, y
  descubres que el índice existe pero la consulta no puede usarlo.

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **SQL de verdad, no el mínimo para que compile:** reuniones internas y externas, agregación
  correcta, subconsultas, funciones de ventana y el comportamiento de los nulos.
- **Modelado:** entidades, claves, normalización hasta donde tenga sentido y desnormalización
  deliberada cuando la carga lo justifique.
- **Restricciones como red de seguridad:** `NOT NULL`, `UNIQUE`, `CHECK` y claves foráneas. La
  validación en la aplicación se salta; la del motor, no.
- **Transacciones y aislamiento:** qué garantiza cada nivel y qué anomalías deja pasar. Este es
  el punto donde más código correcto en apariencia falla bajo carga.
- **Índices y planes:** por qué una consulta usa o no usa un índice, y qué cuesta cada índice
  en escritura.
- **Parametrización:** la única defensa real contra la inyección SQL, y por qué escapar a mano
  no cuenta como defensa.

### Herramientas del oficio

- Un cliente de SQL decente y `EXPLAIN` (o su equivalente) como reflejo, no como último recurso.
- El driver o el ORM de tu lenguaje, sabiendo **qué SQL genera**. Un ORM que no sabes leer es
  una caja negra que decide por ti.
- Migraciones versionadas en el repositorio, aplicadas en orden y reversibles.
- Contenedores para tener el mismo motor que producción en tu máquina, no uno parecido.

### Habilidades no técnicas

- **Leer un requisito y detectar la regla de negocio** que debería ser una restricción.
- **Explicar por qué un cambio de esquema no es "solo añadir un campo"** a quien pide plazos.
- **Escribir el porqué**, no solo el qué: la próxima persona que abra esa tabla serás tú
  dentro de un año.

## 📚 Tu ruta en el programa

10 partes, 172 horas estimadas. El orden importa: cada parte apoya a la siguiente.

1. 📚 [**Parte 01 — Fundamentos, sistemas y método**](../classes/part-01-fundamentos-datos-sistemas-y-metodo/README.md)
   (4 clases · 12 h). Qué resuelve un gestor y qué no, y cómo montar un entorno donde puedas
   comprobar lo que afirmas.
2. 📚 [**Parte 02 — Modelado conceptual y requisitos**](../classes/part-02-modelado-conceptual-y-requisitos/README.md)
   (5 clases · 16 h). De requisitos a entidades. Clase que no puedes saltarte:
   [007 — Claves, identidad y el debate natural frente a sustituta](../classes/part-02-modelado-conceptual-y-requisitos/017-claves-identidad-natural-y-sustituta/README.md).
3. 📚 [**Parte 03 — Modelo relacional y álgebra**](../classes/part-03-modelo-relacional-y-algebra/README.md)
   (4 clases · 13 h). Por qué SQL se comporta como se comporta.
4. 📚 [**Parte 04 — SQL en profundidad**](../classes/part-04-sql-en-profundidad/README.md)
   (6 clases · 20 h). El núcleo del rol. Imprescindibles:
   [014 — DDL: el esquema como contrato](../classes/part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md),
   [016 — Reuniones](../classes/part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/README.md)
   y [019 — Nulos y lógica de tres valores](../classes/part-04-sql-en-profundidad/029-nulos-y-logica-de-tres-valores/README.md),
   que explica los resultados «imposibles» que verás en producción.
5. 📚 [**Parte 05 — Motores relacionales y dialectos**](../classes/part-05-motores-relacionales-y-dialectos/README.md)
   (4 clases · 12 h). Lo que cambia al pasar de SQLite a PostgreSQL o MySQL.
6. 📚 [**Parte 06 — Documentos y clave-valor**](../classes/part-06-documentos-y-clave-valor/README.md)
   (4 clases · 13 h). Cuándo un documento o una caché ayudan, y qué consistencia pierdes.
7. 📚 [**Parte 08 — Transacciones, concurrencia y recuperación**](../classes/part-08-transacciones-concurrencia-y-recuperacion/README.md)
   (5 clases · 18 h). La parte que separa al que escribe consultas del que escribe sistemas.
   Clase clave: [037 — Concurrencia en la aplicación](../classes/part-08-transacciones-concurrencia-y-recuperacion/047-concurrencia-en-la-aplicacion/README.md).
8. 📚 [**Parte 09 — Almacenamiento, índices y planes**](../classes/part-09-almacenamiento-indices-y-planes/README.md)
   (5 clases · 17 h). Para dejar de adivinar por qué algo va lento.
9. 📚 [**Parte 11 — Operación, seguridad y gobierno**](../classes/part-11-operacion-seguridad-y-gobierno/README.md)
   (6 clases · 19 h). Aquí solo dos son obligatorias para ti:
   [049 — Migraciones evolutivas sin ventana de caída](../classes/part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md)
   y [051 — Inyección SQL y el contrato de parametrización](../classes/part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md).
10. 📚 [**Parte 14 — Arquitectura y proyecto final**](../classes/part-14-arquitectura-y-proyecto-final/README.md)
    (3 clases · 12 h). Cierra con una decisión defendida.

Practica en los laboratorios, que es donde el conocimiento se vuelve tuyo:

- 🧪 [`01-sql-foundations`](../labs/01-sql-foundations/README.md) — consultas e invariantes
  sobre el dominio educativo.
- 🧪 [`03-transactions`](../labs/03-transactions/README.md) — reproduce una actualización
  perdida con dos hilos reales y corrígela de tres formas. Si un día vendiste dos veces el
  mismo asiento, aquí está la explicación y el arreglo.
- 🧪 [`04-indexing`](../labs/04-indexing/README.md) — el plan antes y después del índice, y lo
  que ese índice cuesta en cada escritura.

## 🧪 Qué tienes que poder demostrar

Al terminar la ruta, en una entrevista o en una revisión de código deberías poder:

- diseñar un esquema para un dominio nuevo y **justificar cada restricción** que pones;
- explicar qué devuelve una reunión externa cuando no hay coincidencias, y por qué
  `WHERE columna <> 'x'` descarta las filas con nulo;
- reproducir una actualización perdida y corregirla con actualización atómica, control
  optimista o bloqueo, sabiendo cuál conviene en cada caso;
- leer un plan de ejecución y decir por qué la consulta no usa el índice que existe;
- describir una migración de esquema en pasos reversibles, sin ventana de caída;
- demostrar que tu código parametriza, y explicar por qué escapar comillas no es equivalente.

## 🎓 Credenciales

Para este rol, **las certificaciones de base de datos pesan poco**: contratan por lo que
demuestras en código. Ninguna credencial sustituye un repositorio donde se vea tu esquema, tus
migraciones y tus pruebas. Si tu empresa trabaja sobre una nube concreta, la credencial de esa
nube puede abrir la puerta de RR. HH., pero llega después, no antes.

Lo que sí funciona como portafolio: un proyecto pequeño con esquema versionado, migraciones,
pruebas de concurrencia y un `EXPLAIN` comentado. Eso es exactamente lo que produce el
[proyecto final](../projects/capstone.md) de este programa.

## 📈 Progresión y mercado

Camino habitual, con nombres que cambian según la empresa:

1. **Desarrollador junior** — trabajas dentro de un esquema que otros diseñaron.
2. **Desarrollador** — diseñas tus tablas, revisas las de otros y llevas tus migraciones.
3. **Desarrollador sénior / referente técnico** — decides el modelo de datos de una parte del
   producto y respondes por su evolución.
4. **Bifurcación:** [ingeniería de datos](ingenieria-de-datos.md), si te atrae mover y modelar
   datos a escala; [arquitectura](arquitectura.md), si te atrae decidir y defender; o
   especialización en rendimiento y fiabilidad, cerca de [DBA / SRE](fiabilidad-y-operacion.md).

Sobre dinero, este repositorio solo publica cifras con fuente. La referencia pública más
sólida es estadounidense: el [Occupational Outlook Handbook](https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm)
del U.S. Bureau of Labor Statistics. Para desarrollo puro no hay un epígrafe equivalente en
español con datos comparables, así que **aquí no encontrarás rangos inventados para tu país**:
consulta ofertas reales de tu mercado y contrástalas entre varias fuentes.

## ⚠️ Mitos y errores comunes

- **«El ORM me abstrae de SQL.»** Te abstrae de escribirlo, no de entenderlo. El día que
  genere una consulta con veinte reuniones, tendrás que leerla.
- **«Valido en la aplicación, no necesito restricciones.»** Toda validación que no está en el
  motor se salta: por otro servicio, por un script, por una carga masiva.
- **«Ya funciona en mi máquina con cien filas.»** El plan de ejecución cambia con el volumen y
  con las estadísticas. Prueba con datos que se parezcan a los reales.
- **«Añado un índice y listo.»** Cada índice se mantiene en cada `INSERT`, `UPDATE` y
  `DELETE`. El laboratorio 04 lo mide: dos índices encarecen la escritura de forma visible.
- **«Guardo todo por si acaso.»** Los datos personales que no guardas no se filtran, no se
  auditan y no hay que borrarlos. La minimización es diseño, no burocracia.
- **«Los nulos son como los ceros.»** No: son «no se sabe», y contaminan comparaciones,
  agregados y reuniones de formas que sorprenden a todo el mundo una vez.

## 🚀 Siguientes pasos

1. Haz las Partes 00 → 01 → 02 sin saltarte nada, aunque ya sepas SQL: son el vocabulario.
2. Ataca la Parte 04 completa y ejecuta [`01-sql-foundations`](../labs/01-sql-foundations/README.md)
   prediciendo cada resultado **antes** de ejecutarlo.
3. Ejecuta [`03-transactions`](../labs/03-transactions/README.md) y reescribe una operación
   crítica de tu propio proyecto con la corrección que corresponda.
4. Ejecuta [`04-indexing`](../labs/04-indexing/README.md) y repite el experimento contra tu
   motor real, con `EXPLAIN` en la mano.
5. Aplica el [reto de transferencia](../docs/LEARNING-MODEL.md) de cada clase a tu código de
   trabajo: es donde el programa deja de ser teoría.
6. Cierra con el [proyecto final](../projects/capstone.md) y guarda la evidencia: es tu
   portafolio.

## 📖 De dónde sale esto

- **Bill Karwin**, *SQL Antipatterns* — el catálogo de errores de esquema y consulta que
  comete todo equipo de desarrollo.
- **C. J. Date**, *SQL and Relational Theory* — por qué SQL se aparta del modelo relacional y
  qué problemas causa eso en el código.
- **OWASP**, *SQL Injection Prevention Cheat Sheet* — la defensa por parametrización, en su
  fuente original.
- **Stack Overflow**, *Developer Survey 2025* — uso declarado de cada motor, con su sesgo de
  muestra.

Las fichas completas, con ISBN, DOI o URL oficial, están en el
[registro de fuentes](../catalog/sources.json) y en la
[bibliografía del sitio](https://vladimiracunadev-create.github.io/database-systems-labs/fuentes.html).

---

- ⬅️ [Volver al índice de rutas](README.md)
- 🏠 [Inicio del programa](../README.md)
