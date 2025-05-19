# Agentes

Aprende a crear agentes con la API de OpenAI.

Los agentes representan **sistemas que ejecutan tareas de forma inteligente**, desde flujos de trabajo simples hasta objetivos complejos y abiertos.

OpenAI ofrece un **conjunto completo de primitivas componibles para construir agentes**. Esta guía describe esas primitivas y cómo se combinan para formar una plataforma de agentes robusta.

## Descripción general

Crear agentes implica ensamblar componentes de varios dominios—como **modelos, herramientas, conocimiento y memoria, audio y voz, controles de seguridad (guardrails) y orquestación**—y OpenAI proporciona primitivas componibles para cada uno.

| Dominio                | Descripción                                                                                            | Primitivas de OpenAI                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| Modelos                | Inteligencia central capaz de razonar, tomar decisiones y procesar múltiples modalidades.              | o1, o3-mini, GPT-4.5, GPT-4o, GPT-4o-mini                                    |
| Herramientas           | Interfaz con el mundo, interactuar con el entorno, llamada de funciones, herramientas integradas, etc. | Llamada de funciones, Búsqueda web, Búsqueda en archivos, Uso de computadora |
| Conocimiento y memoria | Ampliar los agentes con conocimiento externo y persistente.                                            | Almacenes vectoriales, Búsqueda en archivos, Embeddings                      |
| Audio y voz            | Crear agentes que comprendan audio y respondan en lenguaje natural.                                    | Generación de audio, en tiempo real, Agentes de audio                        |
| Controles de seguridad | Evitar comportamientos irrelevantes, dañinos o no deseados.                                            | Moderación, Jerarquía de instrucciones                                       |
| Orquestación           | Desarrollar, desplegar, monitorear y mejorar agentes.                                                  | SDK de agentes, Trazado (Tracing), Evaluaciones, Fine-tuning                 |
| Agentes de voz         | Crear agentes que comprendan audio y respondan en lenguaje natural.                                    | API en tiempo real, Soporte de voz en el SDK de agentes                      |

## Modelos

| Modelo       | Fortalezas agenticas                                                       |
| ------------ | -------------------------------------------------------------------------- |
| o3 y o4-mini | Ideales para planificación a largo plazo, tareas complejas y razonamiento. |
| GPT-4.1      | Óptimo para ejecución agentica.                                            |
| GPT-4.1-mini | Buen equilibrio entre capacidad agentica y baja latencia.                  |
| GPT-4.1-nano | Ideal para latencia ultrabaja.                                             |

Los modelos de lenguaje grande (LLM) son el núcleo de muchos sistemas agenticos, responsables de tomar decisiones e interactuar con el mundo. Los modelos de OpenAI ofrecen amplias capacidades:

* **Alta inteligencia:** Capacidad de [razonar](/docs/guides/reasoning) y planificar para abordar tareas complejas.
* **Herramientas:** [Llamar funciones](/docs/guides/function-calling) y aprovechar [herramientas integradas](/docs/guides/tools).
* **Multimodalidad:** Comprensión nativa de texto, imágenes, audio, código y documentos.
* **Baja latencia:** Soporte para conversaciones de [audio en tiempo real](/docs/guides/realtime) y modelos más pequeños y rápidos.

Consulta la página de [modelos](/docs/models) para comparaciones detalladas.

## Herramientas

Las herramientas permiten que los agentes interactúen con el mundo. OpenAI admite [**llamada de funciones**](/docs/guides/function-calling) para conectarse con tu código y [**herramientas integradas**](/docs/guides/tools) para tareas comunes como búsqueda web o recuperación de datos.

| Herramienta          | Descripción                                           |
| -------------------- | ----------------------------------------------------- |
| Llamada de funciones | Interactuar con código definido por el desarrollador. |
| Búsqueda web         | Obtener información actualizada de la web.            |
| Búsqueda en archivos | Realizar búsquedas semánticas en tus documentos.      |
| Uso de computadora   | Comprender y controlar una computadora o navegador.   |
| Shell local          | Ejecutar comandos en una máquina local.               |

## Conocimiento y memoria

El conocimiento y la memoria permiten a los agentes almacenar, recuperar y usar información más allá de sus datos de entrenamiento. Los **almacenes vectoriales** permiten búsquedas semánticas en tus documentos para recuperar información relevante en tiempo real. Los **embeddings** representan datos de forma eficiente para una recuperación rápida, lo que impulsa soluciones de conocimiento dinámico y memoria a largo plazo.

Puedes integrar tus datos usando los [almacenes vectoriales](/docs/guides/retrieval#vector-stores) y la [API de Embeddings](/docs/guides/embeddings).

## Controles de seguridad (Guardrails)

Los controles de seguridad aseguran que tus agentes se comporten de forma segura, coherente y dentro de los límites que tú definas—lo cual es crítico en entornos de producción. Usa la [API de moderación](/docs/guides/moderation) gratuita de OpenAI para filtrar automáticamente contenido inseguro. También puedes controlar el comportamiento del agente utilizando la [jerarquía de instrucciones](https://openai.github.io/openai-agents-python/guardrails/), que prioriza tus indicaciones y mitiga comportamientos no deseados.

## Orquestación

Crear agentes es un proceso. OpenAI ofrece herramientas para construir, desplegar, monitorear, evaluar y mejorar sistemas agenticos de forma efectiva.

![Interfaz de trazado de agentes en el panel de OpenAI](https://cdn.openai.com/API/docs/images/orchestration.png)

| Fase              | Descripción                                                                                                            | Primitivas de OpenAI      |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| Crear y desplegar | Construye agentes rápidamente, aplica controles de seguridad y gestiona flujos conversacionales con el SDK de agentes. | SDK de agentes            |
| Monitorear        | Observa el comportamiento del agente en tiempo real, depura problemas y obtén información útil mediante trazado.       | Trazado (Tracing)         |
| Evaluar y mejorar | Mide el rendimiento del agente, identifica áreas de mejora y refina tu agente.                                         | Evaluaciones, Fine-tuning |

## Primeros pasos

Comienza instalando el [SDK de Agentes de OpenAI para Python](https://github.com/openai/openai-agents-python) con:

```text
pip install openai-agents
```

Explora el [repositorio](https://github.com/openai/openai-agents-python) y la [documentación](https://openai.github.io/openai-agents-python/) para más detalles.
