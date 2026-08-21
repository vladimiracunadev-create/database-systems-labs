# 058 — Respaldo y restauración: solo cuenta lo que se ha restaurado

> [Programa](../../../README.md) · [Parte 11](../README.md) · [← Anterior](../../part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) · [Siguiente →](../../part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md)

Parte 11 — Operación, seguridad y gobierno · Intermedio ·
4 horas estimadas · motores `postgresql`, `sqlite`, `mongodb` · laboratorio
[`labs/08-recovery`](../../../labs/08-recovery/README.md) · 3 fuentes.

**Conceptos centrales:** `RPO` · `RTO` · `recuperación a un punto en el tiempo` · `prueba de restauración`

**En este caso se comparan 7 motores**: 5 lo resuelven (5 con el resultado comprobado por máquina) y 2 no, con el motivo escrito.

---

## Propósito

Convertir la copia de seguridad en una garantía verificada. Una copia que nunca se ha restaurado no es una copia: es una carpeta que ocupa espacio.

## Resultados de aprendizaje

Al terminar podrás:

1. Definir RPO y RTO y derivarlos de una exigencia de negocio.
2. Distinguir copia lógica, física y recuperación a un punto en el tiempo.
3. Diseñar un plan que cubra los cinco modos de pérdida.
4. Ejecutar y cronometrar una restauración completa.
5. Explicar por qué una réplica no es una copia de seguridad.

## Fundamentos

### RPO y RTO

- **RPO (objetivo de punto de recuperación):** cuántos datos se acepta perder, en tiempo. Determina la frecuencia de copia y el modo de replicación.
- **RTO (objetivo de tiempo de recuperación):** cuánto se acepta estar caído. Determina el tipo de copia y el procedimiento.

Ambos salen de una conversación con el negocio, no de una preferencia técnica. La pregunta útil es concreta: *«si perdiéramos los datos de las últimas cuatro horas, ¿qué habría que rehacer y cuánto costaría?»*.

| RPO | Mecanismo necesario |
|---|---|
| 24 h | Copia diaria |
| 1 h | Copia diaria + archivado de WAL cada hora |
| 5 min | Archivado continuo de WAL |
| ~0 | Réplica síncrona **más** copias |

| RTO | Mecanismo necesario |
|---|---|
| 24 h | Restaurar copia lógica |
| 1 h | Copia física + WAL |
| 5 min | Réplica en caliente con conmutación |
| ~0 | Multimaestro o activo-activo |

### Los cinco modos de pérdida

Un plan solo está completo si cubre los cinco:

| Modo | Cubre |
|---|---|
| Fallo de hardware | Réplica, RAID |
| Corrupción de datos | Copia + WAL desde antes de la corrupción |
| **Error humano** (`DROP TABLE`) | Recuperación a un punto en el tiempo |
| **Ataque** (cifrado o borrado) | Copia inmutable, fuera de línea o con retención bloqueada |
| Desastre regional | Copia en otra región |

Los dos marcados son los que la réplica **no** cubre, y son los más frecuentes. Un `DELETE` erróneo se replica en milisegundos a todas las réplicas. Un atacante con credenciales de administrador borra el primario y las réplicas.

**Una réplica no es una copia de seguridad.** Protege contra fallo de hardware y nada más.

### Tipos de copia

| Tipo | Qué es | Restauración | Verificación |
|---|---|---|---|
| **Lógica** (`pg_dump`) | SQL o formato propio | Lenta; reconstruye índices | Fácil: se puede leer |
| **Física** (`pg_basebackup`) | Archivos del clúster | Rápida | Requiere el mismo motor y versión mayor |
| **PITR** | Copia física + WAL archivado | A cualquier instante | La más completa |
| **Instantánea de volumen** | Copia del almacenamiento | Muy rápida | Debe ser atómica entre volúmenes |

La copia lógica tiene una ventaja subestimada: es legible y portable entre versiones mayores. La física es mucho más rápida de restaurar pero está atada al motor.

### La regla 3-2-1

