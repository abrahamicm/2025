# Salidas Estructuradas  
==================  

Garantiza que las respuestas cumplan con un esquema JSON.  

Pruébalo  
----------

Pruébalo en el [Playground](/playground) o genera una definición de esquema lista para usar y experimenta con salidas estructuradas.  

Generar  

Introducción  
------------

JSON es uno de los formatos más utilizados en el mundo para el intercambio de datos entre aplicaciones.  

**Salidas Estructuradas** es una función que garantiza que el modelo siempre generará respuestas que cumplan con el [Esquema JSON](https://json-schema.org/overview/what-is-jsonschema) que proporciones, por lo que no tendrás que preocuparte por que el modelo omita una clave requerida o genere un valor de enumeración inválido.  

Algunos beneficios de las Salidas Estructuradas incluyen:  

1.  **Seguridad de tipos confiable:** No es necesario validar o reintentar respuestas con formato incorrecto.  
2.  **Rechazos explícitos:** Los rechazos del modelo basados en seguridad ahora son detectables programáticamente.  
3.  **Indicaciones más simples:** No necesitas indicaciones elaboradas para lograr un formato consistente.  

Además de admitir Esquema JSON en la API REST, los SDKs de OpenAI para [Python](https://github.com/openai/openai-python/blob/main/helpers.md#structured-outputs-parsing-helpers) y [JavaScript](https://github.com/openai/openai-node/blob/master/helpers.md#structured-outputs-parsing-helpers) también facilitan la definición de esquemas de objetos utilizando [Pydantic](https://docs.pydantic.dev/latest/) y [Zod](https://zod.dev/), respectivamente. A continuación, puedes ver cómo extraer información de texto no estructurado que cumpla con un esquema definido en código.  

### Obtener una respuesta estructurada  

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text_format=CalendarEvent,
)

event = response.output_parsed
```

### Modelos admitidos  

Las Salidas Estructuradas están disponibles en nuestros [últimos modelos de lenguaje avanzado](/docs/models), comenzando con GPT-4o. Modelos anteriores como `gpt-4-turbo` y versiones anteriores pueden usar [Modo JSON](#json-mode) en su lugar.  

### Cuándo usar Salidas Estructuradas mediante llamadas a funciones vs. mediante `text.format`  

Las Salidas Estructuradas están disponibles en dos formas en la API de OpenAI:  

1.  Al usar [llamadas a funciones](/docs/guides/function-calling).  
2.  Al usar un formato de respuesta `json_schema`.  

Las llamadas a funciones son útiles cuando estás construyendo una aplicación que conecta los modelos con la funcionalidad de tu aplicación.  

Por ejemplo, puedes darle al modelo acceso a funciones que consulten una base de datos para construir un asistente de IA que ayude a los usuarios con sus pedidos, o funciones que interactúen con la interfaz de usuario.  

Por el contrario, las Salidas Estructuradas mediante `response_format` son más adecuadas cuando deseas indicar un esquema estructurado para que el modelo lo use al responder al usuario, en lugar de cuando el modelo llama a una herramienta.  

Por ejemplo, si estás construyendo una aplicación de tutoría de matemáticas, podrías querer que el asistente responda a tu usuario utilizando un Esquema JSON específico para generar una interfaz de usuario que muestre diferentes partes de la salida del modelo de manera distinta.  

En resumen:  

*   Si estás conectando el modelo con herramientas, funciones, datos, etc. en tu sistema, entonces debes usar llamadas a funciones.  
*   Si deseas estructurar la salida del modelo cuando responde al usuario, entonces debes usar un `text.format` estructurado.  

El resto de esta guía se centrará en casos de uso sin llamadas a funciones en la API de Respuestas. Para obtener más información sobre cómo usar Salidas Estructuradas con llamadas a funciones, consulta la guía [Llamadas a Funciones](/docs/guides/function-calling#function-calling-with-structured-outputs).  

### Salidas Estructuradas vs. Modo JSON  

Las Salidas Estructuradas son la evolución del [Modo JSON](#json-mode). Mientras que ambos garantizan que se produzca JSON válido, solo las Salidas Estructuradas garantizan el cumplimiento del esquema. Tanto las Salidas Estructuradas como el Modo JSON son compatibles con la API de Respuestas, la API de Finalizaciones de Chat, la API de Asistentes, la API de Fine-tuning y la API de Lotes.  

Recomendamos usar siempre Salidas Estructuradas en lugar del Modo JSON cuando sea posible.  

Sin embargo, las Salidas Estructuradas con `response_format: {type: "json_schema", ...}` solo son compatibles con las instantáneas de modelos `gpt-4o-mini`, `gpt-4o-mini-2024-07-18` y `gpt-4o-2024-08-06` y versiones posteriores.  

||Salidas Estructuradas|Modo JSON|  
|---|---|---|  
|Genera JSON válido|Sí|Sí|  
|Cumple con el esquema|Sí (ver esquemas admitidos)|No|  
|Modelos compatibles|gpt-4o-mini, gpt-4o-2024-08-06 y posteriores|gpt-3.5-turbo, gpt-4-* y modelos gpt-4o-*|  
|Habilitación|`text: { format: { type: "json_schema", "strict": true, "schema": ... } }`|`text: { format: { type: "json_object" } }`|  

## Ejemplos  
--------  

### Cadena de pensamiento  

Puedes pedirle al modelo que genere una respuesta de manera estructurada, paso a paso, para guiar al usuario a través de la solución.  

**Salidas Estructuradas para tutoría de matemáticas con cadena de pensamiento**  

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
        },
        {"role": "user", "content": "how can I solve 8x + 7 = -23"},
    ],
    text_format=MathReasoning,
)

math_reasoning = response.output_parsed
```  

#### Ejemplo de respuesta  

```json
{
  "steps": [
    {
      "explanation": "Start with the equation 8x + 7 = -23.",
      "output": "8x + 7 = -23"
    },
    {
      "explanation": "Subtract 7 from both sides to isolate the term with the variable.",
      "output": "8x = -23 - 7"
    },
    {
      "explanation": "Simplify the right side of the equation.",
      "output": "8x = -30"
    },
    {
      "explanation": "Divide both sides by 8 to solve for x.",
      "output": "x = -30 / 8"
    },
    {
      "explanation": "Simplify the fraction.",
      "output": "x = -15 / 4"
    }
  ],
  "final_answer": "x = -15 / 4"
}
```  

### Extracción de datos estructurados  

Puedes definir campos estructurados para extraer de datos de entrada no estructurados, como artículos de investigación.  

**Extracción de datos de artículos de investigación usando Salidas Estructuradas**  

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class ResearchPaperExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure.",
        },
        {"role": "user", "content": "..."},
    ],
    text_format=ResearchPaperExtraction,
)

