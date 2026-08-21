# Contrato para ampliar el programa

Este documento es el contrato interno —para personas y para asistentes de
inteligencia artificial— que permite añadir clases, motores y laboratorios sin
degradar la coherencia del repositorio.

Si una instrucción de este archivo choca con lo que pide quien encarga el
cambio, gana este archivo o se cambia este archivo primero. Lo que no se puede
es saltárselo en silencio.

## 1. La regla que no se negocia

> **Ninguna clase se publica sin fuentes, y ninguna cita apunta al vacío.**

Consecuencias operativas:

- Toda clase declara **al menos dos** fuentes existentes en `catalog/sources.json`.
- Toda fuente del registro está citada por al menos una clase.
- Todo libro lleva ISBN; todo artículo, DOI o sede de publicación.
- Ninguna afirmación técnica se apoya en un blog anónimo, un foro o material
  generado por un modelo de lenguaje.

`scripts/validate_repository.py` comprueba lo anterior y falla el `push`. No es
una guía de estilo: es una puerta.

## 1 bis. La segunda regla

> **Ningún motor se compara sin decir qué se paga por usarlo.**

Consecuencias operativas:

- Todo motor de un `motores.yaml` declara `porque_si` **y** `porque_no`. Un motor
  que solo tiene ventajas no se entendió: se copió del folleto del fabricante.
- Todo motor declara `doc:`, y ese enlace **tiene que colgar del dominio oficial**
  que registra `catalog/databases.json`. Una opinión sobre PostgreSQL se apoya en
  `postgresql.org`, no en un blog.
- Un motor que **no** resuelve el caso se declara igualmente, con `aplica: no`, su
  motivo y la `alternativa` que se usa en su lugar.
- Lo que se dice que se ejecuta, se ejecuta. `ejecucion: nucleo` o `servicio`
  significa que `scripts/verificar_equivalencia.py` lo corre de verdad; si no se
  puede, se declara `declarado` y se dice por qué.

## 2. Dónde se edita cada cosa

| Quieres cambiar | Edita | **No** edites |
|---|---|---|
| La materia de una clase | `classes/**/lesson.md` | `classes/**/README.md` |
| El caso comparado y la matriz de motores | `classes/**/motores.yaml` | `classes/**/README.md` |
| El código de un motor en una clase | `classes/**/implementaciones/<motor>/` | el bloque de código del README |
| Horas, nivel, conceptos, fuentes | `curriculum.yaml` | los README |
| La bibliografía | `catalog/sources.json` | `docs/SOURCES.md` |
| Los motores cubiertos | `catalog/databases.json` | el sitio |
| El aspecto del sitio | `site/assets/*` y `scripts/generate_site.py` | el HTML de `site/` |

`classes/**/README.md`, `classes/README.md`, los índices de parte y **todo**
`site/` son artefactos generados. Editarlos a mano es trabajo que se pierde en
la siguiente generación, y la integración continua lo detecta.

## 3. Añadir una clase

1. **Declararla en `curriculum.yaml`** dentro de su parte, con identificador
   correlativo (sin huecos), `slug` en ASCII-kebab, horas entre 1 y 12, nivel,
   conceptos, motores existentes en el catálogo, laboratorio existente y sus
   fuentes.
2. **Escribir `classes/part-NN-.../NNN-slug/lesson.md`** con estas secciones,
   todas obligatorias:

   ```markdown
   ## Propósito
   ## Resultados de aprendizaje
   ## Fundamentos
   ## Ejemplo trabajado
   ## Comparación
   ## Errores frecuentes
   ## De la clase a la operación
   ## Reto de transferencia
   ## Preguntas de evaluación
   ```

3. **Escribir `motores.yaml`** con el caso y la matriz. El caso lleva título,
   contrato, columnas y la **salida esperada**, que es la misma para todos los
   motores que lo resuelvan:

   ```yaml
   caso:
     titulo: ...
     contrato: |
       Qué hay que devolver, con qué datos y en qué orden.
     columnas: [a, b]
     esperado:
       - [Ada, "90"]

   motores:
     - id: sqlite
       aplica: si
       ejecucion: nucleo          # nucleo | servicio | declarado
       archivo: implementaciones/sqlite/consulta.sql
       porque_si: ...
       porque_no: ...
       doc: https://sqlite.org/...
     - id: redis
       aplica: no
       porque_no: ...
       alternativa: ...
       doc: https://redis.io/docs/latest/...
   ```

   Reglas del caso:

   - **Al menos un motor de núcleo** (SQLite o DuckDB). Si nada se puede ejecutar
     sin servicios, no hay caso: hay una opinión.
   - La salida esperada se compara como **texto**, así que conviene evitar
     decimales y nulos, que cada cliente imprime a su manera. Un centinela
     explícito (`sin-curso`) enseña más y compara mejor.
   - Cuando la decisión no se pueda reducir a una consulta con resultado
     —consenso, CAP, gobierno del dato— se declara `modo: conceptual` y cada
     motor añade `como:` en vez de código. La clase dirá, con esas palabras, que
     ahí no hay sello de máquina.

