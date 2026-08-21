# Arquitectura del repositorio

## Principio

Una sola fuente de verdad por cada cosa, y todo lo demás generado a partir de
ella. La alternativa —mantener a mano el currículo, los índices, los README y el
sitio— produce la incoherencia clásica: el índice dice 60 clases, el README dice
58 y el sitio publica 55.

```mermaid
flowchart TD
    CY["curriculum.yaml<br/>partes · clases · horas · fuentes"] --> BC["scripts/build_classes.py"]
    LM["classes/**/lesson.md<br/>la materia, escrita a mano"] --> BC
    MY["classes/**/motores.yaml<br/>el caso y la matriz de motores"] --> BC
    IM["classes/**/implementaciones/<br/>el código real, uno por motor"] --> BC
    SJ["catalog/sources.json<br/>120 fuentes"] --> BC
    BC --> CR["classes/**/README.md<br/>+ índices de parte<br/>(generados)"]

    MY --> VE["scripts/verificar_equivalencia.py"]
    IM --> VE
    VE --> MO{"¿todos los motores<br/>dan la misma respuesta?"}

    CY --> GS["scripts/generate_site.py"]
    CR --> GS
    SJ --> GS
    DJ["catalog/databases.json<br/>27 motores"] --> GS
    GS --> ST["site/<br/>una página por clase + busqueda.json<br/>(generado)"]

    CY --> VR["scripts/validate_repository.py"]
    SJ --> VR
    DJ --> VR
    LM --> VR
    MY --> VR
    RD["reference-data/"] --> VR
    VR --> OK{"¿main en verde?"}
```

## Qué es fuente y qué es artefacto

| Ruta | Naturaleza | Se edita a mano |
|---|---|---|
| `curriculum.yaml` | Fuente | **Sí** |
| `classes/**/lesson.md` | Fuente | **Sí** |
| `classes/**/motores.yaml` | Fuente | **Sí** |
| `classes/**/implementaciones/**` | Fuente | **Sí** |
| `catalog/*.json` | Fuente | **Sí** |
| `labs/`, `reference-data/`, `docs/` | Fuente | **Sí** |
| `classes/**/README.md` | Artefacto | No |
| `classes/README.md` y `classes/part-*/README.md` | Artefacto | No |
| `site/**` | Artefacto | No |

La integración continua ejecuta los generadores con `--check` y falla si algún
artefacto quedó desactualizado. Es lo que impide que el sitio publicado y el
repositorio digan cosas distintas.

## Los componentes

### `curriculum.yaml`

Metadatos de las 74 clases: identificador, `slug`, título, horas, nivel,
conceptos, motores, laboratorio y **fuentes**. También las rutas por objetivo y
los pesos de evaluación. Nada de lo que aquí se declara se repite en otro sitio.

### `catalog/sources.json`

Registro único de la bibliografía. Cada entrada lleva tipo, autoría, año, URL y
una nota que explica para qué sirve en este programa; los libros llevan ISBN y
los artículos, DOI o sede. Ver [la política de fuentes](SOURCES.md).

### `catalog/databases.json`

Los motores cubiertos, con su familia, lenguaje de consulta, documentación
oficial y si tienen laboratorio ejecutable (`core_lab`) o solo ficha
comparativa. La distinción evita prometer dominio de tecnologías que solo se
mencionan.

### `classes/`

Una carpeta por clase con cuatro cosas, y solo la última es artefacto:

| Archivo | Qué es |
|---|---|
| `lesson.md` | La materia, escrita a mano |
| `motores.yaml` | El **caso** con su salida esperada y la **matriz de motores**, con el porqué sí y el porqué no de cada uno |
| `implementaciones/<motor>/` | El código real que resuelve el caso en ese motor |
| `README.md` | El documento publicable, **generado** a partir de los tres anteriores |

La separación permite que las 74 clases compartan encabezado, rúbrica y formato
de bibliografía sin 74 copias que mantener, y que el código de cada motor viva
en un archivo que se puede ejecutar tal cual, no dentro de un bloque de
Markdown.

