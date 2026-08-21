# ⚖️ Gobierno y privacidad del dato

> Respondes tres preguntas que casi ninguna empresa sabe contestar de memoria: **quién accede a
> qué**, **con qué base legal** y **hasta cuándo se conserva**. Y tienes que poder demostrarlo,
> no afirmarlo.
>
> **Nivel de entrada:** intermedio · **Foco:** control de acceso, minimización, retención,
> trazabilidad y evidencia auditable · **Cargos habituales:** responsable de gobierno del dato,
> especialista en cumplimiento de datos, delegado de protección de datos con perfil técnico.

## 🧭 Qué es y por qué importa

Este rol vive en la frontera entre lo técnico y lo normativo, y sufre cuando se queda solo en
uno de los dos lados. Un comité que redacta políticas que nadie puede implementar no gobierna
nada; un equipo técnico que cifra por costumbre sin saber qué dato protege, tampoco. El trabajo
consiste en traducir una obligación —legal o de negocio— a un control que existe en el sistema
y deja rastro.

Importa por dos razones que se refuerzan. La primera es de riesgo: los datos personales
concentran multas, incidentes reputacionales y pérdida de confianza. La segunda es más
cotidiana: **una organización que no sabe qué datos tiene no puede decidir sobre ellos**, ni
migrarlos, ni borrarlos cuando alguien lo pide, ni responder a una auditoría sin un mes de
arqueología.

