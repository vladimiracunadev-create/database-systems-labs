# Parte 00 — Primeros pasos: del archivo a la base de datos

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

La rampa de entrada. Qué es un dato, por qué una hoja de cálculo deja de servir, y las primeras órdenes de SQL —crear, insertar, leer, cambiar— hasta llegar a dos tablas relacionadas. Termina con las dos preguntas que hay que saber contestar antes de seguir: cuándo NO hace falta una base de datos y qué familias de motores existen.

**10 clases · 20 horas · 46 conceptos · 14 fuentes**

## Antes de esta parte

Ninguno. Es la puerta de entrada al programa y no supone nada anterior.

## De qué trata esta parte

Esta parte existe porque el resto del programa da por sabidas cosas que casi nadie aprendió de forma ordenada. Antes de discutir normalización, aislamiento o consenso hay que poder decir sin dudar qué es un dato, qué es una fila, qué garantiza una clave y por qué una hoja de cálculo deja de servir. Diez clases, veinte horas, y ninguna teoría que no se pueda ejecutar en la misma sesión en que se lee.

El recorrido tiene una forma deliberada. Las tres primeras clases construyen el vocabulario y la primera base de datos real. Las tres siguientes enseñan a leer, a cambiar datos sin destruirlos y a elegir tipos que no mientan. Las dos siguientes introducen la identidad —la clave primaria— y la primera relación entre tablas, que es donde aparecen por primera vez las anomalías que justifican toda la parte 02. Las dos últimas cierran con las dos preguntas de criterio que un profesional debe saber contestar: cuándo NO hace falta una base de datos, y qué familias de motores existen.

El motor de referencia es SQLite, porque no hay que instalar nada ni operar nada y así el ruido no compite con el concepto. Aun así cada clase muestra el mismo problema resuelto en varios motores, incluidos los que no lo resuelven y por qué, para que la costumbre de comparar se instale desde el primer día.

Si ya sabes SQL y quieres ir más rápido, no te saltes las clases 006, 009 y 010: tipos, criterio de decisión y mapa de familias son las tres que más se dan por sabidas y menos se dominan.

## Al terminar esta parte podrás

1. Explicar la diferencia entre dato, información, registro, campo y tabla con un ejemplo propio.
2. Crear una base de datos, poblarla y consultarla desde cero sin copiar instrucciones.
3. Cambiar datos comprobando antes el alcance y usando la transacción como red de seguridad.
4. Elegir el tipo correcto para dinero, fechas e identificadores, y decir qué se rompe con el tipo equivocado.
5. Declarar claves primarias y foráneas, y justificar la elección entre clave natural y sustituta.
6. Argumentar cuándo un archivo o un motor embebido es la respuesta correcta y cuándo no.

## Mapa de la parte

