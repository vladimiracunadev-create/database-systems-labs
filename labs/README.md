# Laboratorios

Cinco de los seis laboratorios se ejecutan sin instalar nada y sin levantar ningún servidor: usan solo la biblioteca estándar de Python y se comprueban en integración continua sobre Python 3.11, 3.12 y 3.13. Los contenedores son opcionales y sirven para contrastar contra los motores reales.

| Laboratorio | Ejecutable | Dependencias | Resultado |
| --- | --- | --- | --- |
| 01 SQL foundations | `python labs/01-sql-foundations/run_lab.py` | Python 3.11+ | esquema, datos, consultas e invariantes |
| 02 Polyglot modeling | — (diseño) | editor de texto | modelo relacional, documental y grafo |
| 03 Transactions | `python labs/03-transactions/run_transactions_lab.py` | Python 3.11+ | actualización perdida reproducida y tres correcciones |
| 04 Indexing | `python labs/04-indexing/run_indexing_lab.py` | Python 3.11+ | plan antes/después y costo de escritura |
| 05 NoSQL workloads | `python labs/05-nosql-workloads/run_nosql_lab.py` | Python 3.11+ | elección por patrón de acceso, medida |
| 06 Vector search | `python labs/06-vector-search/run_vector_lab.py` | Python 3.11+ | similitud y métricas de recuperación |

Cada script termina con su marca (`LAB_OK`, `TRANSACTIONS_LAB_OK`, `INDEXING_LAB_OK`, `NOSQL_LAB_OK`, `VECTOR_LAB_OK`). Si no aparece, el laboratorio falló: el problema está en el código, no en el entorno.

## Qué se mide y qué no

Ningún laboratorio afirma nada en milisegundos. Un tiempo depende de la máquina, de la carga del momento y del sistema de archivos, así que no sirve como evidencia compartida. Lo que sí se afirma:

- **invariantes**: cuántas reservas se aceptaron para una plaza;
- **planes**: si el motor recorre la tabla o busca por índice;
- **trabajo**: instrucciones de la máquina virtual, accesos, bytes reescritos, páginas;
- **métricas de recuperación**: `recall@k` sobre vectores deterministas.

Cuando midas tiempos en tu propio motor, hazlo aparte, con repeticiones, mediana y dispersión, y declara la máquina.

Cada laboratorio debe registrar hipótesis, entorno, resultado, explicación y limpieza. No ejecutes comandos destructivos fuera de datos creados específicamente para el ejercicio.
