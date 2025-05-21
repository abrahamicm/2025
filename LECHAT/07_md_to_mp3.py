import os
import subprocess
import re
import sys
from wordfreq import word_frequency

def limpiar_markdown(texto):
    """Limpia el texto en formato markdown para una mejor lectura por voz."""
    texto = re.sub(r'\*\*([^*]+)\*\*', r'\1', texto)      # elimina negritas
    texto = re.sub(r'\*([^*]+)\*', r'\1', texto)        # elimina cursivas
    texto = re.sub(r'\[([^]]+)\]\(.*?\)', r'\1', texto)  # conserva texto de enlaces pero elimina URLs
    texto = re.sub(r'`[^`]*`', '', texto)               # elimina código inline
    texto = re.sub(r'```[\s\S]*?```', '', texto)         # elimina bloques de código
    texto = re.sub(r'\n{2,}', '\n\n', texto)              # reduce múltiples saltos a doble salto
    texto = re.sub(r'#+ ', '', texto)                     # elimina símbolos de encabezado
    return texto.strip()

def detectar_idioma(palabra, siguiente_palabra=None):
    """Detecta el idioma de una palabra usando la frecuencia de palabras y contexto."""

    # Si la palabra es una letra o número, no podemos determinar el idioma directamente,
    # por lo que miramos la siguiente palabra
    if palabra.isalpha() and len(palabra) == 1:  # Si es una letra
        if siguiente_palabra:
            return detectar_idioma(siguiente_palabra)  # Llamamos recursivamente con la siguiente palabra
        else:
            return 'es'  # Default a español si no hay palabra siguiente

    if palabra.isdigit():  # Si es un número
        if siguiente_palabra:
            return detectar_idioma(siguiente_palabra)  # Llamamos recursivamente con la siguiente palabra
        else:
            return 'es'  # Default a español si no hay palabra siguiente

    # Normalmente verificamos la frecuencia de la palabra
    frecuencia_esp = word_frequency(palabra, 'es')
    frecuencia_eng = word_frequency(palabra, 'en')

    # Si la frecuencia en español es mayor, lo consideramos español
    if frecuencia_esp > frecuencia_eng:
        return 'es'  # Español
    else:
        return 'en'  # Inglés

def envolver_en_voz(texto, idioma_actual, voz_esp, voz_eng):
    """Envuelve el texto en las etiquetas <voice> según el idioma detectado y escapa '/'."""
    palabras = texto.split()  # Dividimos el texto en palabras
    resultado = []
    bloque = []

    # Iteramos sobre las palabras y las procesamos
    for i, palabra in enumerate(palabras):
        # Escapar el carácter '/' en la palabra
        palabra_escapada = palabra.replace('/', '')
        
        # Miramos la siguiente palabra para detectar el idioma
        siguiente_palabra = palabras[i+1] if i+1 < len(palabras) else None
        idioma_palabra = detectar_idioma(palabra_escapada, siguiente_palabra) # Usamos palabra_escapada para la detección si es relevante

        # Si cambia de idioma, cerramos el bloque anterior y comenzamos uno nuevo
        if idioma_palabra != idioma_actual:
            if bloque:
                if idioma_actual == 'es':
                    resultado.append(f'<voice required="Name={voz_esp}">{ " ".join(bloque) }</voice>')
                else:
                    resultado.append(f'<voice required="Name={voz_eng}">{ " ".join(bloque) }</voice>')
            bloque = [palabra_escapada]
            idioma_actual = idioma_palabra
        else:
            bloque.append(palabra_escapada)

    # Al final agregamos el bloque restante
    if bloque:
        if idioma_actual == 'es':
            resultado.append(f'<voice required="Name={voz_esp}">{ " ".join(bloque) }</voice>')
        else:
            resultado.append(f'<voice required="Name={voz_eng}">{ " ".join(bloque) }</voice>')

    return " ".join(resultado)

