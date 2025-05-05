import tkinter as tk
from tkinter import filedialog
import markdown
import re
import os
import pyttsx3
from detector_idioma import detectar_idioma  # Importa tu función de detección de idioma
from obtener_texto_plano_markdown import obtener_texto_plano_markdown # Importa la función de extracción de texto plano

def leer_markdown_con_tts_local():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo Markdown",
        filetypes=[("Archivos Markdown", "*.md")]
    )

    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenido_markdown = f.read()
            texto_plano = obtener_texto_plano_markdown(contenido_markdown)
            palabras = re.findall(r'\b\w+\b', texto_plano.lower()) # Extraer palabras

            # Cargar diccionarios (asume que están en el mismo directorio)
            def cargar_diccionario(nombre_archivo):
                try:
                    with open(nombre_archivo, 'r', encoding='utf-8') as f:
                        return set(line.strip().lower() for line in f)
                except FileNotFoundError:
                    print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
                    return set()

            diccionario_es = cargar_diccionario("palabras_espanol.txt")
            diccionario_en = cargar_diccionario("palabras_ingles.txt")
            diccionario_co = cargar_diccionario("cognados.txt")

            engine = pyttsx3.init()

            for palabra in palabras:
                if palabra:
                    lang_code = detectar_idioma(palabra, diccionario_es, diccionario_en, diccionario_co)
                    voice = None
                    for v in engine.getProperty('voices'):
                        if lang_code == 'es' and 'spanish' in v.name.lower():
                            voice = v.id
                            break
                        elif lang_code == 'en' and 'english' in v.name.lower():
                            voice = v.id
                            break
                    if voice:
                        engine.setProperty('voice', voice)
                    engine.say(palabra)
                    engine.runAndWait()

            engine.stop()

        except FileNotFoundError:
            print(f"Error: No se pudo abrir el archivo '{file_path}'.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    leer_markdown_con_tts_local()