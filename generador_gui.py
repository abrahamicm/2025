import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv
import threading # Necesario para evitar que la GUI se congele
import re # Necesario para la función de sanear nombres de archivo

# --- Configuración de la API de Gemini y variables de entorno ---
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-pro")

if not gemini_api_key:
    # Si no hay API Key, mostramos un error y salimos
    messagebox.showerror("Error de Configuración", "La API key de Gemini no está configurada en el archivo .env. Asegúrate de tener GEMINI_API_KEY='TU_CLAVE' allí.")
    exit()

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(gemini_model_name)

# --- Temas de Flutter (propuestos, puedes editarlos en la GUI) ---
default_flutter_topics = [
    # Fundamentos de Flutter y Dart
    "Introducción a Flutter: ¿Qué es y por qué usarlo?",
    "Configuración del entorno de desarrollo de Flutter (SDK, IDE)",
    "Conceptos básicos de Dart: Variables, tipos de datos y operadores",
    "Conceptos básicos de Dart: Estructuras de control (if/else, loops)",
    "Conceptos básicos de Dart: Funciones y clases",
    "Hello World en Flutter: Tu primera aplicación",

    # Widgets Fundamentales
    "Entendiendo los Widgets: Stateless vs Stateful",
    "Widgets de diseño básicos: Container, Row, Column",
    "Widgets de texto y estilo: Text, TextStyle",
    "Widgets de entrada de usuario: Button, TextField",
    "Concepto de 'Hot Reload' y 'Hot Restart'",
    "Explorando el árbol de widgets",

    # Manejo de Estado Básico
    "Conceptos de manejo de estado en Flutter",
    "StatefulWidget: La clase State y setState()",
    "Concepto de elevación de estado (lifting state up)",
    "Pasando datos entre Widgets (props en React/Vue)",

    # Navegación y Rutas
    "Navegación básica: Navigator y MaterialPageRoute",
    "Pasando argumentos entre pantallas",
    "Rutas con nombre (Named Routes)",

    # Listas y Desplazamiento
    "Creando listas con ListView.builder",
    "Widgets de desplazamiento: SingleChildScrollView, CustomScrollView",

    # Integración Web (Comparación y Transición)
    "Paralelismos entre Flutter y HTML/CSS: Widgets como elementos",
    "Cómo se maneja el diseño responsive en Flutter vs CSS Flexbox/Grid",
    "Comparación de manejo de eventos: JS Event Listeners vs Flutter Gestures",
    "Estado global en la web (Redux/Vuex) vs soluciones de estado en Flutter",

    # Recursos y Siguientes Pasos
    "Recursos oficiales de Flutter y Dart",
    "Comunidad de Flutter en español y dónde encontrar ayuda",
    "Herramientas de depuración en Flutter (DevTools)",
    "Introducción a la gestión de paquetes con pub.dev"
]

