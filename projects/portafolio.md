# Portafolio verificable

Al terminar el programa tendrás ocho evidencias de laboratorio, un proyecto final con su
defensa y unos cuantos registros de decisión. Eso **ya es** un portafolio; solo hace falta que
alguien pueda verlo sin tener que creerte.

> La diferencia entre un currículum y un portafolio: el currículum afirma, el portafolio
> demuestra. En este oficio, demostrar significa que otra persona ejecuta y obtiene lo mismo.

## Qué tienes al terminar

| Material | De dónde sale | Qué demuestra |
|---|---|---|
| 8 evidencias de laboratorio | [`assessments/evidencias.md`](../assessments/evidencias.md) | Que sabes medir y declarar límites |
| 1 proyecto final ejecutable | [`capstone.md`](capstone.md) | Que sabes diseñar y sostenerlo con datos |
| 3–6 registros de decisión | Clase [063](../classes/part-14-arquitectura-y-proyecto-final/073-registro-de-decisiones-y-costo-total/README.md) | Que sabes decidir y revisar la decisión |
| Retos de transferencia | Al final de cada clase | Que lo aplicaste a tu contexto real |
| Un guion de defensa | [`capstone.md`](capstone.md#la-defensa) | Que sabes explicarlo a quien pregunta |

## Cómo se publica

Un solo repositorio público, con un `README.md` que responda en treinta segundos: qué hay,
cómo se ejecuta y qué se demuestra.

```text
portafolio-datos/
  README.md                 el índice: qué demuestra cada cosa, con enlaces
  proyecto/                 el proyecto final completo
  evidencias/
    lab-01-sql/             hipótesis, comando, entorno, salida, explicación, límite
    lab-03-transacciones/
    ...
  decisiones/               los ADR, con fecha y criterio de revisión
```

Tres reglas que valen más que el diseño de la página:

1. **Ejecutable de verdad.** Un `README` con dos comandos que funcionan pesa más que diez
   capturas.
2. **Datos sintéticos siempre.** Un portafolio con datos reales de un empleador anterior es un
   problema legal, no un mérito.
3. **Límites declarados.** «Esto no mide latencia real» es la frase que distingue a quien
   entiende de quien presume.

## Cómo se enseña en una entrevista

No lo enseñes entero: lleva **una** evidencia y ofrécela.

- Para un puesto de desarrollo: la del [laboratorio 03](../labs/03-transactions/README.md). Casi
  todo el mundo ha vendido dos veces el mismo asiento; poca gente puede reproducirlo y explicar
  las tres correcciones con sus costos.
- Para operación o fiabilidad: la del [laboratorio 08](../labs/08-recovery/README.md), con tu
  RPO y tu RTO en números. La pregunta «¿cuánto tardaríais en volver?» aparece siempre y casi
  nadie la responde con un dato.
- Para ingeniería de datos o analítica: el grano de tus tablas de hechos y la prueba de que
  reprocesar no duplica.
- Para arquitectura: un ADR con la alternativa que descartaste. Sirve más que el diagrama.

Y una respuesta preparada para la pregunta que decide la entrevista: **«¿qué no demuestra
esto?»**.

## Lo que este portafolio no es

- **No es experiencia.** No sustituye haber operado un sistema con usuarios reales, con guardias
  y con presupuesto. Dice que sabes el mecanismo y que trabajas con método; el resto se gana
  trabajando, y conviene decirlo así en la entrevista.
- **No es un certificado.** Si necesitas una credencial para pasar un filtro de RR. HH., mira
  las [certificaciones](../certificaciones/README.md) y su cobertura medida.
- **No caduca, pero envejece.** Vuelve una vez al año, ejecútalo entero y actualiza lo que ya no
  corra. Un portafolio que no arranca resta.

## Un detalle que sorprende a la gente

Este repositorio es, él mismo, un ejemplo del método: cada afirmación con su fuente, cada
artefacto generado y comprobado, y una [suite de pruebas](../tests/) que rompe el validador a
propósito para exigir que detecte el error. Si tu portafolio se parece a eso —aunque sea a
escala mínima—, ya está por encima de la media.