research_paper = response.output_parsed
```  

#### Ejemplo de respuesta  

```json
{
  "title": "Application of Quantum Algorithms in Interstellar Navigation: A New Frontier",
  "authors": [
    "Dr. Stella Voyager",
    "Dr. Nova Star",
    "Dr. Lyra Hunter"
  ],
  "abstract": "This paper investigates the utilization of quantum algorithms to improve interstellar navigation systems. By leveraging quantum superposition and entanglement, our proposed navigation system can calculate optimal travel paths through space-time anomalies more efficiently than classical methods. Experimental simulations suggest a significant reduction in travel time and fuel consumption for interstellar missions.",
  "keywords": [
    "Quantum algorithms",
    "interstellar navigation",
    "space-time anomalies",
    "quantum superposition",
    "quantum entanglement",
    "space travel"
  ]
}
```  

### Generación de UI  

Puedes generar HTML válido representándolo como estructuras de datos recursivas con restricciones, como enumeraciones.  

**Generación de HTML usando Salidas Estructuradas**  

```python
from enum import Enum
from typing import List

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class UIType(str, Enum):
    div = "div"
    button = "button"
    header = "header"
    section = "section"
    field = "field"
    form = "form"

class Attribute(BaseModel):
    name: str
    value: str

class UI(BaseModel):
    type: UIType
    label: str
    children: List["UI"]
    attributes: List[Attribute]

UI.model_rebuild()  # Required for recursive types

class Response(BaseModel):
    ui: UI

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "You are a UI generator AI. Convert the user input into a UI.",
        },
        {"role": "user", "content": "Make a User Profile Form"},
    ],
    text_format=Response,
)

