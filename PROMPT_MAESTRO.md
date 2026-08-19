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

## 2. Dónde se edita cada cosa

| Quieres cambiar | Edita | **No** edites |
|---|---|---|
| La materia de una clase | `classes/**/lesson.md` | `classes/**/README.md` |
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

3. **Regenerar y validar:**

   ```bash
   python scripts/build_classes.py
   python scripts/generate_site.py
   python scripts/validate_repository.py
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
  lea como un cuerpo y no como 64 fichas sueltas.
- **Ninguna comparación entre productos se apoya en material comercial.**

Longitud mínima comprobada: 2 500 caracteres y al menos un bloque de código.
Son mínimos, no objetivos.

## 5. Añadir un motor

1. Entrada en `catalog/databases.json` con `id`, `name`, `families`,
   `core_lab`, `query` y `official_docs` en HTTPS.
2. Si `core_lab` es `true`, debe existir un laboratorio ejecutable que lo use.
   Declarar `true` sin laboratorio es prometer de más.
3. Añadir su documentación oficial a `catalog/sources.json` y citarla desde la
   clase que lo trate.

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
python scripts/validate_repository.py     # estructura, fuentes, enlaces, codificación
python scripts/build_classes.py --check   # ¿quedaron README sin regenerar?
python scripts/generate_site.py --check   # ¿quedó el sitio desactualizado?
python labs/01-sql-foundations/run_lab.py
python labs/06-vector-search/run_vector_lab.py
python scripts/check_external_links.py    # opcional; obligatorio si tocaste el registro
```

Los cinco primeros son los que ejecuta la integración continua. Si pasan en
local, `main` seguirá en verde.
