import os
import subprocess
import re

# Configuraciones
input_folder = "./"
output_folder = "audios"
balcon_path = "balcon.exe"
voz_esp = "Microsoft Helena Desktop"  # Cambia esto según la voz instalada en tu sistema

os.makedirs(output_folder, exist_ok=True)

def clean_markdown(text):
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text, flags=re.DOTALL)
    text = re.sub(r'>+', '', text)
    text = re.sub(r'[#*_~`]', '', text)
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

def convert_to_audio(md_file):
    base_name = os.path.splitext(md_file)[0]
    txt_path = os.path.join(output_folder, f"{base_name}.txt")
    wav_path = os.path.join(output_folder, f"{base_name}.wav")
    mp3_path = os.path.join(output_folder, f"{base_name}.mp3")

    with open(os.path.join(input_folder, md_file), "r", encoding="utf-8") as f:
        raw_text = f.read()
    
    cleaned_text = clean_markdown(raw_text)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    comando = [
        balcon_path,
        "-f", txt_path,
        "-w", wav_path,
        "-n", voz_esp,
        "-v", "100",
        "-m", "1",
        "--encoding", "utf8"
    ]

    subprocess.run(comando, check=True)
    subprocess.run(["ffmpeg", "-y", "-i", wav_path, mp3_path], check=True)

    os.remove(txt_path)
    os.remove(wav_path)

    print(f"✅ Generado: {mp3_path}")

# Ejecutar para todos los .md
for archivo in os.listdir(input_folder):
    if archivo.endswith(".md"):
        try:
            convert_to_audio(archivo)
        except Exception as e:
            print(f"❌ Error con {archivo}: {e}")