Tres copias, en dos medios distintos, una fuera del sitio. En la práctica actual: primario + copia local + copia en almacenamiento de objetos de otra región, esta última con **retención bloqueada** para que ni siquiera un administrador comprometido pueda borrarla.

```mermaid
flowchart TD
    P[("Primario")] --> R[("Réplica<br/>fallo de hardware")]
    P --> B["Copia base<br/>diaria"]
    P --> W["Archivado continuo<br/>de WAL"]
    B --> L["Almacenamiento local<br/>RTO bajo"]
    B --> O["Objetos, otra región<br/>desastre regional"]
    O --> I["Retención bloqueada<br/>ataque"]
    W --> PITR["PITR<br/>error humano"]
    L --> T["PRUEBA MENSUAL<br/>restaurar y verificar"]
    O --> T
    T --> M["Registrar RTO real<br/>y filas verificadas"]
```

## Ejemplo trabajado

Requisito de negocio: *«no podemos perder más de 15 minutos de inscripciones y debemos volver en menos de 2 horas»*. → RPO = 15 min, RTO = 2 h.

**Configuración:**

```bash
# postgresql.conf
archive_mode = on
archive_command = 'test ! -f /archivo/%f && cp %p /archivo/%f'
archive_timeout = 300          # fuerza cierre de segmento cada 5 min → RPO ≤ 5 min

# copia base diaria
pg_basebackup -D /copias/base-$(date +%F) -Ft -z -X stream -c fast
```

**Escenario: a las 14:37 alguien ejecuta `DELETE FROM enrollments;` sin `WHERE`.**

Lo que **no** sirve:

- La réplica: recibió el `DELETE` en 12 ms.
- La copia de las 03:00 sin WAL: perdería 11 horas y media de trabajo.

Lo que sirve:

```bash
# 1. Detener el servicio y preservar el estado actual (por si acaso)
systemctl stop postgresql
mv /var/lib/postgresql/16/main /var/lib/postgresql/16/main.roto

# 2. Restaurar la copia base más reciente
tar xzf /copias/base-2026-08-19/base.tar.gz -C /var/lib/postgresql/16/main

# 3. Reproducir el WAL hasta JUSTO ANTES del error
cat > /var/lib/postgresql/16/main/postgresql.auto.conf <<'EOF'
restore_command = 'cp /archivo/%f %p'
recovery_target_time = '2026-08-19 14:36:30'
recovery_target_action = 'pause'
EOF
touch /var/lib/postgresql/16/main/recovery.signal

# 4. Arrancar; PostgreSQL reproduce y se detiene en el objetivo
systemctl start postgresql
```

**Verificación antes de promover** —este paso es el que casi nadie hace y el que evita restaurar sobre un estado equivocado—:

```sql
SELECT count(*) FROM enrollments;                       -- ¿coincide con lo esperado?
SELECT max(registrada_en) FROM enrollments;             -- ¿llega hasta 14:36?
SELECT * FROM enrollments ORDER BY registrada_en DESC LIMIT 5;
```

Solo si cuadra:

```sql
SELECT pg_wal_replay_resume();   -- o promover
```

**Cronometraje real de una prueba** sobre 500 GB:

```text
Descarga de la copia desde otra región    38 min
Descompresión y colocación                12 min
Reproducción de 11 h de WAL               24 min
Verificación de integridad y conteos       8 min
                                        --------
RTO real medido                           82 min      ✔ por debajo de las 2 h
RPO real medido                       ≤ 5 min         ✔ por debajo de 15 min
```

**Sin esta medición, el RTO es una suposición.** Y las suposiciones se descubren falsas el día del incidente, que es el peor día.

**La prueba mensual, automatizada:**

```bash
#!/usr/bin/env bash
set -euo pipefail
INICIO=$(date +%s)

restaurar_en_entorno_aislado /copias/base-mas-reciente
esperar_a_que_acepte_conexiones

# Comprobar contenido, no solo que el proceso arranque: una base
# restaurada vacía arranca perfectamente.
FILAS=$(psql -tAc "SELECT count(*) FROM enrollments")
test "$FILAS" -gt 1000000 || { echo "::error::restauración vacía: $FILAS filas"; exit 1; }
psql -tAc "SELECT count(*) FROM (
             SELECT e.student_id FROM enrollments e
             LEFT JOIN courses c ON c.id = e.course_id
             WHERE c.id IS NULL) t" | grep -qx 0 || { echo "::error::integridad"; exit 1; }

echo "RTO medido: $(( ($(date +%s) - INICIO) / 60 )) min · filas: $FILAS"
```

