# 014 — DDL: el esquema como contrato ejecutable

> [Programa](../../../README.md) · [Parte 03](../README.md) · [← Anterior](../../part-02-modelo-relacional-y-algebra/013-integridad-restricciones-y-acciones-referenciales/README.md) · [Siguiente →](../../part-03-sql-en-profundidad/015-select-filtrado-proyeccion-y-orden/README.md)

Parte 03 — SQL en profundidad · Fundamentos ·
3 horas estimadas · motores `postgresql`, `sqlite`, `mysql` · laboratorio
[`labs/01-sql-foundations`](../../../labs/01-sql-foundations/README.md) · 4 fuentes.

**Conceptos centrales:** `tipo de dato` · `restricción` · `valor por defecto` · `DDL transaccional`

---

## Propósito

Escribir el esquema como un contrato ejecutable: cada línea de DDL es una promesa que el motor hace cumplir. Un esquema laxo traslada esa responsabilidad a cada programa cliente, presente y futuro.

## Resultados de aprendizaje

Al terminar podrás:

1. Elegir tipos por el dominio del dato, no por costumbre.
2. Justificar por qué el dinero no se guarda en coma flotante, con una demostración.
3. Aplicar el criterio de tipos para fechas, horas y zonas horarias.
4. Aprovechar el DDL transaccional donde existe y protegerte donde no.
5. Escribir un esquema en el que un dato inválido sea imposible, no improbable.

## Fundamentos

### El tipo es la primera restricción

Antes de cualquier `CHECK`, el tipo ya limita el dominio. Elegirlo mal deja pasar valores que ninguna restricción posterior recupera.

| Dato | Tipo correcto | Tipo frecuente y equivocado | Qué se rompe |
|---|---|---|---|
| Dinero | `NUMERIC(12,2)` / entero de centavos | `FLOAT`, `REAL` | Errores de redondeo acumulativos |
| Fecha y hora con huso | `TIMESTAMPTZ` | `TIMESTAMP` sin huso | Ambigüedad en cambios de hora |
| Fecha sin hora | `DATE` | `TEXT` | Comparaciones y aritmética imposibles |
| Identificador externo | `TEXT` con `CHECK` de formato | `INTEGER` | Se pierden ceros a la izquierda |
| Booleano | `BOOLEAN` | `INTEGER`, `CHAR(1)` | Tres estados donde debe haber dos |
| Enumeración corta | `TEXT` + `CHECK IN (...)` | `TEXT` libre | Valores nuevos sin control |
| Duración | Entero de segundos o `INTERVAL` | `TEXT` «2h 30m» | Aritmética imposible |

### Dinero en coma flotante: la demostración

Los tipos `FLOAT` y `DOUBLE` siguen IEEE 754, que representa en binario. El valor decimal `0,1` no tiene representación binaria finita, igual que 1/3 no la tiene en decimal.

```sql
SELECT 0.1 + 0.2 = 0.3;             -- en coma flotante: falso
SELECT CAST(0.1 AS REAL) + CAST(0.2 AS REAL);   -- 0.30000000000000004
```

Con 10 000 transacciones de un producto de 19,99, el error acumulado deja de ser teórico y aparece en la conciliación contable como un descuadre de céntimos que nadie sabe explicar. `NUMERIC` almacena en base 10 y es exacto para estos valores; a cambio, la aritmética es más lenta. Para dinero, esa lentitud es irrelevante y la exactitud no lo es.

### Fechas y husos horarios

`TIMESTAMP WITHOUT TIME ZONE` guarda una pared de reloj sin decir de qué reloj. Dos consecuencias:

- Un evento registrado a las 02:30 durante el retroceso del horario de verano es **ambiguo**: ocurrió dos veces.
- Comparar registros de dos regiones da resultados incorrectos sin conversión explícita.

`TIMESTAMPTZ` (en PostgreSQL) guarda un instante absoluto normalizado a UTC y lo presenta en el huso de la sesión. Regla operativa: **almacenar instantes en UTC, convertir solo al presentar**. La excepción legítima es la fecha civil sin instante —un cumpleaños, un feriado—, que es `DATE` y no tiene huso.

### DDL transaccional

