import google.generativeai as genai
import os
from dotenv import load_dotenv
import time # Import the time module

# --- Load environment variables ---
load_dotenv()

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-pro")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

genai.configure(api_key=GEMINI_API_KEY) 

model = genai.GenerativeModel(GEMINI_MODEL_NAME)

# --- List of important English verbs ---
important_verbs = [
    "to be", "to have", "to do", "to go", "to make", "to get", 
    "to say", "to see", "to come", "to know", "to take"
    # Expand this list with more verbs
]

# --- Tenses to generate for each verb ---
tenses = {
    "Present_Simple": "present simple tense",
    "Past_Simple": "past simple tense",
    "Future_Simple": "future simple tense using 'will'",
    "Future_Going_To": "future tense using 'going to'"
}

# --- Output directory for Markdown files ---
output_directory = "verb_tense_markdown_files"
os.makedirs(output_directory, exist_ok=True)

# --- Base Prompt Template ---
base_prompt_template = """Act as an English teacher specialized in immersive and bilingual learning.

I want you to create a complete and structured list of short English sentences using the verb “{verb}” in the {tense_instruction}, organized by the following topics:

Affirmative
Negative
Questions
Affirmative Contractions
Negative Contractions
Questions Contractions
Constructions with Wh- Questions
Identity and Personal Introduction
Nationality and Origin
Profession or Occupation
Physical or Emotional States
Age
Location or Place
Physical and Personality Descriptions
Permanent Characteristics (General Truths)
Weather, Time, and Clock
Price, Quantity or Measurement
{auxiliary_clause}
Impersonal Expressions
Structures with “There is / There are”
Modifiers with Modals
Idiomatic Expressions and Fixed Phrases

For each topic, generate:

10 different English sentences using the verb “{verb}” in the {tense_instruction}.

Each sentence must include a Spanish translation right after it.

✔️ Keep the vocabulary beginner-friendly.
✔️ Make the examples visual and realistic.
✔️ Do NOT explain grammar. Only show examples.
✔️ Label each section clearly with the topic name.
✔️ Instead of numbering (ol), use lists (li)
✔️ place a dot at the end of each title
✔️ no greetings no farewells in promps generates only the answer

Format suggestion:

I’m tired. — Estoy cansado.

Are you a teacher? — ¿Eres profesor?

She was happy yesterday. — Ella estaba feliz ayer.

We will be late. — Llegaremos tarde.
"""

# --- Function to generate content and save to Markdown ---
def generate_and_save_markdown(verb, tense_name, tense_instruction):
    """
    Generates content for a given verb and tense using the Gemini API and saves it as a Markdown file.
    """
    # Special handling for "to be" auxiliary forms
    if verb == "to be":
        auxiliary_clause = """Use of “to be” as an Auxiliary in Continuous Tenses
Use of “to be” as an Auxiliary in the Passive Voice"""
    else:
        auxiliary_clause = "" # Most general approach: remove for non-"to be" verbs

    prompt = base_prompt_template.format(
        verb=verb, 
        tense_instruction=tense_instruction,
        auxiliary_clause=auxiliary_clause
    )

    print(f"Generating content for verb: '{verb}' - Tense: '{tense_name}'...")
    try:
        response = model.generate_content(prompt)
        markdown_content = response.text

        sanitized_verb = verb.replace(" ", "_").replace("“", "").replace("”", "").lower()
        file_name = os.path.join(output_directory, f"{sanitized_verb}_{tense_name.lower()}.md")
        
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Successfully created '{file_name}'")

    except Exception as e:
        print(f"Error generating content for '{verb}' - '{tense_name}': {e}")
        with open(os.path.join(output_directory, f"{sanitized_verb}_{tense_name.lower()}_error.txt"), "w", encoding="utf-8") as f:
            f.write(f"Prompt:\n{prompt}\n\nError: {e}")

# --- Main execution ---
if __name__ == "__main__":
    request_count = 0
    start_time = time.time()

    for verb in important_verbs:
        for tense_name, tense_instruction in tenses.items():
            # Check rate limit before making a request
            if request_count >= 30:
                elapsed_time = time.time() - start_time
                if elapsed_time < 60:
                    sleep_time = 60 - elapsed_time
                    print(f"Rate limit approaching. Sleeping for {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time)
                
                # Reset count and timer for the next minute
                request_count = 0
                start_time = time.time()
            
            generate_and_save_markdown(verb, tense_name, tense_instruction)
            request_count += 1
            
            # Add a small delay after each request to smooth out usage
            # A 2-second delay means max 30 requests per minute (60/2 = 30)
            time.sleep(2) 

    print("\n--- Generation complete! ---")
    print(f"Markdown files are saved in the '{output_directory}' directory.")