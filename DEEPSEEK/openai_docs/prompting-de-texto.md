# Generación y prompting de texto

Aprende cómo indicarle a un modelo que genere texto.

Con la API de OpenAI, puedes usar un [modelo de lenguaje grande](https://www.google.com/search?q=/docs/models) para generar texto a partir de una indicación, como podrías hacerlo usando [ChatGPT](https://chatgpt.com). Los modelos pueden generar casi cualquier tipo de respuesta de texto, como código, ecuaciones matemáticas, datos JSON estructurados o prosa similar a la humana.

Aquí tienes un ejemplo sencillo utilizando la [API de Respuestas](https://www.google.com/search?q=/docs/api-reference/responses).

Generar texto a partir de una indicación simple

```javascript
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-4.1",
    input: "Escribe una historia corta para dormir de una frase sobre un unicornio."
});

console.log(response.output_text);
```

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="Escribe una historia corta para dormir de una frase sobre un unicornio."
)

print(response.output_text)
```

```bash
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-4.1",
        "input": "Escribe una historia corta para dormir de una frase sobre un unicornio."
    }'
```

Un array de contenido generado por el modelo se encuentra en la propiedad `output` de la respuesta. En este ejemplo sencillo, solo tenemos una salida que se ve así:

```json
[
    {
        "id": "msg_67b73f697ba4819183a15cc17d011509",
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "output_text",
                "text": "Bajo el suave brillo de la luna, Luna el unicornio danzaba por campos de polvo de estrellas brillantes, dejando rastros de sueños para cada niño dormido.",
                "annotations": []
            }
        ]
    }
]
```

**¡El array `output` a menudo tiene más de un elemento\!** Puede contener llamadas a herramientas, datos sobre los tokens de razonamiento generados por [modelos de razonamiento](https://www.google.com/search?q=/docs/guides/reasoning) y otros elementos. No es seguro asumir que la salida de texto del modelo está presente en `output[0].content[0].text`.

Algunos de nuestros [SDKs oficiales](https://www.google.com/search?q=/docs/libraries) incluyen una propiedad `output_text` en las respuestas del modelo para mayor comodidad, que agrega todas las salidas de texto del modelo en una sola cadena. Esto puede ser útil como un atajo para acceder a la salida de texto del modelo.

Además de texto plano, también puedes hacer que el modelo devuelva datos estructurados en formato JSON; esta función se llama [**Salidas Estructuradas**](https://www.google.com/search?q=/docs/guides/structured-outputs).

## Elegir un modelo

Una elección clave al generar contenido a través de la API es qué modelo deseas utilizar: el parámetro `model` de los ejemplos de código anteriores. [Puedes encontrar una lista completa de los modelos disponibles aquí](https://www.google.com/search?q=/docs/models). Aquí tienes algunos factores a considerar al elegir un modelo para la generación de texto.

\*   Los **[modelos de razonamiento](https://www.google.com/search?q=/docs/guides/reasoning)** generan una cadena de pensamiento interna para analizar la indicación de entrada y sobresalen en la comprensión de tareas complejas y la planificación de varios pasos. Generalmente también son más lentos y más caros de usar que los modelos GPT.
\*   Los **modelos GPT** son rápidos, rentables y muy inteligentes, pero se benefician de instrucciones más explícitas sobre cómo realizar las tareas.
\*   Los **modelos grandes y pequeños (mini o nano)** ofrecen compensaciones en cuanto a velocidad, costo e inteligencia. Los modelos grandes son más efectivos para comprender las indicaciones y resolver problemas en diversos dominios, mientras que los modelos pequeños generalmente son más rápidos y económicos de usar.

En caso de duda, [`gpt-4.1`](https://www.google.com/search?q=/docs/models/gpt-4.1) ofrece una sólida combinación de inteligencia, velocidad y rentabilidad.

## Ingeniería de prompts

La **ingeniería de prompts** es el proceso de escribir instrucciones efectivas para un modelo, de modo que genere consistentemente contenido que cumpla con tus requisitos.

Debido a que el contenido generado por un modelo no es determinista, construir un prompt que genere contenido en el formato deseado es una combinación de arte y ciencia. Sin embargo, existen varias técnicas y mejores prácticas que puedes aplicar para obtener resultados consistentemente buenos de un modelo.

Algunas técnicas de ingeniería de prompts funcionarán con todos los modelos, como el uso de roles de mensajes. Pero diferentes tipos de modelos (como los de razonamiento versus los GPT) podrían necesitar indicaciones diferentes para producir los mejores resultados. Incluso diferentes instantáneas de modelos dentro de la misma familia podrían producir resultados diferentes. Por lo tanto, a medida que construyas aplicaciones más complejas, te recomendamos encarecidamente que:

\*   Fijes tus aplicaciones de producción a [instantáneas de modelos](https://www.google.com/search?q=/docs/models) específicas (como `gpt-4.1-2025-04-14` por ejemplo) para garantizar un comportamiento consistente.
\*   Construyas [evaluaciones](https://www.google.com/search?q=/docs/guides/evals) que midan el comportamiento de tus prompts, para que puedas monitorear el rendimiento de tus prompts a medida que iteras sobre ellos, o cuando cambias y actualizas las versiones del modelo.

Ahora, examinemos algunas herramientas y técnicas disponibles para construir prompts.

## Roles de mensajes y seguimiento de instrucciones

Puedes proporcionar instrucciones al modelo con [diferentes niveles de autoridad](https://model-spec.openai.com/2025-02-12.html#chain_of_command) utilizando el parámetro `instructions` de la API o **roles de mensajes**.

El parámetro `instructions` proporciona al modelo instrucciones de alto nivel sobre cómo debe comportarse al generar una respuesta, incluyendo el tono, los objetivos y ejemplos de respuestas correctas. Cualquier instrucción proporcionada de esta manera tendrá prioridad sobre un prompt en el parámetro `input`.

Generar texto con instrucciones

```javascript
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-4.1",
    instructions: "Habla como un pirata.",
    input: "¿Son opcionales los puntos y comas en JavaScript?",
});

