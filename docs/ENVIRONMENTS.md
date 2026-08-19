# Entornos de trabajo

## Ruta A — Sin contenedores

Python 3.11+ y SQLite integrado. Es la ruta inicial y la utilizada por validación continua.

## Ruta B — Contenedores locales

Docker Desktop, Docker Engine o alternativa compatible con Compose. Levanta solo el perfil necesario y detén servicios al terminar:

```bash
docker compose --profile relational up -d
docker compose --profile relational down --volumes
```

`--volumes` elimina datos del laboratorio; nunca lo uses sobre un proyecto real.

## Ruta C — Instalación nativa

Útil para administración profunda. Documenta versión, puerto, ruta de datos y servicio. No mezcles una instalación real con las credenciales de demostración.

## Ruta D — Servicio administrado

Solo para módulos donde la administración del proveedor sea parte del objetivo. Define presupuesto, alertas de costo, región, eliminación final y política de datos. Ningún laboratorio básico requiere nube.

## Compatibilidad

Los comandos principales se documentan para PowerShell y shell POSIX cuando difieren. Las rutas dentro de scripts Python usan `pathlib`.
