# Entradas de Archivos  
===========  

Aprende cómo usar archivos PDF como entradas en la API de OpenAI.  

Los modelos de OpenAI con capacidades de visión también pueden aceptar archivos PDF como entrada. Proporciona los PDF como datos codificados en Base64 o como IDs de archivo obtenidos después de cargarlos en el endpoint `/v1/files` a través de la [API](/docs/api-reference/files) o el [panel de control](/storage/files/).  

## Cómo funciona  
------------  

Para ayudar a los modelos a entender el contenido de los PDF, incluimos en el contexto del modelo tanto el texto extraído como una imagen de cada página. El modelo puede usar tanto el texto como las imágenes para generar una respuesta. Esto es útil, por ejemplo, si los diagramas contienen información clave que no está en el texto.  

## Carga de archivos  
---------------  

En el siguiente ejemplo, primero cargamos un PDF usando la [API de Archivos](/docs/api-reference/files) y luego referenciamos su ID de archivo en una solicitud a la API del modelo.  

### Cargar un archivo para usar en una respuesta  


```python
from openai import OpenAI
client = OpenAI()

file = client.files.create(
    file=open("draconomicon.pdf", "rb"),
    purpose="user_data"
)

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": file.id,
                },
                {
                    "type": "input_text",
                    "text": "What is the first dragon in the book?",
                },
            ]
        }
    ]
)

print(response.output_text)
```

## Archivos codificados en Base64  
--------------------  

También puedes enviar archivos PDF como entradas codificadas en Base64.  

### Codificar un archivo en Base64 para usar en una respuesta  


```python
import base64
from openai import OpenAI
client = OpenAI()

with open("draconomicon.pdf", "rb") as f:
    data = f.read()

base64_string = base64.b64encode(data).decode("utf-8")

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "filename": "draconomicon.pdf",
                    "file_data": f"data:application/pdf;base64,{base64_string}",
                },
                {
                    "type": "input_text",
                    "text": "What is the first dragon in the book?",
                },
            ],
        },
    ]
)

print(response.output_text)
```

## Consideraciones de uso  
--------------------  

A continuación, se presentan algunas consideraciones a tener en cuenta al usar archivos PDF como entradas.  

**Uso de tokens**  

Para ayudar a los modelos a entender el contenido de los PDF, incluimos en el contexto del modelo tanto el texto extraído como una imagen de cada página, independientemente de si la página contiene imágenes. Antes de implementar tu solución a escala, asegúrate de entender las implicaciones de precios y uso de tokens al usar PDF como entrada. [Más sobre precios](/docs/pricing).  

**Limitaciones de tamaño de archivo**  

Puedes cargar hasta 100 páginas y 32MB de contenido total en una sola solicitud a la API, entre múltiples entradas de archivos.  

**Modelos admitidos**  

Solo los modelos que admiten entradas de texto e imágenes, como gpt-4o, gpt-4o-mini u o1, pueden aceptar archivos PDF como entrada. [Consulta las características de los modelos aquí](/docs/models).  

**Propósito de carga de archivos**  

Puedes cargar estos archivos en la API de Archivos con cualquier [propósito](/docs/api-reference/files/create#files-create-purpose), pero recomendamos usar el propósito `user_data` para archivos que planeas usar como entradas del modelo.  

## Próximos pasos  
----------  

Ahora que conoces los conceptos básicos de las entradas y salidas de texto, puedes consultar estos recursos a continuación.  

[

Experimenta con entradas de PDF en el Playground  

Usa el Playground para desarrollar e iterar en prompts con entradas de PDF.  

](/playground)[

Referencia completa de la API  

Consulta la referencia de la API para más opciones.  

](/docs/api-reference/responses)