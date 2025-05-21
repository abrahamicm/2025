import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

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
    # Add more verbs as needed
]

# --- Tenses to generate for each verb ---
tenses = {
    "Present_Simple": "present simple tense",
    "Past_Simple": "past simple tense",
    "Future_Simple": "future simple tense using 'will'",
    "Future_Going_To": "future tense using 'going to'"
}

# --- Output directory ---
output_directory = "verb_tense_markdown_files_english"
os.makedirs(output_directory, exist_ok=True)

# --- Base Prompt Template ---
base_prompt_template = """Act as an English teacher specialized in immersive and bilingual learning.

Generate a structured list of beginner-friendly English sentences using the verb "{verb}" in the {tense_instruction}. Organize the content under the following real-life topics:

- Affirmative.
- Negative.
- Questions.
- Affirmative Contractions.
- Negative Contractions.
- Questions Contractions.
- Wh- Questions.
- Identity and Personal Introduction.
- Nationality and Origin.
- Profession or Occupation.
- Physical or Emotional States.
- Age.
- Location or Place.
- Physical and Personality Descriptions.
- Permanent Characteristics (General Truths).
- Weather, Time, and Clock.
- Price, Quantity or Measurement.
{auxiliary_section}
- Impersonal Expressions.
- There is / There are constructions.
- Modifiers with Modals.
- Idiomatic Expressions and Fixed Phrases.

For each topic, generate 10 realistic and visual English sentences using "{verb}" in the {tense_instruction}.

✔️ Output only the examples in markdown format.  
✔️ Use bullet points for all lists (no numbering).  
✔️ Label each section clearly with a title ending in a dot.  
✔️ Avoid greetings or explanations — only the examples.  
✔️ Keep the vocabulary simple and relevant for everyday use.
"""

# --- Auxiliary section logic ---
def get_auxiliary_section(verb):
    if verb == "to be":
        return "- Use of “to be” as an Auxiliary in Continuous Tenses.\n- Use of “to be” as an Auxiliary in the Passive Voice."
    elif verb in ["to have", "to do"]:
        return f"- Use of \"{verb}\" as an Auxiliary in questions or perfect/compound tenses."
    else:
        return ""

# --- Function to generate and save ---
def generate_and_save_markdown(verb, tense_name, tense_instruction):
    auxiliary_section = get_auxiliary_section(verb)

    prompt = base_prompt_template.format(
        verb=verb,
        tense_instruction=tense_instruction,
        auxiliary_section=auxiliary_section
    )

    print(f"Generating content for verb: '{verb}' - Tense: '{tense_name}'...")
    try:
        response = model.generate_content(prompt)
        markdown_content = response.text

        sanitized_verb = verb.replace(" ", "_").replace("“", "").replace("”", "").lower()
        file_name = os.path.join(output_directory, f"{sanitized_verb}_{tense_name.lower()}.md")
        
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"✅ Created: '{file_name}'")

    except Exception as e:
        print(f"❌ Error: '{verb}' - '{tense_name}': {e}")
        with open(os.path.join(output_directory, f"{sanitized_verb}_{tense_name.lower()}_error.txt"), "w", encoding="utf-8") as f:
            f.write(f"Prompt:\n{prompt}\n\nError: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    request_count = 0
    start_time = time.time()

    for verb in important_verbs:
        for tense_name, tense_instruction in tenses.items():
            # Rate limiting
            if request_count >= 30:
                elapsed_time = time.time() - start_time
                if elapsed_time < 60:
                    time.sleep(60 - elapsed_time)
                request_count = 0
                start_time = time.time()

            generate_and_save_markdown(verb, tense_name, tense_instruction)
            request_count += 1
            time.sleep(2)

    print("\n--- ✅ All Markdown files generated successfully! ---")
    print(f"Files saved in: '{output_directory}'")
