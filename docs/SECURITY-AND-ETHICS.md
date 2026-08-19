# Seguridad, privacidad y ética

## Datos de aprendizaje

Usa identificadores ficticios y datos sintéticos. No copies bases productivas aunque reemplaces nombres: combinaciones de fechas, cursos, ubicaciones o resultados pueden reidentificar personas.

## Controles mínimos

- credenciales fuera del código;
- conexiones cifradas fuera del equipo local;
- roles separados para migración, aplicación, lectura y respaldo;
- consultas parametrizadas;
- puertos locales enlazados a `127.0.0.1`;
- logs sin secretos ni datos sensibles;
- respaldos cifrados y con acceso restringido;
- eliminación comprobable de exportaciones temporales.

## Contextos educativos y psicométricos

Resultados de evaluación, necesidades educativas, comportamiento y salud requieren tratamiento reforzado. El acceso debe obedecer finalidad, rol y mínimo necesario. Un informe agregado no debe permitir inferir a una persona en grupos pequeños.

## Contextos financieros

Un saldo calculado no reemplaza un libro contable inmutable y conciliable. Diseña doble registro, idempotencia, auditoría, segregación de funciones y reconciliación.

## IA y vectores

Los embeddings pueden filtrar información del origen y deben heredar su clasificación y política de borrado. Evalúa aislamiento entre usuarios, procedencia, envenenamiento del conocimiento y derecho de eliminación.

## Práctica de ataques

Solo en datos y servicios locales deliberadamente vulnerables. Nunca escanees ni pruebes sistemas ajenos o productivos.
