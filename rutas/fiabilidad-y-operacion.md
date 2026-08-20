# 🛡️ DBA / SRE de datos

> Eres quien responde cuando la base de datos deja de responder. Tu trabajo se mide en dos
> números: cuánto tiempo estuvo caída y cuántos datos se perdieron. Todo lo demás —índices,
> réplicas, planes— existe para mantener esos dos números bajos.
>
> **Nivel de entrada:** intermedio · **Foco:** disponibilidad, rendimiento, recuperación
> demostrada y cambios sin caída · **Cargos habituales:** administrador de bases de datos, SRE
> de datos, ingeniero de fiabilidad.

## 🧭 Qué es y por qué importa

El rol clásico de DBA —crear usuarios, ejecutar respaldos, vigilar espacio— se ha ido
fundiendo con el de SRE: la operación se automatiza, se versiona y se mide con objetivos de
servicio. Lo que no ha cambiado es la responsabilidad de fondo: **eres el último punto entre un
incidente y la pérdida de datos**. Un servicio sin estado se reinicia; una base de datos
corrupta sin respaldo restaurable es una empresa con un problema existencial.

La afirmación que ordena el oficio es incómoda: *un respaldo que nunca se ha restaurado no es
un respaldo, es un archivo*. La mitad del trabajo consiste en convertir supuestos en evidencia:
restaurar de verdad y cronometrarlo, provocar una conmutación por error a propósito, medir el
retraso de la réplica bajo carga, comprobar que la migración se puede revertir.

Es un rol con guardias, con presión y con una asimetría desagradable: cuando todo va bien,
nadie lo nota. Compensa con algo que pocos puestos dan: entiendes el sistema entero, del disco
al plan de ejecución, y tu criterio pesa en decisiones caras.

Lo que este programa **no** te da: la experiencia de un incidente real a las tres de la mañana,
ni el músculo político para negociar una ventana de mantenimiento. Sí te da el método y las
mediciones con las que se argumenta.

## 🗓️ Un día en el puesto

- **Revisión de la noche.** Respaldos, réplicas, alertas, consumo de espacio. Primero el estado
  real; después el trabajo planificado.
- **Una consulta que degradó el sistema.** La localizas, lees su plan, decides si es índice,
  estadísticas, esquema o una aplicación que pide demasiado.
- **Prueba de restauración.** Con calendario, no cuando haga falta. Restaurar a un punto en el
  tiempo y cronometrarlo, para poder responder con un número al «cuánto tardaríamos».
- **Una migración de esquema en producción.** En pasos compatibles hacia atrás, con
  interruptor de vuelta y sin bloquear escrituras.
- **Capacidad.** Proyectar crecimiento y decidir con antelación, en vez de reaccionar cuando el
  disco llega al 90 %.
- **Un incidente.** Contención, diagnóstico, recuperación y —lo que más valor deja— un análisis
  posterior sin culpables que cambie algo del sistema.

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **Recuperación:** registro anticipado (WAL), punto de recuperación, restauración a un punto
  en el tiempo, y los dos objetivos que gobiernan todo: RPO y RTO.
- **Transacciones y aislamiento por dentro:** bloqueo en dos fases, MVCC, versiones muertas y
  su recolección.
- **Almacenamiento e índices:** páginas, buffer, B-tree frente a LSM, amplificación de
  escritura y coste real de cada índice.
- **Planes de ejecución:** leer `EXPLAIN`, entender estadísticas y refutar hipótesis con
  medición.
- **Réplica y distribución:** líder único frente a multilíder, retraso de réplica, conmutación
  por error y qué se pierde en cada opción.
- **Operación segura:** privilegio mínimo, seguridad por fila, cifrado y gestión de
  credenciales.
- **Observabilidad:** métricas que importan, objetivos de servicio (SLO), presupuesto de error
  y alertas que se pueden atender.

### Herramientas del oficio

- El motor que operas, a fondo: PostgreSQL, MySQL, SQL Server u Oracle —y su documentación
  oficial como primera parada, no el blog de turno—.
- Herramientas de respaldo y restauración del motor, automatizadas y verificadas.
- Métricas y trazas (Prometheus, Grafana o equivalentes) con paneles que respondan preguntas,
  no que decoren.
- Infraestructura y cambios de esquema versionados: nada de tocar producción a mano.

