import os
import subprocess
import re
import sys

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

def main():
    voz_esp = "Microsoft Helena Desktop"  # Cambia aquí si deseas otra voz española

    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        carpeta = sys.argv[1]
    else:
        carpeta = os.path.dirname(os.path.abspath(__file__))

    archivos_md = [archivo for archivo in os.listdir(carpeta) if archivo.endswith(".md")]
    if not archivos_md:
        print("⚠️ No se encontraron archivos Markdown (.md) en la carpeta.")
        return

    for archivo in archivos_md:
        try:
            nombre_base = os.path.splitext(archivo)[0]
            ruta_md = os.path.join(carpeta, archivo)
            ruta_txt = os.path.join(carpeta, f"{nombre_base}.txt")
            ruta_wav = os.path.join(carpeta, f"{nombre_base}.wav")

            try:
                with open(ruta_md, "r", encoding="utf-8") as f:
                    contenido = f.read()
            except UnicodeDecodeError:
                with open(ruta_md, "r", encoding="latin-1") as f:
                    contenido = f.read()

            texto_limpio = limpiar_markdown(contenido)

            with open(ruta_txt, "w", encoding="utf-8") as f:
                f.write(texto_limpio)

            if os.path.getsize(ruta_txt) == 0:
                print(f"⚠️ El archivo {archivo} está vacío después de limpiarlo. Se omitirá.")
                os.remove(ruta_txt)
                continue

            comando = [
                "balcon",
                "-f", ruta_txt,
                "-w", ruta_wav,
                "-n", voz_esp,
                "-v", "100",
                "-m", "1",
                "--encoding", "utf8"
            ]

            print(f"🔊 Procesando: {archivo}")
            resultado = subprocess.run(comando, capture_output=True, text=True)
            
            if resultado.returncode != 0:
                print(f"❌ Error al procesar {archivo}: {resultado.stderr}")
            else:
                print(f"✅ Generado: {nombre_base}.wav")

            if os.path.exists(ruta_txt):
                os.remove(ruta_txt)

        except Exception as e:
            print(f"❌ Error procesando {archivo}: {str(e)}")

    print("🎉 Proceso completado.")

if __name__ == "__main__":
    main()