4. **Escribir las implementaciones** en `implementaciones/<motor>/`, cada una con
   su cabecera y sus dos secciones:

   ```sql
   -- motor: postgresql
   -- doc: https://www.postgresql.org/docs/current/...
   -- nota: lo que hay que mirar en este motor y en ningún otro.

   -- === preparacion ===
   CREATE TABLE ...;
   INSERT INTO ...;

   -- === consulta ===
   SELECT ...;
   ```

   En los motores que no devuelven tablas —MongoDB, Redis, Neo4j— la consulta
   **imprime** las filas con las columnas separadas por `|`: comparar entre
   modelos distintos solo es posible sobre una forma común.

5. **Regenerar y validar:**

   ```bash
   python scripts/build_classes.py
   python scripts/generate_site.py
   python scripts/validate_repository.py
   python scripts/verificar_equivalencia.py --verbose
   ```

## 4. Qué es una clase aceptable

No basta con que las secciones existan. El criterio de contenido:

- **El ejemplo trabajado lleva números o código reales**, con su traza. «Es más
  rápido» no es un ejemplo; «de 65 790 páginas a 4, con este plan» sí lo es.
- **Se explica el mecanismo, no la receta.** Quien lea debe poder predecir el
  comportamiento en un caso que la clase no cubre.
- **Los errores frecuentes traen causa y corrección**, no solo el síntoma.
- **Se declara lo que la clase no demuestra.** Es la sección que distingue el
  material honesto del promocional.
- **Se enlaza con las clases vecinas** por su número, para que el programa se
  lea como un cuerpo y no como 74 fichas sueltas.
- **Ninguna comparación entre productos se apoya en material comercial.**
- **El `porque_no` de cada motor es concreto y comprobable.** «Puede ser lento»
  no vale; «`$lookup` no usa índices del lado interno con la misma libertad que
  un motor relacional» sí, porque se puede ir a la documentación y verificarlo.
- **Los motores descartados dicen qué se hace en su lugar.** Un `aplica: no` sin
  `alternativa` deja al lector sin salida.

Longitud mínima comprobada: 2 500 caracteres y al menos un bloque de código.
Son mínimos, no objetivos.

## 5. Añadir un motor

1. Entrada en `catalog/databases.json` con `id`, `name`, `families`,
   `core_lab`, `query` y `official_docs` en HTTPS.
2. Si `core_lab` es `true`, debe existir un laboratorio ejecutable que lo use.
   Declarar `true` sin laboratorio es prometer de más.
3. Añadir su documentación oficial a `catalog/sources.json` y citarla desde la
   clase que lo trate.
4. Si se quiere que sus implementaciones **se ejecuten**, añadir el servicio a
   `docker-compose.yml` con su healthcheck y el adaptador correspondiente en
   `SERVICIOS`, dentro de `scripts/verificar_equivalencia.py`. Mientras eso no
   exista, sus implementaciones van como `ejecucion: declarado`. Decir que algo
   se ejecuta sin ejecutarlo es la única mentira que este repositorio no admite.

## 6. Seguridad y ética

- Las credenciales del repositorio son **locales y públicas**: están en archivos
  versionados. Nunca se copian a otro entorno, y ninguna clase sugiere lo contrario.
- Ninguna clase incluye datos personales reales. El dominio canónico es sintético.
- Las técnicas ofensivas se tratan solo en su vertiente defensiva: la clase de
  inyección SQL enseña a impedirla, con el ejemplo mínimo necesario para
  entender por qué la defensa funciona.
- Toda afirmación de rendimiento declara sus condiciones y lo que **no**
  demuestra.

## 7. Antes de abrir un cambio

```bash
python scripts/validate_repository.py       # estructura, fuentes, motores, enlaces, codificación
python scripts/build_classes.py --check     # ¿quedaron README sin regenerar?
python scripts/generate_site.py --check     # ¿quedó el sitio desactualizado?
python scripts/verificar_equivalencia.py    # SQLite y DuckDB, sin servicios
python labs/01-sql-foundations/run_lab.py
python -m pytest -q
```

Y si tocaste implementaciones de motores con servicio:

```bash
docker compose --profile todo up -d --wait
python scripts/verificar_equivalencia.py --con-servicios --verbose
docker compose --profile todo down --volumes
```

Si tocaste el registro de fuentes o algún enlace `doc:`:

```bash
python scripts/check_external_links.py      # los dos registros
python scripts/check_external_links.py --solo motores
```

Todo lo anterior lo ejecuta la integración continua. Si pasa en local, `main`
seguirá en verde.
