# Dominio canónico: plataforma educativa

## Reglas

- Un estudiante puede matricularse una vez en cada curso.
- Una matrícula tiene estado `active`, `completed` o `withdrawn`.
- Una evaluación pertenece a un curso y tiene puntaje máximo positivo.
- Un estudiante solo puede enviar una respuesta si está matriculado.
- Existe como máximo una entrega vigente por evaluación y estudiante.
- El puntaje está entre cero y el máximo de la evaluación.
- Los identificadores y nombres son sintéticos.

## Patrones de acceso

1. listar estudiantes activos de un curso;
2. calcular progreso y promedio por estudiante;
3. detectar evaluaciones pendientes;
4. obtener resumen de un curso;
5. registrar una entrega de forma idempotente;
6. auditar cambios de puntaje sin sobrescribir historia en un sistema real.

El esquema inicial simplifica la auditoría para concentrarse en SQL. El proyecto final debe incorporar historial.
