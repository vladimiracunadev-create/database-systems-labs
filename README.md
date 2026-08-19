# Database Systems Labs

[![validación](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/ci.yml/badge.svg)](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/ci.yml)
[![sitio](https://github.com/vladimiracunadev-create/database-systems-labs/actions/workflows/pages.yml/badge.svg)](https://vladimiracunadev-create.github.io/database-systems-labs/)
[![licencia MIT](https://img.shields.io/badge/licencia-MIT-2ee6c5)](LICENSE)

Programa de ingeniería de bases de datos que va del modelado conceptual a la
arquitectura distribuida, la operación y los sistemas de recuperación para
inteligencia artificial.

**🌐 [Ver el programa completo](https://vladimiracunadev-create.github.io/database-systems-labs/)**
· **[Empezar por la clase 001](classes/part-00-fundamentos-datos-sistemas-y-metodo/001-que-resuelve-un-sistema-de-bases-de-datos/README.md)**
· **[Bibliografía](catalog/sources.json)**

| | |
|---|---|
| **Partes** | 14 |
| **Clases** | 64 |
| **Horas estimadas** | 210 |
| **Fuentes verificadas** | 109 |
| **Motores en catálogo** | 27 |

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

### Laboratorios con contenedores

Los motores llegan por perfiles, para no levantarlos todos a la vez:

```bash
docker compose --profile relational up -d
```

Las credenciales del `compose` son locales y están a la vista en un archivo
versionado. **Nunca deben copiarse a otro entorno.**

## Cómo está construido

```text
curriculum.yaml     fuente única de verdad: partes, clases, horas, fuentes
catalog/            registro de fuentes y catálogo de motores
classes/            lesson.md (escrito a mano) → README.md (generado)
labs/               experimentos reproducibles
reference-data/     dominio, esquema y datos sintéticos
site/               sitio de GitHub Pages (generado)
scripts/            generadores y validadores
docs/               arquitectura, metodología, seguridad y decisiones
assessments/        diagnóstico y rúbricas
projects/           casos integradores y proyecto final
```

Los `README.md` de clase y todo `site/` son **artefactos derivados**: se generan
y la integración continua comprueba que no quedan desactualizados. La materia se
edita en el `lesson.md` de cada clase.

```bash
python scripts/build_classes.py          # regenera los README de clase
python scripts/generate_site.py          # regenera el sitio
python scripts/check_external_links.py   # comprueba las 109 fuentes
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
