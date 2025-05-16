import os
import glob

def unir_markdown(directorio, archivo_salida="unido.md"):
    """
    Une todos los archivos .md de un directorio en uno solo.
    
    Args:
        directorio (str): Ruta del directorio con archivos .md.
        archivo_salida (str): Nombre del archivo de salida.
    """
    # Buscar todos los archivos .md en el directorio (incluyendo subdirectorios)
    archivos_md = glob.glob(os.path.join(directorio, '**/*.md'), recursive=True)
    
    if not archivos_md:
        print("No se encontraron archivos .md en el directorio.")
        return
    
    # Ordenar los archivos alfabéticamente (opcional)
    archivos_md.sort()
    
    with open(archivo_salida, 'w', encoding='utf-8') as archivo_unido:
        for ruta_archivo in archivos_md:
            nombre_archivo = os.path.basename(ruta_archivo)
            
            # Añadir un encabezado con el nombre del archivo original
            archivo_unido.write(f"\n\n<!-- Archivo: {nombre_archivo} -->\n\n")
            
            # Leer y escribir el contenido del archivo
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                archivo_unido.write(archivo.read())
    
    print(f"¡Hecho! Archivos unidos en: {archivo_salida}")

# Ejemplo de uso
unir_markdown(
    directorio="./",  # Cambia esto por tu ruta
    archivo_salida="adjetovos_unidos.md"  # Cambia esto por tu nombre de archivo deseado
)