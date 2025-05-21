#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob

def extract_plain_text_from_markdown(markdown_content):
    """
    Extrae el texto plano de un archivo Markdown eliminando elementos de formato.
    
    Args:
        markdown_content (str): Contenido del archivo Markdown.
    
    Returns:
        str: Texto plano extraído del Markdown.
    """
    # Eliminar enlaces [texto](url) -> texto
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', markdown_content)
    
    # Eliminar imágenes ![alt](url) -> alt
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)
    
    # Eliminar encabezados # Texto -> Texto
    text = re.sub(r'^#+\s+(.+)$', r'\1', text, flags=re.MULTILINE)
    
    # Eliminar negrita y cursiva **texto** o __texto__ o *texto* o _texto_ -> texto
    text = re.sub(r'(\*\*|__|\*|_)([^*_]+)(\*\*|__|\*|_)', r'\2', text)
    
    # Eliminar bloques de código ```código``` -> código
    text = re.sub(r'```[^\n]*\n(.*?)\n```', r'\1', text, flags=re.DOTALL)
    
    # Eliminar código en línea `código` -> código
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Eliminar líneas horizontales --- o *** o ___
    text = re.sub(r'^(---|\*\*\*|___)$', '', text, flags=re.MULTILINE)
    
    # Eliminar citas > texto -> texto
    text = re.sub(r'^>\s+(.+)$', r'\1', text, flags=re.MULTILINE)
    
    # Eliminar listas - item o * item o + item -> item
    text = re.sub(r'^[\-\*\+]\s+(.+)$', r'\1', text, flags=re.MULTILINE)
    
    # Eliminar listas numeradas 1. item -> item
    text = re.sub(r'^\d+\.\s+(.+)$', r'\1', text, flags=re.MULTILINE)
    
    # Eliminar líneas en blanco múltiples
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def process_markdown_files():
    """
    Busca todos los archivos Markdown en la misma carpeta del script,
    extrae el texto plano y lo guarda en archivos de texto correspondientes.
    """
    # Obtener la ruta del directorio donde se encuentra el script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Si script_directory está vacío (cuando se ejecuta desde el directorio actual)
    if not script_directory:
        script_directory = os.getcwd()
    
    print(f"Buscando archivos Markdown en: {script_directory}")
    
    # Buscar todos los archivos .md en el directorio
    markdown_files = glob.glob(os.path.join(script_directory, "*.md"))
    
    if not markdown_files:
        print("No se encontraron archivos Markdown en el directorio.")
        return
    
    print(f"Se encontraron {len(markdown_files)} archivos Markdown.")
    
    # Procesar cada archivo Markdown
    for md_file_path in markdown_files:
        try:
            # Obtener el nombre del archivo sin la extensión
            file_name = os.path.basename(md_file_path)
            base_name = os.path.splitext(file_name)[0]
            
            # Crear el nombre del archivo de texto de salida
            txt_file_path = os.path.join(script_directory, f"{base_name}.txt")
            
            print(f"Procesando: {file_name}")
            
            # Leer el contenido del archivo Markdown
            with open(md_file_path, 'r', encoding='utf-8') as md_file:
                markdown_content = md_file.read()
            
            # Extraer el texto plano
            plain_text = extract_plain_text_from_markdown(markdown_content)
            
            # Guardar el texto plano en un archivo de texto
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(plain_text)
            
            print(f"  → Archivo de texto creado: {base_name}.txt")
            
        except Exception as e:
            print(f"Error al procesar {md_file_path}: {str(e)}")
    
    print("Proceso completado.")

if __name__ == "__main__":
    process_markdown_files()