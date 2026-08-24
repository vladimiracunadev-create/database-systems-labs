# Parte 11 — Operación, seguridad y gobierno

> [Programa](../../README.md) · [Índice de clases](../README.md) ·
> [Glosario](../../GLOSARIO.md) · [Modelo de aprendizaje](../../docs/LEARNING-MODEL.md)

Lo que separa un ejercicio de un sistema: restauración probada, migraciones sin caída, control de acceso, observabilidad y privacidad.

**6 clases · 19 horas · 24 conceptos · 17 fuentes**

## Antes de esta parte

Esta parte se apoya en lo trabajado antes. Si vienes de fuera del programa, revisa al menos el vocabulario de:

- [Parte 08 — Transacciones, concurrencia y recuperación](../part-08-transacciones-concurrencia-y-recuperacion/README.md)

## De qué trata esta parte

Lo que separa un ejercicio de un sistema. Seis clases sobre las tareas que no aparecen en ningún tutorial de SQL y que son las que deciden si el sistema sobrevive a su segundo año: restaurar, migrar sin caída, controlar el acceso, no ser vulnerable, medir lo que los usuarios notan y tratar el dato personal como una obligación de diseño.

El orden es el de la gravedad de las consecuencias. Primero el respaldo, con la afirmación más incómoda del programa: solo cuenta lo que se ha restaurado. Después las migraciones evolutivas con expandir y contraer, que es el patrón que permite desplegar esquema y código por separado. Luego el control de acceso, con una comprobación que suele salir mal: si la aplicación se conecta como propietaria del esquema, no hay privilegio mínimo. Después la inyección SQL, explicada por su causa y con su solución completa. Luego la observabilidad, donde la media oculta y el p99 enseña. Y al final privacidad, retención y gobierno.

La clase 061 está clasificada como fundamentos a propósito, aunque esté en una parte avanzada: no hay nivel de experiencia en el que la parametrización sea opcional.

## Al terminar esta parte podrás

1. Declarar RPO y RTO en números y demostrarlos con una restauración cronometrada.
2. Ejecutar una migración de esquema sin ventana de caída usando expandir y contraer.
3. Configurar roles con privilegio mínimo y seguridad por fila, y comprobar que el filtro no se puede eludir.
4. Escribir código inmune a inyección y validar los identificadores dinámicos con lista blanca.
5. Definir objetivos de servicio por percentil y usar el presupuesto de error para decidir.
6. Diseñar retención y supresión de datos personales incluyendo respaldos y réplicas.

## Mapa de la parte

```mermaid
flowchart LR
    C058["058<br/>Respaldo y restauración: solo cuenta lo q…"]
    C059["059<br/>Migraciones evolutivas sin ventana de caída"]
    C060["060<br/>Control de acceso: privilegio mínimo, rol…"]
    C061["061<br/>Inyección SQL y el contrato de parametriz…"]
    C062["062<br/>Observabilidad, objetivos de servicio y c…"]
    C063["063<br/>Privacidad, retención y gobierno del dato"]
    C058 --> C059
    C059 --> C060
    C060 --> C061
    C061 --> C062
    C062 --> C063
    classDef fund fill:#0b3d2e,stroke:#3fb950,color:#fff
    classDef inter fill:#0d2d5e,stroke:#58a6ff,color:#fff
    classDef avan fill:#2d1b4e,stroke:#bc8cff,color:#fff
    class C058 inter
    class C059 avan
    class C060 inter
    class C061 fund
    class C062 avan
    class C063 inter
```

| # | Clase | Nivel | Horas | Fuentes |
|---|---|---|---:|---:|
| [058](058-respaldo-y-restauracion-probada/README.md) | [Respaldo y restauración: solo cuenta lo que se ha restaurado](058-respaldo-y-restauracion-probada/README.md) | Intermedio | 4 | 3 |
| [059](059-migraciones-evolutivas-sin-caida/README.md) | [Migraciones evolutivas sin ventana de caída](059-migraciones-evolutivas-sin-caida/README.md) | Avanzado | 3 | 3 |
| [060](060-control-de-acceso-y-seguridad-por-fila/README.md) | [Control de acceso: privilegio mínimo, roles y seguridad por fila](060-control-de-acceso-y-seguridad-por-fila/README.md) | Intermedio | 3 | 4 |
| [061](061-inyeccion-sql-y-parametrizacion/README.md) | [Inyección SQL y el contrato de parametrización](061-inyeccion-sql-y-parametrizacion/README.md) | Fundamentos | 3 | 4 |
| [062](062-observabilidad-slo-y-capacidad/README.md) | [Observabilidad, objetivos de servicio y capacidad](062-observabilidad-slo-y-capacidad/README.md) | Avanzado | 3 | 3 |
| [063](063-privacidad-retencion-y-gobierno-del-dato/README.md) | [Privacidad, retención y gobierno del dato](063-privacidad-retencion-y-gobierno-del-dato/README.md) | Intermedio | 3 | 3 |

