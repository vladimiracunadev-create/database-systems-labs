# Laboratorio 05 — Elección por carga de trabajo en almacenes no relacionales

> La misma pareja de modelos gana o pierde según la carga. Una decisión de modelado sin carga
> declarada no es una decisión: es una preferencia.

**Duración:** 90 minutos · **Dependencias:** Python 3.11+. MongoDB y Redis, opcionales
· **Marca de éxito:** `NOSQL_LAB_OK`
· **Partes:** [05](../../classes/part-06-documentos-y-clave-valor/README.md) ·
[06](../../classes/part-07-grafos-columnas-tiempo-y-busqueda/README.md)

## 🎯 Qué demuestra

Tres riesgos que se suelen suponer resueltos y que aquí se cuentan:

1. una caché con expiración **no** da coherencia;
2. incrustar frente a referenciar se decide con la relación lectura/escritura, no por gusto;
3. una clave de partición mal elegida concentra la carga en un solo nodo.

## 🔬 Hipótesis

1. Con TTL de 300 s y sin invalidación, las lecturas posteriores a una revocación de permisos
   seguirán devolviendo el permiso viejo durante toda la ventana.
2. Con carga de lectura dominante, incrustar reducirá los accesos en un orden de magnitud y su
   coste de escritura seguirá siendo asumible.
3. Con carga de escritura dominante, la conclusión se invertirá: incrustar reescribirá muchos
   más bytes.
4. Un arreglo incrustado que crece con el uso tendrá un techo alcanzable frente al límite de
   16 MiB por documento.
5. Compartimentar la clave de partición por mes repartirá una clave caliente.

## ▶️ Ejecutar

```bash
python labs/05-nosql-workloads/run_nosql_lab.py
```

## 📊 Lo que verás

| Medición | Resultado |
| --- | --- |
| TTL frente a coherencia | 5 lecturas obsoletas sin invalidar · 0 invalidando en la escritura |
| Lectura dominante (1000 lecturas, 10 escrituras) | incrustado: 1 000 accesos y 11 320 B · referenciado: 13 000 accesos y 850 B |
| Escritura dominante (10 lecturas, 1000 escrituras) | incrustado: 1 132 000 B escritos · referenciado: 85 000 B |
| Crecimiento del agregado | ~70 492 comentarios de 238 B antes del límite de 16 MiB |
| Clave de partición | 30 000 eventos en la mayor por `student_id` · 5 000 al compartimentar por mes |

## 🧠 Por qué está hecho así

- **Reloj lógico.** El laboratorio nunca duerme: avanza el tiempo a mano. Un `sleep` haría el
  experimento lento y dependiente de la máquina sin añadir nada.
- **Se cuentan accesos y bytes,** no milisegundos. Son las magnitudes que sobreviven al cambio
  de motor y de hardware.
- **Los dos escenarios de documento usan el mismo modelo** y solo cambian la carga. Esa es toda
  la lección: la respuesta correcta depende de una variable que casi nadie declara.
- **El límite de 16 MiB no es un adorno:** es el techo real de un documento en MongoDB, y define
  cuándo un arreglo incrustado deja de ser viable.

## ⚠️ Lo que este laboratorio no demuestra

- **Modela**, no mide un motor real: los números describen el comportamiento esperado, no el
  rendimiento de MongoDB o Redis en tu infraestructura.
- No cubre índices sobre documentos, esquemas de validación ni transacciones multidocumento.
- No modela la latencia de red, que en un almacén remoto cambia el peso relativo de los accesos.
- La caché es de un solo nodo: no aparecen las incoherencias entre réplicas de caché.

## 🧪 Extensiones

1. Cambia la relación a 100 lecturas y 100 escrituras: busca el punto de equilibrio donde las
   dos opciones empatan y anótalo. Ese número es tu criterio de decisión.
2. Duplica el número de módulos de la ficha: los accesos del modelo referenciado crecen
   linealmente y los del incrustado no.
3. Modela una invalidación que falla (mensaje perdido) y cuenta las lecturas obsoletas: así se
   justifica que el TTL siga existiendo aunque haya invalidación.
4. Aplica el reparto por mes a tu propia clave caliente y comprueba si tus consultas siguen
   siendo eficientes: compartimentar abarata la escritura y encarece algunas lecturas.

## 🏭 Llevarlo a motores reales

```bash
docker compose --profile document --profile cache up -d
```

En MongoDB, contrasta el tamaño real del documento (`Object.bsonsize`) con el estimado aquí; en
Redis, comprueba el comportamiento de `EXPIRE` y la expiración perezosa frente a la activa.

## 🎓 Dónde encaja

- **Clases:** [024–027](../../classes/part-06-documentos-y-clave-valor/README.md) y
  [029 — Columnas anchas: modelar desde la consulta](../../classes/part-07-grafos-columnas-tiempo-y-busqueda/039-columnas-anchas-modelar-desde-la-consulta/README.md).
- **Rutas:** [Ingeniero de datos](../../rutas/ingenieria-de-datos.md),
  [Ingeniero de IA aplicada y recuperación](../../rutas/ia-y-recuperacion.md),
  [Desarrollador de aplicaciones](../../rutas/desarrollo-de-aplicaciones.md).
- **Certificaciones:** dominio de datos no relacionales del
  [DP-900](../../certificaciones/dp-900.md) y gestión de almacenes del
  [AWS Data Engineer Associate](../../certificaciones/aws-dea-c01.md).

## 📖 Fuentes

- **MongoDB: Data Modeling** — incrustar frente a referenciar, en la fuente oficial.
- **Redis Documentation** — expiración y el comportamiento real del TTL.
- **Apache Cassandra Documentation** — claves de partición y el efecto de una clave caliente.
- **Pramod Sadalage, Martin Fowler**, *NoSQL Distilled* — el agregado como unidad de
  consistencia.
- **Giuseppe DeCandia y otros**, *Dynamo* — el artículo del que desciende medio ecosistema de
  clave-valor distribuido.

Fichas completas en el [registro de fuentes](../../catalog/sources.json).

## 🧹 Limpieza

No hace falta para el guion. Si levantaste contenedores:
`docker compose --profile document --profile cache down -v`.
