import markdown
import re

def obtener_texto_plano_markdown(contenido_markdown):
    """
    Convierte contenido Markdown a texto plano eliminando la sintaxis Markdown.

    Args:
        contenido_markdown (str): El contenido del texto en formato Markdown.

    Returns:
        str: El texto plano resultante.
    """
    html = markdown.markdown(contenido_markdown)
    texto_plano = ''.join(html.splitlines())
    texto_plano = re.sub(r'<[^>]+>', '', texto_plano)
    return texto_plano

