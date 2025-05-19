## Inicio rápido para desarrolladores

Da tus primeros pasos con la API de OpenAI.

La API de OpenAI ofrece una interfaz simple para acceder a modelos de IA de última generación para generación de texto, procesamiento de lenguaje natural, visión por computadora y más. Este ejemplo genera [texto a partir de un mensaje](/docs/guides/text), como lo harías usando [ChatGPT](https://chatgpt.com).

### Generar texto desde un modelo

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="Escribe un cuento de buenas noches en una sola oración sobre un unicornio."
)

print(response.output_text)
```

### Retención de datos para respuestas del modelo

Las respuestas se conservan durante 30 días por defecto. Puedes verlas en la página de [registros](/logs?api=responses) del panel o [recuperarlas mediante la API](/docs/api-reference/responses/get). Puedes desactivar esta opción estableciendo `store` en `false` al crear la respuesta.

OpenAI no utiliza los datos enviados por API para entrenar nuestros modelos sin tu consentimiento explícito—[más información](/docs/guides/your-data).

* [Configura tu entorno de desarrollo](/docs/libraries)
* [Aplicación de inicio con Responses](https://github.com/openai/openai-responses-starter-app)
* [Guía sobre generación de texto y prompts](/docs/guides/text)

---

## Analizar entradas de imagen

También puedes proporcionar imágenes como entrada al modelo. Escanea recibos, analiza capturas de pantalla o detecta objetos en el mundo real con [visión por computadora](/docs/guides/images).

### Analizar el contenido de una imagen

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "user", "content": "¿Qué dos equipos están jugando en esta foto?"},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/LeBron_James_Layup_%28Cleveland_vs_Brooklyn_2018%29.jpg"
                }
            ]
        }
    ]
)

print(response.output_text)
```

* [Guía de visión por computadora](/docs/guides/images)

---

## Extiende el modelo con herramientas

Dale al modelo acceso a nuevos datos y capacidades usando [herramientas](/docs/guides/tools). Puedes invocar tu propio [código personalizado](/docs/guides/function-calling) o usar las [herramientas integradas de OpenAI](/docs/guides/tools). Este ejemplo usa [búsqueda web](/docs/guides/tools-web-search) para acceder a la información más reciente en Internet.

### Obtener información desde Internet para la respuesta

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "web_search_preview"}],
    input="¿Cuál fue una noticia positiva de hoy?"
)

print(response.output_text)
```

* [Usar herramientas integradas](/docs/guides/tools)
* [Guía de llamadas a funciones personalizadas](/docs/guides/function-calling)

---

## Ofrece experiencias de IA ultrarrápidas

Usando la nueva [API en tiempo real](/docs/guides/realtime) o [eventos transmitidos](/docs/guides/streaming-responses), puedes crear experiencias de alto rendimiento y baja latencia para tus usuarios.

### Transmitir eventos desde el servidor

```python
from openai import OpenAI
client = OpenAI()

stream = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": "Di 'baño de burbujas dobles' diez veces rápido.",
        },
    ],
    stream=True,
)

for event in stream:
    print(event)
```

* [Usar eventos transmitidos](/docs/guides/streaming-responses)
* [Empezar con la API en tiempo real](/docs/guides/realtime)

---

## Crear agentes

Usa la plataforma de OpenAI para crear [agentes](/docs/guides/agents) capaces de actuar—como [controlar computadoras](/docs/guides/tools-computer-use)—en nombre de tus usuarios. Usa el [SDK de agentes para Python](/docs/guides/agents-sdk) para orquestar la lógica desde el backend.

```python
from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Agente en español",
    instructions="Solo hablas español.",
)

english_agent = Agent(
    name="Agente en inglés",
    instructions="Solo hablas inglés.",
)

triage_agent = Agent(
    name="Agente de triaje",
    instructions="Entrega al agente apropiado según el idioma de la solicitud.",
    handoffs=[spanish_agent, english_agent],
)

async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

# ¡Hola! Estoy bien, gracias por preguntar. ¿Y tú, cómo estás?
```

* [Crear agentes capaces de actuar](/docs/guides/agents)

---

## Explora más

Apenas hemos tocado la superficie de lo que es posible con la plataforma de OpenAI. Aquí tienes algunos recursos adicionales:

* [Profundiza en prompts y generación de texto](/docs/guides/text)
* [Analiza contenido de imágenes](/docs/guides/images)
* [Genera datos JSON estructurados](/docs/guides/structured-outputs)
* [Invoca código personalizado](/docs/guides/function-calling)
* [Usa tus propios datos o la web](/docs/guides/tools)
* [Aplicación de inicio con Responses](https://github.com/openai/openai-responses-starter-app)
* [Construye agentes que actúan por el usuario](/docs/guides/agents)
* [Referencia completa de la API](/docs/api-reference)


