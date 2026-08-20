<div align="center">

<img src="site/assets/icon.svg" alt="" width="96" height="96">

# 🗄️ Database Systems Labs

## **14 partes · 64 clases · 210 horas · 109 fuentes verificables**

**Programa abierto de ingeniería de bases de datos, del modelado conceptual a la
arquitectura distribuida, la operación y los sistemas de recuperación para
inteligencia artificial. Ninguna clase se publica sin fuentes, y ninguna cita
apunta al vacío: lo comprueba la integración continua en cada `push`.**

[![Validación](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/ci.yml)
[![Sitio](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/pages.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/pages.yml)
[![Enlaces](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/enlaces.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/enlaces.yml)
[![CodeQL](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/codeql.yml)

[![Versión](https://img.shields.io/badge/versión-2.0.0-orange?style=for-the-badge)](CHANGELOG.md)
[![Clases](https://img.shields.io/badge/clases-64%20·%2014%20partes-4aa8ff?style=for-the-badge)](classes/README.md)
[![Fuentes](https://img.shields.io/badge/fuentes-109%20con%20ISBN%20·%20DOI%20·%20norma-0b7285?style=for-the-badge)](catalog/sources.json)
[![Laboratorios](https://img.shields.io/badge/laboratorios-5%20ejecutables%20en%20CI-2ee6c5?style=for-the-badge)](labs/README.md)
[![Licencia](https://img.shields.io/badge/licencia-MIT-3fb950?style=for-the-badge)](LICENSE)

[![Python](https://img.shields.io/badge/Python-3.11%20·%203.12%20·%203.13-3776AB?style=flat-square&logo=python&logoColor=white)](requirements.txt)
[![Sin dependencias](https://img.shields.io/badge/laboratorios-solo%20stdlib-0ea5e9?style=flat-square)](labs/README.md)
[![Pruebas](https://img.shields.io/badge/pruebas-74%20pytest-8957e5?style=flat-square&logo=pytest&logoColor=white)](tests/)
[![Motores](https://img.shields.io/badge/motores-27%20en%20catálogo-ffc861?style=flat-square&logo=postgresql&logoColor=white)](catalog/databases.json)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-sitio%20vivo-222?style=flat-square&logo=githubpages&logoColor=white)](https://vladimiracunadev-create.github.io/database-systems-labs/)

[🌐 **Sitio de estudio**](https://vladimiracunadev-create.github.io/database-systems-labs/) ·
[▶️ **Empezar por la clase 001**](classes/part-00-fundamentos-datos-sistemas-y-metodo/001-que-resuelve-un-sistema-de-bases-de-datos/README.md) ·
[🧪 **Laboratorios**](https://vladimiracunadev-create.github.io/database-systems-labs/laboratorios.html) ·
[📝 **Autoevaluación**](https://vladimiracunadev-create.github.io/database-systems-labs/autoevaluacion.html) ·
[📚 **Bibliografía**](https://vladimiracunadev-create.github.io/database-systems-labs/fuentes.html) ·
[🗺️ **Roadmap**](ROADMAP.md)

</div>

## La regla del repositorio

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

## Modelo pedagógico

Cada clase sigue la misma estructura, y la validación comprueba que están todas
las secciones:

| Sección | Qué aporta |
|---|---|
| Propósito | Qué problema resuelve la clase |
| Resultados de aprendizaje | Cinco capacidades comprobables |
| Fundamentos | El mecanismo, no la receta |
| **Ejemplo trabajado** | Números y código reales, con su traza |
| Comparación | Tabla de decisiones con sus costos |
| Errores frecuentes | El error, su causa y su corrección |
| De la clase a la operación | Qué cambia cuando el sistema es real |
| Reto de transferencia | Aplicarlo al propio contexto |
| Preguntas de evaluación | Cuatro preguntas que exigen explicar |

A eso el generador añade el laboratorio, la rúbrica y la bibliografía de la
clase. El criterio de aprobación es explícito: **un resultado correcto sin
explicación no demuestra transferencia**.

## Programa

| Parte | Tema | Clases | Horas |
|---|---|---:|---:|
| [00](classes/part-00-fundamentos-datos-sistemas-y-metodo/README.md) | Fundamentos, sistemas y método | 4 | 12 |
| [01](classes/part-01-modelado-conceptual-y-requisitos/README.md) | Modelado conceptual y requisitos | 5 | 16 |
| [02](classes/part-02-modelo-relacional-y-algebra/README.md) | Modelo relacional y álgebra | 4 | 13 |
| [03](classes/part-03-sql-en-profundidad/README.md) | SQL en profundidad | 6 | 20 |
| [04](classes/part-04-motores-relacionales-y-dialectos/README.md) | Motores relacionales y dialectos | 4 | 12 |
| [05](classes/part-05-documentos-y-clave-valor/README.md) | Documentos y clave-valor | 4 | 13 |
| [06](classes/part-06-grafos-columnas-tiempo-y-busqueda/README.md) | Grafos, columnas, tiempo y búsqueda | 5 | 15 |
| [07](classes/part-07-transacciones-concurrencia-y-recuperacion/README.md) | Transacciones, concurrencia y recuperación | 5 | 18 |
| [08](classes/part-08-almacenamiento-indices-y-planes/README.md) | Almacenamiento, índices y planes | 5 | 19 |
| [09](classes/part-09-distribucion-replica-y-consistencia/README.md) | Distribución, réplica y consistencia | 5 | 19 |
| [10](classes/part-10-operacion-seguridad-y-gobierno/README.md) | Operación, seguridad y gobierno | 6 | 19 |
| [11](classes/part-11-analitica-integracion-y-streaming/README.md) | Analítica, integración y streaming | 4 | 13 |
| [12](classes/part-12-vectores-recuperacion-y-rag/README.md) | Vectores, recuperación y RAG | 4 | 13 |
| [13](classes/part-13-arquitectura-y-proyecto-final/README.md) | Arquitectura y proyecto final | 3 | 12 |

El índice completo está en [`classes/README.md`](classes/README.md) y el
currículo canónico, en [`curriculum.yaml`](curriculum.yaml).

### Rutas por objetivo

| Ruta | Partes |
|---|---|
| Desarrollador de aplicaciones | 00 · 01 · 02 · 03 · 04 · 05 · 07 · 08 · 10 · 13 |
| Ingeniero de datos | 00 · 01 · 02 · 03 · 06 · 09 · 11 · 12 · 13 |
| DBA / SRE de datos | 00 · 01 · 03 · 04 · 07 · 08 · 09 · 10 · 13 |
| Arquitecto de datos | todas |

## Empezar

Requiere Python 3.11 o superior. Sin instalar ningún servidor:

```bash
python scripts/validate_repository.py
python labs/01-sql-foundations/run_lab.py
```

El laboratorio base usa SQLite en memoria: carga el dominio educativo canónico,
ejecuta consultas y comprueba invariantes. Si falla, el problema está en el
código, no en el entorno.

Cinco de los seis laboratorios se ejecutan igual, sin dependencias y sin
servidores, y los cinco corren en integración continua sobre Python 3.11, 3.12
y 3.13:

```bash
python labs/03-transactions/run_transactions_lab.py   # reproduce una actualización perdida y la corrige de tres formas
python labs/04-indexing/run_indexing_lab.py           # plan y trabajo antes y después del índice
python labs/05-nosql-workloads/run_nosql_lab.py       # TTL, incrustar o referenciar, y clave de partición caliente
python labs/06-vector-search/run_vector_lab.py        # similitud coseno y recall@k
```

Ninguno afirma nada en milisegundos: un tiempo depende de la máquina. Lo que
afirman son invariantes, planes de ejecución, accesos y bytes. El detalle está
en [`labs/README.md`](labs/README.md).

Para trabajar sobre el repositorio (generadores, validador y sus pruebas):

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

### Laboratorios con contenedores

Los motores llegan por perfiles, para no levantarlos todos a la vez:

```bash
docker compose --profile relational up -d
```

Las credenciales del `compose` son locales y están a la vista en un archivo
versionado. **Nunca deben copiarse a otro entorno.**

## El sitio

[**vladimiracunadev-create.github.io/database-systems-labs**](https://vladimiracunadev-create.github.io/database-systems-labs/)
— 102 páginas generadas desde este mismo repositorio, sin analítica y sin cuentas:

| | |
|---|---|
| **Catálogo** | las 64 clases con búsqueda en el cliente y filtros por parte, nivel y motor |
| **Clase** | lectura larga con barra de avance, anterior/siguiente, diagramas Mermaid y copiar bloque de código |
| **[Laboratorios](https://vladimiracunadev-create.github.io/database-systems-labs/laboratorios.html)** | qué mide cada uno, cómo se ejecuta y de qué fuente sale su criterio |
| **[Autoevaluación](https://vladimiracunadev-create.github.io/database-systems-labs/autoevaluacion.html)** | las 256 preguntas del programa, enlazadas a su clase |
| **[Fuentes](https://vladimiracunadev-create.github.io/database-systems-labs/fuentes.html)** | las 109 entradas con ISBN, DOI o URL oficial y quién las cita |
| **[Documentación](https://vladimiracunadev-create.github.io/database-systems-labs/docs/index.html)** | arquitectura, método, rúbrica, entornos y roadmap, publicados desde sus `.md` |
| **Progreso** | marcar clases como completadas; se guarda solo en tu navegador |
| **Tema** | claro y oscuro, siguiendo la preferencia del sistema o tu elección |
| **Sin conexión** | aplicación instalable (PWA) con service worker y manifiesto |

Los iconos y la portada social también son artefactos generados: se dibujan
píxel a píxel con `zlib` y `struct` en
[`scripts/brand_assets.py`](scripts/brand_assets.py), sin Pillow ni ninguna otra
dependencia, para que cualquiera pueda reproducirlos byte a byte.

## Cómo está construido

```text
curriculum.yaml     fuente única de verdad: partes, clases, horas, fuentes
catalog/            registro de fuentes y catálogo de motores
classes/            lesson.md (escrito a mano) → README.md (generado)
labs/               experimentos reproducibles
reference-data/     dominio, esquema y datos sintéticos
site/               sitio de GitHub Pages (generado)
scripts/            generadores y validadores
tests/              pruebas de los generadores y del validador
docs/               arquitectura, metodología, seguridad y decisiones
assessments/        diagnóstico y rúbricas
projects/           casos integradores y proyecto final
```

Los `README.md` de clase y todo `site/` son **artefactos derivados**: se generan
y la integración continua comprueba que no quedan desactualizados. La materia se
edita en el `lesson.md` de cada clase.

```bash
python scripts/build_classes.py          # regenera los README de clase
python scripts/generate_site.py          # regenera el sitio, los iconos y el sitemap
python scripts/brand_assets.py           # solo la marca gráfica (iconos y portada social)
python scripts/check_external_links.py   # comprueba las 109 fuentes
python -m pytest                         # 74 pruebas: laboratorios, generadores, validador y sitio
```

## Alcance de la cobertura de motores

Tres capas, declaradas para no prometer de más:

- **Núcleo ejecutable:** motores con laboratorios completos.
- **Fichas comparativas:** tecnologías relevantes con su documentación oficial.
- **Catálogo extensible:** registro que permite incorporar motores nuevos.

Aparecer en el catálogo no equivale a dominar la tecnología.

## Uso con inteligencia artificial

[`PROMPT_MAESTRO.md`](PROMPT_MAESTRO.md) contiene el contrato para ampliar
clases, motores y laboratorios sin romper la coherencia ni la regla de las
fuentes.

## Licencia

MIT. Los productos citados conservan sus respectivas licencias y marcas.
