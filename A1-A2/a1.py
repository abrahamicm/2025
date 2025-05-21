import google.generativeai as genai
import os
import time
import datetime
import json
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar la API de Gemini usando variables de entorno
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-pro")  # Valor por defecto si no está definido

if not gemini_api_key:
    raise ValueError("La API key de Gemini no está configurada en el archivo .env")

genai.configure(api_key=gemini_api_key)

# Modelo a utilizar desde .env
model = genai.GenerativeModel(gemini_model_name)

# Lista de temas (solo A1)
english_topics = [
    # NIVEL A1 (PRINCIPIANTE)
    # Fundamentos del Idioma
    "English alphabet and basic pronunciation",
    "Numbers from 1 to 100",
    "Basic colors",
    "Days of the week and months",
    "Time and dates",
    "Countries and nationalities",
    
    # Gramática Básica A1
    "Verb 'to be' (affirmative, negative and interrogative forms)",
    "Personal pronouns (I, you, he, she, it, we, they)",
    "Possessive adjectives (my, your, his, her, its, our, their)",
    "Demonstrative pronouns (this, that, these, those)",
    "Present simple tense (common verbs, affirmative, negative, questions)",
    "Third person singular (-s)",
    "There is / There are",
    "Countable and uncountable nouns",
    "Some / Any",
    "Prepositions of place (in, on, under, next to, between)",
    "Prepositions of time (in, on, at)",
    "Articles - a, an, the",
    
    # Vocabulario A1
    "Greetings and farewells",
    "Personal introductions",
    "Family and relationships",
    "Occupations and workplaces",
    "House and furniture",
    "Food and drinks",
    "Clothes and accessories",
    "Parts of the body",
    "Daily routine",
    "Free time activities",
    "Places in the city",
    "Basic transportation",
    "Basic weather",
    
    # Habilidades Comunicativas A1
    "Greeting and saying goodbye",
    "Introducing yourself and others",
    "Giving basic personal information",
    "Asking simple questions",
    "Expressing likes and dislikes (like/don't like)",
    "Asking for and giving simple directions",
    "Talking about daily routine",
    "Ordering food in a restaurant",
    "Shopping for basic items",
    "Talking about abilities (can/can't)",
    
    # Comprensión Escrita y Oral A1
    "Reading comprehension - public signs and notices",
    "Reading comprehension - simple advertisements",
    "Reading comprehension - restaurant menus",
    "Reading comprehension - schedules and programs",
    "Reading comprehension - informal emails",
    "Listening comprehension - everyday dialogues",
    "Listening comprehension - simple public announcements",
    "Listening comprehension - instructions and directions",
    
    # Expresión Escrita A1
    "Writing short notes and messages",
    "Filling out forms (personal data)",
    "Writing postcards and brief letters",
    
    # Temas Culturales y Sociales A1
    "Politeness formulas in English",
    "Festivities in English-speaking countries",
    "Typical foods in English-speaking countries",
    
    # Estrategias de Aprendizaje A1
    "Vocabulary memorization techniques",
    "Using bilingual dictionaries",
    "Language learning applications"
]

# Agregar numeración a los temas para referencias cruzadas
numbered_topics = []
section_counters = {
    "A1 Fundamentals": 1,
    "A1 Grammar": 2,
    "A1 Vocabulary": 3,
    "A1 Communication": 4,
    "A1 Reading & Listening": 5,
    "A1 Writing": 6,
    "A1 Cultural": 7,
    "A1 Learning": 8
}

current_section = "A1 Fundamentals"
counter = 1
subcounter = 1

# Clasificar cada tema en su sección correcta
for topic in english_topics:
    # Determinar a qué sección pertenece cada tema
    if counter <= 6:
        current_section = "A1 Fundamentals"
        section_num = 1
    elif counter <= 18:
        current_section = "A1 Grammar"
        section_num = 2
    elif counter <= 31:
        current_section = "A1 Vocabulary"
        section_num = 3
    elif counter <= 41:
        current_section = "A1 Communication"
        section_num = 4
    elif counter <= 49:
        current_section = "A1 Reading & Listening"
        section_num = 5
    elif counter <= 52:
        current_section = "A1 Writing"
        section_num = 6
    elif counter <= 55:
        current_section = "A1 Cultural"
        section_num = 7
    else:
        current_section = "A1 Learning"
        section_num = 8
    
    # Crear la numeración en formato "X.Y. Tema"
    numbered_topic = f"{section_num}.{subcounter}. {topic}"
    numbered_topics.append(numbered_topic)
    
    counter += 1
    
    # Resetear el subcounter cuando cambia la sección
    if counter <= 6:
        if current_section != "A1 Fundamentals":
            current_section = "A1 Fundamentals"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 18:
        if current_section != "A1 Grammar":
            current_section = "A1 Grammar"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 31:
        if current_section != "A1 Vocabulary":
            current_section = "A1 Vocabulary"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 41:
        if current_section != "A1 Communication":
            current_section = "A1 Communication"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 49:
        if current_section != "A1 Reading & Listening":
            current_section = "A1 Reading & Listening"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 52:
        if current_section != "A1 Writing":
            current_section = "A1 Writing"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 55:
        if current_section != "A1 Cultural":
            current_section = "A1 Cultural"
            subcounter = 1
        else:
            subcounter += 1
    else:
        if current_section != "A1 Learning":
            current_section = "A1 Learning"
            subcounter = 1
        else:
            subcounter += 1