| Motor | ¿`CREATE`/`ALTER` dentro de una transacción con reversión? |
|---|---|
| PostgreSQL | Sí, casi todo el DDL |
| SQLite | Sí |
| SQL Server | Sí, en su mayor parte |
| MySQL / MariaDB | **No**: cada sentencia DDL confirma implícitamente |
| Oracle | No: confirmación implícita |

La consecuencia es enorme para las migraciones. En PostgreSQL, una migración de cinco pasos que falla en el cuarto revierte entera. En MySQL, deja el esquema a medias y hay que escribir el camino de vuelta a mano. Quien despliega sobre MySQL necesita migraciones idempotentes y verificadas paso a paso (clase 049).

```mermaid
flowchart TD
    D["Regla del dominio"] --> T{"¿La limita<br/>el tipo?"}
    T -- "Sí" --> TY["Elegir el tipo exacto"]
    T -- "No" --> N{"¿Puede faltar<br/>el valor?"}
    N -- "No" --> NN["NOT NULL"]
    N -- "Sí" --> NU["Nulo con semántica documentada"]
    TY --> C{"¿Hay valores del tipo<br/>que el dominio prohíbe?"}
    NN --> C
    C -- "Sí" --> CK["CHECK"]
    C -- "No" --> OK["Listo"]
    CK --> U{"¿Debe ser único?"}
    U -- "Sí" --> UQ["UNIQUE (parcial si aplica)"]
    U -- "No" --> OK
```

## Ejemplo trabajado

Esquema laxo, del tipo que se escribe en el primer prototipo y sobrevive tres años:

```sql
CREATE TABLE pagos (
  id      INTEGER,
  alumno  TEXT,
  monto   REAL,
  fecha   TEXT,
  estado  TEXT
);
```

Valores que este esquema acepta sin protestar, y que no significan nada:

```sql
INSERT INTO pagos VALUES (1, NULL, -0.1, 'ayer', 'PAGADO');
INSERT INTO pagos VALUES (1, 'Ana', 1e308, '2026-13-45', 'pagadoo');
```

Dos filas con `id = 1`, un monto negativo, otro que desborda cualquier moneda real, dos fechas imposibles y un estado con una errata. Todo dentro del contrato, porque el contrato no dice nada.

Esquema como contrato:

```sql
CREATE TABLE pagos (
  id          INTEGER PRIMARY KEY,
  student_id  INTEGER NOT NULL REFERENCES students(id) ON DELETE RESTRICT,
  monto_clp   INTEGER NOT NULL CHECK (monto_clp > 0),
  pagado_en   TEXT    NOT NULL CHECK (pagado_en LIKE '____-__-__T__:__:__Z'),
  estado      TEXT    NOT NULL DEFAULT 'pendiente'
              CHECK (estado IN ('pendiente','pagado','anulado')),
  referencia  TEXT    UNIQUE
);
```

Decisiones y su motivo:

- **`monto_clp` como entero.** El peso chileno no tiene decimales, así que el entero es exacto y natural. Para monedas con decimales, `NUMERIC(12,2)` o enteros de centavos con el nombre del campo diciéndolo (`monto_centavos`).
- **`pagado_en` en texto ISO-8601 con `Z`.** SQLite no tiene tipo de fecha; el patrón fuerza el formato y el sufijo declara UTC. En PostgreSQL sería `TIMESTAMPTZ NOT NULL`.
- **`estado` enumerado con `CHECK`.** «pagadoo» ahora falla en la inserción, no en el informe trimestral.
- **`referencia UNIQUE`.** Impide registrar dos veces el mismo pago del proveedor: es idempotencia declarada en el esquema (clase 037).
- **`ON DELETE RESTRICT`.** Un pago es evidencia contable; borrar al estudiante no puede borrarlo.

**Comprobación de que el contrato funciona:**

```sql
INSERT INTO pagos (id, student_id, monto_clp, pagado_en, estado)
VALUES (1, 999, -500, 'ayer', 'pagadoo');
-- FOREIGN KEY constraint failed  /  CHECK constraint failed
```

Cuatro errores detectados en la inserción en lugar de cuatro incidencias en producción.

