# Política de seguridad

No publiques vulnerabilidades con datos, credenciales o servicios reales. Describe el problema con un caso mínimo sintético y un procedimiento de reproducción seguro.

Los secretos del laboratorio deben residir en variables locales ignoradas por Git. Las credenciales de `docker-compose.yml` son deliberadamente locales y no son aptas para producción.

Áreas prioritarias:

- inyección y construcción dinámica de consultas;
- privilegios excesivos;
- puertos expuestos;
- respaldos o exportaciones accesibles;
- datos sensibles en logs;
- cifrado y rotación de claves;
- dependencias o imágenes vulnerables;
- aislamiento inadecuado entre estudiantes.

Consulta `docs/SECURITY-AND-ETHICS.md` para el tratamiento pedagógico.