# --- Plantilla de Prompt (puedes editarla en la GUI) ---
default_prompt_template = """
Crea una lección Markdown completa sobre "{topic_text}" para desarrolladores web con experiencia en HTML, JavaScript y CSS que desean aprender Flutter.
El contenido debe estar en **español** y será utilizado tanto para texto-a-voz (TTS) como para visualización en Markdown.

Sigue estas reglas de formato y contenido:

- Todo el contenido debe empezar con un encabezado H1 (# Título), usando esta numeración de sección: {numbered_topic} ({section_num}.{subsection_num}).
- **No** uses listas numeradas ni tablas Markdown.
- **Puedes** usar listas no ordenadas (usando `-` o `*`), siempre que cada elemento sea corto y claro.
- Evita usar barras diagonales (/); en su lugar, usa comas o escribe cada elemento en una nueva línea.
- Siempre usa oraciones completas y con un sonido natural, adecuadas para TTS. Evita fragmentos de oraciones o palabras aisladas.
- Usa encabezados de sección (##) para dividir el contenido lógicamente.
- Introduce cada sección con una oración (ej. "En esta sección, exploraremos...").
- Usa transiciones en estilo de voz como “Ahora, veamos algunos ejemplos” o “Aquí tienes algunas frases útiles.”

El Markdown debe incluir:

## Introducción
Un párrafo corto que explique la importancia de este tema para un desarrollador web que aprende Flutter. Haz **comparaciones directas y útiles** con conceptos de HTML/CSS/JavaScript cuando sea relevante para facilitar la comprensión.

## Explicación
Una explicación clara y amigable para principiantes, escrita en párrafos completos. Incluye ejemplos simples incrustados donde sea útil. **Enfócate en cómo los conceptos de Flutter se relacionan o difieren de la experiencia web del usuario.**

## Ejemplos
Introduce esta sección con una oración como: “Ahora, veamos algunos ejemplos prácticos.”
- Lista códigos o conceptos clave relacionados con este tema de Flutter.
- Proporciona 2-5 fragmentos de código Flutter cortos y claros que demuestren el uso correcto.
- Usa listas no ordenadas o líneas separadas, sin tablas ni elementos numerados.
- **Añade comentarios dentro de los ejemplos de código** si es necesario para aclarar algo específico para un desarrollador web.

## Práctica: Preguntas y Respuestas
Crea 3-5 preguntas de práctica cortas relacionadas con el tema. Después de cada pregunta, inserta una cuenta regresiva escrita así:
**5... 4... 3... 2... 1...**
Luego, proporciona la respuesta en una nueva línea.

Ejemplo:
**Pregunta:** ¿Cuál es el equivalente de un `div` en Flutter para agrupar contenido?
**5... 4... 3... 2... 1...**
**Respuesta:** El widget `Container` o `Column`/`Row` para organizar.

Asegúrate de que el tono sea amigable, con un ritmo pausado y atractivo. Evita términos técnicos a menos que se expliquen en contexto.
"""

# --- Variables globales para el progreso y límites de tasa ---
output_dir = Path("flutter_course_materials_es")
output_dir.mkdir(exist_ok=True)
progress_file = output_dir / "progress.json"
completed_topics = {}
daily_requests = 0
requests_start_time = time.time()

# Cargar progreso previo si existe
if progress_file.exists():
    try:
        with open(progress_file, "r") as f:
            progress_data = json.load(f)
            completed_topics = progress_data.get("completed_topics", {})
            daily_requests = progress_data.get("daily_requests", 0)
            requests_start_time = progress_data.get("requests_start_time", time.time())
    except json.JSONDecodeError:
        print("Error al leer el archivo de progreso. Comenzando desde cero.")

# Verificar si ha pasado un día desde el último reinicio del contador
current_time = time.time()
if (current_time - requests_start_time) >= 86400:  # 86400 segundos = 24 horas
    daily_requests = 0
    requests_start_time = current_time

# --- Funciones de Lógica de Negocio (Rate Limiting, Guardar Progreso, Sanear Nombres) ---
def wait_for_rate_limit():
    """Maneja los límites de tasa de la API de Gemini."""
    global daily_requests, requests_start_time

    # Comprobar el límite diario (1500 solicitudes para el nivel gratuito)
    if daily_requests >= 1500:
        time_since_start = time.time() - requests_start_time
        if time_since_start < 86400:  # 86400 segundos = 24 horas
            wait_time = 86400 - time_since_start
            print(f"Límite diario alcanzado. Esperando {wait_time/3600:.2f} horas hasta reiniciar.")
            save_progress() # Guardar progreso antes de esperar mucho tiempo
            messagebox.showinfo("Límite Diario Alcanzado", f"Has alcanzado el límite diario de solicitudes. La aplicación esperará {wait_time/3600:.2f} horas para reanudar.")
            time.sleep(wait_time) # Espera real
            daily_requests = 0
            requests_start_time = time.time() # Reiniciar contador y tiempo

    # Límite de tasa por minuto (30 RPM para el nivel gratuito, ~2 segundos por solicitud)
    time.sleep(2) # Esperar 2 segundos entre solicitudes para mantener un máximo de 30 por minuto

