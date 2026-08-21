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
- **Pruebas** (`tests/`): 127 pruebas que ejecutan los laboratorios, comprueban
  que no importan dependencias externas, verifican la idempotencia de los
  generadores y su modo `--check`, y someten al validador a un repositorio roto
  a propósito —clase con una sola fuente, cita al vacío, fuente huérfana, libro
  sin ISBN, artículo sin DOI ni sede, motor fuera del catálogo, lección sin una
  sección obligatoria, lección demasiado corta, enlace relativo roto,
  codificación corrupta y archivo obligatorio ausente— exigiendo que lo detecte.
- `requirements-dev.txt` y `pytest.ini` para el entorno de desarrollo.
- Trabajo `pruebas` en integración continua, y los tres laboratorios nuevos en
  la matriz de Python 3.11, 3.12 y 3.13.
- **Sitio como producto**: barra de navegación y pie comunes a las 120 páginas,
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
- **Laboratorio 07 ejecutable** (`labs/07-replication/run_replication_lab.py`): un líder y dos
  seguidores con retraso declarado. Cuenta las lecturas que no ven la escritura propia del
  cliente y las no monótonas al repartir entre réplicas, y aplica las tres correcciones —leer
  del líder, esperar la posición propia, exigir quórum— midiendo lo que cuesta cada una.
- **Laboratorio 08 ejecutable** (`labs/08-recovery/run_recovery_lab.py`): respalda una base real
  con la API del motor, archiva cada transacción, provoca un borrado sin filtro y compara tres
  recuperaciones. Solo la restauración a un punto en el tiempo devuelve el estado bueno, y se
  demuestra comparando el contenido, no mirándolo por encima.
- **Guías de laboratorio completas**: las ocho pasan de una página de instrucciones a una guía
  con qué demuestra, hipótesis que predecir antes de ejecutar, la salida real, por qué el
  experimento está hecho así, **lo que no demuestra**, extensiones, cómo llevarlo a un motor
  real, y las clases, rutas y certificaciones donde encaja.
- **Certificaciones** (`certificaciones/`): mapeo del temario oficial de DP-300, DP-900 y AWS
  Data Engineer Associate contra las clases del programa, con la cobertura calculada desde los
  pesos que publica cada proveedor. Dos métodos declarados —medición por subáreas oficiales y
  estimación por dominio— y la brecha explicada en cada ficha.
- Google Professional Data Engineer, CDMP y las credenciales de Oracle se listan **sin
  porcentaje**, con el motivo: su ponderación no está disponible en una fuente verificable, y
  este repositorio no publica un número que no pueda comprobar.
- `scripts/generar_certificaciones.py` calcula la cobertura y genera las fichas, con `--check`
  en integración continua como el resto de los generadores.
- **Evaluación como datos**: la rúbrica del proyecto final pasa a `curriculum.yaml` con diez
  dimensiones, sus **cuatro niveles descritos**, el mínimo exigido por dimensión, la evidencia
  que hay que ver y las clases y laboratorios donde se aprende. Se genera con
  `scripts/generar_evaluacion.py`, así que no puede contradecir al programa.
- **Examen final por rol** (`assessments/examen-por-rol.md`): teoría, práctica y defensa para
  cada una de las siete rutas, con sus laboratorios y clases clave, generado desde el currículo.
- **Diagnóstico inicial con clave de corrección**: qué menciona una respuesta sólida, qué es
  señal de alarma, y a qué parte o ruta te encamina cada resultado.
- **[Evidencias de laboratorio](assessments/evidencias.md)**: qué cuenta como evidencia
  —hipótesis previa, comando, entorno, salida completa y **límite declarado**—, con plantilla,
  la afirmación que debe sostener cada uno de los ocho laboratorios y el criterio de corrección.
- **Proyectos**: el proyecto final pasa de nueve viñetas a nueve fases con su entregable y su
  dimensión de rúbrica, las siete preguntas de la defensa, la estructura de entrega y la lista
  de comprobación previa. Los cinco dominios canónicos declaran ahora su invariante, su patrón
  de acceso, su dato sensible y **la forma concreta en que cada uno rompe**.
- **[Portafolio verificable](projects/portafolio.md)**: cómo convertir la evidencia acumulada en
  algo que se enseñe, qué llevar a una entrevista según el puesto y qué **no** es un portafolio.
- Seis páginas más en el sitio: cómo se evalúa, rúbrica, examen por rol, evidencias, proyectos y
  portafolio.

### Cambiado

- `scripts/validate_repository.py` exige la presencia de los cinco laboratorios
  ejecutables, valida la sección `laboratorios` y cuenta también sus citas al
  buscar fuentes huérfanas.
- `labs/README.md` declara qué mide cada laboratorio y por qué ninguno afirma
  nada en milisegundos.
- `scripts/generate_site.py` pasa de 82 a 120 páginas y admite artefactos
  binarios, con `--check` byte a byte también para los iconos.
- Los README de clase pierden la tabla de metadatos y las cifras del README raíz dejan de
  duplicar las insignias; la ficha de clase pasa a una línea corrida.