def main():
    # Voces
    voz_esp = "Microsoft Helena Desktop"   # Español
    voz_eng = "Microsoft Zira Desktop"    # Inglés

    # Carpeta actual o carpeta especificada como argumento
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        carpeta = sys.argv[1]
    else:
        carpeta = os.path.dirname(os.path.abspath(__file__))

    # Verificar si existe algún archivo .md
    archivos_md = [archivo for archivo in os.listdir(carpeta) if archivo.endswith(".md")]
    if not archivos_md:
        print("⚠️ No se encontraron archivos Markdown (.md) en la carpeta.")
        return

    # Procesar todos los archivos .md en la carpeta
    for archivo in archivos_md:
        try:
            nombre_base = os.path.splitext(archivo)[0]
            ruta_md = os.path.join(carpeta, archivo)
            ruta_txt = os.path.join(carpeta, f"{nombre_base}.txt")
            ruta_mp3 = os.path.join(carpeta, f"{nombre_base}.mp3")

            # Leer y limpiar el texto
            try:
                with open(ruta_md, "r", encoding="utf-8") as f:
                    contenido = f.read()
                texto_limpio = limpiar_markdown(contenido)

                # Envuelve el texto limpio en las etiquetas <voice>
                texto_con_voz = envolver_en_voz(texto_limpio, 'es', voz_esp, voz_eng)

                # Guardar como .txt
                with open(ruta_txt, "w", encoding="utf-8") as f:
                    f.write(texto_con_voz)
            except UnicodeDecodeError:
                # Intentar con otra codificación si utf-8 falla
                with open(ruta_md, "r", encoding="latin-1") as f:
                    contenido = f.read()
                texto_limpio = limpiar_markdown(contenido)
                texto_con_voz = envolver_en_voz(texto_limpio, 'es', voz_esp, voz_eng)

                with open(ruta_txt, "w", encoding="utf-8") as f:
                    f.write(texto_con_voz)

            # Verificar si el archivo de texto está vacío
            if os.path.getsize(ruta_txt) == 0:
                print(f"⚠️ El archivo {archivo} está vacío después de limpiarlo. Se omitirá.")
                os.remove(ruta_txt)
                continue

            # Ejecutar Balcon para generar el archivo WAV
            ruta_wav_temp = os.path.join(carpeta, f"{nombre_base}_temp.wav")
            comando_wav = [
                "balcon",
                "-f", ruta_txt,
                "-w", ruta_wav_temp,
                "-n", voz_esp,
                "-v", "100",    # Volumen principal
                "-m", "1",      # Modo de cambio automático entre voces
                "--encoding", "utf8",  # Especificar codificación UTF-8 para acentos y caracteres especiales
            ]

            print(f"🔊 Procesando a WAV: {archivo}")
            resultado_wav = subprocess.run(comando_wav, capture_output=True, text=True)

            if resultado_wav.returncode != 0:
                print(f"❌ Error al generar WAV para {archivo}: {resultado_wav.stderr}")
            else:
                print(f"✅ Generado (WAV): {nombre_base}_temp.wav")

                # Convertir el archivo WAV a MP3 usando ffmpeg
                comando_mp3 = [
                    "ffmpeg",
                    "-i", ruta_wav_temp,
                    "-vn",  # No incluir video
                    "-acodec", "libmp3lame",
                    ruta_mp3
                ]
                print(f"🎼 Convirtiendo a MP3: {nombre_base}.mp3")
                resultado_mp3 = subprocess.run(comando_mp3, capture_output=True, text=True)

                if resultado_mp3.returncode != 0:
                    print(f"❌ Error al convertir a MP3 para {archivo}: {resultado_mp3.stderr}")
                else:
                    print(f"✅ Generado (MP3): {nombre_base}.mp3")

            # Eliminar archivos temporales
            if os.path.exists(ruta_txt):
                os.remove(ruta_txt)
            if os.path.exists(ruta_wav_temp):
                os.remove(ruta_wav_temp)

        except Exception as e:
            print(f"❌ Error procesando {archivo}: {str(e)}")

    print("🎉 Proceso completado.")

if __name__ == "__main__":
    main()