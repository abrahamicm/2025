
# Estado de conversación

Aprende a gestionar el estado de la conversación durante una interacción con el modelo.

OpenAI ofrece varias formas de manejar el estado de la conversación, lo cual es importante para preservar información a lo largo de múltiples mensajes o turnos en una conversación.

## Gestionar manualmente el estado de la conversación

Aunque cada solicitud de generación de texto es independiente y sin estado (a menos que utilices la [API de Asistentes](/docs/assistants/overview)), aún puedes implementar **conversaciones de varios turnos** proporcionando mensajes adicionales como parámetros en tu solicitud de generación de texto. Considera este chiste:

### Construir manualmente una conversación anterior

```javascript
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4o-mini",
    input: [
        { role: "user", content: "toc toc." },
        { role: "assistant", content: "¿Quién es?" },
        { role: "user", content: "Naranja." },
    ],
});

console.log(response.output_text);
```

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {"role": "user", "content": "toc toc."},
        {"role": "assistant", "content": "¿Quién es?"},
        {"role": "user", "content": "Naranja."},
    ],
)

print(response.output_text)
```

Al usar mensajes alternos con los roles `user` y `assistant`, capturas el estado previo de la conversación en una sola solicitud al modelo.

Para compartir manualmente el contexto entre respuestas generadas, incluye la respuesta anterior del modelo como entrada, y añade esa entrada a tu siguiente solicitud.

En el siguiente ejemplo, se le pide al modelo que cuente un chiste, y luego otro. Al agregar respuestas anteriores a nuevas solicitudes, las conversaciones se sienten más naturales y conservan el contexto de interacciones previas.

### Gestionar manualmente el estado de la conversación con la API de Responses

```javascript
import OpenAI from "openai";

const openai = new OpenAI();

let history = [
    {
        role: "user",
        content: "cuéntame un chiste",
    },
];

const response = await openai.responses.create({
    model: "gpt-4o-mini",
    input: history,
    store: true,
});

console.log(response.output_text);

// Añadir la respuesta al historial
history = [
    ...history,
    ...response.output.map((el) => {
        // TODO: Eliminar este paso
        delete el.id;
        return el;
    }),
];

history.push({
    role: "user",
    content: "cuéntame otro",
});

const secondResponse = await openai.responses.create({
    model: "gpt-4o-mini",
    input: history,
    store: true,
});

console.log(secondResponse.output_text);
```

```python
from openai import OpenAI

client = OpenAI()

history = [
    {
        "role": "user",
        "content": "cuéntame un chiste"
    }
]

response = client.responses.create(
    model="gpt-4o-mini",
    input=history,
    store=False
)

print(response.output_text)

# Añadir la respuesta a la conversación
history += [{"role": el.role, "content": el.content} for el in response.output]

history.append({ "role": "user", "content": "cuéntame otro" })

second_response = client.responses.create(
    model="gpt-4o-mini",
    input=history,
    store=False
)

print(second_response.output_text)
```

## APIs de OpenAI para el estado de conversación

Nuestras APIs facilitan la gestión automática del estado de conversación, evitando tener que pasar las entradas manualmente en cada turno.

Comparte contexto entre respuestas generadas con el parámetro `previous_response_id`. Este parámetro te permite encadenar respuestas y crear una conversación en forma de hilo.

En el siguiente ejemplo, se le pide al modelo contar un chiste. Luego, en una solicitud separada, se le pide que explique por qué es gracioso, y el modelo tiene el contexto necesario para dar una buena respuesta.

### Gestionar manualmente el estado de conversación con la API de Responses

```javascript
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4o-mini",
    input: "cuéntame un chiste",
    store: true,
});

console.log(response.output_text);

const secondResponse = await openai.responses.create({
    model: "gpt-4o-mini",
    previous_response_id: response.id,
    input: [{"role": "user", "content": "explica por qué es gracioso."}],
    store: true,
});

console.log(secondResponse.output_text);
```

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="cuéntame un chiste",
)
print(response.output_text)

second_response = client.responses.create(
    model="gpt-4o-mini",
    previous_response_id=response.id,
    input=[{"role": "user", "content": "explica por qué es gracioso."}],
)
print(second_response.output_text)
```

## Retención de datos de las respuestas del modelo

Los objetos de respuesta se guardan durante 30 días de forma predeterminada. Puedes verlos en la página de [registros](/logs?api=responses) del panel o [recuperarlos](/docs/api-reference/responses/get) a través de la API. Puedes desactivar este comportamiento configurando `store` en `false` al crear una respuesta.

OpenAI no utiliza los datos enviados a través de la API para entrenar nuestros modelos sin tu consentimiento explícito—[más información](/docs/guides/your-data).

Incluso al usar `previous_response_id`, todos los tokens de entrada de respuestas anteriores en la cadena se facturan como tokens de entrada en la API.

## Gestión de la ventana de contexto

Comprender las ventanas de contexto te ayudará a crear conversaciones encadenadas y a gestionar el estado entre interacciones con el modelo.

La **ventana de contexto** es el número máximo de tokens que pueden usarse en una sola solicitud. Este número máximo incluye los tokens de entrada, salida y, en algunos modelos, de razonamiento. Para conocer la ventana de contexto de tu modelo, consulta los [detalles del modelo](/docs/models).

### Gestión del contexto en generación de texto

A medida que tus entradas se vuelvan más complejas, o incluyas más turnos en una conversación, deberás considerar los límites tanto de **tokens de salida** como de **ventana de contexto**. Las entradas y salidas del modelo se miden en [**tokens**](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them), que se analizan y ensamblan para generar respuestas coherentes. Los modelos tienen límites sobre el uso de tokens durante el ciclo de vida de una solicitud.

* **Tokens de salida**: son los tokens generados por el modelo en respuesta a un prompt. Cada modelo tiene diferentes [límites de tokens de salida](/docs/models). Por ejemplo, `gpt-4o-2024-08-06` puede generar hasta 16,384 tokens de salida.
* **Ventana de contexto**: describe el total de tokens que pueden usarse entre entrada, salida y (en algunos modelos) [tokens de razonamiento](/docs/guides/reasoning). Consulta los [límites de ventana de contexto](/docs/models). Por ejemplo, `gpt-4o-2024-08-06` tiene una ventana de contexto total de 128,000 tokens.

Si creas un prompt muy grande —por ejemplo, incluyendo contexto adicional, datos o ejemplos— corres el riesgo de exceder la ventana de contexto del modelo, lo que podría resultar en salidas truncadas.

Usa la [herramienta de tokenización](/tokenizer), basada en la librería [tiktoken](https://github.com/openai/tiktoken), para ver cuántos tokens tiene un texto.

Por ejemplo, al hacer una solicitud a la [API de Responses](/docs/api-reference/responses) con un modelo habilitado para razonamiento, como el modelo [o1](/docs/guides/reasoning), los siguientes recuentos de tokens aplican al total de la ventana de contexto:

* Tokens de entrada (incluidos en el array `input`)
* Tokens de salida (generados por el modelo)
* Tokens de razonamiento (utilizados por el modelo para planificar la respuesta)

Los tokens generados que excedan el límite de la ventana de contexto pueden ser truncados en las respuestas de la API.

![visualización de la ventana de contexto](context-window.png)

Puedes estimar el número de tokens que usarán tus mensajes con la [herramienta de tokenización](/tokenizer).

---

