# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## 2.0.0 — 2026-08-19

Reescritura del programa en torno a una regla: **ninguna clase se publica sin
fuentes, y ninguna cita apunta al vacío**.

### Añadido

- **Registro de fuentes** (`catalog/sources.json`): 109 entradas —27 libros,
  36 artículos, 9 normas y 37 documentaciones oficiales— con autoría, año, URL,
  ISBN o DOI y una nota que explica su papel en el programa.
- **64 clases** repartidas en 14 partes y 210 horas, cada una con propósito,
  resultados de aprendizaje, fundamentos, ejemplo trabajado con números o código
  reales, tabla comparativa, diagrama, errores frecuentes, paso a la operación,
  reto de transferencia y preguntas de evaluación.
- **`curriculum.yaml`** como fuente única de verdad: partes, clases, horas,
  niveles, conceptos, motores, laboratorios, fuentes, rutas y evaluación.
- **Sitio de GitHub Pages** (`site/`): 82 páginas con búsqueda en el cliente,
  filtros por parte, nivel y motor, diagramas Mermaid, bibliografía renderizada
  y catálogo de motores.
- **Generadores**: `scripts/build_classes.py` y `scripts/generate_site.py`,
  ambos con modo `--check` para detectar artefactos desactualizados.
- **Verificador de enlaces** (`scripts/check_external_links.py`) que distingue
  enlace roto de enlace protegido contra clientes automáticos.
- **Integración continua** en cuatro trabajos: estructura y fuentes, artefactos
  regenerados, lint de Markdown y laboratorios sobre Python 3.11, 3.12 y 3.13.
- Comprobación semanal del estado de las 109 fuentes.
- Apache Kafka en el catálogo de motores.

### Cambiado

- **`scripts/validate_repository.py`** pasa de comprobar la existencia de unos
  archivos a hacer cumplir el contrato completo: mínimo de fuentes por clase,
  citas existentes, ausencia de fuentes huérfanas, ISBN en libros y DOI o sede
  en artículos, motores presentes en el catálogo, secuencia de clases sin
  huecos, secciones obligatorias en cada lección, enlaces relativos resueltos y
  codificación UTF-8 sin mojibake.
- `docs/SOURCES.md` deja de ser un listado y pasa a ser la política de citación;
  el listado vive solo en el registro.
- `PROMPT_MAESTRO.md` y `docs/ARCHITECTURE.md` reescritos alrededor de la
  separación entre fuentes y artefactos derivados.
- El README raíz declara las cifras del programa y cómo se verifican.

### Eliminado

- `curriculum/` (13 archivos Markdown): sustituido por `curriculum.yaml` más las
  64 clases. Mantener ambos garantizaba que acabaran contradiciéndose.

## 0.1.0 — 2026-08-19

- estructura inicial del programa;
- prompt maestro interno;
- doce módulos progresivos;
- catálogo extensible de sistemas de datos;
- dominio educativo y laboratorio SQLite ejecutable;
- perfiles de contenedores para laboratorios;
- evaluaciones, proyectos y plantillas.
