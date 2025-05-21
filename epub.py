import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, Listbox, END, SINGLE, MULTIPLE, VERTICAL, Scrollbar
import os
import time
import json
from pathlib import Path
import threading
import re
import subprocess
import shutil

# --- Función para sanear nombres de archivo (reutilizada) ---
def sanitize_filename(name):
    """
    Limpia una cadena para usarla como nombre de archivo, eliminando caracteres inválidos.
    """
    cleaned_name = re.sub(r'[^\w\s\-\.]', '', name)
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
    cleaned_name = cleaned_name.replace(' ', '_')
    cleaned_name = cleaned_name.strip('_.')
    return cleaned_name

# --- Funciones de la GUI ---
def update_status(message, color="black"):
    """Actualiza el mensaje de estado en la GUI."""
    status_label.config(text=message, fg=color)
    root.update_idletasks() # Forzar actualización de la GUI

def select_markdown_files():
    """Permite al usuario seleccionar múltiples archivos Markdown."""
    filepaths = filedialog.askopenfilenames(
        title="Seleccionar Archivos Markdown",
        filetypes=[("Archivos Markdown", "*.md"), ("Todos los archivos", "*.*")]
    )
    if filepaths:
        # Limpiar la lista existente y añadir los nuevos archivos
        listbox_files.delete(0, END)
        for fp in filepaths:
            listbox_files.insert(END, fp)
        update_status(f"Archivos seleccionados: {len(filepaths)}. Ordénalos si es necesario.", "blue")
    else:
        update_status("No se seleccionaron archivos.", "orange")

def move_up():
    """Mueve el elemento seleccionado hacia arriba en la lista."""
    selected_indices = listbox_files.curselection()
    if not selected_indices:
        return
    
    # Obtener el primer índice seleccionado
    idx = selected_indices[0]
    if idx > 0:
        text = listbox_files.get(idx)
        listbox_files.delete(idx)
        listbox_files.insert(idx - 1, text)
        listbox_files.selection_set(idx - 1) # Mantener seleccionado el elemento movido

def move_down():
    """Mueve el elemento seleccionado hacia abajo en la lista."""
    selected_indices = listbox_files.curselection()
    if not selected_indices:
        return
    
    # Obtener el primer índice seleccionado
    idx = selected_indices[0]
    if idx < listbox_files.size() - 1:
        text = listbox_files.get(idx)
        listbox_files.delete(idx)
        listbox_files.insert(idx + 1, text)
        listbox_files.selection_set(idx + 1) # Mantener seleccionado el elemento movido

def select_output_directory():
    """Permite al usuario seleccionar un directorio de salida."""
    directory = filedialog.askdirectory(title="Seleccionar Directorio de Salida")
    if directory:
        output_dir_entry.delete(0, END)
        output_dir_entry.insert(0, directory)
        update_status(f"Directorio de salida: {directory}", "blue")

def select_cover_image():
    """Permite al usuario seleccionar una imagen de portada."""
    filepath = filedialog.askopenfilename(
        title="Seleccionar Imagen de Portada",
        filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.gif"), ("Todos los archivos", "*.*")]
    )
    if filepath:
        cover_image_entry.delete(0, END)
        cover_image_entry.insert(0, filepath)
        update_status(f"Imagen de portada seleccionada: {filepath}", "blue")

