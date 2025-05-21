import os

def agregar_h1_si_no_existe(ruta_archivo):
    """
    Revisa un archivo Markdown y agrega un encabezado H1 al principio
    si no existe, utilizando el nombre del archivo como título.
    """
    try:
        with open(ruta_archivo, 'r+', encoding='utf-8') as archivo:
            contenido = archivo.readlines()
            tiene_h1 = any(line.startswith('# ') for line in contenido)

            if not tiene_h1 and contenido:
                nombre_archivo_sin_extension = os.path.splitext(os.path.basename(ruta_archivo))[0].replace('-', ' ').title()
                nuevo_contenido = ["# " + nombre_archivo_sin_extension + "\n\n"] + contenido
                archivo.seek(0)
                archivo.writelines(nuevo_contenido)
                archivo.truncate()
                print(f"Se agregó el encabezado '# {nombre_archivo_sin_extension}' a: {ruta_archivo}")
            elif not contenido:
                nombre_archivo_sin_extension = os.path.splitext(os.path.basename(ruta_archivo))[0].replace('-', ' ').title()
                archivo.write("# " + nombre_archivo_sin_extension + "\n")
                print(f"Se creó un archivo con el encabezado '# {nombre_archivo_sin_extension}': {ruta_archivo}")
            else:
                print(f"El archivo ya tiene un encabezado H1: {ruta_archivo}")
    except UnicodeDecodeError as e:
        print(f"Error al decodificar el archivo '{ruta_archivo}': {e}")
        print("Asegúrate de que el archivo esté guardado con una codificación compatible (como UTF-8).")
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo '{ruta_archivo}': {e}")

def buscar_y_procesar_markdown(carpeta_raiz):
    """
    Busca recursivamente archivos Markdown en la carpeta dada y los procesa.
    """
    for raiz, _, archivos in os.walk(carpeta_raiz):
        for archivo in archivos:
            if archivo.endswith(".md"):
                ruta_completa = os.path.join(raiz, archivo)
                agregar_h1_si_no_existe(ruta_completa)

if __name__ == "__main__":
    # Obtiene la ruta del directorio donde se encuentra el script
    carpeta_a_revisar = os.path.dirname(os.path.abspath(__file__))
    print(f"Revisando la carpeta: {carpeta_a_revisar}")
    buscar_y_procesar_markdown(carpeta_a_revisar)
    print("Proceso completado.")