El punto crítico está en el comentario: **una base restaurada vacía arranca sin errores**. Comprobar que el servicio responde no demuestra nada; hay que contar el contenido.

## Comparación

| Amenaza | Réplica | Copia diaria | PITR | Copia inmutable externa |
|---|---|---|---|---|
| Fallo de disco | Sí | Sí | Sí | Sí |
| Corrupción lógica | **No** | Parcial | **Sí** | Sí |
| `DROP TABLE` | **No** | Parcial | **Sí** | Sí |
| Cifrado por atacante | **No** | **No** | **No** | **Sí** |
| Desastre regional | Si es remota | Si es remota | Si es remota | **Sí** |

## Errores frecuentes

1. **No probar nunca la restauración.** El fallo más grave y el más común.
2. **Confundir réplica con copia.** No cubre error humano ni ataque.
3. **Copias en la misma cuenta y con los mismos permisos que el primario.** Un atacante las borra también.
4. **Verificar que el servicio arranca y no el contenido.** Una base vacía arranca.
5. **No cronometrar.** El RTO declarado no coincide con el real.
6. **Copias sin cifrar en almacenamiento de objetos.** La fuga es tan grave como la pérdida.
7. **Retener el WAL sin límite o sin vigilancia.** Llena el disco del primario.

## De la clase a la operación

La métrica que resume la salud del plan es la fecha de la última restauración verificada. Si es de hace más de un mes, el plan es una hipótesis. Publicarla en el panel de operación cambia la conducta del equipo más que cualquier documento.

## Reto de transferencia

1. Deriva RPO y RTO de una conversación real de negocio, con la pregunta concreta.
2. Configura archivado continuo y realiza una recuperación a un punto en el tiempo.
3. Cronometra la restauración completa y compara con el RTO declarado.
4. Automatiza la prueba mensual con verificación de contenido, no solo de arranque.

## Preguntas de evaluación

1. ¿Por qué una réplica no protege de un `DELETE` sin `WHERE`?
2. Calcula el RPO real de tu configuración actual, en minutos.
3. ¿Qué comprobarías tras restaurar, antes de promover a producción?
4. Diseña la protección de tus copias frente a un atacante con credenciales de administrador.

---

## 🌐 El mismo problema en cada motor

**Caso:** Un respaldo que nadie ha restaurado no es un respaldo, es un archivo

La única propiedad que importa de una copia de seguridad no es que exista:
es que se pueda **restaurar y comprobar**. Y comprobar no es mirar si el
archivo pesa lo esperado: es contar lo restaurado y compararlo con el
origen.

El caso reduce esa disciplina a su forma mínima: seis notas, una copia, y la
pareja de cifras que las compara —cuántas filas y cuánto suman—. En
producción la copia la hace `pg_dump`, `mysqldump`, `mongodump` o una
instantánea del volumen; lo que aquí se compara no es la herramienta, es el
**método de verificación**, que es el mismo en todas partes y el que casi
nadie ejecuta hasta el día del incidente.

Salida esperada, idéntica en todos los motores que lo resuelven:

| copia | filas | suma |
|---|---|---|
| `origen` | `6` | `402` |
| `restaurado` | `6` | `402` |

El contrato vive en [`motores.yaml`](motores.yaml) y lo comprueba
`python scripts/verificar_equivalencia.py --clase 058`: 5 de
las 5 implementaciones se ejecutan de verdad y su
resultado se compara con esa tabla; el resto se declara como material revisado,
no ejecutado.

