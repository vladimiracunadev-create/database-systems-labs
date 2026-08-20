# Laboratorios

Siete de los ocho laboratorios se ejecutan sin instalar nada y sin levantar ningún servidor:
usan solo la biblioteca estándar de Python y se comprueban en integración continua sobre
Python 3.11, 3.12 y 3.13. Los contenedores son opcionales y sirven para contrastar contra los
motores reales.

| Laboratorio | Ejecutable | Qué demuestra |
| --- | --- | --- |
| [01 SQL foundations](01-sql-foundations/README.md) | `python labs/01-sql-foundations/run_lab.py` | consultas e invariantes sobre el dominio canónico |
| [02 Polyglot modeling](02-polyglot-modeling/README.md) | — (se entrega escrito) | el mismo dominio en relacional, documental y grafo |
| [03 Transactions](03-transactions/README.md) | `python labs/03-transactions/run_transactions_lab.py` | actualización perdida reproducida y tres correcciones |
| [04 Indexing](04-indexing/README.md) | `python labs/04-indexing/run_indexing_lab.py` | plan y trabajo antes y después del índice, y su costo |
| [05 NoSQL workloads](05-nosql-workloads/README.md) | `python labs/05-nosql-workloads/run_nosql_lab.py` | TTL frente a coherencia, incrustar frente a referenciar |
| [06 Vector search](06-vector-search/README.md) | `python labs/06-vector-search/run_vector_lab.py` | similitud coseno y `recall@k` sobre vectores deterministas |
| [07 Replication](07-replication/README.md) | `python labs/07-replication/run_replication_lab.py` | lecturas obsoletas, garantías de sesión y quórum |
| [08 Recovery](08-recovery/README.md) | `python labs/08-recovery/run_recovery_lab.py` | RPO, RTO y restauración a un punto en el tiempo |

Cada guion termina con su marca (`LAB_OK`, `TRANSACTIONS_LAB_OK`, `INDEXING_LAB_OK`,
`NOSQL_LAB_OK`, `VECTOR_LAB_OK`, `REPLICATION_LAB_OK`, `RECOVERY_LAB_OK`). Si no aparece, el
laboratorio falló: el problema está en el código, no en el entorno.

## Qué se mide y qué no

Ningún laboratorio afirma nada en milisegundos. Un tiempo depende de la máquina, de la carga del
momento y del sistema de archivos, así que no sirve como evidencia compartida. Lo que sí se
afirma:

- **invariantes**: cuántas reservas se aceptaron para una plaza;
- **planes**: si el motor recorre la tabla o busca por índice;
- **trabajo**: instrucciones de la máquina virtual, accesos, bytes reescritos, páginas;
- **garantías**: cuántas lecturas no vieron la escritura propia del cliente;
- **recuperación**: transacciones perdidas (RPO) y operaciones reproducidas;
- **métricas de recuperación de información**: `recall@k` sobre vectores deterministas.

Cuando midas tiempos en tu propio motor, hazlo aparte, con repeticiones, mediana y dispersión, y
declara la máquina.

## Cómo se lee una guía de laboratorio

Todas siguen la misma estructura, para que puedas ir directo a lo que necesitas:

| Sección | Para qué sirve |
| --- | --- |
| Qué demuestra | La afirmación que el laboratorio sostiene |
| Hipótesis | Lo que deberías predecir **antes** de ejecutar |
| Ejecutar | El comando exacto |
| Lo que verás | La salida real, para comparar |
| Por qué está hecho así | Las decisiones de diseño del experimento |
| Lo que **no** demuestra | El límite declarado, que es lo que separa evidencia de propaganda |
| Extensiones | Qué cambiar y qué debería pasar |
| Llevarlo a un motor real | El mismo experimento con contenedores |
| Dónde encaja | Clases, rutas por rol y certificaciones |
| Fuentes | De dónde sale el criterio |

## Registro de evidencia

Cada laboratorio debe registrar hipótesis, entorno, resultado, explicación y limpieza. Una
captura sin comando no es evidencia: no se puede repetir. No ejecutes comandos destructivos
fuera de datos creados específicamente para el ejercicio.

## Contenedores

```bash
docker compose --profile relational up -d          # PostgreSQL y MySQL
docker compose --profile document --profile cache up -d   # MongoDB y Redis
```

Las credenciales del `compose` son locales y están a la vista en un archivo versionado. **Nunca
deben copiarse a otro entorno.** Al terminar: `docker compose --profile <perfil> down -v`.