console.log(response.output_text);
```

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    instructions="Habla como un pirata.",
    input="¿Son opcionales los puntos y comas en JavaScript?",
)

print(response.output_text)
```

```bash
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-4.1",
        "instructions": "Habla como un pirata.",
        "input": "¿Son opcionales los puntos y comas en JavaScript?"
    }'
```

El ejemplo anterior es aproximadamente equivalente a usar los siguientes mensajes de entrada en el array `input`:

Generar texto con mensajes utilizando diferentes roles

```javascript
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-4.1",
    input: [
        {
            role: "developer",
            content: "Habla como un pirata."
        },
        {
            role: "user",
            content: "¿Son opcionales los puntos y comas en JavaScript?",
        },
    ],
});

console.log(response.output_text);
```

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "developer",
            "content": "Habla como un pirata."
        },
        {
            "role": "user",
            "content": "¿Son opcionales los puntos y comas en JavaScript?"
        }
    ]
)

print(response.output_text)
```

```bash
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-4.1",
        "input": [
            {
                "role": "developer",
                "content": "Habla como un pirata."
            },
            {
                "role": "user",
                "content": "¿Son opcionales los puntos y comas en JavaScript?"
            }
        ]
    }'
```

Ten en cuenta que el parámetro `instructions` solo se aplica a la solicitud de generación de respuesta actual. Si estás [gestionando el estado de la conversación](https://www.google.com/search?q=/docs/guides/conversation-state) con el parámetro `previous_response_id`, las `instructions` utilizadas en turnos anteriores no estarán presentes en el contexto.

La [especificación del modelo de OpenAI](https://model-spec.openai.com/2025-02-12.html#chain_of_command) describe cómo nuestros modelos dan diferentes niveles de prioridad a los mensajes con diferentes roles.

|developer|user|assistant|
|---|---|---|
|Los mensajes del desarrollador son instrucciones proporcionadas por el desarrollador de la aplicación, priorizadas por delante de los mensajes del usuario.|Los mensajes del usuario son instrucciones proporcionadas por un usuario final, priorizadas por detrás de los mensajes del desarrollador.|Los mensajes generados por el modelo tienen el rol de asistente.|

Una conversación de varios turnos puede constar de varios mensajes de estos tipos, junto con otros tipos de contenido proporcionados tanto por ti como por el modelo. Obtén más información sobre [la gestión del estado de la conversación aquí](https://www.google.com/search?q=/docs/guides/conversation-state).

Podrías pensar en los mensajes `developer` y `user` como una función y sus argumentos en un lenguaje de programación.

\*   Los mensajes `developer` proporcionan las reglas del sistema y la lógica de negocio, como la definición de una función.
\*   Los mensajes `user` proporcionan entradas y configuración a las que se aplican las instrucciones del mensaje `developer`, como los argumentos de una función.

## Formato de mensajes con Markdown y XML

Al escribir mensajes `developer` y `user`, puedes ayudar al modelo a comprender los límites lógicos de tu prompt y los datos de contexto utilizando una combinación de formato [Markdown](https://commonmark.org/help/) y [etiquetas XML](https://www.w3.org/TR/xml/).

Los encabezados y las listas de Markdown pueden ser útiles para marcar secciones distintas de un prompt y para comunicar jerarquía al modelo. También pueden hacer que tus prompts sean más legibles durante el desarrollo. Las etiquetas XML pueden ayudar a delimitar dónde comienza y termina una pieza de contenido (como un documento de apoyo utilizado como referencia). Los atributos XML también se pueden utilizar para definir metadatos sobre el contenido del prompt que pueden ser referenciados por tus instrucciones.

En general, un mensaje de desarrollador contendrá las siguientes secciones, generalmente en este orden (aunque el contenido y el orden óptimos exactos pueden variar según el modelo que estés utilizando):

\*   **Identidad:** Describe el propósito, el estilo de comunicación y los objetivos de alto nivel del asistente.
\*   **Instrucciones:** Proporciona orientación al modelo sobre cómo generar la respuesta que deseas. ¿Qué reglas debe seguir? ¿Qué debe hacer el modelo y qué nunca debe hacer? Esta sección podría contener muchas subsecciones según sea relevante para tu caso de uso, como cómo el modelo debe [llamar a funciones personalizadas](https://www.google.com/search?q=/docs/guides/function-calling).
\*   **Ejemplos:** Proporciona ejemplos de posibles entradas, junto con la salida deseada del modelo.
\*   **Contexto:** Proporciona al modelo cualquier información adicional que pueda necesitar para generar una respuesta, como datos privados/propietarios fuera de sus datos de entrenamiento, o cualquier otro dato que sepas que será particularmente relevante. Este contenido generalmente se coloca mejor cerca del final de tu prompt, ya que puedes incluir diferentes contextos para diferentes solicitudes de generación.

A continuación, se muestra un ejemplo del uso de etiquetas Markdown y XML para construir un mensaje `developer` con secciones distintas y ejemplos de apoyo.

Ejemplo de prompt

Un mensaje de desarrollador para la generación de código

```text
# Identidad

