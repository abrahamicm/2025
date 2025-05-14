# detectar_idioma_lista.py

from wordfreq import word_frequency

def detectar_idioma_lista(palabras):
    total_en = 0
    total_es = 0

    for palabra in palabras:
        palabra = palabra.strip().lower()
        freq_en = word_frequency(palabra, 'en')
        freq_es = word_frequency(palabra, 'es')

        print(f"Palabra: {palabra}")
        print(f"  Frecuencia en inglés:  {freq_en}")
        print(f"  Frecuencia en español: {freq_es}")

        total_en += freq_en
        total_es += freq_es

    print("\n===== RESULTADO GENERAL =====")
    print(f"Total frecuencia inglés:  {total_en}")
    print(f"Total frecuencia español: {total_es}")

    if total_en > total_es:
        print("👉 El idioma predominante es INGLÉS.")
    elif total_es > total_en:
        print("👉 El idioma predominante es ESPAÑOL.")
    else:
        print("❓ No se puede determinar el idioma predominante.")

if __name__ == "__main__":
    palabras = [
        "hello", "beautiful", "strong", "confident",  # Inglés
        "hola", "feliz", "seguro", "contento"         # Español
    ]

    detectar_idioma_lista(palabras)
