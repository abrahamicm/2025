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

# Lista de temas (usar la lista anterior)
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
    
    # NIVEL A2 (ELEMENTAL)
    # Gramática A2
    "Present continuous tense (formation, usage, contrast with present simple)",
    "Past simple tense (was/were, regular verbs, common irregular verbs)",
    "Future with 'going to'",
    "Future with present continuous",
    "Comparative and superlative adjectives",
    "Adverbs of frequency (always, usually, often, sometimes, rarely, never)",
    "Prepositions of movement (to, from, across, through)",
    "Modal verbs (can/can't, could, should/shouldn't, must/mustn't, have to/don't have to)",
    "Possessive pronouns (mine, yours, his, hers, ours, theirs)",
    "Present perfect simple (formation with have/has + past participle)",
    "Present perfect with ever/never/just/already/yet",
    "Contrast between present perfect and past simple",
    "First conditional (If + present simple, will + infinitive)",
    "Questions with 'How' (How much, How many, How often, How long)",
    "Too much / Too many / Not enough",
    "Infinitive of purpose (to + verb)",
    "Verbs followed by gerund (-ing)",
    "Basic connectors (and, but, or, because, so)",
    
    # Vocabulario A2
    "Physical and personality descriptions",
    "Travel and holidays",
    "Leisure activities and hobbies",
    "Sports and exercise",
    "Movie and book genres",
    "Education and studies",
    "Basic technology (electronic devices)",
    "Nature and environment",
    "Health and common illnesses",
    "Services (bank, post office, hospital)",
    "Extended professions",
    "Shopping and stores",
    "Food and cooking",
    "City and urban facilities",
    "Feelings and emotions",
    "Celebrations and festivities",
    "Extended weather vocabulary",
    
    # Habilidades Comunicativas A2
    "Narrating past experiences",
    "Talking about future plans",
    "Making and responding to invitations",
    "Suggesting activities",
    "Comparing people, places and things",
    "Expressing basic opinions",
    "Giving and asking for advice",
    "Talking about obligations",
    "Describing symptoms and health problems",
    "Expressing agreement and disagreement",
    "Apologizing and responding to apologies",
    "Making appointments",
    "Expressing preferences",
    "Talking about life experiences",
    "Making reservations (hotel, restaurant)",
    "Buying transport tickets",
    
    # Comprensión Escrita y Oral
    
    # Expresión Escrita
    "Writing short notes and messages",
    "Filling out forms (personal data)",
    "Writing informal emails",
    "Writing postcards and brief letters",
    "Writing descriptions of people and places",
    "Writing simple past narratives",
    "Writing brief biographies",
    "Writing about future plans and projects",
    
    # Temas Culturales y Sociales
    "Politeness formulas in English",
    "Festivities in English-speaking countries",
    "Typical foods in English-speaking countries",
    "Basic educational systems in English-speaking countries",
    "Basic cultural differences",
    "Geography of English-speaking countries",
    
    # Estrategias de Aprendizaje
    "Vocabulary memorization techniques",
    "Using bilingual dictionaries",
    "Language learning applications",
    "Conversation groups",
    "Online resources for beginners",
    "Pronunciation practice techniques",
    "Tips for autonomous practice"
        "Articles - a, an, the",
    "Reading comprehension - public signs and notices",
    "Reading comprehension - simple advertisements",
    "Reading comprehension - restaurant menus",
    "Reading comprehension - schedules and programs",
    "Reading comprehension - informal emails",
    "Reading comprehension - basic blogs and posts",
    "Reading comprehension - adapted short stories",
    "Listening comprehension - everyday dialogues",
    "Listening comprehension - simple public announcements",
    "Listening comprehension - instructions and directions",
    "Listening comprehension - simple presentations",
    "Listening comprehension - descriptions of people and places",
    "Listening comprehension - simple news"

]

# Agregar numeración a los temas para referencias cruzadas
numbered_topics = []
section_counters = {
    "A1 Fundamentals": 1,
    "A1 Grammar": 2,
    "A1 Vocabulary": 3,
    "A1 Communication": 4,
    "A2 Grammar": 5,
    "A2 Vocabulary": 6,
    "A2 Communication": 7,
    "Reading & Listening": 8,
    "Writing": 9,
    "Cultural": 10,
    "Learning": 11
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
    elif counter <= 59:
        current_section = "A2 Grammar"
        section_num = 5
    elif counter <= 76:
        current_section = "A2 Vocabulary"
        section_num = 6
    elif counter <= 92:
        current_section = "A2 Communication"
        section_num = 7
    elif counter <= 105:
        current_section = "Reading & Listening"
        section_num = 8
    elif counter <= 113:
        current_section = "Writing"
        section_num = 9
    elif counter <= 119:
        current_section = "Cultural"
        section_num = 10
    else:
        current_section = "Learning"
        section_num = 11
    
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
    elif counter <= 59:
        if current_section != "A2 Grammar":
            current_section = "A2 Grammar"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 76:
        if current_section != "A2 Vocabulary":
            current_section = "A2 Vocabulary"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 92:
        if current_section != "A2 Communication":
            current_section = "A2 Communication"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 105:
        if current_section != "Reading & Listening":
            current_section = "Reading & Listening"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 113:
        if current_section != "Writing":
            current_section = "Writing"
            subcounter = 1
        else:
            subcounter += 1
    elif counter <= 119:
        if current_section != "Cultural":
            current_section = "Cultural"
            subcounter = 1
        else:
            subcounter += 1
    else:
        if current_section != "Learning":
            current_section = "Learning"
            subcounter = 1
        else:
            subcounter += 1

# Directorio para guardar los archivos markdown
output_dir = Path("english_course_materials")
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
    Create a comprehensive markdown lesson about "{topic_text}" for English language learners at A1-A2 level.
    
    Use the following section numbering in your markdown title: {numbered_topic}
    
    The markdown should include:
    1. A clear title with the section number {section_num}.{subsection_num}
    2. A brief introduction explaining the importance of this topic
    3. Detailed explanation with examples
    4. Common phrases or vocabulary related to this topic

    
    Make it educational, practical and engaging for beginners.
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