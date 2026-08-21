# Modelo de aprendizaje

## Progresión

Cada módulo alterna explicación breve, práctica guiada, diagnóstico y transferencia. El estudiante debe predecir el resultado antes de ejecutar y explicar diferencias después.

## Ciclo de laboratorio

1. **Pregunta:** formular una duda comprobable.
2. **Hipótesis:** anticipar resultado y mecanismo.
3. **Control:** fijar datos, entorno y operación.
4. **Ejecución:** registrar comandos y resultados.
5. **Diagnóstico:** explicar planes, logs o estado.
6. **Transferencia:** repetir en otro motor o dominio.
7. **Decisión:** documentar uso y contraindicación.

## Niveles de evidencia

| Nivel | Evidencia |
| --- | --- |
| Reconoce | Define y distingue términos |
| Aplica | Ejecuta un caso guiado |
| Diagnostica | Explica un fallo observado |
| Transfiere | Resuelve el mismo concepto en otro motor |
| Diseña | Selecciona y defiende una arquitectura |
| Opera | Recupera, protege y mide el sistema |

## Inclusión

- instrucciones divididas en pasos observables;
- glosario antes de acrónimos;
- alternativas visuales y textuales;
- datos pequeños para equipos limitados;
- retos opcionales de profundidad;
- pausas de comprobación;
- evaluación por evidencia, no por velocidad de escritura.

El apoyo adapta la vía de acceso, no elimina el objetivo esencial de aprendizaje.

## El eje comparado

A partir de la versión 3, cada clase añade una sección que no existe en un curso
de SQL corriente: **el mismo problema resuelto en varios motores**.

Funciona así. La clase declara un **caso** —un enunciado y su salida esperada— y
lo resuelve en cada motor donde tenga sentido resolverlo. Después, por cada
motor, escribe dos cosas que pesan lo mismo:

- **Por qué sí** conviene resolverlo ahí.
- **Por qué no** — porque ningún motor sale gratis.

Y aparecen también los motores que **no** resuelven el caso, con el motivo y con
lo que se hace en su lugar. Descartar Redis para una reunión con un argumento
enseña más que usarlo bien: es la mitad del criterio de arquitectura.

### Qué demuestra la máquina y qué no

Que las respuestas coincidan no es una promesa del texto: lo ejecuta
`scripts/verificar_equivalencia.py` contra los motores reales. Pero conviene ser
exacto sobre lo que eso demuestra y lo que no:

| Demuestra | **No** demuestra |
|---|---|
| Que las implementaciones devuelven el mismo resultado | Que rindan igual |
| Que el código mostrado compila y corre | Que sea la mejor forma de escribirlo |
| Que la sintaxis es válida en ese motor | Que la decisión de arquitectura sea correcta |

Las clases marcadas como **comparación conceptual** —consenso, CAP, gobierno del
dato— no tienen salida que comparar, y lo dicen: ahí se compara lo que cada
motor **ofrece** y a qué precio, con la página oficial al lado de cada
afirmación.

### Por qué el orden es este

Primero el concepto, después los motores. Nunca al revés. Quien aprende «cómo se
hace en MongoDB» antes de saber qué es un agregado, acaba escribiendo SQL en
MongoDB o documentos en PostgreSQL. La pregunta del programa no es «¿cómo se
escribe en X?», sino **«¿qué permanece y qué cambia —y por qué— al pasar de un
motor a otro?»**.