### Habilidades no técnicas

- **Calma bajo presión** y método: contener antes de diagnosticar, diagnosticar antes de
  arreglar.
- **Escribir análisis posteriores** que cambien el sistema y no busquen culpables.
- **Decir que no con datos**: negarse a un cambio arriesgado con una medición delante convence;
  sin ella, solo molesta.

## 📚 Tu ruta en el programa

9 partes, 143 horas estimadas.

1. 📚 [**Parte 00 — Fundamentos**](../classes/part-00-fundamentos-datos-sistemas-y-metodo/README.md)
   (4 clases · 12 h).
2. 📚 [**Parte 01 — Modelado conceptual**](../classes/part-01-modelado-conceptual-y-requisitos/README.md)
   (5 clases · 16 h). Operar un modelo malo cuesta el doble; conviene reconocerlo.
3. 📚 [**Parte 03 — SQL en profundidad**](../classes/part-03-sql-en-profundidad/README.md)
   (6 clases · 20 h).
4. 📚 [**Parte 04 — Motores relacionales y dialectos**](../classes/part-04-motores-relacionales-y-dialectos/README.md)
   (4 clases · 12 h). Lo que cambia de un motor a otro cuando toca operarlo.
5. 📚 [**Parte 07 — Transacciones, concurrencia y recuperación**](../classes/part-07-transacciones-concurrencia-y-recuperacion/README.md)
   (5 clases · 18 h). Imprescindible:
   [036 — Registro anticipado y recuperación (WAL y ARIES)](../classes/part-07-transacciones-concurrencia-y-recuperacion/036-registro-anticipado-y-recuperacion/README.md).
6. 📚 [**Parte 08 — Almacenamiento, índices y planes**](../classes/part-08-almacenamiento-indices-y-planes/README.md)
   (5 clases · 17 h). Con
   [038 — Páginas, filas y buffer](../classes/part-08-almacenamiento-indices-y-planes/038-paginas-filas-y-buffer-pool/README.md)
   y [042 — Planes de ejecución y refutación](../classes/part-08-almacenamiento-indices-y-planes/042-planes-de-ejecucion-y-refutacion/README.md).
7. 📚 [**Parte 09 — Distribución, réplica y consistencia**](../classes/part-09-distribucion-replica-y-consistencia/README.md)
   (5 clases · 17 h).
8. 📚 [**Parte 10 — Operación, seguridad y gobierno**](../classes/part-10-operacion-seguridad-y-gobierno/README.md)
   (6 clases · 19 h). El núcleo del rol:
   [048 — Respaldo y restauración probada](../classes/part-10-operacion-seguridad-y-gobierno/048-respaldo-y-restauracion-probada/README.md),
   [049 — Migraciones evolutivas sin caída](../classes/part-10-operacion-seguridad-y-gobierno/049-migraciones-evolutivas-sin-caida/README.md)
   y [052 — Observabilidad, objetivos de servicio y capacidad](../classes/part-10-operacion-seguridad-y-gobierno/052-observabilidad-slo-y-capacidad/README.md).
9. 📚 [**Parte 13 — Arquitectura y proyecto final**](../classes/part-13-arquitectura-y-proyecto-final/README.md)
   (3 clases · 12 h).

Laboratorios de la ruta:

- 🧪 [`01-sql-foundations`](../labs/01-sql-foundations/README.md).
- 🧪 [`03-transactions`](../labs/03-transactions/README.md) — el comportamiento concurrente que
  vas a tener que explicar a un equipo de desarrollo.
- 🧪 [`04-indexing`](../labs/04-indexing/README.md) — planes y coste de escritura medidos, que
  es como se argumenta un índice ante quien lo pide «por si acaso».

## 🧪 Qué tienes que poder demostrar

- **restaurar** una base a un punto en el tiempo y decir cuánto tardaste;
- declarar el RPO y el RTO que tu sistema cumple hoy, con la prueba que lo respalda;
- leer un plan de ejecución y explicar por qué el motor eligió ese camino;
- describir el efecto de un índice nuevo sobre la escritura, con números;
- explicar el retraso de réplica y qué lecturas pueden ver datos viejos;
- planificar una migración sin ventana de caída, con vuelta atrás;
- definir un objetivo de servicio útil y una alerta que alguien pueda atender.

## 🎓 Credenciales

