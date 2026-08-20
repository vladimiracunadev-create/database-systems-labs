# Contribuir

1. Abre una propuesta que identifique concepto, nivel, motor y evidencia.
2. Usa las plantillas de `templates/`.
3. Conserva los datasets sintéticos y deterministas.
4. Agrega fuentes oficiales y fecha de verificación.
5. Ejecuta `python scripts/validate_repository.py`.
6. Si tocas `scripts/`, `labs/` o `tests/`, ejecuta también `python -m pytest` (necesita `pip install -r requirements-dev.txt`).
7. Un laboratorio nuevo del núcleo se ejecuta sin dependencias externas, termina con su marca `*_LAB_OK` y afirma invariantes, planes o conteos —nunca milisegundos—; añádelo a la matriz de `.github/workflows/ci.yml`.
8. No incluyas credenciales, volcados productivos, material sin licencia ni resultados inventados.

Una contribución de catálogo no equivale a un laboratorio completo. Las afirmaciones comparativas necesitan pruebas reproducibles.
