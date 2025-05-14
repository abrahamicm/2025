import os
import subprocess
import re
import sys

def limpiar_markdown(texto):
    """Limpia el texto en formato markdown para una mejor lectura por voz."""
    texto = re.sub(r'\*\*([^*]+)\*\*', r'\1', texto)     # elimina negritas
    texto = re.sub(r'\*([^*]+)\*', r'\1', texto)         # elimina cursivas
    texto = re.sub(r'\[([^]]+)\]\(.*?\)', r'\1', texto)  # conserva texto de enlaces pero elimina URLs
    texto = re.sub(r'`[^`]*`', '', texto)                # elimina código inline
    texto = re.sub(r'```[\s\S]*?```', '', texto)         # elimina bloques de código
    texto = re.sub(r'\n{2,}', '\n\n', texto)             # reduce múltiples saltos a doble salto
    texto = re.sub(r'#+ ', '', texto)                    # elimina símbolos de encabezado
    return texto.strip()

def main():
    # Voces
    voz_principal = "Microsoft Helena Desktop"  # Español
    voz_secundaria = "Microsoft Zira Desktop"   # Inglés

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
            ruta_wav = os.path.join(carpeta, f"{nombre_base}.wav")

            # Leer y limpiar el texto
            try:
                with open(ruta_md, "r", encoding="utf-8") as f:
                    contenido = f.read()
                texto_limpio = limpiar_markdown(contenido)

                # Guardar como .txt
                with open(ruta_txt, "w", encoding="utf-8") as f:
                    f.write(texto_limpio)
            except UnicodeDecodeError:
                # Intentar con otra codificación si utf-8 falla
                with open(ruta_md, "r", encoding="latin-1") as f:
                    contenido = f.read()
                texto_limpio = limpiar_markdown(contenido)
                
                with open(ruta_txt, "w", encoding="utf-8") as f:
                    f.write(texto_limpio)

            # Verificar si el archivo de texto está vacío
            if os.path.getsize(ruta_txt) == 0:
                print(f"⚠️ El archivo {archivo} está vacío después de limpiarlo. Se omitirá.")
                os.remove(ruta_txt)
                continue

            # Ejecutar Balcon
            comando = [
                "balcon",
                "-f", ruta_txt,
                "-w", ruta_wav,
                "-n", voz_principal,
                "-v", "100",  # Volumen principal
                "-m", "1",    # Modo de cambio automático entre voces
                "-al", "es",  # Idioma principal (español)
                "-nl", "en",  # Idioma para detectar y cambiar (inglés)
                "-sv", voz_secundaria,  # Voz secundaria para texto en inglés
                "-lr", "2",   # Sensibilidad para detectar idioma (ajustar según necesidad)
                "--encoding", "utf8",  # Especificar codificación UTF-8 para acentos y caracteres especiales
                "-isb", "-icb", "-iab", "-irb", "-iu", "-ic"  # Ignora paréntesis, URLs, comentarios...
            ]

            print(f"🔊 Procesando: {archivo}")
            resultado = subprocess.run(comando, capture_output=True, text=True)
            
            if resultado.returncode != 0:
                print(f"❌ Error al procesar {archivo}: {resultado.stderr}")
            else:
                print(f"✅ Generado: {nombre_base}.wav")

            # Eliminar archivo temporal .txt
            if os.path.exists(ruta_txt):
                os.remove(ruta_txt)
                
        except Exception as e:
            print(f"❌ Error procesando {archivo}: {str(e)}")

    print("🎉 Proceso completado.")

if __name__ == "__main__":
    main()