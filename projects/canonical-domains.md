# Dominios canónicos

## 1. Plataforma educativa y psicométrica

Personas, cursos, instrumentos, aplicaciones, respuestas, puntajes e informes. Requiere privacidad, operación offline eventual, trazabilidad de correcciones y agregados que no reidentifiquen grupos pequeños.

## 2. Comercio electrónico

Catálogo, inventario, precios, carritos, pedidos, pagos y envíos. Permite estudiar reservas concurrentes, búsquedas, eventos, idempotencia y consistencia entre servicios.

## 3. Libro contable y pagos

Cuentas, asientos de doble entrada, transferencias, conciliación y auditoría. Ninguna operación puede crear o destruir valor por un reintento. El saldo es una proyección verificable del libro.

## 4. Red social

Usuarios, publicaciones, comentarios, reacciones, seguidores, moderación y recomendaciones. Permite comparar joins, documentos, grafos, feeds y búsqueda.

## 5. Memoria para agentes de IA

Fuentes, fragmentos, permisos, embeddings, sesiones, herramientas y trazas. Requiere procedencia, aislamiento por usuario, borrado coherente y evaluación de recuperación.

## Contrato común

Cada implementación debe declarar:

- invariantes;
- patrones de acceso;
- clasificación de datos;
- escala inicial y crecimiento;
- consistencia y disponibilidad;
- RPO/RTO;
- estrategia de migración;
- métricas y costo;
- alternativa más simple.