def generate_epub_process():
    """
    Función que genera el EPUB a partir de los archivos Markdown seleccionados.
    Se ejecuta en un hilo separado.
    """
    generate_epub_button.config(state=tk.DISABLED)
    select_files_button.config(state=tk.DISABLED)
    move_up_button.config(state=tk.DISABLED)
    move_down_button.config(state=tk.DISABLED)
    select_output_dir_button.config(state=tk.DISABLED)
    select_cover_image_button.config(state=tk.DISABLED)


    try:
        # Obtener la lista de archivos Markdown del Listbox
        markdown_files = [listbox_files.get(i) for i in range(listbox_files.size())]

        if not markdown_files:
            messagebox.showwarning("No hay archivos Markdown", "Por favor, selecciona archivos Markdown primero.")
            update_status("Creación de EPUB cancelada: No hay archivos seleccionados.", "orange")
            return

        # Obtener metadatos de los campos de entrada
        title = title_entry.get().strip()
        author = author_entry.get().strip()
        lang = lang_entry.get().strip()
        description = description_text.get("1.0", END).strip()
        
        if not title or not author or not lang:
            messagebox.showwarning("Metadatos incompletos", "Por favor, rellena el título, autor e idioma del EPUB.")
            update_status("Creación de EPUB cancelada: Metadatos incompletos.", "orange")
            return

        output_directory = Path(output_dir_entry.get())
        if not output_directory.is_dir():
            messagebox.showwarning("Directorio de Salida Inválido", "El directorio de salida especificado no existe o no es válido.")
            update_status("Creación de EPUB cancelada: Directorio de salida inválido.", "orange")
            return
        
        epub_filename = sanitize_filename(title) + ".epub"
        epub_output_path = output_directory / epub_filename

        cover_image_path_str = cover_image_entry.get().strip()
        temp_cover_image_name = None # Nombre temporal si copiamos la imagen
        
        update_status("Iniciando la creación del EPUB...", "blue")

        # 1. Preparar los metadatos del EPUB en un archivo YAML temporal
        metadata_content = f"""---
title: "{title}"
author: "{author}"
date: "{time.strftime('%Y-%m-%d')}"
lang: {lang}
description: "{description}"
rights: "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License"
...
"""
        metadata_file = output_directory / "metadata_temp.yaml"
        with open(metadata_file, "w", encoding="utf-8") as f:
            f.write(metadata_content)

        # 2. Copiar imagen de portada si se especificó, para que Pandoc la encuentre fácilmente
        final_cover_path = None
        if cover_image_path_str and Path(cover_image_path_str).is_file():
            try:
                cover_source = Path(cover_image_path_str)
                temp_cover_image_name = f"cover_{cover_source.name}"
                final_cover_path = output_directory / temp_cover_image_name
                shutil.copy(cover_source, final_cover_path)
                update_status(f"Copiando imagen de portada a: {final_cover_path}", "blue")
            except Exception as e:
                update_status(f"Advertencia: No se pudo copiar la imagen de portada: {e}", "orange")
                final_cover_path = None # No usar imagen de portada si falla la copia


        # 3. Construir el comando de Pandoc
        pandoc_command = [
            "pandoc",
            "--standalone",
            "--embed-resources", # Incluir recursos (como imágenes) en el EPUB
            "--metadata-file", str(metadata_file),
            "--output", str(epub_output_path),
            "--toc", # Generar tabla de contenidos
            "--toc-depth=2", # Hasta H2 en la tabla de contenidos
            "--epub-chapter-level=1" # Cada H1 será un nuevo capítulo
        ]
        
        if final_cover_path and final_cover_path.is_file():
            pandoc_command.extend(["--epub-cover-image", str(final_cover_path)])

        # Añadir todos los archivos Markdown al comando
        pandoc_command.extend([str(Path(f)) for f in markdown_files]) # Asegurarse de que sean objetos Path o cadenas

        # Ejecutar el comando de Pandoc
        result = subprocess.run(pandoc_command, capture_output=True, text=True, check=True)
        
        update_status(f"EPUB generado exitosamente en: {epub_output_path}", "green")
        messagebox.showinfo("EPUB Creado", f"El EPUB ha sido generado exitosamente en:\n{epub_output_path}")
        print(f"Pandoc stdout:\n{result.stdout}")
        if result.stderr:
            print(f"Pandoc stderr:\n{result.stderr}")
            # Puedes considerar mostrar un messagebox de advertencia si Pandoc emite errores menores
            # messagebox.showwarning("Advertencias de Pandoc", f"Pandoc generó advertencias:\n{result.stderr}")

    except FileNotFoundError:
        messagebox.showerror("Error: Pandoc no encontrado", "Pandoc no está instalado o no está en tu PATH. Por favor, instálalo desde pandoc.org.")
        update_status("Error: Pandoc no encontrado.", "red")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error al generar EPUB", f"Pandoc falló. Código de salida: {e.returncode}\nError: {e.stderr}")
        update_status("Error al generar EPUB. Revisa la consola para más detalles.", "red")
        print(f"Pandoc stdout:\n{e.stdout}")
        print(f"Pandoc stderr:\n{e.stderr}")
    except Exception as e:
        messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado al crear el EPUB: {e}")
        update_status("Error inesperado al crear EPUB.", "red")
    finally:
        # Limpiar el archivo de metadatos temporal
        if metadata_file.exists():
            os.remove(metadata_file)
        # Limpiar la imagen de portada temporal si se copió
        if temp_cover_image_name and (output_directory / temp_cover_image_name).exists():
             os.remove(output_directory / temp_cover_image_name)

        generate_epub_button.config(state=tk.NORMAL)
        select_files_button.config(state=tk.NORMAL)
        move_up_button.config(state=tk.NORMAL)
        move_down_button.config(state=tk.NORMAL)
        select_output_dir_button.config(state=tk.NORMAL)
        select_cover_image_button.config(state=tk.NORMAL)


def start_epub_generation_threaded():
    """Inicia el proceso de generación de EPUB en un nuevo hilo."""
    threading.Thread(target=generate_epub_process).start()


# --- Configuración de la Ventana Principal de Tkinter ---
root = tk.Tk()
root.title("Compilador de EPUB desde Markdown")
root.geometry("800x850") # Ajusta el tamaño de la ventana
root.resizable(True, True)

