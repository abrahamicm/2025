# Búsqueda en archivos

Permite a los modelos buscar en tus archivos información relevante antes de generar una respuesta.

## Visión general

La búsqueda en archivos es una herramienta disponible en la [API de respuestas](/docs/api-reference/responses). Permite a los modelos recuperar información desde una base de conocimientos de archivos previamente subidos mediante búsqueda semántica y por palabras clave. Al crear almacenes vectoriales y subir archivos a ellos, puedes ampliar el conocimiento inherente de los modelos dándoles acceso a estas bases de conocimiento o `vector_stores`.

Para obtener más información sobre cómo funcionan los almacenes vectoriales y la búsqueda semántica, consulta nuestra [guía de recuperación](/docs/guides/retrieval).

Esta es una herramienta alojada y gestionada por OpenAI, lo que significa que no necesitas implementar código por tu parte para manejar su ejecución. Cuando el modelo decida usarla, llamará automáticamente a la herramienta, recuperará información de tus archivos y devolverá una salida.

## Cómo usarla

Antes de usar la búsqueda en archivos con la API de respuestas, necesitas haber configurado una base de conocimientos en un almacén vectorial y haber subido archivos a él.

Crear un almacén vectorial y subir un archivo

Sigue estos pasos para crear un almacén vectorial y subir un archivo. Puedes usar [este archivo de ejemplo](https://cdn.openai.com/API/docs/deep_research_blog.pdf) o subir uno propio.

#### Subir el archivo a la API de archivos

Subir un archivo

```python
import requests
from io import BytesIO
from openai import OpenAI

client = OpenAI()

def create_file(client, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # Descargar el contenido del archivo desde la URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        # Manejar ruta de archivo local
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )
    print(result.id)
    return result.id

# Sustituye con tu propia ruta de archivo o URL
file_id = create_file(client, "https://cdn.openai.com/API/docs/deep_research_blog.pdf")
```

#### Crear un almacén vectorial

```python
vector_store = client.vector_stores.create(
    name="knowledge_base"
)
print(vector_store.id)
```

#### Agregar el archivo al almacén vectorial

```python
client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file_id
)
print(result)
```

#### Verificar estado

Ejecuta este código hasta que el archivo esté listo para usarse (es decir, cuando el estado sea `completed`).

```python
result = client.vector_stores.files.list(
    vector_store_id=vector_store.id
)
print(result)
```

Una vez configurada tu base de conocimientos, puedes incluir la herramienta `file_search` en la lista de herramientas disponibles para el modelo, junto con la lista de almacenes vectoriales en los que buscar.

Actualmente, solo puedes buscar en un almacén vectorial a la vez, por lo que solo puedes incluir un ID de almacén vectorial al llamar a la herramienta de búsqueda en archivos.

Herramienta de búsqueda en archivos

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="What is deep research by OpenAI?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["<vector_store_id>"]
    }]
)
print(response)
```

Cuando el modelo llama a esta herramienta, recibirás una respuesta con múltiples salidas:

1. Un elemento de salida `file_search_call`, que contiene el ID de la llamada de búsqueda en archivos.
2. Un elemento de salida `message`, que contiene la respuesta del modelo, junto con las citas de archivos.

Respuesta de búsqueda en archivos

```json
{
  "output": [
    {
      "type": "file_search_call",
      "id": "fs_67c09ccea8c48191ade9367e3ba71515",
      "status": "completed",
      "queries": ["What is deep research?"],
      "search_results": null
    },
    {
      "id": "msg_67c09cd3091c819185af2be5d13d87de",
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "La investigación profunda es una capacidad sofisticada que permite una indagación extensa y una síntesis de información a través de diversos dominios. Está diseñada para llevar a cabo tareas de investigación en múltiples pasos, recopilar datos de múltiples fuentes en línea y proporcionar informes completos similares a los que produciría un analista de investigación. Esta funcionalidad es particularmente útil en campos que requieren información detallada y precisa...",
          "annotations": [
            {
              "type": "file_citation",
              "index": 992,
              "file_id": "file-2dtbBZdjtDKS8eqWxqbgDi",
              "filename": "deep_research_blog.pdf"
            },
            {
              "type": "file_citation",
              "index": 992,
              "file_id": "file-2dtbBZdjtDKS8eqWxqbgDi",
              "filename": "deep_research_blog.pdf"
            },
            {
              "type": "file_citation",
              "index": 1176,
              "file_id": "file-2dtbBZdjtDKS8eqWxqbgDi",
              "filename": "deep_research_blog.pdf"
            },
            {
              "type": "file_citation",
              "index": 1176,
              "file_id": "file-2dtbBZdjtDKS8eqWxqbgDi",
              "filename": "deep_research_blog.pdf"
            }
          ]
        }
      ]
    }
  ]
}
```

## Personalización de recuperación

### Limitar el número de resultados

Usando la herramienta de búsqueda en archivos con la API de respuestas, puedes personalizar la cantidad de resultados que deseas recuperar de los almacenes vectoriales. Esto puede ayudar a reducir tanto el uso de tokens como la latencia, aunque puede afectar la calidad de la respuesta.

Limitar el número de resultados

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="What is deep research by OpenAI?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["<vector_store_id>"],
        "max_num_results": 2
    }]
)
print(response)
```