# Directorio para guardar los archivos markdown
output_dir = Path("english_course_materials_a1")
output_dir.mkdir(exist_ok=True)

# Archivo para guardar el progreso y poder reanudar si se interrumpe
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

# Función para manejar los límites de tasa
def wait_for_rate_limit():
    global daily_requests, requests_start_time
    
    # Comprobar el límite diario (1500 solicitudes)
    if daily_requests >= 1500:
        time_since_start = time.time() - requests_start_time
        if time_since_start < 86400:  # 86400 segundos = 24 horas
            wait_time = 86400 - time_since_start
            print(f"Límite diario alcanzado. Esperando {wait_time/3600:.2f} horas hasta reiniciar.")
            # Guardar progreso antes de esperar
            save_progress()
            time.sleep(wait_time)
            daily_requests = 0
            requests_start_time = time.time()
    
    # Límite de tasa por minuto (30 RPM para el nivel gratuito)
    # Esperar 2 segundos entre solicitudes para mantener un máximo de 30 por minuto
    time.sleep(2)

# Función para guardar el progreso
def save_progress():
    with open(progress_file, "w") as f:
        progress_data = {
            "completed_topics": completed_topics,
            "daily_requests": daily_requests,
            "requests_start_time": requests_start_time
        }
        json.dump(progress_data, f)

# Crear un archivo markdown para cada tema numerado
for i, numbered_topic in enumerate(numbered_topics):
    # Extraer el número y el tema
    section_num = numbered_topic.split('.')[0]
    subsection_num = numbered_topic.split('.')[1]
    topic_text = '.'.join(numbered_topic.split('.')[2:]).strip()
    
    # Crear nombre de archivo con la numeración
    filename = f"{section_num}_{subsection_num}_{topic_text.lower().replace(' ', '_').replace('/', '_')}.md"
    file_path = output_dir / filename
    
    # Verificar si este tema ya fue completado
    if filename in completed_topics:
        print(f"Tema ya completado: {numbered_topic}")
        continue
    
    # Crear el prompt para Gemini con la numeración incluida
    prompt = f"""
    Create a comprehensive Markdown lesson about "{topic_text}" for English language learners at A1 level.
    This content will be used for text-to-speech (TTS) as well as displayed visually in Markdown.

    Follow these formatting and content rules:

    - All content must start with an H1 heading (# Title), using this section number: {numbered_topic} ({section_num}.{subsection_num}).
    - Do **not** use numbered lists or Markdown tables.
    - You **may** use unordered lists (using `-` or `*`), as long as each item is short and clear.
    - Avoid using slashes (/); instead, use commas or write each item on a new line.
    - Always use full, natural-sounding sentences suitable for TTS. Avoid sentence fragments or isolated words.
    - Use section headings (##) to divide content logically.
    - Introduce each section with a sentence (e.g., "In this section, we’ll explore...").
    - Use spoken-style transitions like “Now, let’s look at some examples” or “Here are some useful phrases.”

    The Markdown should include:

    ## Introduction
    A short paragraph explaining the importance of this topic for A1 learners.

    ## Explanation
    A clear and beginner-friendly explanation, written in full paragraphs. Include simple embedded examples where helpful.

    ## Examples
    Introduce this section with a sentence like: “Now, let’s look at some examples.”
    - List common phrases or vocabulary related to this topic
    - Provide 2–5 short example sentences that demonstrate correct usage
    - Use unordered lists or separate lines, no tables or numbered items

    ## Practice: Questions and Answers
    Create 3–5 short practice questions related to the topic. After each question, insert a countdown written like this:
    **5... 4... 3... 2... 1...**
    Then provide the answer on a new line.

    Example:
    **Question:** How do you say “Hola” in English?  
    **5... 4... 3... 2... 1...**  
    **Answer:** Hello

    Make the tone friendly, slow-paced, and engaging. Avoid technical terms unless explained in context.
    """
    
    try:
        # Esperar según los límites de tasa
        wait_for_rate_limit()
        
        # Generar el contenido con Gemini
        response = model.generate_content(prompt)
        daily_requests += 1
        
        # Guardar el contenido en un archivo markdown
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        # Marcar como completado
        completed_topics[filename] = True
        save_progress()
        
        print(f"Creado tema {i+1}/{len(numbered_topics)}: {numbered_topic}")
        print(f"Solicitudes realizadas hoy: {daily_requests}/1500")
        
        # Guardar el progreso cada 5 temas
        if (i + 1) % 5 == 0:
            save_progress()
            
    except Exception as e:
        print(f"Error generando contenido para {numbered_topic}: {e}")
        
        # Si el error es por límite de tasa, esperar y reintentar
        if "rate" in str(e).lower() or "limit" in str(e).lower() or "429" in str(e):
            print("Detectado límite de tasa. Esperando 60 segundos...")
            time.sleep(60)
            # No incrementar el contador para que se reintente
            i -= 1
        else:
            # Guardar progreso en caso de error no relacionado con límites
            save_progress()
            time.sleep(5)  # Pequeña pausa antes de continuar con el siguiente tema

print("¡Todos los temas han sido creados exitosamente!")
print(f"Total de solicitudes realizadas: {daily_requests}")
print(f"Archivos generados: {len(completed_topics)}")