# Roadmap

Los hitos no fijan versiones de productos. Cada incorporación verifica soporte y
documentación oficial en la fecha de implementación, y añade sus fuentes al
registro antes de escribir una sola línea de clase.

## 2.0 — Programa con fuentes verificables *(actual)*

- 14 partes, 64 clases, 210 horas.
- Registro de 109 fuentes con ISBN, DOI o URL oficial.
- Validación que bloquea cualquier clase sin respaldo bibliográfico.
- Sitio de GitHub Pages generado, con búsqueda y filtros.
- Integración continua sobre Python 3.11, 3.12 y 3.13.

## 2.1 — Laboratorios ejecutables por parte

El núcleo ejecutable pasó de dos laboratorios a cinco: todos sin dependencias
externas y comprobados en integración continua sobre Python 3.11, 3.12 y 3.13.

Hecho:

- actualización perdida reproducida con hilos reales y corregida con
  actualización atómica, control optimista y bloqueo pesimista;
- laboratorio de planes de ejecución con aserciones sobre el plan y sobre el
  trabajo —instrucciones de la máquina virtual—, no sobre el tiempo, para que
  sea reproducible en cualquier máquina;
- laboratorio de cargas NoSQL que mide TTL frente a coherencia, incrustar
  frente a referenciar y el efecto de una clave de partición caliente;
- pruebas que someten al validador a un repositorio roto a propósito, para que
  la regla de las fuentes esté demostrada y no solo declarada.

Pendiente:

- reproducción automatizada de las anomalías de aislamiento (método de
  Hermitage) contra PostgreSQL y MySQL en contenedor;
- laboratorio de réplica con medición del retraso bajo carga;
- laboratorio de recuperación a un punto en el tiempo, cronometrado;
- cobertura del resto de las partes: quedan nueve sin laboratorio propio.

## 2.2 — Autoevaluación y trazabilidad del aprendizaje

Hecho:

- banco de preguntas publicado en el sitio con las 256 preguntas de evaluación,
  cada una enlazada a su clase y a la rúbrica que la corrige;
- registro de avance por clase, guardado localmente en el navegador, con
  contador en la portada y filtro de clases pendientes.

Pendiente:

- cuestionario interactivo con corrección orientativa en el cliente, sin
  servidor y sin convertir preguntas de explicación en preguntas de opción
  múltiple, que sería empobrecerlas;
- rúbrica del proyecto final aplicable por una tercera persona sin conocer el
  programa.

## 2.3 — Material descargable

- PDF por parte y PDF del programa completo, generados desde las mismas
  lecciones;
- versión en blanco y negro apta para impresión, sin cortar bloques de código;
- cuadernos ejecutables por laboratorio.

## 2.4 — Ampliación de la cobertura

Cada motor nuevo entra con ficha, documentación oficial en el registro y una
clase que lo trate; nunca solo con una línea en el catálogo:

- motores distribuidos SQL (CockroachDB, TiDB, YugabyteDB);
- formatos de tabla abiertos (Iceberg, Delta, Hudi) sobre almacenamiento de objetos;
- motores vectoriales adicionales y comparación medida de recall entre ellos.

## 3.0 — Programa evaluable de extremo a extremo

- proyecto final con conjunto de datos de mayor escala y mediciones esperadas;
- guion de defensa técnica con criterios públicos;
- portafolio verificable a partir de las evidencias generadas;
- traducción al inglés, conservando el mismo registro de fuentes;
- mapa de cobertura por certificación, al estilo del que ya existe para las rutas: qué
  parte del temario de DP-300, Professional Data Engineer o CDMP cubre cada parte del
  programa, medido y no afirmado.

## Criterios para cerrar un hito

Un hito se da por cerrado cuando: la validación pasa, los artefactos están
regenerados, las fuentes nuevas están en el registro y citadas, y existe una
evidencia reproducible de lo que el hito afirma haber conseguido.