ui = response.output_parsed
```  

#### Ejemplo de respuesta  

```json
{
  "type": "form",
  "label": "User Profile Form",
  "children": [
    {
      "type": "div",
      "label": "",
      "children": [
        {
          "type": "field",
          "label": "First Name",
          "children": [],
          "attributes": [
            {
              "name": "type",
              "value": "text"
            },
            {
              "name": "name",
              "value": "firstName"
            },
            {
              "name": "placeholder",
              "value": "Enter your first name"
            }
          ]
        },
        {
          "type": "field",
          "label": "Last Name",
          "children": [],
          "attributes": [
            {
              "name": "type",
              "value": "text"
            },
            {
              "name": "name",
              "value": "lastName"
            },
            {
              "name": "placeholder",
              "value": "Enter your last name"
            }
          ]
        }
      ],
      "attributes": []
    },
    {
      "type": "button",
      "label": "Submit",
      "children": [],
      "attributes": [
        {
          "name": "type",
          "value": "submit"
        }
      ]
    }
  ],
  "attributes": [
    {
      "name": "method",
      "value": "post"
    },
    {
      "name": "action",
      "value": "/submit-profile"
    }
  ]
}
```  

### Moderación  

Puedes clasificar entradas en múltiples categorías, una forma común de realizar moderación.  

**Moderación usando Salidas Estructuradas**  

```python
from enum import Enum
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class Category(str, Enum):
    violence = "violence"
    sexual = "sexual"
    self_harm = "self_harm"

class ContentCompliance(BaseModel):
    is_violating: bool
    category: Optional[Category]
    explanation_if_violating: Optional[str]

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {
            "role": "system",
            "content": "Determine if the user input violates specific guidelines and explain if they do.",
        },
        {"role": "user", "content": "How do I prepare for a job interview?"},
    ],
    text_format=ContentCompliance,
)

compliance = response.output_parsed
```  

#### Ejemplo de respuesta  

```json
{
  "is_violating": false,
  "category": null,
  "explanation_if_violating": null
}
```  

## Cómo usar Salidas Estructuradas con `text.format`  
----------------------------------------------  

### Paso 1: Define tu esquema  

Primero, debes diseñar el Esquema JSON que el modelo debe seguir. Consulta los [ejemplos](/docs/guides/structured-outputs#examples) al inicio de esta guía como referencia.  

Aunque las Salidas Estructuradas admiten gran parte de JSON Schema, algunas funciones no están disponibles por razones técnicas o de rendimiento. Consulta [aquí](/docs/guides/structured-outputs#supported-schemas) para más detalles.  

#### Consejos para tu Esquema JSON  

Para maximizar la calidad de las generaciones del modelo, recomendamos lo siguiente:  

*   Nombra las claves de manera clara e intuitiva.  
*   Crea títulos y descripciones claras para las claves importantes en tu estructura.  
*   Crea y utiliza evaluaciones para determinar la estructura que mejor funcione para tu caso de uso.  

### Paso 2: Proporciona tu esquema en la llamada API  

Para usar Salidas Estructuradas, simplemente especifica:  

```json
text: { format: { type: "json_schema", "strict": true, "schema": … } }
```  

Por ejemplo:  

```python
response = client.responses.create(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "how can I solve 8x + 7 = -23"}
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "calendar_event",
            "schema": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": {"type": "string"},
                                "output": {"type": "string"}
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": False
                        }
                    },
                    "final_answer": {"type": "string"}
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

print(response.output_text)
```  

**Nota:** La primera solicitud que hagas con cualquier esquema tendrá una latencia adicional mientras nuestra API procesa el esquema, pero las solicitudes posteriores con el mismo esquema no tendrán latencia adicional.  

### Paso 3: Maneja casos extremos  

En algunos casos, el modelo podría no generar una respuesta válida que coincida con el Esquema JSON proporcionado.  

Esto puede ocurrir en caso de un rechazo, si el modelo se niega a responder por razones de seguridad, o si, por ejemplo, alcanzas un límite de tokens máximo y la respuesta está incompleta.  

```python
try:
    response = client.responses.create(
        model="gpt-4o-2024-08-06",
        input=[
            {
                "role": "system",
                "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
            },
            {"role": "user", "content": "how can I solve 8x + 7 = -23"},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "math_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "explanation": {"type": "string"},
                                    "output": {"type": "string"},
                                },
                                "required": ["explanation", "output"],
                                "additionalProperties": False,
                            },
                        },
                        "final_answer": {"type": "string"},
                    },
                    "required": ["steps", "final_answer"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
    )
