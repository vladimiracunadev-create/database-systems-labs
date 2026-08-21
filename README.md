<div align="center">

<img src="site/assets/icon.svg" alt="" width="96" height="96">

# 🗄️ Database Systems Labs

## **15 partes · 74 clases · 230 horas · 120 fuentes verificables**

### **408 implementaciones en 27 motores · 267 ejecutadas contra el motor real**

**Programa abierto de ingeniería de bases de datos, del modelado conceptual a la
arquitectura distribuida, la operación y los sistemas de recuperación para
inteligencia artificial. Ninguna clase se publica sin fuentes, y ninguna cita
apunta al vacío: lo comprueba la integración continua en cada `push`.**

[![Validación](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/ci.yml)
[![Sitio](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/pages.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/pages.yml)
[![Enlaces](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/enlaces.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/enlaces.yml)
[![CodeQL](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/codeql.yml)

[![Versión](https://img.shields.io/badge/versión-3.0.0-orange?style=for-the-badge)](CHANGELOG.md)
[![Clases](https://img.shields.io/badge/clases-74%20·%2015%20partes-4aa8ff?style=for-the-badge)](classes/README.md)
[![Fuentes](https://img.shields.io/badge/fuentes-120%20con%20ISBN%20·%20DOI%20·%20norma-0b7285?style=for-the-badge)](catalog/sources.json)
[![Laboratorios](https://img.shields.io/badge/laboratorios-7%20ejecutables%20en%20CI-2ee6c5?style=for-the-badge)](labs/README.md)
[![Licencia](https://img.shields.io/badge/licencia-MIT-3fb950?style=for-the-badge)](LICENSE)

[![Python](https://img.shields.io/badge/Python-3.11%20·%203.12%20·%203.13-3776AB?style=flat-square&logo=python&logoColor=white)](requirements.txt)
[![Sin dependencias](https://img.shields.io/badge/laboratorios-solo%20stdlib-0ea5e9?style=flat-square)](labs/README.md)
[![Pruebas](https://img.shields.io/badge/pruebas-127%20pytest-8957e5?style=flat-square&logo=pytest&logoColor=white)](tests/)
[![Motores](https://img.shields.io/badge/motores-27%20en%20catálogo-ffc861?style=flat-square&logo=postgresql&logoColor=white)](catalog/databases.json)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-sitio%20vivo-222?style=flat-square&logo=githubpages&logoColor=white)](https://vladimiracunadev-create.github.io/database-systems-labs/)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-verificado-4169E1?style=flat-square&logo=postgresql&logoColor=white)](docker-compose.yml)
[![MySQL](https://img.shields.io/badge/MySQL-verificado-4479A1?style=flat-square&logo=mysql&logoColor=white)](docker-compose.yml)
[![SQLite](https://img.shields.io/badge/SQLite-núcleo-003B57?style=flat-square&logo=sqlite&logoColor=white)](labs/01-sql-foundations/README.md)
[![DuckDB](https://img.shields.io/badge/DuckDB-núcleo-FFF000?style=flat-square&logo=duckdb&logoColor=black)](labs/README.md)
[![MongoDB](https://img.shields.io/badge/MongoDB-verificado-47A248?style=flat-square&logo=mongodb&logoColor=white)](docker-compose.yml)
[![Redis](https://img.shields.io/badge/Redis-verificado-FF4438?style=flat-square&logo=redis&logoColor=white)](docker-compose.yml)
[![Neo4j](https://img.shields.io/badge/Neo4j-verificado-4581C3?style=flat-square&logo=neo4j&logoColor=white)](docker-compose.yml)

[🌐 **Sitio de estudio**](https://vladimiracunadev-create.github.io/database-systems-labs/) ·
[▶️ **Empezar por la clase 001**](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md) ·
[📚 **Índice de las 74 clases**](classes/README.md) ·
[🧭 **Rutas por rol**](rutas/README.md) ·
[🧪 **Laboratorios**](labs/README.md) ·
[📝 **Autoevaluación**](https://vladimiracunadev-create.github.io/database-systems-labs/autoevaluacion.html) ·
[🎓 **Certificaciones**](certificaciones/README.md) ·
[📖 **Bibliografía**](https://vladimiracunadev-create.github.io/database-systems-labs/fuentes.html) ·
[🗺️ **Roadmap**](ROADMAP.md)

<br>

| 📚 Clases | 🗂️ Partes | ⏱️ Horas | 🧩 Motores | 🔬 Implementaciones | 🧪 Labs | 📖 Fuentes | 📝 Preguntas |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **74** | **15** | **230** | **27** | **408** | **8** | **120** | **296** |

</div>

---

## 🎯 Qué es esto

Un programa **secuencial y completo** de ingeniería de datos: 74 clases numeradas
(001 → 074) repartidas en 15 partes, de «qué es un dato» hasta réplica, consenso,
gobierno y recuperación para IA.

No es un curso de SQL con capítulos sueltos. Tiene dos reglas que lo gobiernan y que
la máquina hace cumplir en cada `push`: **toda afirmación lleva fuente**, y **todo
motor se compara resolviendo el mismo problema**, diciendo también por qué no conviene.

Cada clase es una carpeta con la misma anatomía:

| | Sección | Qué aporta |
|:---:|---|---|
| 🎯 | **Propósito** | Qué problema resuelve la clase |
| 📚 | **Resultados de aprendizaje** | Cinco capacidades comprobables |
| 🧠 | **Fundamentos** | El mecanismo, no la receta |
| 🔬 | **Ejemplo trabajado** | Números y código reales, con su traza |
| ⚖️ | **Comparación** | Tabla de decisiones con sus costos |
| ⚠️ | **Errores frecuentes** | El error, su causa y su corrección |
| 🏭 | **De la clase a la operación** | Qué cambia cuando el sistema es real |
| 🔄 | **Reto de transferencia** | Aplicarlo al propio contexto |
| ❓ | **Preguntas de evaluación** | Cuatro preguntas que exigen explicar |
| 🌐 | **El mismo problema en cada motor** | El caso resuelto —o descartado— en varios motores |
| 🧪 | **Laboratorio, rúbrica y fuentes** | Añadidos por el generador desde el currículo |

## ⚖️ La regla del repositorio

> [!IMPORTANT]
> **Ninguna clase se publica sin fuentes, y ninguna cita apunta al vacío.**

Todo lo que el programa afirma procede de un libro, un artículo con DOI, una
norma o la documentación oficial de un producto. Esas fuentes viven en un
registro único, [`catalog/sources.json`](catalog/sources.json), y cada clase
declara cuáles usa.

La regla no es una intención: la hace cumplir
[`scripts/validate_repository.py`](scripts/validate_repository.py), que falla el
`push` si una clase tiene menos de dos fuentes, si cita un identificador que no
existe, si una fuente del registro no la cita nadie, si un libro no lleva ISBN o
si un artículo no lleva DOI ni sede de publicación.

Y el validador tampoco se cree a sí mismo: [`tests/`](tests/) lo somete a un
repositorio roto a propósito —una clase con una sola fuente, una cita al vacío,
un libro sin ISBN, una lección a la que le falta una sección, un enlace
relativo muerto— y exige que lo detecte. Ver pasar a un validador sobre un
repositorio sano no demuestra que sirva.

## 🌐 El mismo problema, en cada motor

La segunda regla, la que cambia la forma de estudiar: **una clase no explica un
concepto, lo pone a competir**.

Cada clase declara un caso con su salida esperada en
[`motores.yaml`](classes/part-04-sql-en-profundidad/026-reuniones-inner-outer-semi-y-anti/motores.yaml),
lo resuelve en varios motores dentro de `implementaciones/`, y por cada motor
escribe dos cosas que pesan lo mismo:

- ✅ **Por qué sí** conviene resolverlo ahí.
- ❌ **Por qué no** — porque ningún motor sale gratis, y un motor que solo tiene
  ventajas no se ha entendido: se ha copiado del folleto del fabricante.

Y también aparecen los motores que **no** resuelven el caso, con el motivo y con
lo que se hace en su lugar. Descartar Redis para una reunión con un argumento
enseña más que usarlo bien: es la mitad del criterio de arquitectura.

Que las respuestas coincidan no es una promesa del texto. Lo ejecuta una
máquina:

```bash
python scripts/verificar_equivalencia.py                  # SQLite y DuckDB, sin nada instalado
docker compose --profile todo up -d --wait
python scripts/verificar_equivalencia.py --con-servicios  # PostgreSQL, MySQL, MongoDB, Redis, Neo4j
```

Tres niveles de prueba, y la clase dice siempre cuál es cuál:

| | Nivel | Motores | Qué significa |
|:---:|---|---|---|
| ✅ | **Núcleo** | SQLite, DuckDB | Se ejecuta en cualquier máquina y en todos los trabajos de CI, sin levantar nada |
| 🐳 | **Servicio** | PostgreSQL, MySQL, MongoDB, Redis, Neo4j | Se ejecuta contra el motor real levantado con `docker compose`, usando su propio cliente oficial |
| ⚪ | **Declarado** | SQL Server, Oracle, Cassandra, ClickHouse… | El código se muestra y se revisa contra la documentación citada; la máquina **no** lo ejecuta, y así se dice |

Además, cada afirmación sobre un motor lleva al lado el enlace a **su página de
documentación oficial**, y el validador comprueba que ese enlace cuelga del
dominio que el catálogo registra para ese motor: una opinión sobre PostgreSQL
tiene que apoyarse en `postgresql.org`, no en un blog.

## 🗺️ El mapa del programa

Las 15 partes no son una lista: son una progresión. Cada bloque apoya al
siguiente, y saltarse el cimiento se paga en las partes de escala.

```mermaid
flowchart LR
    subgraph CIM["🧱 Cimientos"]
        direction TB
        P00["🪜 00 · Primeros pasos"] --> P01["🧱 01 · Fundamentos"]
        P01 --> P02["📐 02 · Modelado"]
        P02 --> P03["🔗 03 · Relacional y álgebra"]
    end

    subgraph LEN["🔎 Lenguaje y motores"]
        direction TB
        P04["🔎 04 · SQL en profundidad"] --> P05["🐘 05 · Motores y dialectos"]
    end

    subgraph MOD["🗃️ Otros modelos"]
        direction TB
        P06["📄 06 · Documentos y clave-valor"] --> P07["🕸️ 07 · Grafos, columnas y búsqueda"]
    end

    subgraph INT["⚙️ Dentro del motor"]
        direction TB
        P08["🔒 08 · Transacciones"] --> P09["🗂️ 09 · Índices y planes"]
    end

    subgraph ESC["🌐 Escala y operación"]
        direction TB
        P10["🌐 10 · Distribución y réplica"] --> P11["🛡️ 11 · Operación y gobierno"]
    end

    subgraph ANA["🧠 Analítica e IA"]
        direction TB
        P12["📊 12 · Analítica y streaming"] --> P13["🧠 13 · Vectores y RAG"]
    end

    CIM --> LEN --> MOD --> INT --> ESC --> ANA --> P14["🏛️ 14 · Arquitectura y proyecto final"]

    classDef ini fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef fin fill:#3d2e0b,stroke:#e8590c,color:#fff
    class P00 ini
    class P14 fin
```

## 🗂️ Programa

| | Parte | Tema | Clases | Horas |
|:---:|:---:|---|---:|---:|
| 🪜 | [00](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/README.md) | Primeros pasos: del archivo a la base de datos | 10 | 20 |
| 🧱 | [01](classes/part-01-fundamentos-datos-sistemas-y-metodo/README.md) | Fundamentos, sistemas y método | 4 | 12 |
| 📐 | [02](classes/part-02-modelado-conceptual-y-requisitos/README.md) | Modelado conceptual y requisitos | 5 | 16 |
| 🔗 | [03](classes/part-03-modelo-relacional-y-algebra/README.md) | Modelo relacional y álgebra | 4 | 13 |
| 🔎 | [04](classes/part-04-sql-en-profundidad/README.md) | SQL en profundidad | 6 | 20 |
| 🐘 | [05](classes/part-05-motores-relacionales-y-dialectos/README.md) | Motores relacionales y dialectos | 4 | 12 |
| 📄 | [06](classes/part-06-documentos-y-clave-valor/README.md) | Documentos y clave-valor | 4 | 13 |
| 🕸️ | [07](classes/part-07-grafos-columnas-tiempo-y-busqueda/README.md) | Grafos, columnas, tiempo y búsqueda | 5 | 15 |
| 🔒 | [08](classes/part-08-transacciones-concurrencia-y-recuperacion/README.md) | Transacciones, concurrencia y recuperación | 5 | 18 |
| 🗂️ | [09](classes/part-09-almacenamiento-indices-y-planes/README.md) | Almacenamiento, índices y planes | 5 | 17 |
| 🌐 | [10](classes/part-10-distribucion-replica-y-consistencia/README.md) | Distribución, réplica y consistencia | 5 | 17 |
| 🛡️ | [11](classes/part-11-operacion-seguridad-y-gobierno/README.md) | Operación, seguridad y gobierno | 6 | 19 |
| 📊 | [12](classes/part-12-analitica-integracion-y-streaming/README.md) | Analítica, integración y streaming | 4 | 13 |
| 🧠 | [13](classes/part-13-vectores-recuperacion-y-rag/README.md) | Vectores, recuperación y RAG | 4 | 13 |
| 🏛️ | [14](classes/part-14-arquitectura-y-proyecto-final/README.md) | Arquitectura y proyecto final | 3 | 12 |

➡️ El índice completo está en [`classes/README.md`](classes/README.md) y el
currículo canónico, en [`curriculum.yaml`](curriculum.yaml).

## 🎓 Modelo pedagógico

Cada clase sigue la misma estructura, y la validación comprueba que están todas
las secciones. A eso el generador añade el laboratorio, la rúbrica y la
bibliografía de la clase. El criterio de aprobación es explícito: **un resultado
correcto sin explicación no demuestra transferencia**.

| | Se exige | Y no vale |
|:---:|---|---|
| 🔬 | El ejemplo trae números o código reales, con su traza | «Es más rápido» sin medición |
| 🧠 | Se explica el mecanismo, para predecir casos no cubiertos | La receta que solo sirve para el caso mostrado |
| ⚠️ | Los errores frecuentes traen causa y corrección | El síntoma suelto |
| 📏 | Se declara lo que la clase **no** demuestra | El silencio que se lee como promesa |
| 📖 | Toda comparación entre productos se apoya en documentación oficial | El material comercial o el blog anónimo |

## 🚀 Cómo usar el programa

```mermaid
flowchart LR
    A["1️⃣ Sitúate<br/>diagnóstico inicial"] --> B["2️⃣ Elige ruta<br/>por rol"]
    B --> C["3️⃣ Lee la clase<br/>fundamentos y ejemplo"]
    C --> D["4️⃣ Ejecuta el caso<br/>en varios motores"]
    D --> E["5️⃣ Haz el laboratorio<br/>y guarda la evidencia"]
    E --> F["6️⃣ Reto de transferencia<br/>a tu contexto"]
    F --> C
    E -.-> G["🏛️ Proyecto final<br/>y portafolio"]
    C -.-> H["📖 Fuentes de la clase<br/>para profundizar"]

    classDef ini fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef extra fill:#1b2733,stroke:#6cb6ff,color:#e6edf3
    class A,B ini
    class G,H extra
```

1. **Sitúate antes de empezar.** El [diagnóstico inicial](assessments/diagnostic.md)
   no tiene nota: dice por qué parte entrar. Un programa de 230 horas empezado en
   el punto equivocado se abandona.
2. **Elige tu [ruta por rol](rutas/README.md).** Las 74 clases no son para todos a
   la vez, y cada ruta ordena las partes según el cargo al que apuntas.
3. **Sigue el orden dentro de la ruta.** La numeración es secuencial por diseño.
4. **Ejecuta el caso en varios motores.** Es la parte que no se puede leer: hay que
   verla dar el mismo resultado —o no darlo— en cada uno.
5. **Guarda la evidencia de cada laboratorio.** Hipótesis previa, comando, entorno,
   salida completa y **límite declarado**. Es el 40 % de la nota, y el material del
   [portafolio](projects/portafolio.md).

## 🧪 Laboratorios ejecutables

Siete de los ocho laboratorios se ejecutan **sin instalar nada**: solo biblioteca
estándar de Python, y los siete corren en integración continua sobre Python 3.11,
3.12 y 3.13.

| | Laboratorio | Qué mide | Parte |
|:---:|---|---|:---:|
| 🔎 | **[SQL foundations](labs/01-sql-foundations/README.md)** | Filas devueltas frente a las esperadas e integridad referencial del conjunto | `04` |
| 📐 | **[Modelado políglota](labs/02-polyglot-modeling/README.md)** | Qué consultas resuelve cada modelo sin trabajo extra, y qué duplicación introduce | `06` |
| 🔒 | **[Transacciones](labs/03-transactions/README.md)** | Una actualización perdida con hilos reales, corregida de tres formas | `08` |
| 🗂️ | **[Índices y planes](labs/04-indexing/README.md)** | Forma del plan y trabajo de la consulta antes y después de cada índice | `09` |
| 📄 | **[Cargas NoSQL](labs/05-nosql-workloads/README.md)** | TTL frente a coherencia, incrustar frente a referenciar y la clave de partición caliente | `06` |
| 🧠 | **[Búsqueda vectorial](labs/06-vector-search/README.md)** | Orden del ranking frente al esperado y `recall@k` sobre el conjunto relevante | `13` |
| 🌐 | **[Réplica](labs/07-replication/README.md)** | Lecturas obsoletas, garantías de sesión rotas y lo que cuesta cada corrección | `10` |
| 💾 | **[Recuperación](labs/08-recovery/README.md)** | RPO, trabajo de recuperación y restauración a un punto en el tiempo | `11` |

> [!NOTE]
> Ninguno afirma nada en milisegundos: un tiempo depende de la máquina. Lo que
> afirman son invariantes, planes de ejecución, accesos y bytes. El detalle está en
> [`labs/README.md`](labs/README.md).

## 🧭 Rutas por rol

Las 74 clases no son para todos a la vez. Siete recorridos ordenan el programa
según el cargo al que apuntas, y cada uno tiene su **guía de carrera**: qué es
el puesto, cómo es un día de trabajo, qué necesitas saber, qué partes hacer y
en qué orden, qué tienes que poder demostrar al terminar, qué credenciales
existen, cómo progresa la carrera y qué mitos conviene desmontar.

| | Ruta | Partes | Nivel | Horas | Guía |
|:---:|---|---|---|---:|---|
| 👩‍💻 | Desarrollador de aplicaciones | 00 · 01 · 02 · 03 · 04 · 05 · 06 · 08 · 09 · 11 · 14 | entrada | 172 | [guía](rutas/desarrollo-de-aplicaciones.md) |
| 🛠️ | Ingeniero de datos | 00 · 01 · 02 · 03 · 04 · 07 · 10 · 12 · 13 · 14 | intermedio | 151 | [guía](rutas/ingenieria-de-datos.md) |
| 🧰 | DBA / SRE de datos | 00 · 01 · 02 · 04 · 05 · 08 · 09 · 10 · 11 · 14 | intermedio | 163 | [guía](rutas/fiabilidad-y-operacion.md) |
| 🏛️ | Arquitecto de datos | todas | avanzado | 230 | [guía](rutas/arquitectura.md) |
| 📊 | Analytics engineer / BI | 00 · 01 · 02 · 03 · 04 · 05 · 09 · 12 · 14 | intermedio | 135 | [guía](rutas/analitica-y-bi.md) |
| 🧠 | Ingeniero de IA aplicada y recuperación | 00 · 01 · 02 · 03 · 04 · 06 · 07 · 09 · 13 · 14 | avanzado | 151 | [guía](rutas/ia-y-recuperacion.md) |
| 🛡️ | Gobierno y privacidad del dato | 00 · 01 · 02 · 04 · 08 · 10 · 11 · 12 · 14 | intermedio | 147 | [guía](rutas/gobierno-y-privacidad.md) |

El índice está en [`rutas/README.md`](rutas/README.md), y las rutas viven como
datos en [`curriculum.yaml`](curriculum.yaml): la validación comprueba que cada
parte, cada clase clave y cada laboratorio que prometen existen, y que las horas
que declara la guía son las que suman sus partes.

Las afirmaciones de mercado van con fuente —el
[Occupational Outlook Handbook](https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm)
del U.S. Bureau of Labor Statistics y la
[Stack Overflow Developer Survey](https://survey.stackoverflow.co/2025/technology)—
y donde no hay fuente pública para el mercado local, **no se publican cifras**.

## 🎓 Certificaciones

Para cada examen se cruza su **temario oficial**, con los pesos que publica el proveedor,
contra las clases del programa, y se calcula qué parte queda cubierta. El cálculo es
reproducible —lo hace [`scripts/generar_certificaciones.py`](scripts/generar_certificaciones.py)
desde [`certificaciones/_mapeo.json`](certificaciones/_mapeo.json)— y la brecha se declara:
saber qué te falta vale más que un porcentaje redondo.

| | Certificación | Código | Cobertura del programa | Cómo se calcula |
|:---:|---|---|---|---|
| 🔷 | [Azure Database Administrator Associate](certificaciones/dp-300.md) | DP-300 | 70 % | medida sobre las 15 subáreas oficiales |
| 🟧 | [AWS Certified Data Engineer – Associate](certificaciones/aws-dea-c01.md) | DEA-C01 | 62 % | estimada por dominio, justificada con clases |
| 🔹 | [Azure Data Fundamentals](certificaciones/dp-900.md) | DP-900 | 60 % | medida sobre las 11 subáreas oficiales |

> [!WARNING]
> Lo que la cobertura **no** mide: tu probabilidad de aprobar. Un examen de proveedor
> pregunta además por nombres de servicios y consolas que este programa no enseña a
> propósito. Un 70 % significa «te faltará estudiar el 30 %, y ya sabes cuál es».

Tres credenciales relevantes —Google Professional Data Engineer, CDMP de DAMA y las de Oracle—
aparecen listadas **sin porcentaje**, porque su ponderación oficial no está disponible en una
fuente verificable. Este repositorio no publica un número que no pueda comprobar.

## ▶️ Empezar

Requiere Python 3.11 o superior. Sin instalar ningún servidor:

```bash
python scripts/validate_repository.py
python labs/01-sql-foundations/run_lab.py
```

El laboratorio base usa SQLite en memoria: carga el dominio educativo canónico,
ejecuta consultas y comprueba invariantes. Si falla, el problema está en el
código, no en el entorno.

Los demás laboratorios ejecutables se corren igual:

```bash
python labs/03-transactions/run_transactions_lab.py   # reproduce una actualización perdida y la corrige de tres formas
python labs/04-indexing/run_indexing_lab.py           # plan y trabajo antes y después del índice
python labs/05-nosql-workloads/run_nosql_lab.py       # TTL, incrustar o referenciar, y clave de partición caliente
python labs/06-vector-search/run_vector_lab.py        # similitud coseno y recall@k
python labs/07-replication/run_replication_lab.py     # lecturas obsoletas, garantías de sesión y quórum
python labs/08-recovery/run_recovery_lab.py           # RPO, RTO y restauración a un punto en el tiempo
```

Para trabajar sobre el repositorio (generadores, validador y sus pruebas):

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

### 🐳 Laboratorios con contenedores

Los motores llegan por perfiles, para no levantarlos todos a la vez:

```bash
docker compose --profile relational up -d
```

> [!CAUTION]
> Las credenciales del `compose` son locales y están a la vista en un archivo
> versionado. **Nunca deben copiarse a otro entorno.**

## 🌐 El sitio

[**vladimiracunadev-create.github.io/database-systems-labs**](https://vladimiracunadev-create.github.io/database-systems-labs/)
— 131 páginas generadas desde este mismo repositorio, sin analítica y sin cuentas:

| | | |
|:---:|---|---|
| 🔍 | **Catálogo** | las 74 clases con búsqueda en el cliente y filtros por parte, nivel y motor |
| 📖 | **Clase** | lectura larga con barra de avance, anterior/siguiente, diagramas Mermaid y copiar bloque de código |
| 🧪 | **[Laboratorios](https://vladimiracunadev-create.github.io/database-systems-labs/laboratorios.html)** | qué mide cada uno, cómo se ejecuta y de qué fuente sale su criterio |
| 📝 | **[Autoevaluación](https://vladimiracunadev-create.github.io/database-systems-labs/autoevaluacion.html)** | las 296 preguntas del programa, enlazadas a su clase |
| 🧭 | **[Rutas por rol](https://vladimiracunadev-create.github.io/database-systems-labs/rutas/index.html)** | siete recorridos con su guía de carrera: recorrido, credenciales, mercado y mitos |
| 🎓 | **[Certificaciones](https://vladimiracunadev-create.github.io/database-systems-labs/certificaciones/index.html)** | qué parte del temario oficial de cada examen cubre el programa, calculado |
| 📚 | **[Fuentes](https://vladimiracunadev-create.github.io/database-systems-labs/fuentes.html)** | las 120 entradas con ISBN, DOI o URL oficial y quién las cita |
| 📄 | **[Documentación](https://vladimiracunadev-create.github.io/database-systems-labs/docs/index.html)** | arquitectura, método, rúbrica, entornos y roadmap, publicados desde sus `.md` |
| ✅ | **Progreso** | marcar clases como completadas; se guarda solo en tu navegador |
| 🌗 | **Tema** | claro y oscuro, siguiendo la preferencia del sistema o tu elección |
| 📱 | **Sin conexión** | aplicación instalable (PWA) con service worker y manifiesto |

Los iconos y la portada social también son artefactos generados: se dibujan
píxel a píxel con `zlib` y `struct` en
[`scripts/brand_assets.py`](scripts/brand_assets.py), sin Pillow ni ninguna otra
dependencia, para que cualquiera pueda reproducirlos byte a byte.

## 📊 Evaluación y proyecto final

El programa no evalúa memoria. La regla es la misma que aparece en cada clase: **un resultado
correcto sin explicación no demuestra transferencia**. De ahí que el 40 % de la nota sean
evidencias de laboratorio —hipótesis previa, comando, entorno, salida y **límite declarado**— y
que la rúbrica esté escrita para que la aplique alguien que no conoce el programa.

| | Pieza | Peso | Qué evalúa |
|:---:|---|---:|---|
| 🧭 | [Diagnóstico inicial](assessments/diagnostic.md) | 0 % | Por dónde empezar, con clave de corrección y encaminamiento |
| 🧪 | [Evidencias de laboratorio](assessments/evidencias.md) | 40 % | Que ejecutaste, entendiste y declaraste qué **no** demuestra |
| 🔄 | Retos de transferencia | 20 % | Que lo aplicaste a tu propio contexto |
| 🏗️ | [Decisiones de arquitectura](projects/capstone.md) | 15 % | Que puedes justificar y revertir una elección |
| 🎓 | [Proyecto final](projects/capstone.md) | 25 % | Todo junto, defendido ante preguntas |

La [rúbrica](assessments/rubric.md) —diez dimensiones, cuatro niveles descritos en cada una,
mínimos por dimensión y seis faltas críticas— y el [examen final por rol](assessments/examen-por-rol.md)
se **generan desde `curriculum.yaml`**: no pueden contradecir al programa, y si una clase cambia
de laboratorio o una parte cambia de horas, la evaluación cambia con ella o la integración
continua falla.

Los [proyectos](projects/README.md) se construyen sobre cinco
[dominios canónicos](projects/canonical-domains.md), cada uno elegido por la forma concreta en
que rompe: la reserva concurrente del último artículo, el asiento que no puede duplicarse al
reintentar, el feed que no escala, el fragmento que no debía recuperarse. Al terminar, la
evidencia acumulada es un [portafolio verificable](projects/portafolio.md).

## ✅ Calidad e integración continua

El repositorio no se publica a ciegas: cada `push` pasa por una validación que
comprueba estructura, fuentes, motores, enlaces, codificación y que ningún
artefacto generado quedó desactualizado. **Nada llega a `main` en rojo.**

| | Workflow | Qué cubre |
|:---:|---|---|
| 🧪 | [ci.yml](.github/workflows/ci.yml) | Validador del repositorio, generadores en modo `--check`, equivalencia entre motores, los siete laboratorios y 127 pruebas sobre Python 3.11, 3.12 y 3.13 |
| 🚀 | [pages.yml](.github/workflows/pages.yml) | Regenera y despliega las 131 páginas del sitio a GitHub Pages |
| 🔗 | [enlaces.yml](.github/workflows/enlaces.yml) | Comprueba en red las 120 fuentes y los 347 enlaces `doc:` de motores, en agenda propia para no teñir de rojo un `push` |
| 🛡️ | [codeql.yml](.github/workflows/codeql.yml) | Análisis estático de los generadores, que producen HTML y podrían inyectar |

Los mismos comprobadores se ejecutan en local antes de subir:

```bash
python scripts/validate_repository.py       # estructura, fuentes, motores, enlaces, codificación
python scripts/build_classes.py --check     # ¿quedaron README de clase sin regenerar?
python scripts/generate_site.py --check     # ¿quedó el sitio desactualizado?
python scripts/verificar_equivalencia.py    # SQLite y DuckDB, sin servicios
python -m pytest                            # 127 pruebas
npx markdownlint-cli2 "**/*.md"             # estilo de Markdown
```

## 🏗️ Cómo está construido

```text
curriculum.yaml     fuente única de verdad: partes, clases, horas, fuentes
catalog/            registro de fuentes y catálogo de motores
classes/            lesson.md (escrito a mano) → README.md (generado)
labs/               experimentos reproducibles
reference-data/     dominio, esquema y datos sintéticos
site/               sitio de GitHub Pages (generado)
rutas/              guías de carrera por rol
certificaciones/    mapeo de temarios oficiales y su cobertura
scripts/            generadores y validadores
tests/              pruebas de los generadores y del validador
docs/               arquitectura, metodología, seguridad y decisiones
assessments/        diagnóstico y rúbricas
projects/           casos integradores y proyecto final
```

> [!NOTE]
> Los `README.md` de clase y todo `site/` son **artefactos derivados**: se generan
> y la integración continua comprueba que no quedan desactualizados. La materia se
> edita en el `lesson.md` de cada clase.

```bash
python scripts/build_classes.py            # regenera los README de clase
python scripts/generate_site.py            # regenera el sitio, los iconos y el sitemap
python scripts/generar_certificaciones.py  # recalcula la cobertura de cada certificación
python scripts/generar_evaluacion.py       # regenera la rúbrica y el examen por rol
python scripts/brand_assets.py             # solo la marca gráfica (iconos y portada social)
python scripts/check_external_links.py     # comprueba las 120 fuentes
```

## 📏 Alcance de la cobertura de motores

Lo que el repositorio promete de cada motor, sin adornos:

- ✅ **Núcleo ejecutable** (SQLite, DuckDB): se ejecuta en cada `push`, sin
  servicios, en cualquier máquina.
- 🐳 **Servicio verificado** (PostgreSQL, MySQL, MongoDB, Redis, Neo4j): se ejecuta
  contra el contenedor real con el cliente oficial del propio motor.
- ⚪ **Declarado** (SQL Server, Oracle, Cassandra, ClickHouse, DynamoDB,
  OpenSearch, Qdrant y el resto del catálogo): el código y las fichas se
  escriben contra la documentación oficial y se revisan a mano. La máquina no
  los ejecuta, y ninguna clase dice lo contrario.

Aparecer en el catálogo no equivale a dominar la tecnología, y ejecutarse en CI
no equivale a haberlo operado en producción.

## 🧭 Qué es y qué no es este programa

| ✅ Lo que sí es | ❌ Lo que no es |
|---|---|
| Un currículo **secuencial y completo**, de «qué es un dato» a réplica, consenso y RAG | Un atajo: la numeración es secuencial por diseño y se nota al saltársela |
| Un programa donde **toda afirmación lleva fuente** con ISBN, DOI o norma | Una recopilación de blogs, foros o material generado por un modelo de lenguaje |
| **Comparación real entre motores**, con el mismo caso resuelto y verificado por máquina | Una tabla de folleto donde cada producto solo tiene ventajas |
| Práctica **reproducible**: siete laboratorios sin instalar nada, verificados en CI | Un curso de leer: sin evidencia ejecutada no hay nota |
| Un mapeo **honesto** a certificaciones, con el método y la brecha declarados | Un simulador de examen ni una promesa de aprobar |
| Material que declara **lo que no demuestra** en cada clase y laboratorio | Una afirmación de rendimiento en milisegundos sin condiciones |

## 👩‍🏫 Para instructores y documentación

| | Documento | Qué contiene |
|:---:|---|---|
| 🏗️ | **[Arquitectura del repositorio](docs/ARCHITECTURE.md)** | Qué es fuente y qué artefacto derivado, y por qué la separación importa |
| 🎓 | **[Modelo pedagógico](docs/LEARNING-MODEL.md)** | Cómo está construida cada clase y qué se exige para darla por superada |
| 📖 | **[Política de fuentes](docs/SOURCES.md)** | La regla que gobierna el repositorio y cómo se hace cumplir |
| ⚖️ | **[Guía de decisión](docs/DECISION-GUIDE.md)** | Cómo elegir motor y modelo a partir de la carga, no de la moda |
| 🐳 | **[Entornos reproducibles](docs/ENVIRONMENTS.md)** | Cómo levantar cada motor y volver al estado inicial sin residuos |
| 🔐 | **[Seguridad y ética](docs/SECURITY-AND-ETHICS.md)** | Datos sintéticos, credenciales locales y límites del material |
| 📊 | **[Rúbrica de evaluación](assessments/rubric.md)** | Diez dimensiones con sus cuatro niveles, aplicable por una tercera persona |
| 🎯 | **[Examen final por rol](assessments/examen-por-rol.md)** | Teoría, práctica y defensa para cada una de las siete rutas |

## 🤖 Uso con inteligencia artificial

[`PROMPT_MAESTRO.md`](PROMPT_MAESTRO.md) contiene el contrato para ampliar
clases, motores y laboratorios sin romper la coherencia ni la regla de las
fuentes. Es el documento que gana si una instrucción lo contradice: o se
cumple, o se cambia primero, pero no se salta en silencio.

## 💡 Idea fuerza

> El valor de este programa no está en enumerar motores, sino en **enseñar a
> decidir entre ellos con evidencia**: el mismo problema resuelto en varios,
> el porqué no de cada uno, fuentes que se pueden abrir y laboratorios que
> cualquiera puede volver a ejecutar para comprobar que lo dicho es cierto.

## 📄 Licencia

[MIT](LICENSE) — úsalo, modifícalo y compártelo. Los productos citados conservan
sus respectivas licencias y marcas.

---

<div align="center">

**Hecho para quien quiere entender las bases de datos por dentro, y poder defender sus decisiones.**

[▶️ Empezar por la primera clase](classes/part-00-primeros-pasos-del-archivo-a-la-base-de-datos/001-que-es-un-dato-un-registro-y-una-tabla/README.md) ·
[🧭 Elegir una ruta](rutas/README.md) ·
[🌐 Ir al sitio](https://vladimiracunadev-create.github.io/database-systems-labs/)

<br>

**¿Te resulta útil? ⭐ Dale una estrella al repositorio.**

[![Stars](https://img.shields.io/github/stars/vladimiracunadev-create/database-systems-labs?style=social)](https://github.com/vladimiracunadev-create/database-systems-labs/stargazers)
[![Forks](https://img.shields.io/github/forks/vladimiracunadev-create/database-systems-labs?style=social)](https://github.com/vladimiracunadev-create/database-systems-labs/network/members)
[![Follow](https://img.shields.io/github/followers/vladimiracunadev-create?style=social&label=Follow)](https://github.com/vladimiracunadev-create)

Hecho con 🧠 y ☕ por [Vladimir Acuña](https://github.com/vladimiracunadev-create)

</div>
