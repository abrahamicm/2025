import os
import subprocess
import re
import sys
import shutil

def limpiar_markdown(texto):
    """Limpia el texto en formato markdown para una mejor lectura por voz."""
    texto = re.sub(r'\*\*([^*]+)\*\*', r'\1', texto)
    texto = re.sub(r'\*([^*]+)\*', r'\1', texto)
    texto = re.sub(r'\[([^]]+)\]\(.*?\)', r'\1', texto)
    texto = re.sub(r'`[^`]*`', '', texto)
    texto = re.sub(r'```[\s\S]*?```', '', texto)
    texto = re.sub(r'\n{2,}', '\n\n', texto)
    texto = re.sub(r'#+ ', '', texto)
    return texto.strip()

def envolver_en_voz(texto, voz_eng):
    """Envuelve todo el texto en inglés con la voz correspondiente."""
    return f'<voice required="Name={voz_eng}">{texto}</voice>'

def verificar_comando(nombre):
    """Verifica si un comando está disponible en el sistema."""
    return shutil.which(nombre) is not None

def main():
    voz_eng = "Microsoft Zira Desktop"

    if not verificar_comando("balcon"):
        print("❌ Error: 'balcon' no está disponible en el sistema o no está en el PATH.")
        return
    if not verificar_comando("ffmpeg"):
        print("❌ Error: 'ffmpeg' no está disponible en el sistema o no está en el PATH.")
        return

    carpeta = sys.argv[1] if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]) else os.path.dirname(os.path.abspath(__file__))
    archivos_md = [archivo for archivo in os.listdir(carpeta) if archivo.endswith(".md")]

    if not archivos_md:
        print("⚠️ No se encontraron archivos Markdown (.md) en la carpeta.")
        return

    for archivo in archivos_md:
        try:
            nombre_base = os.path.splitext(archivo)[0]
            ruta_md = os.path.join(carpeta, archivo)
            ruta_txt = os.path.join(carpeta, f"{nombre_base}.txt")
            ruta_mp3 = os.path.join(carpeta, f"{nombre_base}.mp3")
            ruta_wav_temp = os.path.join(carpeta, f"{nombre_base}_temp.wav")

            try:
                with open(ruta_md, "r", encoding="utf-8") as f:
                    contenido = f.read()
            except UnicodeDecodeError:
                with open(ruta_md, "r", encoding="latin-1") as f:
                    contenido = f.read()

            texto_limpio = limpiar_markdown(contenido)
            if not texto_limpio.strip():
                print(f"⚠️ El archivo {archivo} está vacío o sin contenido útil tras limpiar.")
                continue

            texto_con_voz = envolver_en_voz(texto_limpio, voz_eng)
            with open(ruta_txt, "w", encoding="utf-8") as f:
                f.write(texto_con_voz)

            if os.path.getsize(ruta_txt) == 0:
                print(f"⚠️ El archivo {ruta_txt} está vacío después de escribir. Se omitirá.")
                continue

            comando_wav = [
                "balcon",
                "-f", ruta_txt,
                "-w", ruta_wav_temp,
                "-n", voz_eng,
                "-v", "100",
                "-m", "1",
                "--encoding", "utf8"
            ]

            print(f"\n🔊 Procesando a WAV: {archivo}")
            print(f"📤 Comando: {' '.join(comando_wav)}")
            resultado_wav = subprocess.run(comando_wav, capture_output=True, text=True)

            if resultado_wav.returncode != 0:
                print(f"❌ Error al generar WAV para {archivo}:\n{resultado_wav.stderr}\n{resultado_wav.stdout}")
                continue
            else:
                print(f"✅ Generado (WAV): {os.path.basename(ruta_wav_temp)}")

            if not os.path.exists(ruta_wav_temp):
                print(f"❌ El archivo WAV no se generó: {ruta_wav_temp}")
                continue

            if os.path.exists(ruta_mp3):
                try:
                    os.remove(ruta_mp3)
                except Exception as e:
                    print(f"❌ Error al eliminar MP3 anterior: {ruta_mp3}\n{e}")
                    continue

            comando_mp3 = f'ffmpeg -y -i "{ruta_wav_temp}" -vn -acodec libmp3lame "{ruta_mp3}"'

            print(f"🎼 Convirtiendo a MP3: {nombre_base}.mp3")
            print(f"📤 Comando: {comando_mp3}")
            resultado_mp3 = subprocess.run(comando_mp3, shell=True, capture_output=True, text=True)

            if resultado_mp3.returncode != 0:
                print(f"❌ Error al convertir a MP3 para {archivo}:\n{resultado_mp3.stderr}")
            else:
                print(f"✅ Generado (MP3): {nombre_base}.mp3")

            if os.path.exists(ruta_txt):
                os.remove(ruta_txt)
            if os.path.exists(ruta_wav_temp):
                os.remove(ruta_wav_temp)

        except Exception as e:
            print(f"❌ Error procesando {archivo}: {str(e)}")

    print("\n🎉 Proceso completado.")

if __name__ == "__main__":
    main()