Aquí las credenciales sí pesan, sobre todo en empresas grandes y en consultoría. La más
directa para el mundo Microsoft es
[**Azure Database Administrator Associate (DP-300)**](https://learn.microsoft.com/en-us/credentials/certifications/azure-database-administrator-associate/):
evalúa planificación e implementación de recursos de plataforma de datos, entorno seguro,
monitorización y optimización, automatización de tareas y alta disponibilidad con recuperación
ante desastres. Se rinde en español, entre otros idiomas, y **se renueva cada doce meses**.

Ese temario es, casi punto por punto, la Parte 10 de este programa más partes de la 07, la 08 y
la 09. Si trabajas sobre otro motor, busca el equivalente de tu proveedor: lo que se evalúa es
el mismo oficio.

## 📈 Progresión y mercado

1. **Soporte o desarrollo con inclinación a operación** — la entrada habitual.
2. **DBA junior / operador de plataforma** — ejecutas procedimientos escritos por otros.
3. **DBA / SRE de datos** — respondes por disponibilidad, rendimiento y recuperación.
4. **Sénior o líder de fiabilidad** — defines objetivos de servicio, capacidad y estrategia de
   continuidad; participas en decisiones de arquitectura.

Este es el único rol de las siete rutas con una fuente oficial de mercado dedicada. Según el
[Occupational Outlook Handbook](https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm)
del U.S. Bureau of Labor Statistics —datos de mayo de 2024, Estados Unidos— la mediana salarial
fue de unos **104 620 USD** anuales para administradores de bases de datos y de unos
**135 980 USD** para arquitectos, con una proyección de crecimiento del empleo de alrededor del
**4 % entre 2024 y 2034**. Son cifras de un solo país y con su propio coste de vida: úsalas
como referencia de forma y proporción, no como expectativa local. Consulta la fuente para el
dato vigente, que se actualiza cada año.

## ⚠️ Mitos y errores comunes

- **«Tenemos respaldos.»** Tenéis archivos. Hasta que no restauráis y cronometráis, no sabéis
  si tenéis respaldos.
- **«La réplica es el respaldo.»** La réplica copia también el `DELETE` equivocado, y lo copia
  rápido.
- **«Añadamos índices, no molestan.»** Cada índice se paga en cada escritura y en cada
  recuperación. Mídelo antes.
- **«El motor ya se encarga.»** El motor hace lo que le configuraste, incluidos los valores por
  defecto que nadie revisó.
- **«Ese ajuste funcionó en mi anterior empresa.»** Otra carga, otros datos, otro hardware.
  Refuta o confirma con una medición en tu sistema.
- **«Alta disponibilidad es lo mismo que durabilidad.»** Sobrevivir a la caída de un nodo y no
  perder datos confirmados son problemas distintos, con soluciones distintas.

## 🚀 Siguientes pasos

1. Haz las Partes 07 → 08 → 10 como bloque: es el corazón del rol.
2. Restaura un respaldo real en un entorno de prueba y **cronométralo**. Escribe el número.
3. Ejecuta [`03-transactions`](../labs/03-transactions/README.md) y [`04-indexing`](../labs/04-indexing/README.md),
   y repite ambos contra tu motor real.
4. Define un objetivo de servicio para una base que operes y una alerta que lo vigile.
5. Ensaya una migración sin caída en un entorno de prueba, con su vuelta atrás.
6. Si trabajas con Azure o SQL Server, usa el temario del
   [DP-300](https://learn.microsoft.com/en-us/credentials/certifications/azure-database-administrator-associate/)
   como lista de comprobación de lo aprendido.

## 📖 De dónde sale esto

- **Laine Campbell, Charity Majors**, *Database Reliability Engineering* — el puente entre el
  DBA clásico y la fiabilidad moderna.
- **Betsy Beyer y otros**, *Site Reliability Engineering* — objetivos de servicio, presupuesto
  de error y análisis posteriores sin culpables.
- **U.S. Bureau of Labor Statistics**, *Occupational Outlook Handbook* — las cifras de mercado
  citadas arriba.
- **Microsoft**, *Azure Database Administrator Associate (DP-300)* — temario oficial de la
  credencial.

Fichas completas en el [registro de fuentes](../catalog/sources.json).

---

- ⬅️ [Volver al índice de rutas](README.md)
- 🏠 [Inicio del programa](../README.md)