except Exception as e:
    # Maneja errores como finish_reason, refusal, content_filter, etc.
    pass
```  

### Rechazos con Salidas Estructuradas  

Cuando uses Salidas Estructuradas con entradas generadas por el usuario, los modelos de OpenAI pueden ocasionalmente rechazar cumplir la solicitud por razones de seguridad. Dado que un rechazo no necesariamente sigue el esquema que proporcionaste en `response_format`, la respuesta de la API incluirá un nuevo campo llamado `refusal` para indicar que el modelo rechazó cumplir la solicitud.  

Cuando la propiedad `refusal` aparezca en tu objeto de salida, podrías mostrar el rechazo en tu interfaz de usuario o incluir lógica condicional en el código que consume la respuesta para manejar el caso de una solicitud rechazada.  

```python
class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "how can I solve 8x + 7 = -23"}
    ],
    response_format=MathReasoning,
)

math_reasoning = completion.choices[0].message

# Si el modelo rechaza responder, obtendrás un mensaje de rechazo
if (math_reasoning.refusal):
    print(math_reasoning.refusal)
else:
    print(math_reasoning.parsed)
```  

La respuesta de la API de un rechazo se verá así:  

```json
{
  "id": "resp_1234567890",
  "object": "response",
  "created_at": 1721596428,
  "status": "completed",
  "error": null,
  "incomplete_details": null,
  "input": [],
  "instructions": null,
  "max_output_tokens": null,
  "model": "gpt-4o-2024-08-06",
  "output": [{
    "id": "msg_1234567890",
    "type": "message",
    "role": "assistant",
    "content": [
      {
        "type": "refusal",
        "refusal": "I'm sorry, I cannot assist with that request."
      }
    ]
  }],
  "usage": {
    "input_tokens": 81,
    "output_tokens": 11,
    "total_tokens": 92,
    "output_tokens_details": {
      "reasoning_tokens": 0,
    }
  },
}
```  

### Consejos y mejores prácticas  

#### Manejo de entradas generadas por el usuario  

Si tu aplicación utiliza entradas generadas por el usuario, asegúrate de que tu indicación incluya instrucciones sobre cómo manejar situaciones en las que la entrada no pueda generar una respuesta válida.  

El modelo siempre intentará cumplir con el esquema proporcionado, lo que puede resultar en alucinaciones si la entrada no está relacionada con el esquema.  

Podrías incluir lenguaje en tu indicación para especificar que deseas devolver parámetros vacíos o una oración específica si el modelo detecta que la entrada es incompatible con la tarea.  

#### Manejo de errores  

Las Salidas Estructuradas aún pueden contener errores. Si ves errores, intenta ajustar tus instrucciones, proporcionar ejemplos en las instrucciones del sistema o dividir las tareas en subtareas más simples. Consulta la [guía de ingeniería de prompts](/docs/guides/prompt-engineering) para obtener más orientación sobre cómo ajustar tus entradas.  

#### Evita la divergencia del Esquema JSON  

Para evitar que tu Esquema JSON y los tipos correspondientes en tu lenguaje de programación divergan, recomendamos encarecidamente usar el soporte nativo de Pydantic/Zod en el SDK.  

Si prefieres especificar el Esquema JSON directamente, podrías agregar reglas de CI que marquen cuando se editan el Esquema JSON o los objetos de datos subyacentes, o agregar un paso de CI que genere automáticamente el Esquema JSON a partir de definiciones de tipos (o viceversa).  

## Streaming  
---------  

Puedes usar streaming para procesar las respuestas del modelo o los argumentos de llamadas a funciones a medida que se generan y analizarlos como datos estructurados.  

De esta manera, no tienes que esperar a que se complete toda la respuesta para manejarla. Esto es particularmente útil si deseas mostrar campos JSON uno por uno o manejar argumentos de llamadas a funciones tan pronto como estén disponibles.  

Recomendamos confiar en los SDKs para manejar streaming con Salidas Estructuradas.  

```python
from typing import List

from openai import OpenAI
from pydantic import BaseModel

class EntitiesModel(BaseModel):
    attributes: List[str]
    colors: List[str]
    animals: List[str]

client = OpenAI()

