#!/usr/bin/env python3
import os
import re
import json
import time
import requests
from pathlib import Path

# CONFIGURACIÓN - EDITA ESTAS VARIABLES
GEMINI_API_KEY = "AIzaSyC-UUQVbW4NByRlF659Dx2fOuJIP4SaYSc"  # Tu clave de API de Gemini
CARPETA_ENTRADA = "./"  # Carpeta con archivos de texto plano
CARPETA_SALIDA = "markdown"  # Carpeta donde se guardarán los archivos procesados
CARPETA_PROCESADOS = "procesados"  # Carpeta donde se moverán los archivos de texto ya procesados
INTERVALO_MONITOREO = 60  # Segundos entre cada revisión de la carpeta
LIMITE_ARCHIVOS = 10  # Máximo número de archivos a procesar en cada ciclo

def process_text_with_gemini(text):
    """
    Usa la API de Gemini para convertir texto a Markdown y poner en cursiva las palabras en inglés.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
acomoda el siguiente texto para que tenga mas sentido y sea mas claro
    
    Texto:
    {text}
    """
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Error en la API: {response.status_code}")
            print(response.text)
            return text  # Devolvemos el texto original si hay error
    except Exception as e:
        print(f"Error al llamar a la API: {e}")
        return text

def process_file(input_path, output_path):
    """
    Procesa un archivo de texto y lo guarda como Markdown.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        markdown_content = process_text_with_gemini(content)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        
        # Mover el archivo original a la carpeta de procesados
        processed_dir = Path(CARPETA_PROCESADOS)
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        processed_path = processed_dir / input_path.name
        
        # Si existe un archivo con el mismo nombre en la carpeta de procesados, añadir timestamp
        if processed_path.exists():
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            processed_path = processed_dir / f"{input_path.stem}_{timestamp}{input_path.suffix}"
        
        # Mover el archivo
        input_path.rename(processed_path)
        
        print(f"Procesado: {input_path} → {output_path}")
        print(f"Archivo original movido a: {processed_path}")
        return True
    except Exception as e:
        print(f"Error al procesar {input_path}: {e}")
        return False

def main():
    # Crear las carpetas necesarias si no existen
    output_dir = Path(CARPETA_SALIDA)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processed_dir = Path(CARPETA_PROCESADOS)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    input_dir = Path(CARPETA_ENTRADA)
    if not input_dir.exists():
        print(f"¡Error! La carpeta de entrada '{CARPETA_ENTRADA}' no existe.")
        print(f"Creando la carpeta '{CARPETA_ENTRADA}' para que agregues tus archivos de texto...")
        input_dir.mkdir(parents=True, exist_ok=True)
        return
    
    print(f"Iniciando monitoreo de la carpeta '{CARPETA_ENTRADA}'.")
    print(f"Los archivos Markdown se guardarán en '{CARPETA_SALIDA}'.")
    print(f"Los archivos originales se moverán a '{CARPETA_PROCESADOS}' después de procesarlos.")
    print(f"Se procesarán hasta {LIMITE_ARCHIVOS} archivos en cada ciclo.")
    print("Presiona Ctrl+C para detener.")
    
    try:
        while True:
            # Obtener los archivos ya procesados (basado en los nombres de archivo en la carpeta de salida)
            processed_files = set([f.stem for f in output_dir.glob('*.md')])
            
            # También considerar los archivos ya movidos a la carpeta de procesados
            processed_originals = set([f.stem for f in processed_dir.glob('*.txt')])
            
            # Combinar ambos conjuntos
            all_processed = processed_files.union(processed_originals)
            
            # Procesar archivos
            processed_count = 0
            for file_path in input_dir.glob('*.txt'):
                if processed_count >= LIMITE_ARCHIVOS:
                    break
                    
                if file_path.stem in all_processed:
                    continue
                    
                output_path = output_dir / f"{file_path.stem}.md"
                if process_file(file_path, output_path):
                    processed_count += 1
            
            if processed_count > 0:
                print(f"Se procesaron {processed_count} archivos nuevos")
            else:
                print(f"No hay archivos nuevos para procesar. Esperando {INTERVALO_MONITOREO} segundos...")
            
            time.sleep(INTERVALO_MONITOREO)
            
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario.")

if __name__ == "__main__":
    main()