Eres un asistente de codificación que ayuda a aplicar el uso de variables en snake_case
en código JavaScript, y a escribir código que se ejecutará en
Internet Explorer versión 6.

# Instrucciones

* Al definir variables, utiliza nombres en snake_case (p. ej., mi_variable)
  en lugar de nombres en camelCase (p. ej., miVariable).
* Para admitir navegadores antiguos, declara las variables utilizando la palabra clave más antigua
  "var".
* No proporciones respuestas con formato Markdown, simplemente devuelve
  el código según lo solicitado.

# Ejemplos

<user_query>
¿Cómo declaro una variable de cadena para un nombre?
</user_query>

<assistant_response>
var nombre = "Ana";
</assistant_response>
```

Solicitud API

Enviar un prompt para generar código a través de la API

```javascript
import fs from "fs/promises";
import OpenAI from "openai";
const client = new OpenAI();

const instructions = await fs.readFile("prompt.txt", "utf-8");

const response = await client.responses.create({
    model: "gpt-4.1",
    instructions,
    input: "¿Cómo declararía una variable para un apellido?",
});

console.log(response.output_text);
```

```python
from openai import OpenAI
client = OpenAI()

with open("prompt.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

response = client.responses.create(
    model="gpt-4.1",
    instructions=instructions,
    input="¿Cómo declararía una variable para un apellido?",
)

print(response.output_text)
```

```bash
curl https://api.openai.com/v1/responses
```