with client.responses.stream(
    model="gpt-4.1",
    input=[
        {"role": "system", "content": "Extract entities from the input text"},
        {
            "role": "user",
            "content": "The quick brown fox jumps over the lazy dog with piercing blue eyes",
        },
    ],
    text_format=EntitiesModel,
) as stream:
    for event in stream:
        if event.type == "response.refusal.delta":
            print(event.delta, end="")
        elif event.type == "response.output_text.delta":
            print(event.delta, end="")
        elif event.type == "response.error":
            print(event.error, end="")
        elif event.type == "response.completed":
            print("Completed")
            # print(event.response.output)

    final_response = stream.get_final_response()
    print(final_response)
```  

## Esquemas admitidos  
-----------------  

Las Salidas Estructuradas admiten un subconjunto del lenguaje [JSON Schema](https://json-schema.org/docs).  

#### Tipos admitidos  

Los siguientes tipos son compatibles con Salidas Estructuradas:  

*   String  
*   Number  
*   Boolean  
*   Integer  
*   Object  
*   Array  
*   Enum  
*   anyOf  

#### Los objetos raíz no pueden ser `anyOf`  

Ten en cuenta que el objeto de nivel raíz de un esquema debe ser un objeto y no usar `anyOf`. Un patrón que aparece en Zod (como ejemplo) es usar una unión discriminada, que produce un `anyOf` en el nivel superior. Por lo tanto, código como el siguiente no funcionará:  

```javascript
import { z } from 'zod';
import { zodResponseFormat } from 'openai/helpers/zod';

const BaseResponseSchema = z.object({ /* ... */ });
const UnsuccessfulResponseSchema = z.object({ /* ... */ });

const finalSchema = z.discriminatedUnion('status', [
    BaseResponseSchema,
    UnsuccessfulResponseSchema,
]);