**Unicidad condicional.** Regla frecuente: «solo puede haber un pago pendiente por estudiante». Un `UNIQUE (student_id)` prohibiría también los pagados. La forma correcta es un índice único parcial:

```sql
CREATE UNIQUE INDEX pagos_un_pendiente
  ON pagos (student_id) WHERE estado = 'pendiente';
```

Disponible en PostgreSQL y SQLite. En MySQL se emula con una columna generada que vale `student_id` cuando el estado es pendiente y `NULL` en otro caso, aprovechando que los nulos no colisionan en un índice único.

## Comparación

| Decisión | Esquema laxo | Esquema como contrato |
|---|---|---|
| Dónde falla un dato malo | En el informe, semanas después | En el `INSERT`, al instante |
| Quién valida | Cada cliente, si se acuerda | El motor, siempre |
| Costo de un cliente nuevo | Reimplementar las validaciones | Ninguno |
| Migración de datos sucios | Inevitable | Innecesaria |
| Coste de escritura | Mínimo | Comprobaciones por fila (despreciable) |

## Errores frecuentes

1. **`REAL` para dinero.** Error garantizado, solo cuestión de volumen.
2. **`TEXT` para todo.** Traslada el análisis sintáctico a cada consulta y hace imposible ordenar y comparar.
3. **`VARCHAR(255)` por inercia.** El 255 viene de un límite histórico de MySQL, no del dominio. Si el límite real es 40, escribe 40.
4. **Guardar horas locales sin huso.** Se descubre en el cambio de horario, con datos ya escritos.
5. **Enumeraciones sin `CHECK`.** El estado con errata entra y contamina todos los agregados.
6. **Suponer DDL transaccional en MySQL.** Una migración a medias en producción.

## De la clase a la operación

Los proyectos de «limpieza de datos» existen porque en su día el esquema aceptó lo que no debía. Cada `CHECK` escrito hoy es un proyecto de limpieza que no ocurrirá.

## Reto de transferencia

1. Toma una tabla real y lista los valores absurdos que hoy acepta.
2. Reescribe su DDL como contrato, con tipos, `NOT NULL`, `CHECK` y `UNIQUE`.
3. Demuestra con inserciones fallidas que cada regla se aplica.
4. Escribe la consulta que encuentra los datos existentes que el nuevo contrato rechazaría, y decide qué hacer con ellos.

## Preguntas de evaluación

1. Demuestra numéricamente por qué `REAL` no sirve para dinero.
2. ¿Qué diferencia práctica hay entre `TIMESTAMP` y `TIMESTAMPTZ` durante un cambio de horario?
3. Escribe la unicidad condicional de tu dominio en dos motores distintos.
4. Tu migración falla a mitad en MySQL. Describe el estado del esquema y cómo lo recuperas.

---

## Laboratorio

```bash
python scripts/validate_repository.py
python labs/01-sql-foundations/run_lab.py
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

- **ISO/IEC JTC 1/SC 32** (2023). [ISO/IEC 9075: Information technology - Database languages - SQL](https://www.iso.org/standard/76583.html).  
  Norma del lenguaje SQL. Ningún motor la implementa por completo.
- **PostgreSQL Global Development Group** (2026). [PostgreSQL Documentation](https://www.postgresql.org/docs/current/).  
  Documentación de referencia del motor relacional principal del programa.
- **C. J. Date** (2015). [SQL and Relational Theory: How to Write Accurate SQL Code](https://www.oreilly.com/library/view/sql-and-relational/9781491941164/). 3.a ed. O'Reilly. ISBN 978-1-4919-4117-1.  
  Separa el modelo relacional de lo que SQL realmente implementa, incluidos los nulos.
- **SQLite Consortium** (2026). [SQLite Documentation](https://sqlite.org/docs.html).  
  Motor embebido usado por los laboratorios sin dependencias del programa.

---

> [Programa](../../../README.md) · [Parte 03](../README.md) · [← Anterior](../../part-02-modelo-relacional-y-algebra/013-integridad-restricciones-y-acciones-referenciales/README.md) · [Siguiente →](../../part-03-sql-en-profundidad/015-select-filtrado-proyeccion-y-orden/README.md)