### Incluir resultados de búsqueda en la respuesta

Aunque puedes ver anotaciones (referencias a archivos) en el texto de salida, la llamada de búsqueda en archivos no devolverá resultados de búsqueda por defecto.

Para incluir los resultados de búsqueda en la respuesta, puedes usar el parámetro `include` al crear la respuesta.

Incluir resultados de búsqueda

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="What is deep research by OpenAI?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["<vector_store_id>"]
    }],
    include=["file_search_call.results"]
)
print(response)
```

### Filtrado por metadatos

Puedes filtrar los resultados de búsqueda en función de los metadatos de los archivos. Para más detalles, consulta nuestra [guía de recuperación](/docs/guides/retrieval), que cubre:

* Cómo [asignar atributos a archivos de almacenes vectoriales](/docs/guides/retrieval#attributes)
* Cómo [definir filtros](/docs/guides/retrieval#attribute-filtering)

Filtrado por metadatos

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="What is deep research by OpenAI?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["<vector_store_id>"],
        "filters": {
            "type": "eq",
            "key": "type",
            "value": "blog"
        }
    }]
)
print(response)
```

## Archivos compatibles

*Para los tipos MIME `text/`, la codificación debe ser `utf-8`, `utf-16` o `ascii`.*

| Formato de archivo | Tipo MIME                                                                 |
| ------------------ | ------------------------------------------------------------------------- |
| .c                 | text/x-c                                                                  |
| .cpp               | text/x-c++                                                                |
| .cs                | text/x-csharp                                                             |
| .css               | text/css                                                                  |
| .doc               | application/msword                                                        |
| .docx              | application/vnd.openxmlformats-officedocument.wordprocessingml.document   |
| .go                | text/x-golang                                                             |
| .html              | text/html                                                                 |
| .java              | text/x-java                                                               |
| .js                | text/javascript                                                           |
| .json              | application/json                                                          |
| .md                | text/markdown                                                             |
| .pdf               | application/pdf                                                           |
| .php               | text/x-php                                                                |
| .pptx              | application/vnd.openxmlformats-officedocument.presentationml.presentation |
| .py                | text/x-python                                                             |
| .py                | text/x-script.python                                                      |
| .rb                | text/x-ruby                                                               |
| .sh                | application/x-sh                                                          |
| .tex               | text/x-tex                                                                |
| .ts                | application/typescript                                                    |
| .txt               | text/plain                                                                |

## Limitaciones

A continuación se muestran algunas limitaciones de uso de la búsqueda en archivos que los implementadores deben tener en cuenta.

* Los proyectos están limitados a un tamaño total de 100 GB para todos los archivos
* Los almacenes vectoriales están limitados a un total de 10.000 archivos
* Los archivos individuales pueden tener un tamaño máximo de 512 MB (aproximadamente 5 millones de tokens por archivo)
