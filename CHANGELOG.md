# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## No publicado

Avance del hito 2.1: el núcleo ejecutable pasa de dos laboratorios a cinco, y
el validador deja de ser el único componente sin pruebas.

### Añadido

- **Laboratorio 03 ejecutable** (`labs/03-transactions/run_transactions_lab.py`):
  reproduce una actualización perdida con dos hilos reales sincronizados en una
  barrera, y la corrige con actualización atómica, control optimista por versión
  y bloqueo pesimista (`BEGIN IMMEDIATE`). La evidencia es el invariante —una
  plaza, una reserva—, no un tiempo.
- **Laboratorio 04 ejecutable** (`labs/04-indexing/run_indexing_lab.py`): 20 000
  filas deterministas, `EXPLAIN QUERY PLAN` y trabajo contado en instrucciones
  de la máquina virtual con `set_progress_handler`. Muestra el prefijo izquierdo
  de un índice compuesto, el recorrido por saltos (*skip-scan*) cuando hay
  estadísticas, y el costo en trabajo y páginas de mantener dos índices.
- **Laboratorio 05 ejecutable** (`labs/05-nosql-workloads/run_nosql_lab.py`):
  mide TTL frente a coherencia, incrustar frente a referenciar bajo carga de
  lectura y de escritura, el techo de un arreglo incrustado ante el límite de
  16 MiB por documento, y el reparto de una clave de partición caliente.
- **Pruebas** (`tests/`): 93 pruebas que ejecutan los laboratorios, comprueban
  que no importan dependencias externas, verifican la idempotencia de los
  generadores y su modo `--check`, y someten al validador a un repositorio roto
  a propósito —clase con una sola fuente, cita al vacío, fuente huérfana, libro
  sin ISBN, artículo sin DOI ni sede, motor fuera del catálogo, lección sin una
  sección obligatoria, lección demasiado corta, enlace relativo roto,
  codificación corrupta y archivo obligatorio ausente— exigiendo que lo detecte.
- `requirements-dev.txt` y `pytest.ini` para el entorno de desarrollo.
- Trabajo `pruebas` en integración continua, y los tres laboratorios nuevos en
  la matriz de Python 3.11, 3.12 y 3.13.
- **Sitio como producto**: barra de navegación y pie comunes a las 111 páginas,
  tema claro y oscuro con conmutador que recuerda la elección, progreso de
  lectura por clase guardado en el navegador, filtro «solo pendientes»,
  anterior/siguiente y migas en cada clase, barra de avance, copiar bloque de
  código, enlace para saltar al contenido y estilos de impresión.
- **Páginas nuevas**: [laboratorios](https://vladimiracunadev-create.github.io/database-systems-labs/laboratorios.html)
  (qué mide cada uno, cómo se ejecuta y de qué fuente sale su criterio),
  [autoevaluación](https://vladimiracunadev-create.github.io/database-systems-labs/autoevaluacion.html)
  con las 256 preguntas enlazadas a su clase, 17 páginas de documentación
  publicadas desde los `.md` del repositorio, y una página 404.
- **Aplicación instalable**: `manifest.webmanifest` y service worker con nombre
  de caché derivado de la huella del contenido, para que una versión nueva
  invalide la anterior sin recordar subir ningún número a mano.
- **Descubrimiento**: `sitemap.xml`, `robots.txt`, enlace canónico, etiquetas
  Open Graph y Twitter con portada social, y datos estructurados
  schema.org (`Course` en la portada, `LearningResource` en cada clase).
- **Marca gráfica generada** (`scripts/brand_assets.py`): iconos de 192 y 512 px
  y portada social de 1200×630, dibujados con `zlib` y `struct` de la biblioteca
  estándar —sin Pillow— y reproducibles byte a byte.
- **Laboratorios como datos**: sección `laboratorios` en `curriculum.yaml` con
  el comando, la marca de éxito, lo que mide y sus fuentes; el validador
  comprueba que el guion existe y que imprime de verdad la marca que declara.
- Análisis CodeQL semanal y en cada cambio, y Dependabot mensual para acciones y
  dependencias de Python.
- **Rutas por rol con guía de carrera** (`rutas/`): las cuatro rutas por objetivo pasan
  de una fila en una tabla a siete recorridos con guía completa —qué es el puesto, un día
  en el trabajo, qué necesitas saber, la ruta por partes con sus clases clave, qué tienes
  que poder demostrar, credenciales, progresión, mitos y siguientes pasos—. Se añaden
  Analytics engineer / BI, Ingeniero de IA aplicada y recuperación, y Gobierno y
  privacidad del dato, con lo que las 14 partes quedan cubiertas por alguna ruta.
- Las rutas viven como **datos** en `curriculum.yaml` (nivel, foco, partes, clases clave,
  laboratorios, cargos y fuentes) y el validador comprueba que todo lo que prometen
  existe, que la guía trae sus diez secciones y que **las horas que declara son las que
  suman sus partes**.
- Seis fuentes nuevas para sostener las afirmaciones de oficio y de mercado: el
  *Occupational Outlook Handbook* del U.S. Bureau of Labor Statistics, la *Stack Overflow
  Developer Survey 2025*, el *DB-Engines Ranking* y los temarios oficiales de DP-300,
  Google Professional Data Engineer y CDMP. Donde no hay fuente pública para el mercado
  local, las guías **no publican cifras**.
- Nueve páginas más en el sitio: índice de rutas, cómo elegir y una por rol, con datos
  estructurados de itinerario y las fuentes enlazadas a su ficha.
- Pruebas de coherencia del README: la tabla del programa, la de rutas y las cifras de las
  insignias se comprueban contra `curriculum.yaml` y contra el propio repositorio.

### Cambiado

- `scripts/validate_repository.py` exige la presencia de los cinco laboratorios
  ejecutables, valida la sección `laboratorios` y cuenta también sus citas al
  buscar fuentes huérfanas.
- `labs/README.md` declara qué mide cada laboratorio y por qué ninguno afirma
  nada en milisegundos.
- `scripts/generate_site.py` pasa de 82 a 111 páginas y admite artefactos
  binarios, con `--check` byte a byte también para los iconos.
- Los README de clase pierden la tabla de metadatos y las cifras del README raíz dejan de
  duplicar las insignias; la ficha de clase pasa a una línea corrida.
- El bloque «Laboratorio» de cada clase publica el comando real del laboratorio: antes
  anunciaba un `run_lab.py` que solo existe en el primero.
- Corregidas las horas de las partes 08 y 09 en la tabla del README, que declaraban 19 y
  suman 17.
- El sistema visual se reescribe sobre variables CSS: un solo bloque de tokens
  define color y ritmo, y de ahí sale el tema claro sin excepciones.
- El flujo de Pages vigila todas las entradas del generador; antes ignoraba
  `docs/`, `assessments/`, `projects/` y los documentos de la raíz, así que un
  cambio en ellos no llegaba a publicarse.

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