// Esquema JSON no válido para Salidas Estructuradas
const json = zodResponseFormat(finalSchema, 'final_schema');
```  

#### Todos los campos deben ser `required`  

Para usar Salidas Estructuradas, todos los campos o parámetros de función deben especificarse como `required`.  

```json
{
    "name": "get_weather",
    "description": "Fetches the weather in the given location",
    "strict": true,
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to get the weather for"
            },
            "unit": {
                "type": "string",
                "description": "The unit to return the temperature in",
                "enum": ["F", "C"]
            }
        },
        "additionalProperties": false,
        "required": ["location", "unit"]
    }
}
```  

Aunque todos los campos deben ser obligatorios (y el modelo devolverá un valor para cada parámetro), es posible emular un parámetro opcional utilizando un tipo de unión con `null`.  

```json
{
    "name": "get_weather",
    "description": "Fetches the weather in the given location",
    "strict": true,
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to get the weather for"
            },
            "unit": {
                "type": ["string", "null"],
                "description": "The unit to return the temperature in",
                "enum": ["F", "C"]
            }
        },
        "additionalProperties": false,
        "required": [
            "location", "unit"
        ]
    }
}
```  

#### Los objetos tienen limitaciones en la profundidad de anidación y el tamaño  

Un esquema puede tener hasta 100 propiedades de objetos en total, con un máximo de 5 niveles de anidación.  

#### Limitaciones en el tamaño total de cadenas  

En un esquema, la longitud total de cadena de todos los nombres de propiedades, nombres de definiciones, valores de enumeración y valores constantes no puede exceder los 15,000 caracteres.  

#### Limitaciones en el tamaño de enumeraciones  

Un esquema puede tener hasta 500 valores de enumeración en todas las propiedades de enumeración.  

Para una sola propiedad de enumeración con valores de cadena, la longitud total de cadena de todos los valores de enumeración no puede exceder los 7,500 caracteres cuando hay más de 250 valores de enumeración.  

#### `additionalProperties: false` siempre debe establecerse en objetos  

`additionalProperties` controla si es permitido que un objeto contenga claves/valores adicionales que no se definieron en el Esquema JSON.  

Las Salidas Estructuradas solo admiten generar claves/valores especificados, por lo que requerimos que los desarrolladores establezcan `additionalProperties: false` para optar por Salidas Estructuradas.  

```json
{
    "name": "get_weather",
    "description": "Fetches the weather in the given location",
    "strict": true,
    "schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to get the weather for"
            },
            "unit": {
                "type": "string",
                "description": "The unit to return the temperature in",
                "enum": ["F", "C"]
            }
        },
        "additionalProperties": false,
        "required": [
            "location", "unit"
        ]
    }
}
```  

#### Orden de las claves  

Cuando uses Salidas Estructuradas, las salidas se generarán en el mismo orden que el orden de las claves en el esquema.  

#### Algunas palabras clave específicas de tipos aún no son compatibles  

Palabras clave notables no admitidas incluyen:  

*   **Para cadenas:** `minLength`, `maxLength`, `pattern`, `format`  
*   **Para números:** `minimum`, `maximum`, `multipleOf`  
*   **Para objetos:** `patternProperties`, `unevaluatedProperties`, `propertyNames`, `minProperties`, `maxProperties`  
*   **Para arreglos:** `unevaluatedItems`, `contains`, `minContains`, `maxContains`, `minItems`, `maxItems`, `uniqueItems`  

Si activas Salidas Estructuradas proporcionando `strict: true` y llamas a la API con un Esquema JSON no admitido, recibirás un error.  

#### Para `anyOf`, los esquemas anidados deben ser cada uno un Esquema JSON válido según este subconjunto  

Aquí hay un ejemplo de esquema `anyOf` admitido:  

```json
{
    "type": "object",
    "properties": {
        "item": {
            "anyOf": [
                {
                    "type": "object",
                    "description": "The user object to insert into the database",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the user"
                        },
                        "age": {
                            "type": "number",
                            "description": "The age of the user"
                        }
                    },
                    "additionalProperties": false,
                    "required": [
                        "name",
                        "age"
                    ]
                },
                {
                    "type": "object",
                    "description": "The address object to insert into the database",
                    "properties": {
                        "number": {
                            "type": "string",
                            "description": "The number of the address. Eg. for 123 main st, this would be 123"
                        },
                        "street": {
                            "type": "string",
                            "description": "The street name. Eg. for 123 main st, this would be main st"
                        },
                        "city": {
                            "type": "string",
                            "description": "The city of the address"
                        }
                    },
                    "additionalProperties": false,
                    "required": [
                        "number",
                        "street",
                        "city"
                    ]
                }
            ]
        }
    },
    "additionalProperties": false,
    "required": [
        "item"
    ]
}
```  

#### Se admiten definiciones  

Puedes usar definiciones para definir subesquemas a los que se hace referencia en todo tu esquema. El siguiente es un ejemplo simple.  

```json
{
    "type": "object",
    "properties": {
        "steps": {
            "type": "array",
            "items": {
                "$ref": "#/$defs/step"
            }
        },
        "final_answer": {
            "type": "string"
        }
    },
    "$defs": {
        "step": {
            "type": "object",
            "properties": {
                "explanation": {
                    "type": "string"
                },
                "output": {
                    "type": "string"
                }
            },
            "required": [
                "explanation",
                "output"
            ],
            "additionalProperties": false
        }
    },
    "required": [
        "steps",
        "final_answer"
    ],
    "additionalProperties": false
}
```  

#### Se admiten esquemas recursivos  

Ejemplo de esquema recursivo usando `#` para indicar recursión raíz.  

```json
{
    "name": "ui",
    "description": "Dynamically generated UI",
    "strict": true,
    "schema": {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "description": "The type of the UI component",
                "enum": ["div", "button", "header", "section", "field", "form"]
            },
            "label": {
                "type": "string",
                "description": "The label of the UI component, used for buttons or form fields"
            },
            "children": {
                "type": "array",
                "description": "Nested UI components",
                "items": {
                    "$ref": "#"
                }
            },
            "attributes": {
                "type": "array",
                "description": "Arbitrary attributes for the UI component, suitable for any element",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the attribute, for example onClick or className"
                        },
                        "value": {
                            "type": "string",
                            "description": "The value of the attribute"
                        }
                    },
                    "additionalProperties": false,
                    "required": ["name", "value"]
                }
            }
        },
        "required": ["type", "label", "children", "attributes"],
        "additionalProperties": false
    }
}
```  

Ejemplo de esquema recursivo usando recursión explícita:  

```json
{
    "type": "object",
    "properties": {
        "linked_list": {
            "$ref": "#/$defs/linked_list_node"
        }
    },
    "$defs": {
        "linked_list_node": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number"
                },
                "next": {
                    "anyOf": [
                        {
                            "$ref": "#/$defs/linked_list_node"
                        },
                        {
                            "type": "null"
                        }
                    ]
                }
            },
            "additionalProperties": false,
            "required": [
                "next",
                "value"
            ]
        }
    },
    "additionalProperties": false,
    "required": [
        "linked_list"
    ]
}
```  