# --- Frame para selección de archivos ---
file_selection_frame = tk.LabelFrame(root, text="1. Seleccionar y Ordenar Archivos Markdown", padx=10, pady=10)
file_selection_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

select_files_button = tk.Button(file_selection_frame, text="Seleccionar Archivos Markdown", command=select_markdown_files)
select_files_button.pack(pady=5)

# Listbox para mostrar archivos seleccionados
listbox_frame = tk.Frame(file_selection_frame)
listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)

scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
listbox_files = Listbox(listbox_frame, selectmode=MULTIPLE, width=80, height=15, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_files.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox_files.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Botones para ordenar la lista
order_buttons_frame = tk.Frame(file_selection_frame)
order_buttons_frame.pack(pady=5)

move_up_button = tk.Button(order_buttons_frame, text="Mover Arriba", command=move_up)
move_up_button.pack(side=tk.LEFT, padx=5)
move_down_button = tk.Button(order_buttons_frame, text="Mover Abajo", command=move_down)
move_down_button.pack(side=tk.LEFT, padx=5)

# --- Frame para Metadatos del EPUB ---
metadata_frame = tk.LabelFrame(root, text="2. Metadatos del EPUB", padx=10, pady=10)
metadata_frame.pack(fill=tk.X, padx=10, pady=10)

tk.Label(metadata_frame, text="Título:").grid(row=0, column=0, sticky="w", pady=2)
title_entry = tk.Entry(metadata_frame, width=50)
title_entry.grid(row=0, column=1, sticky="ew", pady=2)
title_entry.insert(0, "Mi Curso de Flutter") # Valor por defecto

tk.Label(metadata_frame, text="Autor:").grid(row=1, column=0, sticky="w", pady=2)
author_entry = tk.Entry(metadata_frame, width=50)
author_entry.grid(row=1, column=1, sticky="ew", pady=2)
author_entry.insert(0, "Tu Nombre o Compañía") # Valor por defecto

tk.Label(metadata_frame, text="Idioma (ej. es, en):").grid(row=2, column=0, sticky="w", pady=2)
lang_entry = tk.Entry(metadata_frame, width=10)
lang_entry.grid(row=2, column=1, sticky="w", pady=2)
lang_entry.insert(0, "es") # Valor por defecto

tk.Label(metadata_frame, text="Descripción:").grid(row=3, column=0, sticky="nw", pady=2)
description_text = scrolledtext.ScrolledText(metadata_frame, wrap=tk.WORD, width=50, height=5)
description_text.grid(row=3, column=1, sticky="ew", pady=2)
description_text.insert("1.0", "Un curso completo sobre el desarrollo de aplicaciones móviles con Flutter.") # Valor por defecto

metadata_frame.grid_columnconfigure(1, weight=1) # Permite que la columna de entrada se expanda

# --- Frame para Directorio de Salida y Portada ---
output_options_frame = tk.LabelFrame(root, text="3. Opciones de Salida", padx=10, pady=10)
output_options_frame.pack(fill=tk.X, padx=10, pady=10)

tk.Label(output_options_frame, text="Directorio de Salida:").grid(row=0, column=0, sticky="w", pady=2)
output_dir_entry = tk.Entry(output_options_frame, width=50)
output_dir_entry.grid(row=0, column=1, sticky="ew", pady=2)
output_dir_entry.insert(0, Path.cwd() / "epub_output") # Directorio por defecto: una subcarpeta
select_output_dir_button = tk.Button(output_options_frame, text="Explorar...", command=select_output_directory)
select_output_dir_button.grid(row=0, column=2, padx=5, pady=2)

tk.Label(output_options_frame, text="Imagen de Portada (opcional):").grid(row=1, column=0, sticky="w", pady=2)
cover_image_entry = tk.Entry(output_options_frame, width=50)
cover_image_entry.grid(row=1, column=1, sticky="ew", pady=2)
select_cover_image_button = tk.Button(output_options_frame, text="Explorar...", command=select_cover_image)
select_cover_image_button.grid(row=1, column=2, padx=5, pady=2)

output_options_frame.grid_columnconfigure(1, weight=1)

# --- Botón Final de Generar EPUB ---
generate_epub_button = tk.Button(root, text="Generar EPUB", command=start_epub_generation_threaded,
                                font=("Helvetica", 14, "bold"), bg="#28A745", fg="white",
                                activebackground="#218838", cursor="hand2")
generate_epub_button.pack(pady=20)

# --- Etiqueta de Estado ---
status_label = tk.Label(root, text="Listo para generar EPUB.", font=("Helvetica", 10), bd=1, relief=tk.SUNKEN, anchor="w")
status_label.pack(side=tk.BOTTOM, fill=tk.X, ipady=5)

# Crear el directorio de salida por defecto si no existe
Path(output_dir_entry.get()).mkdir(parents=True, exist_ok=True)

# Iniciar el bucle principal de la aplicación Tkinter
root.mainloop()