- El bloque «Laboratorio» de cada clase publica el comando real del laboratorio: antes
  anunciaba un `run_lab.py` que solo existe en el primero.
- Corregidas las horas de las partes 08 y 09 en la tabla del README, que declaraban 19 y
  suman 17.
- El sistema visual se reescribe sobre variables CSS: un solo bloque de tokens
  define color y ritmo, y de ahí sale el tema claro sin excepciones.
- Las clases de réplica (043, 046) y de respaldo (048) pasan a apuntar a su laboratorio propio
  en vez de a uno prestado.
- El flujo de Pages vigila todas las entradas del generador; antes ignoraba
  `docs/`, `assessments/`, `projects/` y los documentos de la raíz, así que un
  cambio en ellos no llegaba a publicarse.

## 3.0.0 — 2026-08-20

El repositorio cambia de modelo. Hasta aquí una clase explicaba un concepto y
citaba motores de pasada; a partir de aquí **declara un caso, lo resuelve en
varios motores y escribe, con el mismo peso, por qué sí y por qué no conviene
resolverlo en cada uno**. Los motores que *no* resuelven el caso aparecen
también, con el motivo y con lo que se hace en su lugar.

### Añadido

- **Eje comparado en las 74 clases.** Cada una trae su `motores.yaml` —el caso,
  la salida esperada y la matriz de motores— y su carpeta `implementaciones/`
  con el código real de cada uno. **408 implementaciones**, de las que **267 se
  ejecutan contra el motor real** y el resto se declaran como material revisado
  y no ejecutado.
- **`scripts/verificar_equivalencia.py`.** Ejecuta cada implementación y compara
  su resultado con el contrato de su clase. Tres niveles declarados: *núcleo*
  (SQLite y DuckDB, sin servicios, en cualquier máquina), *servicio*
  (PostgreSQL, MySQL, MongoDB, Redis y Neo4j contra el contenedor real, con el
  cliente oficial de cada uno) y *declarado* (se muestra y se revisa; la máquina
  no lo ejecuta).
- **`scripts/motores_lib.py`.** Carga y valida las comparaciones. Exige
  `porque_no` en todo motor —un motor que solo tiene ventajas no se entendió, se
  copió del folleto— y exige que el enlace `doc:` cuelgue del dominio oficial que
  registra `catalog/databases.json`.
- **Parte 00 nueva, la rampa de entrada.** Diez clases para quien nunca ha
  escrito una consulta: qué es un dato, por qué la hoja de cálculo deja de
  servir, crear/insertar/leer, filtrar y ordenar, cambiar datos y el `WHERE` que
  salva, tipos, clave primaria, dos tablas y una clave foránea, cuándo **no**
  hace falta una base de datos, y el mapa de las seis familias de motores.
- **Trabajo de CI `equivalencia`.** Levanta los cinco motores de servicio con
  `docker compose --profile todo up -d --wait` y ejecuta todas las
  implementaciones contra ellos.
- **Servicio `neo4j`** en `docker-compose.yml`, y perfil `todo` para levantar los
  cinco de una vez.
- **El verificador de enlaces cubre los dos registros:** las fuentes
  bibliográficas y ahora también los `doc:` de cada motor —347 enlaces—, con
  `--solo motores` para comprobar solo estos.

### Cambiado

- **Renumeración.** Partes 00–13 pasan a 01–14 y clases 001–064 pasan a 011–074,
  para dejar sitio a la parte 00. Las referencias por identificador se
  reescribieron en los dos únicos sitios donde viven —`curriculum.yaml` y
  `certificaciones/_mapeo.json`—, más las rutas de enlace de los `.md`.
- **La parte 00 entra en las siete rutas por rol** como rampa común, y las horas
  declaradas en cada guía se actualizaron en consecuencia.
- **`scripts/build_classes.py`** renderiza la sección comparada en cada README, y
  escapa la barra vertical en las celdas de tabla —que aparece de verdad en
  cuanto se habla del operador de concatenación.
- **Dos pruebas de coherencia dejan de escribir cifras a mano:** la que exigía la
  parte «13» como cierre lee ahora la primera y la última del currículo, y la que
  fijaba 210 horas comprueba que la portada dice las que el currículo suma.

### Corregido

- **`docker-compose.yml`: el volumen de PostgreSQL 18** se montaba en
  `/var/lib/postgresql/data` y el contenedor **nunca llegaba a estar sano**. La
  imagen 18 coloca los datos en un subdirectorio con la versión dentro, así que
  el punto de montaje es `/var/lib/postgresql`.
- **Puertos configurables** por variable de entorno, para poder levantar el stack
  en una máquina que ya tenga un PostgreSQL o un MySQL escuchando.
- **`scripts/generate_site.py`:** los enlaces a `motores.yaml` y a
  `implementaciones/` apuntan al archivo en GitHub en vez de morir en el sitio.
- **Tres enlaces de documentación oficial rotos** (DuckDB y dos de Cassandra),
  detectados por el verificador de enlaces en su primera ejecución sobre el
  registro de motores.

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
