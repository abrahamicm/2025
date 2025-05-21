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
    texto = re.sub(r'`[^`]*`', '', texto)              # elimina código inline
    texto = re.sub(r'```[\s\S]*?```', '', texto)         # elimina bloques de código
    texto = re.sub(r'\n{2,}', '\n\n', texto)              # reduce múltiples saltos a doble salto
    texto = re.sub(r'#+ ', '', texto)                     # elimina símbolos de encabezado
    return texto.strip()

def limpiar_palabra(palabra):
    """Elimina caracteres no alfabéticos de una palabra."""
    return re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]', '', palabra).lower()

def detectar_idioma(palabra, palabras_contexto=None):
    """
    Detecta el idioma de una palabra usando la frecuencia de palabras y contexto.
    Ahora considera palabras de contexto (anteriores y posteriores).
    """
    palabra_limpia = limpiar_palabra(palabra)

    if not palabra_limpia:
        return 'es'  # Si la palabra está vacía después de limpiar, asumimos español por defecto

    # Si la palabra es una letra o número, o muy corta, usamos el contexto
    if len(palabra_limpia) <= 2 or not palabra_limpia.isalpha():
        if palabras_contexto:
            for p_contexto in palabras_contexto:
                p_contexto_limpia = limpiar_palabra(p_contexto)
                if p_contexto_limpia and len(p_contexto_limpia) > 2 and p_contexto_limpia.isalpha():
                    frecuencia_esp_contexto = word_frequency(p_contexto_limpia, 'es')
                    frecuencia_eng_contexto = word_frequency(p_contexto_limpia, 'en')
                    if frecuencia_esp_contexto > frecuencia_eng_contexto:
                        return 'es'
                    elif frecuencia_eng_contexto > frecuencia_esp_contexto:
                        return 'en'
            return 'es' # Si no se encuentra un idioma claro en el contexto, default a español
        else:
            return 'es' # Default a español si no hay contexto

    frecuencia_esp = word_frequency(palabra_limpia, 'es')
    frecuencia_eng = word_frequency(palabra_limpia, 'en')

    # Si la frecuencia en español es significativamente mayor, lo consideramos español
    if frecuencia_esp > frecuencia_eng * 1.5:  # Umbral para español
        return 'es'
    # Si la frecuencia en inglés es significativamente mayor, lo consideramos inglés
    elif frecuencia_eng > frecuencia_esp * 1.5: # Umbral para inglés
        return 'en'
    else:
        # Si la confianza no es alta, intentamos con el contexto
        if palabras_contexto:
            for p_contexto in palabras_contexto:
                p_contexto_limpia = limpiar_palabra(p_contexto)
                if p_contexto_limpia and len(p_contexto_limpia) > 2 and p_contexto_limpia.isalpha():
                    frecuencia_esp_contexto = word_frequency(p_contexto_limpia, 'es')
                    frecuencia_eng_contexto = word_frequency(p_contexto_limpia, 'en')
                    if frecuencia_esp_contexto > frecuencia_eng_contexto:
                        return 'es'
                    elif frecuencia_eng_contexto > frecuencia_esp_contexto:
                        return 'en'
        return 'es' # Default a español si el contexto no ayuda

def envolver_en_voz(texto, idioma_actual, voz_esp, voz_eng):
    """Envuelve el texto en las etiquetas <voice> según el idioma detectado y escapa '/'."""
    palabras = texto.split()
    resultado = []
    bloque = []

    for i, palabra in enumerate(palabras):
        # Escapar el carácter '/' en la palabra (se mantiene en la palabra original para la salida)
        palabra_para_comparar = palabra.replace('/', '') # Esta es la palabra que se usa para la detección de idioma

        # Obtener palabras de contexto (anterior y siguiente)
        contexto = []
        if i > 0:
            contexto.append(palabras[i-1]) # Palabra anterior
        if i < len(palabras) - 1:
            contexto.append(palabras[i+1]) # Palabra siguiente

        idioma_palabra = detectar_idioma(palabra_para_comparar, contexto)

        if idioma_palabra != idioma_actual:
            if bloque:
                if idioma_actual == 'es':
                    resultado.append(f'<voice required="Name={voz_esp}">{ " ".join(bloque) }</voice>')
                else:
                    resultado.append(f'<voice required="Name={voz_eng}">{ " ".join(bloque) }</voice>')
            bloque = [palabra] # Añadimos la palabra original (sin limpiar '/') al bloque
            idioma_actual = idioma_palabra
        else:
            bloque.append(palabra) # Añadimos la palabra original (sin limpiar '/') al bloque

    if bloque:
        if idioma_actual == 'es':
            resultado.append(f'<voice required="Name={voz_esp}">{ " ".join(bloque) }</voice>')
        else:
            resultado.append(f'<voice required="Name={voz_eng}">{ " ".join(bloque) }</voice>')

    return " ".join(resultado)

def main():
    # Voces
    voz_esp = "Microsoft Helena Desktop"    # Español
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