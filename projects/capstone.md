# Proyecto final — Plataforma de datos defendible

## Encargo

Selecciona un dominio canónico y diseña su plataforma de datos para una primera versión y una evolución a tres años.

## Fases

1. Descubrimiento de requisitos y amenazas.
2. Modelo conceptual y patrones de acceso.
3. Alternativa simple con un solo motor.
4. Prototipo ejecutable y pruebas de invariantes.
5. Prueba de concurrencia y rendimiento.
6. Respaldo, destrucción controlada y restauración.
7. Evolución: decidir si se justifica persistencia políglota.
8. Observabilidad, capacidad y costos.
9. ADR final y defensa de 20 minutos.

## Restricciones

- datos sintéticos;
- ningún secreto en Git;
- no más de tres motores sin justificación excepcional;
- una ruta local reproducible;
- resultados acompañados de entorno y protocolo;
- plan de salida para servicios propietarios.

## Definición de terminado

Otra persona puede clonar, ejecutar, probar, destruir y restaurar el entorno siguiendo la documentación.
