# Política de fuentes

Este documento explica **cómo** se cita en el repositorio. El listado de fuentes
no vive aquí: vive en [`catalog/sources.json`](../catalog/sources.json), que es
el registro único, y se publica renderizado en la
[página de fuentes](https://vladimiracunadev-create.github.io/database-systems-labs/fuentes.html).

Tener el listado en un solo sitio evita el problema que este repositorio existe
para no tener: dos bibliografías que se contradicen y nadie sabe cuál rige.

## La regla

> Ninguna clase se publica sin fuentes, y ninguna cita apunta al vacío.

Toda afirmación del programa procede de una entrada del registro. Una clase que
no declara al menos dos fuentes no pasa la validación y por tanto no llega a
`main`.

## Qué se acepta como fuente

| Tipo | Requisito para entrar en el registro |
|---|---|
| `book` | Título, edición, autoría, año, editorial e **ISBN** |
| `paper` | Autoría, año y **DOI o sede de publicación** verificable |
| `standard` | Organismo emisor, año y URL oficial |
| `docs` | Documentación **oficial** del producto o proyecto |

Todas las entradas llevan además una `note` que dice para qué sirve esa fuente
en este programa. Una fuente sin nota es una fuente que nadie sabe por qué está.

## Qué no se acepta

- Artículos de blog sin autoría identificable.
- Respuestas de foros como fundamento de una afirmación técnica.
- Material generado por un modelo de lenguaje.
- Documentación de un producto usada para afirmar algo sobre **otro** producto.
- Enlaces sin fecha de consulta a contenido que cambia.

Los enlaces de proveedores describen sus propios productos y **no** sustituyen
una comparación independiente. Cuando una clase compara motores, la comparación
se apoya en mediciones reproducibles del propio repositorio o en literatura
independiente, no en material comercial.

## Cómo se comprueba

Tres controles, en tres momentos distintos:

| Control | Qué comprueba | Cuándo |
|---|---|---|
| `scripts/validate_repository.py` | Estructura: mínimo de fuentes, citas existentes, sin fuentes huérfanas, ISBN y DOI presentes | En cada `push` |
| `scripts/check_external_links.py` | Que cada URL sigue siendo alcanzable | Semanalmente y antes de actualizar el catálogo |
| Revisión humana | Que la fuente **sostiene** lo que la clase afirma | Al escribir o modificar una clase |

El tercero no se puede automatizar y es el que más importa. Una cita puede
existir, estar viva y aun así no respaldar la frase que la invoca.

### Sobre los enlaces «protegidos»

Los sitios académicos (ACM, Springer, ISO) responden `403` a cualquier cliente
que no sea un navegador. El verificador los distingue de los enlaces rotos:

- `OK` — respondió 2xx, o 3xx hacia otra ubicación.
- `PROTEGIDO` — respondió 401/403/405/429: existe, pero rechaza clientes automáticos.
- `ROTO` — 404/410, error de red o 5xx sostenido. **Solo esto falla.**

Cuando una fuente desaparece de su ubicación original se sustituye por una copia
estable —el repositorio del autor, un espejo institucional o el Archivo de
Internet— y la nota lo declara.

## Añadir una fuente

1. Añadir la entrada a `catalog/sources.json` con todos sus campos.
2. Citarla desde al menos una clase en `curriculum.yaml`. Una fuente sin citar
   hace fallar la validación, a propósito.
3. Ejecutar `python scripts/check_external_links.py` y comprobar que no sale
   `ROTO`.
4. Regenerar los artefactos: `python scripts/build_classes.py` y
   `python scripts/generate_site.py`.

## Verificación vigente

El campo `verified_on` de `catalog/sources.json` indica la última revisión
completa del registro. Consulta de nuevo las fuentes antes de actualizar
versiones, licencias o ventanas de soporte: son exactamente los datos que
caducan sin avisar.