```mermaid
flowchart LR
    C001["001<br/>Qué es un dato, un registro y una tabla"]
    C002["002<br/>Del archivo y la hoja de cálculo a la bas…"]
    C003["003<br/>Tu primera base de datos: crear, insertar…"]
    C004["004<br/>Leer datos: SELECT, WHERE y ORDER BY"]
    C005["005<br/>Cambiar datos: INSERT, UPDATE, DELETE y e…"]
    C006["006<br/>Tipos de datos: por qué un número no es u…"]
    C007["007<br/>La clave primaria: cómo se distingue una…"]
    C008["008<br/>Dos tablas y una relación: la clave foránea"]
    C009["009<br/>Cuándo NO necesitas una base de datos"]
    C010["010<br/>El mapa de los motores: seis familias y u…"]
    C001 --> C002
    C002 --> C003
    C003 --> C004
    C004 --> C005
    C005 --> C006
    C006 --> C007
    C007 --> C008
    C008 --> C009
    C009 --> C010
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C001 fund
    class C002 fund
    class C003 fund
    class C004 fund
    class C005 fund
    class C006 fund
    class C007 fund
    class C008 fund
    class C009 fund
    class C010 fund
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [001](001-que-es-un-dato-un-registro-y-una-tabla/README.md) | [Qué es un dato, un registro y una tabla](001-que-es-un-dato-un-registro-y-una-tabla/README.md) | Fundamentos | 2 | 3 |
| [002](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) | [Del archivo y la hoja de cálculo a la base de datos](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) | Fundamentos | 2 | 3 |
| [003](003-tu-primera-base-de-datos/README.md) | [Tu primera base de datos: crear, insertar y leer](003-tu-primera-base-de-datos/README.md) | Fundamentos | 2 | 3 |
| [004](004-leer-datos-select-where-y-order-by/README.md) | [Leer datos: SELECT, WHERE y ORDER BY](004-leer-datos-select-where-y-order-by/README.md) | Fundamentos | 2 | 3 |
| [005](005-cambiar-datos-insert-update-delete/README.md) | [Cambiar datos: INSERT, UPDATE, DELETE y el WHERE que salva](005-cambiar-datos-insert-update-delete/README.md) | Fundamentos | 2 | 3 |
| [006](006-tipos-de-datos-un-numero-no-es-un-texto/README.md) | [Tipos de datos: por qué un número no es un texto](006-tipos-de-datos-un-numero-no-es-un-texto/README.md) | Fundamentos | 2 | 3 |
| [007](007-la-clave-primaria/README.md) | [La clave primaria: cómo se distingue una fila de otra](007-la-clave-primaria/README.md) | Fundamentos | 2 | 3 |
| [008](008-dos-tablas-y-una-relacion/README.md) | [Dos tablas y una relación: la clave foránea](008-dos-tablas-y-una-relacion/README.md) | Fundamentos | 2 | 3 |
| [009](009-cuando-no-necesitas-una-base-de-datos/README.md) | [Cuándo NO necesitas una base de datos](009-cuando-no-necesitas-una-base-de-datos/README.md) | Fundamentos | 2 | 3 |
| [010](010-el-mapa-de-los-motores/README.md) | [El mapa de los motores: seis familias y un criterio](010-el-mapa-de-los-motores/README.md) | Fundamentos | 2 | 3 |

## Las clases, una por una

### [001 — Qué es un dato, un registro y una tabla](001-que-es-un-dato-un-registro-y-una-tabla/README.md)

*Fundamentos · 2 h · 3 fuentes · sin prerrequisitos*

La clase que pone nombre a las tres piezas de las que se habla el resto del programa. Separa el dato de la información que produce al interpretarlo, define el registro como un hecho completo y la tabla como el conjunto de filas que comparten forma. Casi todos los errores de diseño de las partes siguientes empiezan en una confusión de este nivel: un campo que guarda dos hechos, un número guardado como texto, una lista a la que se llama tabla.

**Conceptos que introduce:** `dato` · `información` · `registro` · `campo` · `tabla`

[Ir a la clase →](001-que-es-un-dato-un-registro-y-una-tabla/README.md)

### [002 — Del archivo y la hoja de cálculo a la base de datos](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md)

*Fundamentos · 2 h · 3 fuentes · requiere [001](001-que-es-un-dato-un-registro-y-una-tabla/README.md)*

Por qué llega un momento en que la hoja de cálculo deja de servir, expresado en cuatro capacidades que un archivo no tiene: integridad declarada, concurrencia, consulta declarativa y durabilidad. No es una clase contra las hojas de cálculo —siguen siendo la herramienta correcta muchas veces— sino el primer criterio explícito para saber de qué lado está tu problema.

**Conceptos que introduce:** `integridad declarada` · `concurrencia` · `consulta declarativa` · `durabilidad`

[Ir a la clase →](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md)

### [003 — Tu primera base de datos: crear, insertar y leer](003-tu-primera-base-de-datos/README.md)

*Fundamentos · 2 h · 3 fuentes · requiere [001](001-que-es-un-dato-un-registro-y-una-tabla/README.md), [002](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md)*

La primera base de datos real, creada, poblada y consultada en la misma sesión. Introduce la separación entre definir estructuras y manipular contenido, y la primera aparición del nulo. A partir de aquí todo el programa se puede ejecutar, no solo leer.

**Conceptos que introduce:** `CREATE TABLE` · `INSERT` · `SELECT` · `definición frente a manipulación` · `NULL`

[Ir a la clase →](003-tu-primera-base-de-datos/README.md)

### [004 — Leer datos: SELECT, WHERE y ORDER BY](004-leer-datos-select-where-y-order-by/README.md)

*Fundamentos · 2 h · 3 fuentes · requiere [003](003-tu-primera-base-de-datos/README.md)*

Leer con precisión: filtrar filas, elegir columnas y ordenar el resultado. La idea que más consecuencias tendrá después es que el resultado de una consulta no tiene orden hasta que lo declaras, así que `LIMIT` sin `ORDER BY` devuelve filas cualesquiera.

**Conceptos que introduce:** `filtrado` · `proyección` · `orden` · `LIMIT` · `IS NULL`

[Ir a la clase →](004-leer-datos-select-where-y-order-by/README.md)

### [005 — Cambiar datos: INSERT, UPDATE, DELETE y el WHERE que salva](005-cambiar-datos-insert-update-delete/README.md)

*Fundamentos · 2 h · 3 fuentes · requiere [003](003-tu-primera-base-de-datos/README.md), [004](004-leer-datos-select-where-y-order-by/README.md)*

Las tres órdenes que cambian datos y la disciplina que las hace seguras: comprobar el alcance con un `SELECT` antes de escribir, leer el número de filas afectadas y envolver el cambio en una transacción que se pueda deshacer. Es la clase que evita el `UPDATE` sin `WHERE` que todo el mundo cuenta haber hecho una vez.

**Conceptos que introduce:** `UPDATE` · `DELETE` · `alcance del cambio` · `filas afectadas` · `transacción como red`

[Ir a la clase →](005-cambiar-datos-insert-update-delete/README.md)

### [006 — Tipos de datos: por qué un número no es un texto](006-tipos-de-datos-un-numero-no-es-un-texto/README.md)

*Fundamentos · 2 h · 3 fuentes · requiere [003](003-tu-primera-base-de-datos/README.md)*

Por qué el tipo de una columna no es burocracia: decide qué comparaciones tienen sentido, qué ordenaciones son correctas y si el dinero se calcula bien. Distingue decimal exacto de coma flotante, fija el formato ISO-8601 para fechas y explica la afinidad de tipos de SQLite, que es la razón de que un dato inválido entre en un motor y sea rechazado en otro.

**Conceptos que introduce:** `tipo` · `decimal exacto` · `coma flotante` · `fecha ISO-8601` · `afinidad de tipos`

[Ir a la clase →](006-tipos-de-datos-un-numero-no-es-un-texto/README.md)

### [007 — La clave primaria: cómo se distingue una fila de otra](007-la-clave-primaria/README.md)

*Fundamentos · 2 h · 3 fuentes · requiere [003](003-tu-primera-base-de-datos/README.md), [006](006-tipos-de-datos-un-numero-no-es-un-texto/README.md)*

Cómo se distingue una fila de otra. Presenta la clave primaria y el debate entre clave natural y sustituta con su criterio real —cuál de las dos sobrevive a los cambios del mundo— y la clave compuesta, que reaparecerá al hablar de índices y de particionado.

**Conceptos que introduce:** `clave primaria` · `clave natural` · `clave sustituta` · `clave compuesta` · `UNIQUE`

[Ir a la clase →](007-la-clave-primaria/README.md)

### [008 — Dos tablas y una relación: la clave foránea](008-dos-tablas-y-una-relacion/README.md)

*Fundamentos · 2 h · 3 fuentes · requiere [007](007-la-clave-primaria/README.md)*

La segunda tabla y el momento en que aparece la relación. La clave foránea convierte una convención en una regla que el motor impone, la tabla intermedia resuelve el muchos-a-muchos y la reunión permite volver a ver el hecho completo. Aquí se ven por primera vez las anomalías que justifican toda la parte 02.

**Conceptos que introduce:** `clave foránea` · `tabla de relación` · `reunión` · `anomalías de repetición`

[Ir a la clase →](008-dos-tablas-y-una-relacion/README.md)

### [009 — Cuándo NO necesitas una base de datos](009-cuando-no-necesitas-una-base-de-datos/README.md)

*Fundamentos · 2 h · 3 fuentes · requiere [002](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md), [008](008-dos-tablas-y-una-relacion/README.md)*

La clase que da permiso para no usar una base de datos. Enumera los casos en que un archivo, un Parquet o un motor embebido es la respuesta correcta, y pone precio a la alternativa: el costo de operación de un motor servidor no aparece en la factura de licencia sino en las guardias, los respaldos y las actualizaciones.

**Conceptos que introduce:** `criterio de decisión` · `motor embebido` · `costo de operación` · `alternativas`

[Ir a la clase →](009-cuando-no-necesitas-una-base-de-datos/README.md)

### [010 — El mapa de los motores: seis familias y un criterio](010-el-mapa-de-los-motores/README.md)

*Fundamentos · 2 h · 3 fuentes · requiere [009](009-cuando-no-necesitas-una-base-de-datos/README.md)*

El mapa que se usará durante todo el programa: seis familias de motores, qué patrón de acceso optimiza cada una y qué paga a cambio. Cierra la rampa de entrada con un criterio de elección en lugar de una lista de nombres de producto.

**Conceptos que introduce:** `familias de motores` · `modelo de agregado` · `patrón de acceso` · `multimodelo`

[Ir a la clase →](010-el-mapa-de-los-motores/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «Una tabla es una lista.» No: una tabla exige que todas las filas tengan la misma forma. Una lista con filas de distinta estructura no se puede consultar sin saber de antemano qué hay dentro.
- «La clave primaria es un número autoincremental.» Ese es un mecanismo posible, no la definición. La clave primaria es la clave candidata elegida por ser única, no nula y estable.
- «Guardo las fechas como texto porque así las veo bien.» El texto libre no se compara ni se ordena de forma fiable. ISO-8601 ordena alfabéticamente igual que cronológicamente, y esa es toda la discusión.
- «Si usara una base de datos de verdad, esto iría más rápido.» Muchas veces no: un CSV leído entero en memoria le gana a cualquier motor para volúmenes pequeños. La base de datos se justifica por concurrencia, integridad y durabilidad antes que por velocidad.

## Vocabulario de la parte

Los 46 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **afinidad de tipos** | Regla de SQLite por la que la columna sugiere un tipo pero acepta valores de otro y los convierte cuando puede. Explica por qué en SQLite entra un texto en una columna `INTEGER` y por qué ese mismo dato es rechazado en PostgreSQL. | [006](006-tipos-de-datos-un-numero-no-es-un-texto/README.md) |
| **alcance del cambio** | Cuántas filas toca realmente una orden de escritura. La disciplina es comprobarlo antes: escribir el `SELECT` con el mismo `WHERE`, contar, y solo entonces convertirlo en `UPDATE` o `DELETE`. | [005](005-cambiar-datos-insert-update-delete/README.md) |
| **alternativas** | Lo que se usa cuando una base de datos no está justificada: un CSV o un Parquet, un JSON versionado, una hoja de cálculo compartida, un fichero por proceso. Nombrarlas obliga a defender la elección de motor en lugar de darla por hecha. | [009](009-cuando-no-necesitas-una-base-de-datos/README.md) |
| **anomalías de repetición** | Los tres desastres de guardar el mismo hecho en varios sitios: al insertar hay que repetir datos, al actualizar se corrige una copia y no las otras, y al borrar se pierde información que solo vivía ahí. Son el argumento original de la normalización. | [008](008-dos-tablas-y-una-relacion/README.md) |
| **campo** | Una columna: un dato con nombre, tipo y —a veces— una regla. El nombre dice qué significa, el tipo dice qué valores son posibles y la restricción dice cuáles son admisibles. | [001](001-que-es-un-dato-un-registro-y-una-tabla/README.md) |
| **clave compuesta** | Clave primaria formada por dos o más columnas, típica de las tablas de relación: `(estudiante_id, curso_id)`. Fija además el orden de las columnas del índice que la sostiene, y ese orden decide qué consultas se aceleran. | [007](007-la-clave-primaria/README.md) |
| **clave foránea** | Columna que referencia la clave primaria de otra tabla y a la que el gestor obliga a apuntar a una fila existente. Es la integridad referencial hecha declaración: sin ella, las relaciones son una convención que alguien acabará rompiendo. | [008](008-dos-tablas-y-una-relacion/README.md) |
| **clave natural** | Identificador que ya existe en el dominio —RUT, ISBN, matrícula—. Ventaja: significa algo. Riesgo: el mundo la cambia —una persona corrige su documento, un organismo reasigna códigos— y el cambio arrastra a todas las filas que la referencian. | [007](007-la-clave-primaria/README.md) |
| **clave primaria** | La clave candidata elegida para identificar cada fila: única, no nula y estable en el tiempo. Es la dirección por la que el resto del esquema se referirá a esa fila. | [007](007-la-clave-primaria/README.md) |
| **clave sustituta** | Identificador inventado por el sistema y sin significado externo: entero autoincremental, UUID. No cambia nunca porque no depende del mundo, a costa de necesitar además una restricción `UNIQUE` sobre la clave natural real. | [007](007-la-clave-primaria/README.md) |
| **coma flotante** | Representación binaria aproximada (`REAL`, `DOUBLE`) según IEEE 754. Rápida y adecuada para magnitudes físicas, ruinosa para dinero: `0.1 + 0.2` no da `0.3` y la diferencia se acumula fila a fila. | [006](006-tipos-de-datos-un-numero-no-es-un-texto/README.md) |
| **concurrencia** | Varias sesiones leyendo y escribiendo a la vez sobre los mismos datos. Un archivo compartido no la resuelve: el último en guardar pisa al anterior. Un gestor la resuelve con transacciones, bloqueo o versiones. | [002](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) |
| **consulta declarativa** | Se declara *qué* resultado se quiere y el motor decide *cómo* obtenerlo. Quien consulta no escribe recorridos ni bucles; el optimizador elige el plan y puede cambiarlo cuando cambian los datos, sin que nadie reescriba la consulta. | [002](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) |
| **costo de operación** | Todo lo que cuesta mantener vivo un motor después de instalarlo: respaldos probados, actualizaciones, monitorización, personas de guardia. Suele superar con creces el costo de licencia o de cómputo. | [009](009-cuando-no-necesitas-una-base-de-datos/README.md) |
| **CREATE TABLE** | La orden que declara una tabla: columnas, tipos y restricciones. Es el contrato; a partir de ahí el motor rechaza todo lo que no lo cumpla, venga de donde venga. | [003](003-tu-primera-base-de-datos/README.md) |
| **criterio de decisión** | La regla explícita por la que se elige —o se descarta— una tecnología: volumen, concurrencia, garantías necesarias y costo de operación. Sin criterio escrito, la elección se justifica a posteriori y ya no se puede revisar. | [009](009-cuando-no-necesitas-una-base-de-datos/README.md) |
| **dato** | Un valor registrado sin el contexto que lo interpreta: `38`, `Ada`, `2026-03-01`. Por sí solo no afirma nada, porque el mismo valor puede ser una edad, una temperatura o un número de camiseta. Toda base de datos existe para guardar el dato junto al contexto que lo convierte en información. | [001](001-que-es-un-dato-un-registro-y-una-tabla/README.md) |
| **decimal exacto** | Tipo numérico de precisión y escala fijas (`NUMERIC`, `DECIMAL`) que representa exactamente los valores decimales. Es el tipo del dinero: no arrastra el error de representación binaria de la coma flotante. | [006](006-tipos-de-datos-un-numero-no-es-un-texto/README.md) |
| **definición frente a manipulación** | SQL se separa en DDL, que define y cambia estructuras (`CREATE`, `ALTER`, `DROP`), y DML, que consulta y cambia contenido (`SELECT`, `INSERT`, `UPDATE`, `DELETE`). La distinción importa porque no todos los motores dan al DDL las mismas garantías transaccionales. | [003](003-tu-primera-base-de-datos/README.md) |
| **DELETE** | Borra las filas que cumplen el `WHERE`. Igual que `UPDATE`, sin `WHERE` alcanza a toda la tabla; a diferencia de `DROP`, deja la estructura en pie. | [005](005-cambiar-datos-insert-update-delete/README.md) |
| **durabilidad** | Una vez confirmada la transacción, su efecto sobrevive a un corte de luz. Se consigue escribiendo el cambio en un registro secuencial y forzándolo al disco antes de responder «hecho». | [002](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) |
| **familias de motores** | Las formas de organizar datos que estructuran este programa: relacional, documental, clave-valor, grafo, columnas anchas y series temporales, más los índices de búsqueda y los vectoriales como casos especializados. Cada familia optimiza un patrón de acceso y paga en los demás. | [010](010-el-mapa-de-los-motores/README.md) |
| **fecha ISO-8601** | El formato `AAAA-MM-DD` —y `AAAA-MM-DDTHH:MM:SSZ` con hora— que ordena alfabéticamente igual que cronológicamente y no es ambiguo entre día y mes. Guardar fechas como texto libre es la vía directa a datos que no se pueden comparar. | [006](006-tipos-de-datos-un-numero-no-es-un-texto/README.md) |
| **filas afectadas** | El número que el motor devuelve tras una escritura. Es la evidencia de que el cambio alcanzó lo previsto: si esperabas una fila y salieron cuatro mil, el `WHERE` estaba mal. | [005](005-cambiar-datos-insert-update-delete/README.md) |
| **filtrado** | Quedarse con las filas que cumplen un predicado (`WHERE`). En álgebra relacional es la selección: reduce el número de filas, nunca el de columnas. | [004](004-leer-datos-select-where-y-order-by/README.md) |
| **información** | El dato más el contexto que fija su significado: de qué es, de cuándo y de quién. «38» es un dato; «la temperatura del sensor 3 a las 10:15 fue 38 °C» es información. Diseñar un esquema es, literalmente, decidir qué contexto se guarda y cuál se pierde para siempre. | [001](001-que-es-un-dato-un-registro-y-una-tabla/README.md) |
| **INSERT** | La orden que añade filas. Falla —y debe fallar— si la fila viola una restricción declarada: es el momento en que la integridad declarada demuestra que sirve para algo. | [003](003-tu-primera-base-de-datos/README.md) |
| **integridad declarada** | Las reglas del dominio escritas en el esquema —`NOT NULL`, `UNIQUE`, `CHECK`, clave foránea— para que el gestor las imponga a toda aplicación que escriba, no solo a la que recordó comprobarlas. Es la diferencia entre una regla y una esperanza. | [002](002-del-archivo-y-la-hoja-de-calculo-a-la-base-de-datos/README.md) |
| **IS NULL** | El único predicado que comprueba ausencia de valor. `= NULL` nunca es cierto —da `UNKNOWN`— porque nada, ni siquiera otro nulo, es igual a lo desconocido. | [004](004-leer-datos-select-where-y-order-by/README.md) |
| **LIMIT** | Corta el resultado a las primeras N filas. Sin `ORDER BY` no significa nada estable: «las primeras N» sin criterio de orden es «N cualesquiera». | [004](004-leer-datos-select-where-y-order-by/README.md) |
| **modelo de agregado** | Cómo agrupa el motor los datos que lee y escribe de una vez. El relacional trabaja con filas que se recomponen por reunión; los motores de agregado guardan la unidad completa junta y evitan la reunión, a cambio de duplicar. | [010](010-el-mapa-de-los-motores/README.md) |
| **motor embebido** | Base de datos que corre dentro del proceso de la aplicación, sin servidor ni puerto: SQLite, DuckDB. Elimina el costo de operación y la latencia de red, a cambio de no poder servir a varias máquinas. | [009](009-cuando-no-necesitas-una-base-de-datos/README.md) |
| **multimodelo** | Motor que soporta varias familias a la vez —PostgreSQL con JSONB, vectores y búsqueda de texto—. Reduce el número de sistemas que hay que operar; el riesgo es dar por hecho que hacer varias cosas equivale a hacerlas todas bien. | [010](010-el-mapa-de-los-motores/README.md) |
| **NULL** | Marca de ausencia de valor: no es cero, ni cadena vacía, ni «desconocido» codificado a mano. Introduce una lógica de tres valores que cambia el resultado de comparaciones, agregados y `NOT IN`. | [003](003-tu-primera-base-de-datos/README.md) |
| **orden** | El resultado de una consulta es un conjunto: no tiene orden hasta que se declara `ORDER BY`. Confiar en el orden «que salió» es un error que sobrevive en pruebas y falla en producción el día que cambia el plan. | [004](004-leer-datos-select-where-y-order-by/README.md) |
| **patrón de acceso** | La lista concreta de consultas y escrituras que el sistema tendrá que servir, con su frecuencia y su latencia aceptable. Es el dato de entrada del diseño: sin él, elegir modelo o índice es adivinar. | [010](010-el-mapa-de-los-motores/README.md) |
| **proyección** | Quedarse con un subconjunto de columnas. Reduce el ancho de la fila, no su cantidad —salvo que se eliminen los duplicados resultantes con `DISTINCT`, cosa que SQL no hace por defecto y el álgebra sí. | [004](004-leer-datos-select-where-y-order-by/README.md) |
| **registro** | Una fila: un hecho completo sobre una cosa, ni medio hecho ni dos. La regla práctica para detectar el error más común: si para leer un campo hay que partirlo por comas, ese registro esconde varios hechos y viola la primera forma normal. | [001](001-que-es-un-dato-un-registro-y-una-tabla/README.md) |
| **reunión** | Combinar filas de dos tablas emparejándolas por un valor común, normalmente clave foránea contra clave primaria. Es la operación que permite normalizar sin perder la capacidad de ver el hecho completo. | [008](008-dos-tablas-y-una-relacion/README.md) |
| **SELECT** | La orden de lectura. Nunca modifica datos; describe el conjunto que se quiere y deja al motor la estrategia para producirlo. | [003](003-tu-primera-base-de-datos/README.md) |
| **tabla** | Un conjunto de registros con exactamente la misma forma: mismas columnas, mismos tipos, mismo significado por columna. Esa uniformidad es lo que permite consultar sin saber de antemano qué hay dentro. | [001](001-que-es-un-dato-un-registro-y-una-tabla/README.md) |
| **tabla de relación** | Tabla intermedia que resuelve una relación muchos-a-muchos guardando pares de claves foráneas. Deja de ser «solo técnica» en cuanto la relación tiene atributos propios —fecha de inscripción, nota— y pasa a ser una entidad de pleno derecho. | [008](008-dos-tablas-y-una-relacion/README.md) |
| **tipo** | El conjunto de valores posibles de un campo más las operaciones válidas sobre ellos. Declarar el tipo correcto delega en el motor la mitad de las validaciones que, si no, hay que escribir a mano en cada aplicación. | [006](006-tipos-de-datos-un-numero-no-es-un-texto/README.md) |
| **transacción como red** | Envolver un cambio en `BEGIN` … `ROLLBACK` permite ver su efecto y deshacerlo. Es la red de seguridad más barata que existe y la razón práctica de que un `UPDATE` sin transacción sea una apuesta. | [005](005-cambiar-datos-insert-update-delete/README.md) |
| **UNIQUE** | Restricción que prohíbe valores repetidos en una columna o combinación de columnas. A diferencia de la clave primaria admite nulos —y cuántos admite depende del motor, que es una de las divergencias clásicas entre dialectos. | [007](007-la-clave-primaria/README.md) |
| **UPDATE** | Cambia valores de las filas que cumplen el `WHERE`. Sin `WHERE` cambia todas: es la orden que más datos ha destruido en la historia de las bases de datos. | [005](005-cambiar-datos-insert-update-delete/README.md) |

## Fuentes usadas en esta parte

14 obras distintas sostienen lo que se afirma en estas
10 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **William Kent** (2012). [Data and Reality](https://technicspub.com/data-and-reality/). 3.a ed. Technics Publications. ISBN 978-1-935504-21-4.  
  Por qué ningún modelo captura el mundo: fuente del criterio de alcance del programa.  
  *Se cita en las clases 001.*
- **Michael J. Hernandez** (2020). [Database Design for Mere Mortals](https://www.informit.com/store/database-design-for-mere-mortals-a-hands-on-guide-to-9780136788041). 4.a ed. Addison-Wesley. ISBN 978-0-13-678804-1.  
  Método de diseño paso a paso, independiente de producto.  
  *Se cita en las clases 001, 002, 007, 008.*
- **Abraham Silberschatz, Henry F. Korth, S. Sudarshan** (2019). [Database System Concepts](https://db-book.com/). 7.a ed. McGraw-Hill. ISBN 978-0-07-802215-9.  
  Texto de referencia universitario. El sitio oficial publica diapositivas y capítulos de muestra.  
  *Se cita en las clases 002.*
- **Martin Kleppmann** (2017). [Designing Data-Intensive Applications](https://dataintensive.net/). O'Reilly. ISBN 978-1-4493-7332-0.  
  Referencia central del programa para replicación, partición, transacciones distribuidas y streaming.  
  *Se cita en las clases 009, 010.*
- **Ramez Elmasri, Shamkant B. Navathe** (2015). [Fundamentals of Database Systems](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003546). 7.a ed. Pearson. ISBN 978-0-13-397077-7.  
  Modelado entidad-relación tratado con más detalle que en otros manuales.  
  *Se cita en las clases 001, 008.*
- **Pramod J. Sadalage, Martin Fowler** (2012). [NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence](https://martinfowler.com/books/nosql.html). Addison-Wesley. ISBN 978-0-321-82662-6.  
  Origen del término agregado y de la persistencia políglota que estructura este programa.  
  *Se cita en las clases 010.*
- **Bill Karwin** (2010). [SQL Antipatterns: Avoiding the Pitfalls of Database Programming](https://pragprog.com/titles/bksqla/sql-antipatterns/). Pragmatic Bookshelf. ISBN 978-1-934356-55-5.  
  Catálogo de errores de modelado con su corrección y cuando el antipatron es aceptable.  
  *Se cita en las clases 005, 006, 007.*
- **C. J. Date** (2015). [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/). 3.a ed. O'Reilly. ISBN 978-1-4919-4117-1.  
  Separa el modelo relacional de lo que SQL realmente implementa, incluidos los nulos.  
  *Se cita en las clases 004, 006, 007.*
- **solid IT gmbh** (2026). [DB-Engines Ranking](https://db-engines.com/en/ranking).  
  Ranking mensual de más de 400 gestores por menciones, ofertas de empleo y perfiles profesionales. Mide visibilidad y demanda laboral, no calidad técnica.  
  *Se cita en las clases 010.*
- **DuckDB Foundation** (2026). [DuckDB Documentation](https://duckdb.org/docs/).  
  Motor analítico embebido: OLAP columnar sin servidor.  
  *Se cita en las clases 009.*
- **Python Software Foundation** (2026). [Python: sqlite3](https://docs.python.org/3/library/sqlite3.html).  
  API DB-API 2.0 usada por los laboratorios ejecutables del repositorio.  
  *Se cita en las clases 003.*
- **SQLite Consortium** (2026). [SQLite Documentation](https://sqlite.org/docs.html).  
  Motor embebido usado por los laboratorios sin dependencias del programa.  
  *Se cita en las clases 002, 003, 004, 005, 006, 009.*
- **Peter Pin-Shan Chen** (1976). [The Entity-Relationship Model - Toward a Unified View of Data](https://dl.acm.org/doi/10.1145/320434.320440). ACM TODS 1(1). DOI [10.1145/320434.320440](https://doi.org/10.1145/320434.320440).  
  Origen del diagrama entidad-relación.  
  *Se cita en las clases 008.*
- **ISO/IEC JTC 1/SC 32** (2023). [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html).  
  Norma del lenguaje SQL. Ningún motor la implementa por completo.  
  *Se cita en las clases 003, 004, 005.*

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

- [Parte 01 — Fundamentos, sistemas y método](../part-01-fundamentos-datos-sistemas-y-metodo/README.md)
- [Parte 02 — Modelado conceptual y requisitos](../part-02-modelado-conceptual-y-requisitos/README.md)
- [Parte 03 — Modelo relacional y álgebra](../part-03-modelo-relacional-y-algebra/README.md)
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