En español hay una particularidad útil: conviven marcos distintos. El
[Reglamento General de Protección de Datos](https://eur-lex.europa.eu/eli/reg/2016/679/oj) fija
el estándar europeo y ha influido en el resto del mundo; en Chile, la
[Ley 19.628](https://www.bcn.cl/leychile/navegar?idNorma=141599) sobre protección de la vida
privada establece su propio marco. Saber leer ambos —y no confundirlos— es parte del oficio.

Lo que este programa **no** te da: asesoría legal. Aquí se trabaja la parte técnica del
gobierno del dato: los controles, la evidencia y el diseño que hace posible cumplir. La
interpretación jurídica es de abogados, y conviene decirlo en voz alta.

## 🗓️ Un día en el puesto

- **Una petición de acceso o de borrado.** Alguien ejerce sus derechos. ¿Sabes en cuántos
  sistemas está esa persona, incluidas copias, respaldos y almacenes analíticos?
- **Revisar permisos.** Quién tiene acceso a la tabla de clientes y por qué. La respuesta
  habitual —«todo el equipo, por si acaso»— es justamente el hallazgo.
- **Clasificar un conjunto de datos nuevo.** Qué contiene, qué sensibilidad tiene, quién lo
  usa, cuánto tiempo se conserva.
- **Definir retención.** Con negocio y con legal, y después implementarla: la política que no
  se ejecuta como un proceso no existe.
- **Preparar una auditoría.** Reunir evidencia de que los controles funcionaron, no de que
  estaban escritos.
- **Revisar un diseño nuevo** antes de que salga: seudonimizar, minimizar y separar lo que no
  necesita estar junto sale barato al principio y carísimo después.

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **Control de acceso en el motor:** roles, privilegio mínimo y seguridad por fila. La
  diferencia entre «la aplicación filtra» y «el motor no lo entrega».
- **Inyección SQL y parametrización:** el fallo que convierte un control de acceso en
  decorativo.
- **Integridad y restricciones:** un dato que no se puede corromper es un dato que se puede
  auditar.
- **Respaldo, restauración y retención:** los respaldos también contienen datos personales, y
  también caducan.
- **Réplica y distribución:** dónde acaban físicamente los datos, que en materia de
  transferencias internacionales importa.
- **Seudonimización, anonimización y sus límites:** por qué un identificador «anónimo» a menudo
  no lo es cuando se cruza con otra tabla.
- **Trazabilidad:** registros de acceso y de cambio que permitan reconstruir quién hizo qué.

### Herramientas del oficio

- El motor y su modelo de permisos, a fondo —empezando por la documentación oficial de
  seguridad por fila—.
- Un inventario de datos vivo (catálogo), aunque empiece siendo una hoja de cálculo bien
  mantenida.
- Marcos de control como los del NIST para no inventar la lista de comprobación desde cero.
- Automatización de la retención y de los informes de acceso: si depende de que alguien se
  acuerde, fallará.

### Habilidades no técnicas

- **Traducir entre legal y técnico** en los dos sentidos, sin que ninguno se sienta engañado.
- **Escribir políticas implementables**: si no se puede comprobar, no es una política.
- **Sostener un «no» incómodo** cuando un proyecto quiere copiar producción a un entorno de
  pruebas.

## 📚 Tu ruta en el programa

8 partes, 147 horas estimadas.

1. 📚 [**Parte 01 — Fundamentos**](../classes/part-01-fundamentos-datos-sistemas-y-metodo/README.md)
   (4 clases · 12 h).
2. 📚 [**Parte 02 — Modelado conceptual y requisitos**](../classes/part-02-modelado-conceptual-y-requisitos/README.md)
   (5 clases · 16 h). No se gobierna lo que no se sabe nombrar.
3. 📚 [**Parte 04 — SQL en profundidad**](../classes/part-04-sql-en-profundidad/README.md)
   (6 clases · 20 h). Necesitas leer y escribir las consultas que auditas. Añade
   [013 — Integridad: restricciones y acciones referenciales](../classes/part-03-modelo-relacional-y-algebra/023-integridad-restricciones-y-acciones-referenciales/README.md).
4. 📚 [**Parte 08 — Transacciones, concurrencia y recuperación**](../classes/part-08-transacciones-concurrencia-y-recuperacion/README.md)
   (5 clases · 18 h). Para entender qué significa que un dato esté «confirmado».
5. 📚 [**Parte 10 — Distribución, réplica y consistencia**](../classes/part-10-distribucion-replica-y-consistencia/README.md)
   (5 clases · 17 h). Dónde acaban las copias.
6. 📚 [**Parte 11 — Operación, seguridad y gobierno**](../classes/part-11-operacion-seguridad-y-gobierno/README.md)
   (6 clases · 19 h). El núcleo del rol:
   [048 — Respaldo y restauración probada](../classes/part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md),
   [050 — Control de acceso: privilegio mínimo, roles y seguridad por fila](../classes/part-11-operacion-seguridad-y-gobierno/060-control-de-acceso-y-seguridad-por-fila/README.md),
   [051 — Inyección SQL y parametrización](../classes/part-11-operacion-seguridad-y-gobierno/061-inyeccion-sql-y-parametrizacion/README.md)
   y [053 — Privacidad, retención y gobierno del dato](../classes/part-11-operacion-seguridad-y-gobierno/063-privacidad-retencion-y-gobierno-del-dato/README.md).
7. 📚 [**Parte 12 — Analítica, integración y streaming**](../classes/part-12-analitica-integracion-y-streaming/README.md)
   (4 clases · 13 h). El dato personal se multiplica en las tuberías analíticas, y ahí se
   olvida.
8. 📚 [**Parte 14 — Arquitectura y proyecto final**](../classes/part-14-arquitectura-y-proyecto-final/README.md)
   (3 clases · 12 h). Con
   [063 — Registro de decisiones y costo total](../classes/part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md),
   que es el formato en el que se documenta una decisión de gobierno.

Laboratorios de la ruta:

- 🧪 [`01-sql-foundations`](../labs/01-sql-foundations/README.md) — el dominio educativo del
  repositorio usa datos sintéticos a propósito: así se practica sin exponer a nadie.
- 🧪 [`03-transactions`](../labs/03-transactions/README.md) — qué significa que una operación
  quedó registrada, y qué se pierde cuando no.

## 🧪 Qué tienes que poder demostrar

- implementar **privilegio mínimo** sobre un esquema real y demostrar con una consulta que un
  rol no ve lo que no debe;
- aplicar seguridad por fila y explicar en qué se diferencia de filtrar en la aplicación;
- responder «¿dónde está el dato de esta persona?» enumerando sistemas, copias y respaldos;
- definir e **implementar** una política de retención, con el proceso que la ejecuta;
- explicar por qué un conjunto seudonimizado puede reidentificarse al cruzarlo con otro;
- preparar la evidencia de un control: qué registro lo demuestra y durante cuánto se conserva;
- documentar una decisión de gobierno en formato ADR, con su criterio de revisión.

## 🎓 Credenciales

La credencial más establecida del área es el
[**CDMP** (Certified Data Management Professional)](https://cdmp.info/), que administra DAMA
International en tres niveles —Associate, Practitioner y Master—, con exámenes basados en su
cuerpo de conocimiento de gestión de datos. Es de las pocas credenciales del sector que no
pertenece a un fabricante.

En privacidad existen además certificaciones jurídicas y de gestión (de asociaciones
profesionales de privacidad), útiles si tu puesto se inclina hacia lo normativo. Este programa
no las cubre ni las evalúa: aquí se trabaja la capa técnica que hace posible cumplir.

## 📈 Progresión y mercado

1. **Perfil técnico** (DBA, ingeniero de datos) o **perfil de cumplimiento** que se acerca a lo
   técnico: las dos entradas habituales.
2. **Especialista en gobierno del dato** — catálogo, clasificación, políticas y controles.
3. **Responsable de gobierno / privacidad** — defines el marco, coordinas con legal y respondes
   ante auditoría.
4. **Bifurcación:** dirección de datos (CDO) si te atrae la parte organizativa, o
   [arquitectura](arquitectura.md) si te atrae el diseño técnico del conjunto.

No existe un epígrafe oficial de mercado para este rol comparable al del
[Occupational Outlook Handbook](https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm)
para administradores y arquitectos, así que aquí no se publican rangos. Un apunte útil sin
cifras: es un puesto donde la demanda tiende a aparecer **después** de un incidente o de un
cambio normativo, y donde la experiencia previa en operación pesa mucho.

## ⚠️ Mitos y errores comunes

- **«Ciframos, luego cumplimos.»** El cifrado protege frente a un acceso no autorizado al
  medio; no dice nada sobre quién tiene permiso, cuánto se conserva ni con qué base legal se
  trata el dato.
- **«Anonimizamos quitando el nombre.»** Eso es seudonimizar. Con otra tabla y dos cruces, a
  menudo se reidentifica.
- **«Los respaldos no cuentan.»** Contienen los mismos datos personales y también deben tener
  retención y control de acceso.
- **«El entorno de pruebas es interno, no pasa nada.»** Copiar producción a pruebas es una de
  las fugas más comunes y más evitables.
- **«La política ya está aprobada.»** Una política sin control implementado y sin evidencia es
  un documento, no un control.
- **«Guardamos todo por si el negocio lo necesita.»** Cada dato guardado de más es superficie
  de riesgo, coste de almacenamiento y trabajo en cada auditoría.
- **«Esto es cosa de legal.»** Legal define la obligación; el sistema la cumple o no. Sin
  alguien que traduzca, no se cumple.

## 🚀 Siguientes pasos

1. Haz la Parte 11 completa: es tu núcleo, y las cuatro clases citadas son el mínimo.
2. Toma un esquema real y aplícale privilegio mínimo; demuestra con consultas que funciona.
3. Escribe el inventario de datos personales de un sistema que conozcas, con retención por
   categoría.
4. Ensaya la pregunta difícil: «bórrame». Enumera cada lugar donde habría que actuar.
5. Documenta un control con su evidencia, como si mañana llegara una auditoría.
6. Cierra con el [proyecto final](../projects/capstone.md) incorporando el gobierno como
   requisito, no como anexo.

## 📖 De dónde sale esto

- **Parlamento Europeo y Consejo**, *Reglamento (UE) 2016/679* — el marco de protección de
  datos que fija el estándar de referencia.
- **Congreso Nacional de Chile**, *Ley 19.628 sobre protección de la vida privada* — el marco
  chileno.
- **NIST**, *SP 800-53 Rev. 5* — catálogo de controles de seguridad y privacidad del que salen
  las listas de comprobación serias.
- **DAMA International**, *CDMP* — la credencial de gestión de datos citada.

Fichas completas en el [registro de fuentes](../catalog/sources.json).

---

- ⬅️ [Volver al índice de rutas](README.md)
- 🏠 [Inicio del programa](../README.md)