def save_progress():
    """Guarda el estado actual del progreso en un archivo JSON."""
    with open(progress_file, "w") as f:
        progress_data = {
            "completed_topics": completed_topics,
            "daily_requests": daily_requests,
            "requests_start_time": requests_start_time
        }
        json.dump(progress_data, f)

def sanitize_filename(name):
    """
    Limpia una cadena para usarla como nombre de archivo, eliminando caracteres inválidos.
    """
    # Reemplaza caracteres no alfanuméricos (excepto espacios, guiones y puntos) con nada.
    # Luego, reemplaza espacios con guiones bajos.
    # Elimina puntos al principio y al final (excepto la extensión final).
    cleaned_name = re.sub(r'[^\w\s\-\.]', '', name) # Quitar todo lo que no sea letra, número, espacio, guion o punto
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip() # Unir espacios múltiples
    cleaned_name = cleaned_name.replace(' ', '_') # Reemplazar espacios con guiones bajos
    cleaned_name = cleaned_name.strip('_.') # Eliminar guiones bajos o puntos al inicio/fin (excepto la extensión)
    return cleaned_name

# --- Funciones de la GUI ---
def update_status(message, color="black"):
    """Actualiza el mensaje de estado en la GUI."""
    status_label.config(text=message, fg=color)
    root.update_idletasks() # Forzar actualización de la GUI para que se vea el cambio inmediatamente

def generate_content_thread():
    """
    Función que se ejecuta en un hilo separado para generar el contenido.
    Evita que la GUI se congele durante las peticiones a la API.
    """
    global daily_requests, completed_topics

    topics_raw = topics_textarea.get("1.0", tk.END).strip()
    prompt_template = prompt_textarea.get("1.0", tk.END).strip()

    if not topics_raw:
        messagebox.showwarning("Entrada Vacía", "Por favor, ingresa al menos un tema en el campo 'Temas de Flutter'.")
        generate_button.config(state=tk.NORMAL)
        return

    topics_list = [t.strip() for t in topics_raw.split('\n') if t.strip()]
    if not topics_list:
        messagebox.showwarning("Entrada Vacía", "La lista de temas no puede estar vacía. Asegúrate de tener temas válidos.")
        generate_button.config(state=tk.NORMAL)
        return

    update_status("Iniciando generación de contenido...", "blue")
    
    # Simular la numeración de temas (ajusta esta lógica si necesitas una estructura de secciones más compleja)
    numbered_topics = []
    section_num = 1
    subcounter = 1
    
    # Aquí, simplemente asignamos un número de sección basado en un contador genérico.
    # Podrías refinar esto para tener secciones fijas o agrupaciones lógicas más complejas.
    for i, topic in enumerate(topics_list):
        if i > 0 and i % 10 == 0: # Ejemplo: cambia de sección cada 10 temas
            section_num += 1
            subcounter = 1
        
        numbered_topic_str = f"{section_num}.{subcounter}. {topic}"
        numbered_topics.append(numbered_topic_str)
        subcounter += 1

    total_topics = len(numbered_topics)
    success_count = 0
    error_count = 0

    for i, numbered_topic in enumerate(numbered_topics):
        # Separar número de sección, subsección y el texto del tema
        parts = numbered_topic.split('.', 2)
        if len(parts) < 3: # Manejar casos donde el tema no tenga el formato esperado
            update_status(f"Error de formato en el tema: '{numbered_topic}'. Saltando.", "red")
            error_count += 1
            continue
            
        section_part = parts[0]
        sub_part = parts[1]
        topic_text = parts[2].strip()
        
        # Sanear el nombre del tema para usarlo en el nombre del archivo
        cleaned_topic_name = sanitize_filename(topic_text)
        filename = f"{section_part}_{sub_part}_{cleaned_topic_name.lower()}.md"
        file_path = output_dir / filename

        if filename in completed_topics:
            update_status(f"Saltando tema ya completado: {numbered_topic} ({i+1}/{total_topics})", "gray")
            success_count += 1
            continue

        update_status(f"Generando contenido para: {numbered_topic} ({i+1}/{total_topics}). Solicitudes hoy: {daily_requests}/1500", "darkgreen")

        try:
            wait_for_rate_limit() # Esperar para cumplir con los límites de la API

            # Construir el prompt específico para este tema, formateando los placeholders
            current_prompt = prompt_template.format(
                topic_text=topic_text,
                numbered_topic=numbered_topic,
                section_num=section_part,
                subsection_num=sub_part
            )
            
            response = model.generate_content(current_prompt)
            daily_requests += 1

            # Guardar el contenido en un archivo Markdown
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)

            completed_topics[filename] = True
            save_progress() # Guardar progreso después de cada tema completado
            success_count += 1
            
        except Exception as e:
            error_count += 1
            error_message = f"Error al generar '{numbered_topic}': {e}"
            update_status(error_message, "red")
            print(error_message) # También imprimir en consola para depuración
            
            # Reintentar en caso de error de límite de tasa
            if "rate" in str(e).lower() or "limit" in str(e).lower() or "429" in str(e):
                update_status("Detectado límite de tasa. Esperando 60 segundos antes de reintentar el mismo tema...", "orange")
                time.sleep(60)
                # Decrementar 'i' para que el mismo tema se reintente en la siguiente iteración
                i -= 1 
            else:
                time.sleep(5) # Pequeña pausa para otros tipos de errores antes de continuar

    # Mensaje final al terminar el proceso
    update_status(f"¡Proceso completado! Archivos generados: {success_count}/{total_topics} (Errores: {error_count})", "green")
    generate_button.config(state=tk.NORMAL) # Habilitar el botón de nuevo al finalizar