## Modo JSON  
---------  

El Modo JSON es una versión más básica de la función Salidas Estructuradas. Mientras que el Modo JSON garantiza que la salida del modelo sea JSON válido, las Salidas Estructuradas hacen coincidir de manera confiable la salida del modelo con el esquema que especifiques. Recomendamos que uses Salidas Estructuradas si son compatibles con tu caso de uso.  

Cuando el Modo JSON está activado, la salida del modelo está garantizada como JSON válido, excepto en algunos casos extremos que debes detectar y manejar adecuadamente.  

Para activar el Modo JSON con la API de Respuestas, puedes establecer `text.format` en `{ "type": "json_object" }`. Si estás usando llamadas a funciones, el Modo JSON siempre está activado.  

Notas importantes:  

*   Al usar el Modo JSON, siempre debes indicarle al modelo que produzca JSON mediante algún mensaje en la conversación, por ejemplo, a través de tu mensaje del sistema. Si no incluyes una instrucción explícita para generar JSON, el modelo puede generar un flujo interminable de espacios en blanco y la solicitud puede ejecutarse continuamente hasta alcanzar el límite de tokens. Para ayudar a garantizar que no lo olvides, la API generará un error si la cadena "JSON" no aparece en algún lugar del contexto.  
*   El Modo JSON no garantizará que la salida coincida con ningún esquema específico, solo que es válido y se analiza sin errores. Debes usar Salidas Estructuradas para garantizar que coincida con tu esquema o, si eso no es posible, usar una biblioteca de validación y posiblemente reintentos para garantizar que la salida coincida con tu esquema deseado.  
*   Tu aplicación debe detectar y manejar los casos extremos que pueden resultar en que la salida del modelo no sea un objeto JSON completo (ver más abajo).  

**Manejo de casos extremos**  

```python
we_did_not_specify_stop_tokens = True

try:
    response = client.responses.create(
        model="gpt-3.5-turbo-0125",
        input=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": "Who won the world series in 2020? Please respond in the format {winner: ...}"}
        ],
        text={"format": {"type": "json_object"}}
    )

    # Verifica si la conversación fue demasiado larga para la ventana de contexto, lo que resultó en JSON incompleto 
    if response.status == "incomplete" and response.incomplete_details.reason == "max_output_tokens":
        # tu código debe manejar este caso de error
        pass

    # Verifica si el sistema de seguridad de OpenAI rechazó la solicitud y generó un rechazo en su lugar
    if response.output[0].content[0].type == "refusal":
        # tu código debe manejar este caso de error
        # En este caso, el campo .content contendrá la explicación (si la hay) que el modelo generó sobre por qué está rechazando
        print(response.output[0].content[0]["refusal"])

    # Verifica si la salida del modelo incluyó contenido restringido, por lo que la generación de JSON se detuvo y puede ser parcial
    if response.status == "incomplete" and response.incomplete_details.reason == "content_filter":
        # tu código debe manejar este caso de error
        pass

    if response.status == "completed":
        # En este caso, el modelo ha terminado con éxito de generar el objeto JSON según tu esquema, o el modelo generó uno de los tokens que proporcionaste como "stop token"

        if we_did_not_specify_stop_tokens:
            # Si no especificaste ningún stop token, entonces la generación está completa y la clave content contendrá el objeto JSON serializado
            # Esto se analizará con éxito y debería contener "{"winner": "Los Angeles Dodgers"}"
            print(response.output_text)
        else:
            # Verifica si response.output_text termina con uno de tus stop tokens y maneja apropiadamente
            pass
except Exception as e:
    # Tu código debe manejar errores aquí, por ejemplo, un error de red al llamar a la API
    print(e)
```  

## Recursos  
---------  

Para obtener más información sobre Salidas Estructuradas, te recomendamos explorar los siguientes recursos:  

*   Consulta nuestro [libro de cocina introductorio](https://cookbook.openai.com/examples/structured_outputs_intro) sobre Salidas Estructuradas.  
*   Aprende [cómo construir sistemas multiagente](https://cookbook.openai.com/examples/structured_outputs_multi_agent) con Salidas Estructuradas.