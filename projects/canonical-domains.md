# Dominios canónicos

Cinco dominios sobre los que se trabaja en todo el programa. No son ejemplos de juguete
elegidos por comodidad: cada uno está aquí porque **rompe** de una forma distinta, y esas
formas de romper son justo lo que hay que aprender a ver.

Elige uno para el [proyecto final](capstone.md) y quédate con él. Cambiar de dominio a mitad
del programa cuesta más de lo que parece, y perderse la evolución de un mismo sistema es
perderse la parte interesante.

## Cómo elegir

| Si te interesa… | Elige | Porque su dificultad central es… |
|---|---|---|
| El modelado y la privacidad | Plataforma educativa | Datos personales de menores y agregados que no deben reidentificar |
| La concurrencia y el dinero | Comercio electrónico | Dos personas comprando la última unidad |
| La integridad absoluta | Libro contable | Ninguna operación puede crear ni destruir valor |
| Los grafos y la escala de lectura | Red social | Un feed que no se puede calcular en tiempo real ingenuamente |
| La recuperación y los permisos | Memoria para agentes | Aislar por usuario y borrar de verdad |

---

## 1. Plataforma educativa y psicométrica

Personas, cursos, instrumentos de evaluación, aplicaciones, respuestas, puntajes e informes.

- **Invariante que no puede romperse:** un puntaje siempre procede de respuestas registradas y
  de una versión concreta del instrumento; recalcular con otra versión sin decirlo invalida el
  informe.
- **Patrón de acceso dominante:** escritura moderada durante la aplicación, lectura intensa al
  generar informes por grupo.
- **Dato sensible:** respuestas individuales, a menudo de menores. Los agregados por grupos
  pequeños reidentifican con facilidad.
- **Dificultad real:** operar sin conexión durante la aplicación y reconciliar después, sin
  duplicar ni perder respuestas.
- **Dónde se trabaja:** es el dominio del [laboratorio 01](../labs/01-sql-foundations/README.md)
  y del [conjunto de datos de referencia](../reference-data/school/DOMAIN.md).

## 2. Comercio electrónico

Catálogo, inventario, precios, carritos, pedidos, pagos y envíos.

- **Invariante que no puede romperse:** no se vende más inventario del que existe; un pago
  confirmado tiene siempre un pedido, y solo uno.
- **Patrón de acceso dominante:** lectura masiva del catálogo, escrituras concentradas y
  concurrentes sobre pocas filas calientes.
- **Dato sensible:** direcciones y medios de pago. El número de tarjeta no se guarda: se
  tokeniza.
- **Dificultad real:** la reserva concurrente del último artículo, y los reintentos del cliente
  de pago, que exigen idempotencia de extremo a extremo.
- **Dónde se trabaja:** el [laboratorio 03](../labs/03-transactions/README.md) reproduce
  exactamente su fallo característico.

## 3. Libro contable y pagos

Cuentas, asientos de doble entrada, transferencias, conciliación y auditoría.

- **Invariante que no puede romperse:** la suma de los asientos de cada transacción es cero, y
  el saldo es una **proyección** del libro, nunca un número que se edita.
- **Patrón de acceso dominante:** escritura estrictamente ordenada e inmutable; lectura por
  rangos de tiempo y por cuenta.
- **Dato sensible:** todo. Además, el histórico no se corrige: se compensa con un asiento nuevo.
- **Dificultad real:** un reintento no puede crear valor. La idempotencia aquí no es una buena
  práctica: es la diferencia entre un sistema contable y un fraude accidental.
- **Dónde se trabaja:** [transacciones](../classes/part-07-transacciones-concurrencia-y-recuperacion/README.md)
  y [recuperación](../labs/08-recovery/README.md), donde el instante al que restauras decide
  qué operaciones existieron.

## 4. Red social

Usuarios, publicaciones, comentarios, reacciones, seguidores, moderación y recomendaciones.

- **Invariante que no puede romperse:** lo que un usuario bloquea no le llega; lo que se borra
  desaparece también de las copias derivadas —feeds, cachés, índices de búsqueda—.
- **Patrón de acceso dominante:** lectura muy superior a la escritura, con una distribución
  brutalmente desigual: unas pocas cuentas concentran la carga.
- **Dato sensible:** relaciones sociales y contenido privado; el grafo de seguidores es un dato
  personal por sí mismo.
- **Dificultad real:** el feed. Calcularlo al leer no escala; calcularlo al escribir multiplica
  el trabajo de las cuentas con millones de seguidores. La respuesta real es híbrida.
- **Dónde se trabaja:** [grafos](../classes/part-06-grafos-columnas-tiempo-y-busqueda/README.md),
  [claves calientes](../labs/05-nosql-workloads/README.md) y
  [réplica](../labs/07-replication/README.md).

## 5. Memoria para agentes de inteligencia artificial

Fuentes, fragmentos, permisos, embeddings, sesiones, herramientas y trazas.

- **Invariante que no puede romperse:** un usuario nunca recupera un fragmento que no tiene
  permiso de leer, y si el documento original desaparece, sus vectores desaparecen con él.
- **Patrón de acceso dominante:** búsqueda por similitud con filtros de permiso, y escritura por
  lotes al reindexar.
- **Dato sensible:** todo lo que la organización haya indexado sin mirar, que suele ser más de
  lo que cree.
- **Dificultad real:** la procedencia. Cuando el sistema responde, hay que poder decir de qué
  documento salió cada afirmación y con qué versión del índice.
- **Dónde se trabaja:** [vectores y RAG](../classes/part-12-vectores-recuperacion-y-rag/README.md)
  y el [laboratorio 06](../labs/06-vector-search/README.md).

---

## El contrato común

Elijas el que elijas, la entrega tiene que declarar estas nueve cosas. Son las mismas que te
preguntará cualquiera que revise una arquitectura de datos:

1. **Invariantes** — qué tiene que ser siempre verdad, y qué prueba lo comprueba.
2. **Patrones de acceso** — las consultas reales, con su frecuencia relativa.
3. **Clasificación de datos** — qué es personal, qué es sensible y qué es público.
4. **Escala inicial y crecimiento** — volumen hoy y a tres años, con la fuente del número.
5. **Consistencia y disponibilidad** — qué garantía se ofrece y qué se sacrifica al fallar.
6. **RPO y RTO** — cuánto dato se puede perder y cuánto se tarda en volver, en números.
7. **Estrategia de migración** — cómo se llega hasta aquí y cómo se vuelve atrás.
8. **Métricas y costo** — qué se vigila y qué cuesta operarlo, personas incluidas.
9. **Alternativa más simple** — el diseño de un solo motor, y por qué no basta.

El punto 9 es el que más proyectos suspende. Casi siempre **sí** basta, y descubrirlo a tiempo
vale más que la arquitectura elegante que no hacía falta.
