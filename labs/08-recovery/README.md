# Laboratorio 08 — Respaldo, restauración y punto en el tiempo

> Un respaldo que nunca se ha restaurado no es un respaldo: es un archivo.
> Aquí se restaura de verdad, tres veces, y solo una devuelve el estado correcto.

**Duración:** 90 minutos · **Dependencias:** Python 3.11+ (SQLite de la biblioteca estándar)
· **Marca de éxito:** `RECOVERY_LAB_OK`
· **Parte:** [10 — Operación, seguridad y gobierno](../../classes/part-11-operacion-seguridad-y-gobierno/README.md)

## 🎯 Qué demuestra

Que «tenemos respaldos» no responde a la pregunta que importa. Las preguntas son **cuánto dato
puedes perder** (RPO) y **cuánto trabajo cuesta volver** (RTO), y solo se responden restaurando.

El laboratorio provoca el desastre más común —un `DELETE` sin el filtro correcto, confirmado— y
compara tres recuperaciones: solo el respaldo, respaldo más archivo completo, y restauración a
un punto en el tiempo anterior al error.

## 🔬 Hipótesis

1. Restaurar solo el respaldo completo deja la base **congelada**: pierde todas las
   transacciones posteriores, aunque el borrado no aparezca.
2. Reproducir el archivo entero **reproduce también el desastre** con toda fidelidad. Un archivo
   no es una máquina del tiempo: es una grabación.
3. Solo la restauración a un instante anterior al error devuelve exactamente el estado bueno, y
   se puede demostrar comparando el contenido, no mirando por encima.

## ▶️ Ejecutar

```bash
python labs/08-recovery/run_recovery_lab.py
```

## 📊 Lo que verás

| Estrategia | Filas | RPO (transacciones perdidas) | Operaciones reproducidas | ¿Estado correcto? |
| --- | ---: | ---: | ---: | --- |
| solo el respaldo completo | 20 | 12 | 0 | no |
| respaldo + archivo completo | 20 | 12 | 13 | no |
| punto en el tiempo (antes del error) | 32 | 0 | 12 | **sí** |

La tercera fila es la única que cuenta, y su coste está a la vista: doce operaciones
reproducidas. Ese número, en un sistema real con horas de archivo, **es** tu RTO.

## 🧠 Por qué está hecho así

- **El respaldo se toma con la API del propio motor** (`Connection.backup`), en caliente y con
  la base recibiendo escrituras. Copiar el archivo con el sistema operativo mientras hay
  transacciones abiertas es el error clásico que produce respaldos que no abren.
- **El archivo de transacciones se modela como una lista de sentencias con su instante lógico.**
  Es el equivalente didáctico del archivado de WAL: la secuencia de cambios confirmados que
  permite avanzar desde el respaldo hasta cualquier momento posterior.
- **La comprobación no es «parece bien»:** se compara una huella del contenido —todas las filas
  ordenadas— entre la base restaurada y el estado bueno. Restaurar y no verificar es la mitad
  del trabajo, y es la mitad que falla en producción.
- **Nada se mide en segundos.** El RTO se expresa en operaciones reproducidas, que no dependen
  de tu disco.

## ⚠️ Lo que este laboratorio no demuestra

- No usa el archivado real de WAL de PostgreSQL ni `pg_basebackup`: modela su lógica.
- No cubre respaldos incrementales ni diferenciales, ni la compresión y el cifrado que exige
  cualquier política seria.
- No mide el tiempo real de restauración, que en un sistema grande domina el RTO.
- No cubre la parte más difícil de un incidente real: **darse cuenta** de que hubo un borrado
  erróneo y decidir el instante al que volver.

## 🧪 Extensiones

1. Cambia el instante de corte una transacción más atrás: verás RPO 1 y el estado deja de
   coincidir. Ese es el compromiso real de un punto en el tiempo mal elegido.
2. Añade una transacción legítima **después** del borrado y decide qué hacer: recuperar a un
   punto anterior la pierde. Es la conversación incómoda de todo incidente.
3. Corrompe el archivo (borra una entrada del medio) y observa que la recuperación produce un
   estado que no coincide con ninguno real: por eso el archivo se verifica, no solo se guarda.
4. Toma el respaldo **después** de las 12 transacciones y compara el trabajo de recuperación:
   respaldar más a menudo baja el RTO y sube el coste de almacenamiento.

## 🏭 Llevarlo a un motor real

```bash
docker compose --profile relational up -d
```

En PostgreSQL, practica `pg_basebackup`, el archivado de WAL y `recovery_target_time`;
cronometra la restauración completa y **escribe el número**: esa es la respuesta que te pedirán
en el próximo incidente. En MySQL, el equivalente es un respaldo físico más los registros
binarios con `--stop-datetime`.

## 🎓 Dónde encaja

- **Clases:** [048 — Respaldo y restauración probada](../../classes/part-11-operacion-seguridad-y-gobierno/058-respaldo-y-restauracion-probada/README.md)
  y [036 — Registro anticipado y recuperación (WAL y ARIES)](../../classes/part-08-transacciones-concurrencia-y-recuperacion/046-registro-anticipado-y-recuperacion/README.md).
- **Rutas:** [DBA / SRE de datos](../../rutas/fiabilidad-y-operacion.md),
  [Gobierno y privacidad del dato](../../rutas/gobierno-y-privacidad.md).
- **Certificaciones:** cubre de lleno el dominio de alta disponibilidad y recuperación del
  [DP-300](../../certificaciones/dp-300.md), que evalúa recomendar una estrategia por RPO/RTO y
  restaurar a un punto en el tiempo.

## 📖 Fuentes

- **C. Mohan y otros**, *ARIES* — el método de recuperación con registro anticipado del que
  desciende lo que hacen hoy los motores.
- **PostgreSQL: Backup and Restore** — respaldo físico, archivado continuo y recuperación a un
  punto en el tiempo en un motor real.
- **SQLite: Write-Ahead Logging** — el registro anticipado del motor que usa el laboratorio.
- **Laine Campbell, Charity Majors**, *Database Reliability Engineering* — por qué la prueba de
  restauración va en el calendario y no en las buenas intenciones.

Fichas completas en el [registro de fuentes](../../catalog/sources.json).

## 🧹 Limpieza

No hace falta: todo ocurre en un directorio temporal que el guion borra al terminar.