## Las clases, una por una

### [058 — Respaldo y restauración: solo cuenta lo que se ha restaurado](058-respaldo-y-restauracion-probada/README.md)

*Intermedio · 4 h · 3 fuentes · requiere [046](../part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md)*

La clase que convierte una intención en una garantía medida. RPO y RTO se declaran en números, la recuperación a un punto en el tiempo se demuestra restaurando de verdad, y la conclusión es incómoda a propósito: un respaldo que nunca se ha restaurado no es un respaldo, es un fichero con nombre esperanzador.

**Conceptos que introduce:** `RPO` · `RTO` · `recuperación a un punto en el tiempo` · `prueba de restauración`

[Ir a la clase →](058-respaldo-y-restauracion-probada/README.md)

### [059 — Migraciones evolutivas sin ventana de caída](059-migraciones-evolutivas-sin-caida/README.md)

*Avanzado · 3 h · 3 fuentes · requiere [013](../part-01-fundamentos-datos-sistemas-y-metodo/013-independencia-de-datos-y-niveles-de-esquema/README.md), [024](../part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md)*

Cambiar el esquema con el sistema en marcha, usando expandir y contraer: primero añadir sin quitar, después trasladar el tráfico y rellenar el histórico por lotes reanudables, y solo al final eliminar lo viejo. La compatibilidad hacia atrás deja de ser una buena práctica y pasa a ser obligatoria en cuanto el despliegue es gradual.

**Conceptos que introduce:** `expandir y contraer` · `doble escritura` · `relleno` · `compatibilidad hacia atras`

[Ir a la clase →](059-migraciones-evolutivas-sin-caida/README.md)

### [060 — Control de acceso: privilegio mínimo, roles y seguridad por fila](060-control-de-acceso-y-seguridad-por-fila/README.md)

*Intermedio · 3 h · 4 fuentes · requiere [013](../part-01-fundamentos-datos-sistemas-y-metodo/013-independencia-de-datos-y-niveles-de-esquema/README.md), [024](../part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md)*

El control de acceso con una comprobación incómoda como punto de partida: si la aplicación se conecta como propietaria del esquema, no hay privilegio mínimo. Trata roles, separación de funciones y seguridad por fila, cuya ventaja sobre filtrar en la aplicación es que no hay consulta que se pueda olvidar del filtro.

**Conceptos que introduce:** `privilegio mínimo` · `rol` · `seguridad por fila` · `separación de funciones`

[Ir a la clase →](060-control-de-acceso-y-seguridad-por-fila/README.md)

### [061 — Inyección SQL y el contrato de parametrización](061-inyeccion-sql-y-parametrizacion/README.md)

*Fundamentos · 3 h · 4 fuentes · requiere [003](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/003-tu-primera-base-de-datos/README.md), [024](../part-04-sql-en-profundidad/024-ddl-el-esquema-como-contrato/README.md)*

La inyección SQL explicada por su causa —mezclar código y datos en la misma cadena— y su solución completa: la consulta parametrizada, que no es una mitigación sino una defensa total. Cubre además el caso que los parámetros no resuelven, los identificadores dinámicos, que solo se validan con lista blanca.

**Conceptos que introduce:** `consulta parametrizada` · `identificador dinamico` · `lista blanca` · `defensa en profundidad`

[Ir a la clase →](061-inyeccion-sql-y-parametrizacion/README.md)

### [062 — Observabilidad, objetivos de servicio y capacidad](062-observabilidad-slo-y-capacidad/README.md)

*Avanzado · 3 h · 3 fuentes · requiere [052](../part-09-almacenamiento-indices-y-planes/052-planes-de-ejecucion-y-refutacion/README.md), [058](058-respaldo-y-restauracion-probada/README.md)*

