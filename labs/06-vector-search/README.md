# Laboratorio 06 — Recuperación vectorial explicable

Duración: 60 minutos. Dependencia: Python 3.11+.

## Objetivo

Comprender similitud coseno y `recall@k` con vectores deterministas antes de usar embeddings externos.

```bash
python labs/06-vector-search/run_vector_lab.py
```

El script debe finalizar con `VECTOR_LAB_OK`.

## Actividades

- predice qué documento será más cercano a la consulta;
- cambia `k` y observa precisión/recall;
- agrega un filtro de autorización antes del ranking;
- explica por qué una alta similitud no garantiza verdad;
- diseña cómo borrar vectores cuando se elimina el documento original.
