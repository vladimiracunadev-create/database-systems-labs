# 🎓 Certificaciones

Cada certificación mapeada declara de dónde salen sus pesos y con qué método se calcula la cobertura. Un porcentaje sin método es propaganda: aquí el cálculo es reproducible con scripts/generar_certificaciones.py y auditable en este archivo. La cobertura mide temario, no probabilidad de aprobar: un examen práctico exige además horas de producto.

| Certificación | Código | Nivel | Cobertura del programa | Cómo se calcula |
|---|---|---|---|---|
| [Microsoft Certified: Azure Database Administrator Associate](dp-300.md) | DP-300 | Intermedio | `███████░░░` 70 % | medida por subáreas |
| [Microsoft Certified: Azure Data Fundamentals](dp-900.md) | DP-900 | Entrada | `██████░░░░` 60 % | medida por subáreas |
| [AWS Certified Data Engineer – Associate](aws-dea-c01.md) | DEA-C01 | Intermedio | `██████░░░░` 62 % | estimada por dominio |

## Cómo se calcula la cobertura

Hay dos métodos, y cada ficha dice cuál usa:

1. **Por subáreas.** Se listan las subáreas oficiales del temario y se marca cuáles cubre el programa y con qué clases. La cobertura del dominio es subáreas cubiertas / subáreas totales, y el total es la media ponderada por el peso oficial del dominio. Es una medición, no una opinión.
2. **Por dominio.** El proveedor publica el peso del dominio pero no un desglose citable con exactitud, así que la cobertura del dominio es una estimación declarada, justificada con las partes y clases que la sostienen. Se marca como estimación en la ficha.

En ambos casos el total es `Σ (peso del dominio × cobertura del dominio) / 100`. Cuando el
proveedor publica el peso como rango —«15–20 %»— se usa el punto medio. El cálculo lo hace
[`scripts/generar_certificaciones.py`](../scripts/generar_certificaciones.py) desde
[`_mapeo.json`](_mapeo.json), y la integración continua comprueba que estas fichas no quedan
desactualizadas.

**Lo que la cobertura significa y lo que no.** Mide qué parte del temario prepara este
programa. No mide tu probabilidad de aprobar: un examen de proveedor pregunta además por
nombres de servicios, consolas y límites de producto que aquí no se enseñan a propósito, y una
credencial práctica exige horas de laboratorio propio. Un 70 % de cobertura significa «te
faltará estudiar el 30 %, y ya sabes cuál es».

## Certificaciones que no se mapean, y por qué

Este repositorio no publica un porcentaje que no pueda comprobar en la fuente oficial. Estas
credenciales son relevantes para el campo, pero su ponderación no está disponible de forma
verificable:

- **[Google Cloud Professional Data Engineer](https://cloud.google.com/learn/certification/data-engineer)** — La guía del examen se publica como PDF con fuentes incrustadas cuyo texto no se puede extraer de forma fiable. Los pesos por sección circulan en blogs, pero este repositorio no publica un porcentaje que no pueda comprobar en la fuente. La credencial sigue siendo relevante para la ruta de ingeniería de datos y aparece citada en ella.
- **[Certified Data Management Professional (CDMP)](https://cdmp.info/)** — DAMA International publica los niveles del programa, pero la ponderación por área de conocimiento no está disponible en una página verificable sin comprar el material. Se cita en la ruta de gobierno y privacidad del dato como credencial de referencia.
- **[Oracle Database Administration Professional](https://education.oracle.com/certification)** — El temario es de producto y el peso por objetivo no se publica de forma estable. El programa cubre los mecanismos de Oracle en la clase 022, no su administración.

## Antes de inscribirte

- Comprueba la **versión vigente** del temario: los proveedores lo actualizan y estas fichas
  llevan la fecha en que se verificaron.
- Mira primero la [ruta por rol](../rutas/README.md) que te corresponde: la credencial ordena
  el estudio, pero lo que te contrata es lo que puedes demostrar.
- Ninguna certificación sustituye a un [laboratorio](../labs/README.md) ejecutado y explicado.

---

> Mapeo orientativo, no avalado por Microsoft, Amazon Web Services ni ningún otro proveedor. Los temarios cambian: la fecha de verificación de cada uno está en su ficha, y conviene comprobar la versión vigente antes de inscribirse.
