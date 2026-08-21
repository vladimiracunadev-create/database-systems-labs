# Entornos de trabajo

## Ruta A — Sin contenedores

Python 3.11+ y SQLite integrado. Es la ruta inicial y la utilizada por validación continua.

## Ruta B — Contenedores locales

Docker Desktop, Docker Engine o alternativa compatible con Compose. Levanta solo
el perfil necesario y detén los servicios al terminar:

| Perfil | Motores |
|---|---|
| `relational` | PostgreSQL, MySQL |
| `document` | MongoDB |
| `cache` | Redis |
| `graph` | Neo4j |
| `todo` | los cinco a la vez |

```bash
docker compose --profile todo up -d --wait
python scripts/verificar_equivalencia.py --con-servicios --verbose
docker compose --profile todo down --volumes
```

`--wait` no devuelve el control hasta que los healthcheck dan por sanos a los
cinco motores, así que el verificador no arranca antes de tiempo. Y `--volumes`
elimina los datos del laboratorio: nunca lo uses sobre un proyecto real.

Si la máquina ya tiene un PostgreSQL o un MySQL escuchando en el puerto de
siempre, los puertos publicados son configurables:

```bash
PGPORT=5433 MYSQL_PORT=3307 docker compose --profile relational up -d --wait
```

El verificador **no** necesita esos puertos: habla con cada motor a través de
`docker compose exec`, usando el cliente oficial que ya está dentro del
contenedor. Los puertos están publicados solo para poder conectarse con un
cliente gráfico.

### Qué se ejecuta sin contenedores

Los motores de núcleo —SQLite y DuckDB— no necesitan ningún servicio:

```bash
python scripts/verificar_equivalencia.py --verbose
```

Eso cubre las implementaciones de núcleo de las 74 clases. El resto se declara
como no ejecutado, y el informe lo dice con esas palabras.

## Ruta C — Instalación nativa

Útil para administración profunda. Documenta versión, puerto, ruta de datos y servicio. No mezcles una instalación real con las credenciales de demostración.

## Ruta D — Servicio administrado

Solo para módulos donde la administración del proveedor sea parte del objetivo. Define presupuesto, alertas de costo, región, eliminación final y política de datos. Ningún laboratorio básico requiere nube.

## Compatibilidad

Los comandos principales se documentan para PowerShell y shell POSIX cuando difieren. Las rutas dentro de scripts Python usan `pathlib`.