Medir lo que los usuarios notan. La media oculta y el p99 enseña; con veinte consultas por petición, casi todo el mundo toca la cola lenta. Une objetivos de servicio, presupuesto de error, saturación como señal anticipada y el registro de consultas lentas ordenado por tiempo total, no por la peor.

**Conceptos que introduce:** `percentil` · `presupuesto de error` · `saturación` · `consulta lenta`

[Ir a la clase →](062-observabilidad-slo-y-capacidad/README.md)

### [063 — Privacidad, retención y gobierno del dato](063-privacidad-retencion-y-gobierno-del-dato/README.md)

*Intermedio · 3 h · 3 fuentes · requiere [058](058-respaldo-y-restauracion-probada/README.md), [060](060-control-de-acceso-y-seguridad-por-fila/README.md)*

El dato personal como una obligación de diseño y no como un anexo legal. Minimización, limitación de finalidad, seudonimización y derecho de supresión, con el choque que hay que resolver antes de que llegue la solicitud: los respaldos, las réplicas y los registros de auditoría también contienen ese dato.

**Conceptos que introduce:** `minimización` · `limitación de finalidad` · `seudonimización` · `derecho de supresión`

[Ir a la clase →](063-privacidad-retencion-y-gobierno-del-dato/README.md)

## Errores frecuentes en esta parte

Cada uno de estos es una creencia habitual y su corrección. Si alguna te suena
propia, la clase que la desmonta está señalada arriba.

- «Tengo respaldos automáticos.» Tienes ficheros. Hasta que no se restaura uno en un entorno limpio y se cronometra, el RTO real es desconocido.
- «Escapo las comillas y ya estoy protegido.» Escapar a mano falla; parametrizar no. Y para identificadores dinámicos ni una cosa ni la otra: lista blanca.
- «La latencia media está bien.» La media oculta la cola. Con veinte consultas por petición, casi todos los usuarios tocan al menos una lenta.
- «Borro al usuario de la tabla y cumplo.» Sigue estando en los respaldos, en las réplicas y probablemente en el registro de auditoría.

## Vocabulario de la parte

Los 24 términos que esta parte introduce. Cada uno enlaza a la clase
en la que se trabaja, y todos aparecen también en el
[glosario del programa](../../GLOSARIO.md) con sus términos relacionados.

