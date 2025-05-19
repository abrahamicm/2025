import os
import subprocess
import re

# Ruta donde están los archivos .md
input_folder = "./"
# Ruta donde se guardarán los audios
output_folder = "./"
# Ruta del ejecutable de Balcon
balcon_path = "balcon.exe"

# Asegura que exista la carpeta de salida
os.makedirs(output_folder, exist_ok=True)

def clean_markdown(text):
    # Elimina imágenes, links, código, citas, y estilo markdown
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # imágenes ![]()
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # links []()
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text, flags=re.DOTALL)  # código en línea y bloques
    text = re.sub(r'>+', '', text)  # citas
    text = re.sub(r'[#*_\-~`]', '', text)  # símbolos de estilo en línea
    text = re.sub(r'^[=\-~`#_*]{3,}$', '', text, flags=re.MULTILINE)  # líneas separadoras como ===, ---, ***
    text = re.sub(r'\n{2,}', '\n', text)  # múltiples saltos de línea
    return text.strip()


def convert_to_audio(md_file):
    with open(os.path.join(input_folder, md_file), 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    cleaned_text = clean_markdown(raw_text)
    
    # Guarda el texto temporalmente en un .txt
    txt_path = os.path.join(output_folder, "temp.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    
    wav_output = os.path.join(output_folder, md_file.replace('.md', '.wav'))
    mp3_output = os.path.join(output_folder, md_file.replace('.md', '.mp3'))

    # Usa Balcon para generar un .wav
    subprocess.run([balcon_path, "-f", txt_path,  "-enc", "utf8","-w", wav_output], check=True)

    # Convierte el .wav a .mp3 usando ffmpeg
    subprocess.run(["ffmpeg", "-y", "-i", wav_output, mp3_output], check=True)

    # Borra el archivo temporal y el .wav
    os.remove(txt_path)
    os.remove(wav_output)

    print(f"✅ Generado: {mp3_output}")

# Procesa todos los .md en la carpeta
for file in os.listdir(input_folder):
    if file.endswith(".md"):
        try:
            convert_to_audio(file)
        except Exception as e:
            print(f"❌ Error con {file}: {e}")
