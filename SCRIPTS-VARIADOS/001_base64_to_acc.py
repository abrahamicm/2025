import base64

# Cadena Base64 (reemplaza con la cadena completa que tienes)
base64_string = """
""".replace('\n', '').replace('\r', '')

# Decodificamos la cadena Base64
decoded_data = base64.b64decode(base64_string)

# Guardamos como archivo .aac
with open("audio_decodificado.aac", "wb") as f:
    f.write(decoded_data)

print("Archivo guardado como 'audio_decodificado.aac'")