| Término | Qué significa | Se trabaja en |
|---|---|---|
| **compatibilidad hacia atras** | Que el código nuevo siga entendiendo los datos escritos por el viejo, y que el viejo no se rompa con los del nuevo. Es obligatoria en cuanto el despliegue es gradual, porque durante un rato conviven las dos versiones. | [059](059-migraciones-evolutivas-sin-caida/README.md) |
| **consulta lenta** | Registro de las consultas que superan un umbral, agrupadas por forma —`pg_stat_statements` y equivalentes—. Lo que importa no es la más lenta, sino la que multiplica tiempo por frecuencia: mil consultas de 50 ms pesan más que una de 5 s. | [062](062-observabilidad-slo-y-capacidad/README.md) |
| **consulta parametrizada** | Enviar la sentencia y los valores por canales distintos, de modo que el motor nunca interprete el dato como código. Es la defensa completa contra la inyección SQL, no una mitigación: bien usada, no hay cadena de entrada que cambie la estructura de la consulta. | [061](061-inyeccion-sql-y-parametrizacion/README.md) |
| **defensa en profundidad** | Poner varias barreras independientes, de modo que fallar una no baste: parametrizar, además dar privilegio mínimo, además registrar, además limitar por fila. Cada capa asume que las otras pueden fallar. | [061](061-inyeccion-sql-y-parametrizacion/README.md) |
| **derecho de supresión** | Obligación de borrar los datos de una persona cuando lo solicita y no hay base para conservarlos. Choca de frente con los respaldos, las réplicas y los registros de auditoría, y por eso hay que diseñar dónde vive el dato personal antes de que lo pidan. | [063](063-privacidad-retencion-y-gobierno-del-dato/README.md) |
| **doble escritura** | Fase transitoria en la que la aplicación escribe en la estructura vieja y en la nueva a la vez. Sostiene la migración mientras se rellena el histórico; hay que declarar desde el principio cuándo termina, porque si no se queda para siempre. | [059](059-migraciones-evolutivas-sin-caida/README.md) |
| **expandir y contraer** | Patrón de migración en tres tiempos: primero se añade lo nuevo sin quitar lo viejo, después se traslada el tráfico y se rellena, y solo cuando nadie usa lo antiguo se elimina. Es lo que permite desplegar esquema y código por separado sin ventana de caída. | [059](059-migraciones-evolutivas-sin-caida/README.md) |
| **identificador dinamico** | El caso que los parámetros no cubren: nombres de tabla, de columna o la dirección de un `ORDER BY` no se pueden enviar como valor. La única solución correcta es validarlos contra una lista blanca cerrada, nunca escaparlos a mano. | [061](061-inyeccion-sql-y-parametrizacion/README.md) |
| **limitación de finalidad** | Los datos recogidos para un fin no pueden reutilizarse para otro incompatible sin nueva base legal. Es lo que impide que un correo pedido para la facturación acabe alimentando un modelo de recomendación. | [063](063-privacidad-retencion-y-gobierno-del-dato/README.md) |
| **lista blanca** | Permitir solo lo que está explícitamente enumerado y rechazar todo lo demás. Se prefiere a la lista negra porque no hay que anticipar todas las formas de atacar, solo todas las formas válidas de usar. | [061](061-inyeccion-sql-y-parametrizacion/README.md) |
| **minimización** | Recoger solo los datos personales necesarios para la finalidad declarada. Es la medida de protección más eficaz que existe, porque el dato que no se guarda no se filtra, no hay que cifrarlo ni hay que borrarlo después. | [063](063-privacidad-retencion-y-gobierno-del-dato/README.md) |
| **percentil** | El valor por debajo del cual queda un porcentaje de las observaciones. La media oculta el problema; el p99 lo enseña. Y si una petición de usuario abre veinte consultas, casi todos los usuarios tocarán al menos una de la cola lenta. | [062](062-observabilidad-slo-y-capacidad/README.md) |
| **presupuesto de error** | Lo que resta entre el objetivo de servicio y el 100 %: con un SLO de 99,9 % se dispone de unos 43 minutos de fallo al mes. Convierte la fiabilidad en una cantidad que se gasta, y da una regla objetiva para decidir si se despliega o se estabiliza. | [062](062-observabilidad-slo-y-capacidad/README.md) |
| **privilegio mínimo** | Cada identidad recibe exactamente los permisos que necesita para su función y ninguno más. La comprobación práctica es incómoda y reveladora: si la aplicación se conecta como propietaria del esquema, no hay privilegio mínimo. | [060](060-control-de-acceso-y-seguridad-por-fila/README.md) |
| **prueba de restauración** | Restaurar la copia en un entorno limpio, comprobar la integridad de los datos y medir cuánto tardó. Un respaldo que nunca se ha restaurado no es un respaldo: es un fichero con nombre esperanzador. | [058](058-respaldo-y-restauracion-probada/README.md) |
| **recuperación a un punto en el tiempo** | Restaurar una copia base y reaplicar el registro archivado hasta un instante concreto, justo antes del `DELETE` sin `WHERE`. Exige que el archivado del registro esté activo y verificado desde antes del incidente. | [058](058-respaldo-y-restauracion-probada/README.md) |
| **relleno** | Copiar el histórico a la estructura nueva, por lotes y de forma reanudable, para no bloquear la tabla ni saturar el registro. Debe ser idempotente: se va a interrumpir y habrá que relanzarlo. | [059](059-migraciones-evolutivas-sin-caida/README.md) |
| **rol** | Agrupación de privilegios que se concede a personas o a aplicaciones. Permite razonar sobre permisos por función en lugar de por individuo, y revocar el acceso de alguien sin tener que auditar cada objeto. | [060](060-control-de-acceso-y-seguridad-por-fila/README.md) |
| **RPO** | Objetivo de punto de recuperación: cuántos datos se acepta perder, medido en tiempo. Un RPO de cinco minutos obliga a archivar el registro al menos cada cinco minutos; si no está escrito y probado, el RPO real es «el que salga». | [058](058-respaldo-y-restauracion-probada/README.md) |
| **RTO** | Objetivo de tiempo de recuperación: cuánto se acepta estar caído. Se mide restaurando de verdad y cronometrando, no estimando; casi siempre resulta ser varias veces mayor de lo que el equipo suponía. | [058](058-respaldo-y-restauracion-probada/README.md) |
| **saturación** | Cuán lleno está el recurso más escaso: conexiones, entrada y salida, memoria, CPU. Es la señal que anticipa el incidente, porque la latencia se dispara de forma no lineal justo antes de que el recurso se agote. | [062](062-observabilidad-slo-y-capacidad/README.md) |
| **seguridad por fila** | Políticas que el motor añade automáticamente a cada consulta para que un usuario solo vea las filas que le corresponden. La ventaja sobre filtrar en la aplicación es que no hay consulta que se pueda olvidar del filtro. | [060](060-control-de-acceso-y-seguridad-por-fila/README.md) |
| **separación de funciones** | Que quien desarrolla no sea quien despliega en producción, y que quien opera no pueda borrar sus propias huellas de auditoría. Es un control organizativo antes que técnico, y sin él el registro de auditoría no prueba nada. | [060](060-control-de-acceso-y-seguridad-por-fila/README.md) |
| **seudonimización** | Sustituir los identificadores directos por referencias, guardando por separado la tabla que permite revertirlo. Reduce el riesgo pero no convierte el dato en anónimo: mientras exista la clave, sigue siendo dato personal. | [063](063-privacidad-retencion-y-gobierno-del-dato/README.md) |