| Motor | ¿Resuelve el caso? | Nivel de prueba | Código | Fuente |
|---|---|---|---|---|
| PostgreSQL | sí | servicio | [código](implementaciones/postgresql/consulta.sql) | [doc oficial](https://www.postgresql.org/docs/current/continuous-archiving.html) |
| MySQL | sí | servicio | [código](implementaciones/mysql/consulta.sql) | [doc oficial](https://dev.mysql.com/doc/refman/8.4/en/backup-and-recovery.html) |
| SQLite | sí | núcleo | [código](implementaciones/sqlite/consulta.sql) | [doc oficial](https://sqlite.org/backup.html) |
| DuckDB | sí | núcleo | [código](implementaciones/duckdb/consulta.sql) | [doc oficial](https://duckdb.org/docs/stable/sql/statements/export) |
| MongoDB | sí | servicio | [código](implementaciones/mongodb/consulta.js) | [doc oficial](https://www.mongodb.com/docs/database-tools/mongodump/) |
| Redis | **no** | — | — | [doc oficial](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) |
| Apache Cassandra | **no** | — | — | [doc oficial](https://cassandra.apache.org/doc/latest/cassandra/managing/operating/backups.html) |

### Los que resuelven el caso

#### PostgreSQL · [`implementaciones/postgresql/consulta.sql`](implementaciones/postgresql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: postgresql
-- doc: https://www.postgresql.org/docs/current/continuous-archiving.html
-- nota: las dos familias, y hacen falta las dos:
--         pg_dump -Fc base > copia.dump        copia logica, portable
--         pg_basebackup + archive_command      punto en el tiempo
--       La segunda es la unica que salva de un DELETE sin WHERE a las once de
--       la noche: permite restaurar al segundo anterior.

-- === preparacion ===
DROP TABLE IF EXISTS notas_restauradas, notas;

CREATE TABLE notas (
    id         integer PRIMARY KEY,
    estudiante text NOT NULL,
    nota       integer NOT NULL
);
INSERT INTO notas (id, estudiante, nota) VALUES
    (1, 'Ada', 90), (2, 'Ada', 58), (3, 'Linus', 78),
    (4, 'Linus', 66), (5, 'Grace', 55), (6, 'Grace', 55);

-- La copia. En produccion seria pg_dump, mysqldump, mongodump o una
-- instantanea del volumen; aqui es una tabla, para que lo que se compare sea
-- el METODO de verificacion y no la herramienta.
CREATE TABLE notas_restauradas AS SELECT * FROM notas;

-- === consulta ===
-- La unica prueba que cuenta. Un respaldo que nadie ha restaurado no es un
-- respaldo: es un archivo. Y restaurarlo sin comparar tampoco prueba nada, asi
-- que la comprobacion es siempre la misma pareja: cuantas filas y que suman.
SELECT 'origen' AS copia, COUNT(*) AS filas, SUM(nota) AS suma FROM notas
UNION ALL
SELECT 'restaurado', COUNT(*), SUM(nota) FROM notas_restauradas
ORDER BY copia;
```

- **Por qué sí:** Tiene las dos familias y hacen falta las dos: `pg_dump` para una copia lógica portable entre versiones, y el archivado continuo del WAL con `pg_basebackup` para recuperación **a un punto en el tiempo**, que es lo único que salva de un `DELETE` sin `WHERE` a las once de la noche.
- **Por qué no:** `pg_dump` sobre una base grande tarda horas y la restauración tarda más, porque hay que reconstruir todos los índices. Y el archivado continuo no sirve de nada si nadie ha probado la restauración: la copia se verifica restaurando, no listando archivos.
- 📄 Documentación oficial: <https://www.postgresql.org/docs/current/continuous-archiving.html>

#### MySQL · [`implementaciones/mysql/consulta.sql`](implementaciones/mysql/consulta.sql)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```sql
-- motor: mysql
-- doc: https://dev.mysql.com/doc/refman/8.4/en/backup-and-recovery.html
-- nota: mysqldump SIN --single-transaction bloquea las tablas y puede producir
--       una copia incoherente. Y la recuperacion a un punto en el tiempo exige
--       que log_bin este activado y que los registros se conserven: comprobarlo
--       forma parte del plan de respaldo, no del de rendimiento.

-- === preparacion ===
DROP TABLE IF EXISTS notas_restauradas;
DROP TABLE IF EXISTS notas;

CREATE TABLE notas (
    id         INT PRIMARY KEY,
    estudiante VARCHAR(50) NOT NULL,
    nota       INT NOT NULL
);
INSERT INTO notas (id, estudiante, nota) VALUES
    (1, 'Ada', 90), (2, 'Ada', 58), (3, 'Linus', 78),
    (4, 'Linus', 66), (5, 'Grace', 55), (6, 'Grace', 55);

-- La copia. En produccion seria pg_dump, mysqldump, mongodump o una
-- instantanea del volumen; aqui es una tabla, para que lo que se compare sea
-- el METODO de verificacion y no la herramienta.
CREATE TABLE notas_restauradas AS SELECT * FROM notas;

-- === consulta ===
-- La unica prueba que cuenta. Un respaldo que nadie ha restaurado no es un
-- respaldo: es un archivo. Y restaurarlo sin comparar tampoco prueba nada, asi
-- que la comprobacion es siempre la misma pareja: cuantas filas y que suman.
SELECT 'origen' AS copia, COUNT(*) AS filas, SUM(nota) AS suma FROM notas
UNION ALL
SELECT 'restaurado', COUNT(*), SUM(nota) FROM notas_restauradas
ORDER BY copia;
```

- **Por qué sí:** `mysqldump` para la copia lógica y el registro binario para el punto en el tiempo; con el clon de InnoDB o XtraBackup, además, copia física en caliente sin bloquear.
- **Por qué no:** `mysqldump` sin `--single-transaction` bloquea las tablas y produce copias incoherentes entre tablas de motores distintos; y la recuperación desde el registro binario exige que ese registro esté activado y conservado, cosa que **no** es el valor por omisión en todas las instalaciones.
- 📄 Documentación oficial: <https://dev.mysql.com/doc/refman/8.4/en/backup-and-recovery.html>

#### SQLite · [`implementaciones/sqlite/consulta.sql`](implementaciones/sqlite/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: sqlite
-- doc: https://sqlite.org/backup.html
-- nota: en produccion la copia se hace SIN detener la base con
--         VACUUM INTO 'copia-2026-08-19.sqlite';
--       Lo que NO hay que hacer nunca es `cp base.sqlite copia.sqlite` mientras
--       alguien escribe: produce un archivo que parece valido y no lo es.

-- === preparacion ===
CREATE TABLE notas (
    id         INTEGER PRIMARY KEY,
    estudiante TEXT NOT NULL,
    nota       INTEGER NOT NULL
);
INSERT INTO notas (id, estudiante, nota) VALUES
    (1, 'Ada', 90), (2, 'Ada', 58), (3, 'Linus', 78),
    (4, 'Linus', 66), (5, 'Grace', 55), (6, 'Grace', 55);

-- La copia. En produccion seria pg_dump, mysqldump, mongodump o una
-- instantanea del volumen; aqui es una tabla, para que lo que se compare sea
-- el METODO de verificacion y no la herramienta.
CREATE TABLE notas_restauradas AS SELECT * FROM notas;

-- === consulta ===
-- La unica prueba que cuenta. Un respaldo que nadie ha restaurado no es un
-- respaldo: es un archivo. Y restaurarlo sin comparar tampoco prueba nada, asi
-- que la comprobacion es siempre la misma pareja: cuantas filas y que suman.
SELECT 'origen' AS copia, COUNT(*) AS filas, SUM(nota) AS suma FROM notas
UNION ALL
SELECT 'restaurado', COUNT(*), SUM(nota) FROM notas_restauradas
ORDER BY copia;
```

- **Por qué sí:** Tiene la API de respaldo en línea y la orden `VACUUM INTO`, que produce una copia coherente **mientras la base está en uso**, sin detener nada. Para una aplicación de escritorio, eso es todo lo que hace falta.
- **Por qué no:** Copiar el archivo con `cp` mientras alguien escribe produce una copia corrupta que **parece válida** hasta que se abre. Es el error de respaldo más frecuente que se comete con SQLite, y no da ningún aviso.
- 📄 Documentación oficial: <https://sqlite.org/backup.html>

#### DuckDB · [`implementaciones/duckdb/consulta.sql`](implementaciones/duckdb/consulta.sql)

✅ **verificado** — se ejecuta en CI sin servicios

```sql
-- motor: duckdb
-- doc: https://duckdb.org/docs/stable/sql/statements/export
-- nota: aqui el respaldo es exportar a un formato ABIERTO:
--         EXPORT DATABASE 'copia' (FORMAT PARQUET);
--       La copia sobrevive a la desaparicion del motor que la creo, cosa que
--       ningun volcado propietario garantiza. A cambio: no hay punto en el
--       tiempo ni copia incremental.

-- === preparacion ===
CREATE TABLE notas (
    id         INTEGER PRIMARY KEY,
    estudiante VARCHAR NOT NULL,
    nota       INTEGER NOT NULL
);
INSERT INTO notas (id, estudiante, nota) VALUES
    (1, 'Ada', 90), (2, 'Ada', 58), (3, 'Linus', 78),
    (4, 'Linus', 66), (5, 'Grace', 55), (6, 'Grace', 55);

-- La copia. En produccion seria pg_dump, mysqldump, mongodump o una
-- instantanea del volumen; aqui es una tabla, para que lo que se compare sea
-- el METODO de verificacion y no la herramienta.
CREATE TABLE notas_restauradas AS SELECT * FROM notas;

-- === consulta ===
-- La unica prueba que cuenta. Un respaldo que nadie ha restaurado no es un
-- respaldo: es un archivo. Y restaurarlo sin comparar tampoco prueba nada, asi
-- que la comprobacion es siempre la misma pareja: cuantas filas y que suman.
SELECT 'origen' AS copia, COUNT(*) AS filas, SUM(nota) AS suma FROM notas
UNION ALL
SELECT 'restaurado', COUNT(*), SUM(nota) FROM notas_restauradas
ORDER BY copia;
```

- **Por qué sí:** Aquí el respaldo es exportar a Parquet, un formato abierto que otras herramientas leen: la copia sobrevive incluso a la desaparición del motor que la creó, que es una propiedad que ningún volcado propietario tiene.
- **Por qué no:** No hay punto en el tiempo ni copia incremental: se exporta todo o nada, y lo que se pierde entre dos exportaciones se pierde del todo.
- 📄 Documentación oficial: <https://duckdb.org/docs/stable/sql/statements/export>

#### MongoDB · [`implementaciones/mongodb/consulta.js`](implementaciones/mongodb/consulta.js)

✅ **verificado** — se ejecuta contra el motor real levantado con `docker compose`

```javascript
// motor: mongodb
// doc: https://www.mongodb.com/docs/database-tools/mongodump/
// nota: mongodump sobre un conjunto de replicas NO da una copia coherente entre
//       colecciones salvo que se use --oplog, y sobre un cluster fragmentado
//       hay que detener el balanceador. Son detalles que solo se descubren
//       restaurando, y por eso hay que restaurar antes del incidente.

// === preparacion ===
db.notas.drop();
db.notas_restauradas.drop();

db.notas.insertMany([
  { _id: 1, estudiante: "Ada", nota: 90 },
  { _id: 2, estudiante: "Ada", nota: 58 },
  { _id: 3, estudiante: "Linus", nota: 78 },
  { _id: 4, estudiante: "Linus", nota: 66 },
  { _id: 5, estudiante: "Grace", nota: 55 },
  { _id: 6, estudiante: "Grace", nota: 55 },
]);

// La «restauracion»: aqui, una copia de la coleccion.
db.notas.aggregate([{ $out: "notas_restauradas" }]).toArray();

// === consulta ===
for (const [nombre, coleccion] of [["origen", db.notas],
                                   ["restaurado", db.notas_restauradas]]) {
  const r = coleccion
    .aggregate([{ $group: { _id: null, filas: { $sum: 1 }, suma: { $sum: "$nota" } } }])
    .toArray()[0];
  print(nombre + "|" + r.filas + "|" + r.suma);
}
```

- **Por qué sí:** `mongodump` y `mongorestore` para la copia lógica, y en un conjunto de réplicas se puede usar el registro de operaciones para recuperar a un punto en el tiempo.
- **Por qué no:** `mongodump` sobre un conjunto de réplicas **no** da una copia coherente entre colecciones salvo que se use `--oplog`, y sobre un clúster fragmentado la coherencia entre fragmentos exige detener el balanceador. Son detalles que solo se descubren restaurando.
- 📄 Documentación oficial: <https://www.mongodb.com/docs/database-tools/mongodump/>

### Los que no resuelven este caso — y qué se hace en su lugar

Descartar un motor con un argumento es tan formativo como usarlo. Ninguna de estas filas dice que el motor sea peor: dice que este problema no es el suyo.

| Motor | Por qué no | Qué se hace en su lugar | Fuente |
|---|---|---|---|
| Redis | El archivo RDB es una instantánea de un momento, y el AOF un registro de órdenes: los dos se pueden copiar, pero Redis casi nunca es la fuente de la verdad, así que restaurarlo no restaura nada que importe. | Tratar Redis como reconstruible: el plan de recuperación no es restaurarlo, es **volver a llenarlo** desde el sistema que sí guarda la verdad, y medir cuánto tarda ese llenado, porque ese tiempo es el de la caída. | [doc](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) |
| Apache Cassandra | Las instantáneas son por nodo y consisten en enlaces duros a las SSTables: la copia del clúster es la unión de las de todos los nodos, y **no** están tomadas en el mismo instante. No hay una copia coherente del conjunto. | Instantáneas por nodo más el archivado incremental, y aceptar que la restauración devuelve un estado *aproximadamente* coherente que hay que reparar después con `nodetool repair`. | [doc](https://cassandra.apache.org/doc/latest/cassandra/managing/operating/backups.html) |

---

## Laboratorio

```bash
python scripts/validate_repository.py
python labs/08-recovery/run_recovery_lab.py
```

Guarda como evidencia la salida completa, la versión del motor y la semilla o
los parámetros usados. Una captura sin comando no es evidencia: no se puede
repetir.

## Evaluación

| Criterio | Peso | Qué se comprueba |
|---|---:|---|
| Comprensión conceptual | 25 % | Explica el mecanismo, no solo el resultado |
| Ejecución reproducible | 25 % | Otra persona obtiene lo mismo con las instrucciones dadas |
| Interpretación basada en evidencia | 25 % | Cada conclusión se apoya en una salida o una medición |
| Límites y riesgos declarados | 25 % | Dice qué no demuestra el ejercicio y qué faltaría en producción |

La clase se da por superada cuando la respuesta explica el mecanismo, muestra
la salida que la respalda y declara al menos un límite del ejercicio.

## Fuentes de esta clase

Todo lo afirmado arriba procede de estas obras. Los identificadores viven en
[`catalog/sources.json`](../../../catalog/sources.json) y el estado de los
enlaces se comprueba con `python scripts/check_external_links.py`.

- **PostgreSQL Global Development Group** (2026). [PostgreSQL: Backup and Restore](https://www.postgresql.org/docs/current/backup.html).  
  Volcado lógico, copia de archivos y recuperación a un punto en el tiempo.
- **Laine Campbell, Charity Majors** (2017). [Database Reliability Engineering](https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/). O'Reilly. ISBN 978-1-4919-2594-2.  
  Operación, respaldos, objetivos de servicio y gestion de cambios.
- **Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy** (2016). [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/). O'Reilly. ISBN 978-1-4919-2912-4.  
  Lectura libre. Objetivos de nivel de servicio y presupuesto de error.

---

> [Programa](../../../README.md) · [Parte 11](../README.md) · [← Anterior](../../part-10-distribucion-replica-y-consistencia/057-consenso-y-transacciones-distribuidas/README.md) · [Siguiente →](../../part-11-operacion-seguridad-y-gobierno/059-migraciones-evolutivas-sin-caida/README.md)
