import os

def juntar_markdown(carpeta_raiz, archivo_salida="archivo_unificado.md"):
    """
    Busca recursivamente archivos Markdown en la carpeta dada y los junta
    en un único archivo de salida.
    """
    contenido_unificado = []
    archivos_procesados = 0

    for raiz, _, archivos in os.walk(carpeta_raiz):
        for archivo in archivos:
            if archivo.endswith(".md"):
                ruta_completa = os.path.join(raiz, archivo)
                try:
                    with open(ruta_completa, 'r', encoding='utf-8') as archivo_md:
                        contenido = archivo_md.readlines()
                        contenido_unificado.extend(contenido)
                        contenido_unificado.append("\n\n")
                        archivos_procesados += 1
                        print(f"Se agregó el contenido de: {ruta_completa}")
                except UnicodeDecodeError as e:
                    print(f"Error al leer '{ruta_completa}': {e}. Se omitirá este archivo.")
                except Exception as e:
                    print(f"Ocurrió un error al procesar '{ruta_completa}': {e}")

    if contenido_unificado:
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as archivo_final:
                archivo_final.writelines(contenido_unificado)
            print(f"\nSe han juntado {archivos_procesados} archivos en: {archivo_salida}")
        except Exception as e:
            print(f"Ocurrió un error al escribir el archivo de salida: {e}")
    else:
        print("No se encontraron archivos Markdown en la carpeta.")

if __name__ == "__main__":
    carpeta_a_unir = input("Ingresa la ruta de la carpeta que contiene los archivos Markdown: ")
    archivo_de_salida = input("Ingresa el nombre del archivo de salida (por defecto: archivo_unificado.md): ") or "archivo_unificado.md"

    if os.path.isdir(carpeta_a_unir):
        juntar_markdown(carpeta_a_unir, archivo_de_salida)
    else:
        print("La ruta proporcionada no es una carpeta válida.")