## Fuentes usadas en esta parte

17 obras distintas sostienen lo que se afirma en estas
6 clases. Los identificadores viven en
[`catalog/sources.json`](../../catalog/sources.json) y el estado de los enlaces
se comprueba con `python scripts/check_external_links.py`.

- **Laine Campbell, Charity Majors** (2017). [Database Reliability Engineering](https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/). O'Reilly. ISBN 978-1-4919-2594-2.  
  Operación, respaldos, objetivos de servicio y gestion de cambios.  
  *Se cita en las clases 058, 062.*
- **Martin Kleppmann** (2017). [Designing Data-Intensive Applications](https://dataintensive.net/). O'Reilly. ISBN 978-1-4493-7332-0.  
  Referencia central del programa para replicación, partición, transacciones distribuidas y streaming.  
  *Se cita en las clases 059.*
- **Scott W. Ambler, Pramod J. Sadalage** (2006). [Refactoring Databases: Evolutionary Database Design](https://databaserefactoring.com/). Addison-Wesley. ISBN 978-0-321-29353-4.  
  Migraciones con período de transición y compatibilidad hacia atras.  
  *Se cita en las clases 059.*
- **Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy** (2016). [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/). O'Reilly. ISBN 978-1-4919-2912-4.  
  Lectura libre. Objetivos de nivel de servicio y presupuesto de error.  
  *Se cita en las clases 058, 062.*
- **PostgreSQL Global Development Group** (2026). [PostgreSQL Documentation](https://www.postgresql.org/docs/current/).  
  Documentación de referencia del motor relacional principal del programa.  
  *Se cita en las clases 059.*
- **PostgreSQL Global Development Group** (2026). [PostgreSQL: Backup and Restore](https://www.postgresql.org/docs/current/backup.html).  
  Volcado lógico, copia de archivos y recuperación a un punto en el tiempo.  
  *Se cita en las clases 058.*
- **PostgreSQL Global Development Group** (2026). [PostgreSQL: Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).  
  Control de acceso por fila declarado en el propio motor.  
  *Se cita en las clases 060.*
- **Python Software Foundation** (2026). [Python: sqlite3](https://docs.python.org/3/library/sqlite3.html).  
  API DB-API 2.0 usada por los laboratorios ejecutables del repositorio.  
  *Se cita en las clases 061.*
- **Jeffrey Dean, Luiz Andre Barroso** (2013). [The Tail at Scale](https://dl.acm.org/doi/10.1145/2408776.2408794). Communications of the ACM 56(2). DOI [10.1145/2408776.2408794](https://doi.org/10.1145/2408776.2408794).  
  Por qué la latencia se mide en percentiles altos y no en promedio.  
  *Se cita en las clases 062.*
- **Center for Internet Security** (2026). [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks).  
  Guias de configuración endurecida para PostgreSQL, MySQL, MongoDB y otros.  
  *Se cita en las clases 060.*
- **Biblioteca del Congreso Nacional de Chile** (1999). [Ley 19.628 sobre proteccion de la vida privada](https://www.bcn.cl/leychile/navegar?idNorma=141599).  
  Marco chileno de datos personales aplicable a los proyectos del programa.  
  *Se cita en las clases 063.*
- **NIST** (2024). [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework). DOI [10.6028/NIST.CSWP.29](https://doi.org/10.6028/NIST.CSWP.29).  
  Funciones Gobernar, Identificar, Proteger, Detectar, Responder y Recuperar.  
  *Se cita en las clases 063.*
- **NIST** (2020). [NIST SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final).  
  Controles de auditoria, cifrado y acceso aplicables a bases de datos.  
  *Se cita en las clases 060.*
- **OWASP** (2021). [OWASP Top 10](https://owasp.org/Top10/).  
  A03 Inyección y A01 Control de acceso roto afectan directamente al diseño de datos.  
  *Se cita en las clases 060, 061.*
- **Marc-Andre Lemburg** (1999). [PEP 249 - Python Database API Specification v2.0](https://peps.python.org/pep-0249/).  
  Contrato de parametrización que evita la concatenación de entradas.  
  *Se cita en las clases 061.*
- **Union Europea** (2016). [Reglamento (UE) 2016/679 - Proteccion de datos personales](https://eur-lex.europa.eu/eli/reg/2016/679/oj).  
  Minimización, limitación de finalidad y derecho de supresión con efecto en el esquema.  
  *Se cita en las clases 063.*
- **OWASP** (2026). [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).  
  Consultas parametrizadas como defensa principal, con sus excepciones.  
  *Se cita en las clases 061.*

## Cómo estudiar esta parte

El mismo método en las 74 clases, y conviene respetar el orden:

1. **Lee el vocabulario antes que la materia.** Cada clase define sus términos
   arriba precisamente para que no haya que deducirlos del contexto.
2. **Ejecuta el ejemplo trabajado mientras lees**, no después. La mitad de lo
   que se aprende aquí solo aparece cuando la salida no es la esperada.
3. **Compara los motores.** La sección comparada muestra el mismo problema
   resuelto —o descartado con argumento— en varios sistemas. Lee también las
   filas de los que no lo resuelven: descartar con motivo es la habilidad que
   se evalúa en el proyecto final.
4. **Responde las preguntas de evaluación por escrito.** Una respuesta que no
   se puede escribir en tres líneas todavía no está entendida.
5. **Haz el reto de transferencia.** Es el único ejercicio que comprueba si el
   concepto se puede aplicar a un caso que la clase no mostró.
6. **Guarda la evidencia**: comando, versión del motor, semilla y salida
   completa. Sin eso no hay nota, porque no hay nada que revisar.

## Otras partes

- [Parte 00 — Primeros pasos: del archivo a la base de datos](../part-00-primeros-pasos-del-archivo-a-la-base-de-datos/README.md)
- [Parte 01 — Fundamentos, sistemas y método](../part-01-fundamentos-datos-sistemas-y-metodo/README.md)
- [Parte 02 — Modelado conceptual y requisitos](../part-02-modelado-conceptual-y-requisitos/README.md)
- [Parte 03 — Modelo relacional y álgebra](../part-03-modelo-relacional-y-algebra/README.md)
- [Parte 04 — SQL en profundidad](../part-04-sql-en-profundidad/README.md)
- [Parte 05 — Motores relacionales y dialectos](../part-05-motores-relacionales-y-dialectos/README.md)
- [Parte 06 — Documentos y clave-valor](../part-06-documentos-y-clave-valor/README.md)
- [Parte 07 — Grafos, columnas, tiempo y búsqueda](../part-07-grafos-columnas-tiempo-y-busqueda/README.md)
- [Parte 08 — Transacciones, concurrencia y recuperación](../part-08-transacciones-concurrencia-y-recuperacion/README.md)
- [Parte 09 — Almacenamiento, índices y planes](../part-09-almacenamiento-indices-y-planes/README.md)
- [Parte 10 — Distribución, réplica y consistencia](../part-10-distribucion-replica-y-consistencia/README.md)
- [Parte 12 — Analítica, integración y streaming](../part-12-analitica-integracion-y-streaming/README.md)
- [Parte 13 — Vectores, recuperación y RAG](../part-13-vectores-recuperacion-y-rag/README.md)
- [Parte 14 — Arquitectura y proyecto final](../part-14-arquitectura-y-proyecto-final/README.md)
