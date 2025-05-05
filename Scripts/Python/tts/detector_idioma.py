¿import re
import tkinter as tk
from tkinter import filedialog
import markdown
import subprocess
import os

def cargar_diccionario(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return set(line.strip().lower() for line in f)
    except FileNotFoundError:
        return None

def detectar_idioma(palabra, diccionario_es, diccionario_en, diccionario_cognados):
    palabra = palabra.lower()
    if diccionario_cognados and palabra in diccionario_cognados:
        return "en"
    if re.search(r'[áéíóúñü]', palabra):
        return "es"
    if diccionario_es and palabra in diccionario_es:
        return "es"
    if diccionario_en and palabra in diccionario_en:
        return "en"
    return "es"  # predeterminado

def obtener_texto_plano_markdown(md):
    html = markdown.markdown(md)
    texto_plano = re.sub(r'<[^>]+>', '', ''.join(html.splitlines()))
    return texto_plano

def generar_audio(voz, texto, nombre_archivo):
    comando = [
        "balcon",
        "-t", texto,
        "-w", nombre_archivo,
        "-n", voz
    ]
    subprocess.run(comando)

def leer_markdown_tts_balcon_voz_dual():
    root = tk.Tk()
    root.withdraw()

    archivo = filedialog.askopenfilename(title="Seleccionar archivo Markdown", filetypes=[("Archivos Markdown", "*.md")])
    if not archivo:
        return

    with open(archivo, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    texto_plano = obtener_texto_plano_markdown(markdown_text)
    palabras = re.findall(r'\b\w+\b', texto_plano)

    dic_es = cargar_diccionario("palabras_espanol.txt")
    dic_en = cargar_diccionario("palabras_ingles.txt")
    dic_co = cargar_diccionario("cognados.txt")

    resultado = []
    bloque_actual = []
    idioma_actual = None
    archivos_audio = []

    for palabra in palabras:
        idioma = detectar_idioma(palabra, dic_es, dic_en, dic_co)
        if idioma_actual is None:
            idioma_actual = idioma

        if idioma == idioma_actual:
            bloque_actual.append(palabra)
        else:
            texto = ' '.join(bloque_actual)
            # Generar audio para el bloque
            nombre_archivo = f"audio_{len(archivos_audio)}.wav"
            if idioma_actual == "en":
                generar_audio("Microsoft David Desktop", texto, nombre_archivo)
            else:
                generar_audio("Microsoft Helena Desktop", texto, nombre_archivo)
            archivos_audio.append(nombre_archivo)

            bloque_actual = [palabra]
            idioma_actual = idioma

    if bloque_actual:
        texto = ' '.join(bloque_actual)
        nombre_archivo = f"audio_{len(archivos_audio)}.wav"
        if idioma_actual == "en":
            generar_audio("Microsoft David Desktop", texto, nombre_archivo)
        else:
            generar_audio("Microsoft Helena Desktop", texto, nombre_archivo)
        archivos_audio.append(nombre_archivo)

    # Unir los archivos de audio con ffmpeg
    archivos_audio_txt = "archivos_audio.txt"
    with open(archivos_audio_txt, "w") as f:
        for archivo in archivos_audio:
            f.write(f"file '{archivo}'\n")

    comando_ffmpeg = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", archivos_audio_txt,
        "-c", "copy",
        "audio_final.wav"
    ]

    print("Ejecutando:", ' '.join(comando_ffmpeg))
    subprocess.run(comando_ffmpeg)

    # Limpiar archivos temporales
    for archivo in archivos_audio:
        os.remove(archivo)

    os.remove(archivos_audio_txt)

    print("Audio final generado: audio_final.wav")

if __name__ == "__main__":
    leer_markdown_tts_balcon_voz_dual()