### `scripts/verificar_equivalencia.py`

El componente que sostiene la afirmación central del programa: **el mismo
problema, resuelto en varios motores, da la misma respuesta**. Ejecuta cada
implementación contra su motor y compara el resultado con el contrato de la
clase. Tres niveles, declarados siempre:

| Nivel | Motores | Dónde corre |
|---|---|---|
| `nucleo` | SQLite, DuckDB | En cualquier máquina y en todos los trabajos de CI |
| `servicio` | PostgreSQL, MySQL, MongoDB, Redis, Neo4j | Contra el contenedor real, con el cliente oficial de cada motor |
| `declarado` | El resto del catálogo | No se ejecuta, y así se dice |

Cada clase corre en su **propio espacio de nombres** —un esquema en PostgreSQL,
una base en MySQL, una base en MongoDB—, porque sin ese aislamiento las tablas
de una clase impiden borrar las de otra y el verificador acabaría midiendo la
basura que dejó la anterior.

### `labs/`

Experimentos reproducibles. El primero usa SQLite en memoria y no depende de
nada externo; el resto llega por perfiles de `docker-compose.yml`.

### `reference-data/`

El dominio educativo canónico —estudiantes, cursos, inscripciones— que usan
todas las clases. Que el dominio sea el mismo en las 74 clases es lo que permite
comparar motores sin cambiar de problema.

### `site/`

Sitio estático de GitHub Pages: portada con búsqueda y filtros, una página por
clase con diagramas Mermaid, índices por parte, bibliografía renderizada y
catálogo de motores.

## Controles de integridad

| Control | Qué impide |
|---|---|
| Mínimo de dos fuentes por clase | Material sin respaldo |
| Citas existentes en el registro | Bibliografía fantasma |
| Sin fuentes huérfanas | Registro que envejece sin revisar |
| ISBN en libros, DOI o sede en artículos | Citas no localizables |
| Motores citados presentes en el catálogo | Prometer cobertura inexistente |
| Secuencia 001..074 sin huecos | Clases perdidas al reordenar |
| Todo motor con su `porque_no` | Comparativas de folleto, con solo ventajas |
| Todo motor con su `doc:` en el dominio oficial | Afirmaciones sobre un motor sin respaldo |
| Implementación declarada que existe en disco | Código prometido y ausente |
| Resultado idéntico entre motores | «Es equivalente» dicho sin comprobarlo |
| Secciones obligatorias en cada lección | Notas disfrazadas de clase |
| Enlaces relativos resueltos | Navegación rota |
| Codificación UTF-8 sin mojibake | Acentos corrompidos al editar |
| Integridad del conjunto de referencia | Laboratorios sobre datos inconsistentes |
| Artefactos regenerados | Sitio y repositorio en desacuerdo |

## Decisiones y su motivo

- **`lesson.md` separado de `README.md`.** Cambiar la rúbrica o el pie de página
  es un cambio en el generador, no 74 ediciones.
- **El código de cada motor en su propio archivo, no en el Markdown.** Un bloque
  de código dentro de una clase no se puede ejecutar; un archivo, sí. El
  generador lo inserta en el README, así que lo que se lee es exactamente lo que
  la máquina ejecutó.
- **`porque_no` obligatorio.** Es la regla que impide que la comparación degenere
  en una lista de ventajas. Si de un motor no se sabe decir qué se paga por
  usarlo, no se ha entendido lo suficiente como para recomendarlo.
- **Las fuentes en JSON y no en Markdown.** Permite validar la estructura y
  renderizarlas en varios sitios sin duplicarlas.
- **El sitio versionado en el repositorio.** Se puede revisar el diff de lo que
  se publica, y GitHub Pages no necesita construir nada.
- **Los `slug` en ASCII.** Son rutas de carpeta y de URL; los acentos ahí causan
  problemas entre sistemas de archivos.
- **La validación falla, no avisa.** Un aviso que nadie lee es una regla que no
  existe.