def start_generation_threaded():
    """Inicia el proceso de generación en un nuevo hilo."""
    generate_button.config(state=tk.DISABLED) # Deshabilitar el botón para evitar clics dobles
    threading.Thread(target=generate_content_thread).start()

# --- Configuración de la Ventana Principal de Tkinter ---
root = tk.Tk()
root.title("Generador de Contenido de Cursos de Flutter con Gemini")
root.geometry("900x750") # Tamaño inicial de la ventana
root.resizable(True, True) # Permite redimensionar la ventana

# --- Frame principal para organizar los elementos ---
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# --- Widget de Temas ---
tk.Label(main_frame, text="Temas de Flutter (un tema por línea):", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))
topics_textarea = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=100, height=18, font=("Helvetica", 10))
topics_textarea.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
# Cargar temas por defecto al iniciar
for topic in default_flutter_topics:
    topics_textarea.insert(tk.END, topic + "\n")

# --- Widget de Prompt ---
tk.Label(main_frame, text="Plantilla de Prompt para Gemini:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))
prompt_textarea = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=100, height=18, font=("Helvetica", 10))
prompt_textarea.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
# Cargar prompt por defecto al iniciar
prompt_textarea.insert(tk.END, default_prompt_template)

# --- Botón de Generación ---
generate_button = tk.Button(root, text="Generar Contenido", command=start_generation_threaded,
                            font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white",
                            activebackground="#45a049", cursor="hand2")
generate_button.pack(pady=15)

# --- Etiqueta de Estado ---
status_label = tk.Label(root, text="Listo para generar.", font=("Helvetica", 10), bd=1, relief=tk.SUNKEN, anchor="w")
status_label.pack(side=tk.BOTTOM, fill=tk.X, ipady=5)

# Iniciar el bucle principal de la aplicación Tkinter
root.mainloop()