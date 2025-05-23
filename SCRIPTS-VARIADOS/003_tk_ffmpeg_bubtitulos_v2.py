import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import tempfile
import shutil
import platform
import re

def seleccionar_video():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos MP4", "*.mp4")])
    if ruta:
        entrada_video.set(ruta)

def seleccionar_srt():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos SRT", "*.srt")])
    if ruta:
        entrada_srt.set(ruta)

def corregir_formato_srt(ruta_srt):
    """Corrige el formato SRT agregando numeración y formato correcto - UNA LÍNEA"""
    try:
        with open(ruta_srt, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except UnicodeDecodeError:
        # Intentar con otras codificaciones
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                with open(ruta_srt, 'r', encoding=encoding) as f:
                    contenido = f.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            raise Exception("No se pudo leer el archivo SRT con ninguna codificación")

    # Dividir por líneas y procesar
    lineas = contenido.strip().split('\n')
    subtitulos_corregidos = []
    contador = 1
    
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        
        # Buscar líneas que contengan timestamps (formato: timestamp --> timestamp)
        if '-->' in linea:
            # Convertir timestamp decimal a formato SRT (HH:MM:SS,mmm)
            timestamp_match = re.match(r'(\d+\.?\d*)\s*-->\s*(\d+\.?\d*)', linea)
            if timestamp_match:
                inicio = float(timestamp_match.group(1))
                fin = float(timestamp_match.group(2))
                
                # Convertir a formato SRT
                inicio_srt = segundos_a_srt(inicio)
                fin_srt = segundos_a_srt(fin)
                
                # Buscar el texto del subtítulo (líneas siguientes que no sean timestamps)
                texto_lineas = []
                j = i + 1
                while j < len(lineas) and '-->' not in lineas[j]:
                    if lineas[j].strip():
                        texto_lineas.append(lineas[j].strip())
                    j += 1
                
                if texto_lineas:
                    # MEJORA: Unir todas las líneas de texto en una sola línea
                    texto_unificado = ' '.join(texto_lineas)
                    
                    # Agregar subtítulo corregido
                    subtitulos_corregidos.append(str(contador))
                    subtitulos_corregidos.append(f"{inicio_srt} --> {fin_srt}")
                    subtitulos_corregidos.append(texto_unificado)  # Una sola línea
                    subtitulos_corregidos.append("")  # Línea vacía entre subtítulos
                    contador += 1
                
                i = j - 1
        
        i += 1
    
    return '\n'.join(subtitulos_corregidos)

def segundos_a_srt(segundos):
    """Convierte segundos decimales a formato SRT (HH:MM:SS,mmm)"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos_restantes = segundos % 60
    segundos_enteros = int(segundos_restantes)
    milisegundos = int((segundos_restantes - segundos_enteros) * 1000)
    
    return f"{horas:02d}:{minutos:02d}:{segundos_enteros:02d},{milisegundos:03d}"

def incrustar_subtitulos():
    """Método usando archivo temporal con formato corregido"""
    video = entrada_video.get()
    srt = entrada_srt.get()

    if not video or not srt:
        messagebox.showerror("Error", "Debes seleccionar ambos archivos")
        return

    carpeta_salida = os.path.dirname(video)
    nombre_base = os.path.splitext(os.path.basename(video))[0]
    salida = os.path.join(carpeta_salida, f"{nombre_base}_con_subs.mp4")

    try:
        # Crear un directorio temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            # Corregir formato SRT y guardar en archivo temporal
            temp_srt = os.path.join(temp_dir, "subs.srt")
            contenido_corregido = corregir_formato_srt(srt)
            
            with open(temp_srt, 'w', encoding='utf-8') as f:
                f.write(contenido_corregido)
            
            # Escapar correctamente la ruta para el filtro subtitles
            if platform.system() == "Windows":
                temp_srt_escaped = temp_srt.replace('\\', '\\\\').replace(':', '\\:')
            else:
                temp_srt_escaped = temp_srt.replace(':', '\\:')
            
            # Comando FFmpeg
            comando = [
                "ffmpeg",
                "-i", video,
                "-vf", f"subtitles='{temp_srt_escaped}'",
                "-c:v", "libx264",
                "-c:a", "copy",
                "-y",
                salida
            ]
            
            resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
            messagebox.showinfo("Éxito", f"Subtítulos incrustados correctamente en:\n{salida}")
            
    except subprocess.CalledProcessError as e:
        error_msg = f"Error de FFmpeg:\n{e.stderr if e.stderr else str(e)}"
        messagebox.showerror("Error", error_msg)
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")

def incrustar_subtitulos_simple():
    """Método más simple con formato corregido y estilo básico - UNA LÍNEA"""
    video = entrada_video.get()
    srt = entrada_srt.get()

    if not video or not srt:
        messagebox.showerror("Error", "Debes seleccionar ambos archivos")
        return

    carpeta_salida = os.path.dirname(video)
    nombre_base = os.path.splitext(os.path.basename(video))[0]
    salida = os.path.join(carpeta_salida, f"{nombre_base}_con_subs_simple.mp4")

    try:
        # Crear archivo SRT corregido en la misma carpeta
        srt_corregido = os.path.join(carpeta_salida, f"{nombre_base}_subtitulos_corregidos.srt")
        contenido_corregido = corregir_formato_srt(srt)

        with open(srt_corregido, 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)

        # Escapar correctamente la ruta del SRT para el filtro subtitles
        if platform.system() == "Windows":
            srt_corregido_escaped = srt_corregido.replace('\\', '\\\\').replace(':', '\\:')
        else:
            srt_corregido_escaped = srt_corregido.replace(':', '\\:')

        # Comando simplificado con estilo básico pero efectivo
        comando = [
            "ffmpeg",
            "-i", video,
            "-vf", f"subtitles='{srt_corregido_escaped}:force_style='Fontsize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Alignment=2,MarginV=20'",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "copy",
            "-y",
            salida
        ]

        # Ejecutar comando
        subprocess.run(comando, check=True, capture_output=True, text=True)

        messagebox.showinfo("Éxito", f"Subtítulos incrustados en:\n{salida}\n\nArchivo SRT corregido guardado en:\n{srt_corregido}")

    except subprocess.CalledProcessError as e:
        error_msg = f"Error de FFmpeg:\n{e.stderr if e.stderr else str(e)}"
        messagebox.showerror("Error", error_msg)
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")

def incrustar_subtitulos_alternativo():
    """Método alternativo: añadir subtítulos como pista separada"""
    video = entrada_video.get()
    srt = entrada_srt.get()

    if not video or not srt:
        messagebox.showerror("Error", "Debes seleccionar ambos archivos")
        return

    carpeta_salida = os.path.dirname(video)
    nombre_base = os.path.splitext(os.path.basename(video))[0]
    salida = os.path.join(carpeta_salida, f"{nombre_base}_con_subs_alt.mp4")

    try:
        # Crear archivo SRT corregido
        srt_corregido = os.path.join(carpeta_salida, f"{nombre_base}_subtitulos_corregidos.srt")
        contenido_corregido = corregir_formato_srt(srt)
        
        with open(srt_corregido, 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)

        # Comando para añadir subtítulos como pista
        comando = [
            "ffmpeg",
            "-i", video,
            "-i", srt_corregido,
            "-c:v", "copy",      # Copiar video sin re-codificar
            "-c:a", "copy",      # Copiar audio sin cambios
            "-c:s", "mov_text",  # Codec de subtítulos para MP4
            "-y",
            salida
        ]

        subprocess.run(comando, check=True, capture_output=True, text=True)
        messagebox.showinfo("Éxito", f"Subtítulos añadidos como pista opcional en:\n{salida}\n\nArchivo SRT corregido guardado en:\n{srt_corregido}")
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Error de FFmpeg:\n{e.stderr if e.stderr else str(e)}"
        messagebox.showerror("Error", error_msg)
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")

def incrustar_subtitulos_basico():
    """Método más básico sin estilos complejos - UNA LÍNEA"""
    video = entrada_video.get()
    srt = entrada_srt.get()

    if not video or not srt:
        messagebox.showerror("Error", "Debes seleccionar ambos archivos")
        return

    carpeta_salida = os.path.dirname(video)
    nombre_base = os.path.splitext(os.path.basename(video))[0]
    salida = os.path.join(carpeta_salida, f"{nombre_base}_con_subs_basico.mp4")

    try:
        # Crear archivo SRT corregido en la misma carpeta
        srt_corregido = os.path.join(carpeta_salida, f"{nombre_base}_subtitulos_corregidos.srt")
        contenido_corregido = corregir_formato_srt(srt)

        with open(srt_corregido, 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)

        # Escapar correctamente la ruta del SRT para el filtro subtitles
        if platform.system() == "Windows":
            srt_corregido_escaped = srt_corregido.replace('\\', '\\\\').replace(':', '\\:')
        else:
            srt_corregido_escaped = srt_corregido.replace(':', '\\:')

        # Comando básico sin estilos complejos
        comando = [
            "ffmpeg",
            "-i", video,
            "-vf", f"subtitles='{srt_corregido_escaped}'",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "copy",
            "-y",
            salida
        ]

        # Ejecutar comando
        subprocess.run(comando, check=True, capture_output=True, text=True)

        messagebox.showinfo("Éxito", f"Subtítulos incrustados en:\n{salida}\n\nArchivo SRT corregido guardado en:\n{srt_corregido}")

    except subprocess.CalledProcessError as e:
        error_msg = f"Error de FFmpeg:\n{e.stderr if e.stderr else str(e)}"
        messagebox.showerror("Error", error_msg)
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")

def solo_corregir_srt():
    """Solo corregir el formato del archivo SRT - UNA LÍNEA"""
    srt = entrada_srt.get()
    
    if not srt:
        messagebox.showerror("Error", "Debes seleccionar un archivo SRT")
        return
    
    try:
        carpeta_salida = os.path.dirname(srt)
        nombre_base = os.path.splitext(os.path.basename(srt))[0]
        srt_corregido = os.path.join(carpeta_salida, f"{nombre_base}_corregido.srt")
        
        contenido_corregido = corregir_formato_srt(srt)
        
        with open(srt_corregido, 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)
        
        messagebox.showinfo("Éxito", f"Archivo SRT corregido guardado en:\n{srt_corregido}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al corregir SRT:\n{str(e)}")

# GUI con tkinter
ventana = tk.Tk()
ventana.title("Incrustar Subtítulos en Video - Versión Mejorada")
ventana.geometry("600x420")

entrada_video = tk.StringVar()
entrada_srt = tk.StringVar()

# Frame para organizar mejor los elementos
frame_principal = tk.Frame(ventana)
frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

tk.Label(frame_principal, text="Video MP4:", font=("Arial", 10, "bold")).pack(anchor="w")
tk.Entry(frame_principal, textvariable=entrada_video, width=70).pack(fill="x", pady=(0, 5))
tk.Button(frame_principal, text="Seleccionar video", command=seleccionar_video).pack(pady=(0, 15))

tk.Label(frame_principal, text="Archivo SRT:", font=("Arial", 10, "bold")).pack(anchor="w")
tk.Entry(frame_principal, textvariable=entrada_srt, width=70).pack(fill="x", pady=(0, 5))
tk.Button(frame_principal, text="Seleccionar SRT", command=seleccionar_srt).pack(pady=(0, 15))

# Frame para los botones
frame_botones = tk.Frame(frame_principal)
frame_botones.pack(fill="x")

tk.Button(frame_botones, text="Solo Corregir SRT\n(Una línea por subtítulo)", 
          command=solo_corregir_srt, bg="purple", fg="white", height=2).pack(fill="x", pady=(0, 5))

tk.Button(frame_botones, text="Incrustar Subtítulos\n(Método Temporal)", 
          command=incrustar_subtitulos, bg="green", fg="white", height=2).pack(fill="x", pady=(0, 5))

tk.Button(frame_botones, text="Incrustar Subtítulos\n(Método Básico - Sin estilos)", 
          command=incrustar_subtitulos_basico, bg="lightgreen", fg="black", height=2).pack(fill="x", pady=(0, 5))

tk.Button(frame_botones, text="Incrustar Subtítulos\n(Método Simple - Una línea)", 
          command=incrustar_subtitulos_simple, bg="orange", fg="white", height=2).pack(fill="x", pady=(0, 5))

tk.Button(frame_botones, text="Añadir como Pista\n(Subtítulos opcionales)", 
          command=incrustar_subtitulos_alternativo, bg="blue", fg="white", height=2).pack(fill="x")

# Añadir información sobre las opciones
info_text = tk.Text(frame_principal, height=7, wrap="word", font=("Arial", 8))
info_text.pack(fill="x", pady=(20, 0))
info_text.insert("1.0", 
    "🔥 MEJORADO: Subtítulos se muestran en UNA LÍNEA (más elegante)\n"
    "• Solo Corregir SRT: Convierte tu archivo SRT al formato correcto con una línea\n"
    "• Método Temporal: Incrusta subtítulos permanentemente (más seguro)\n"
    "• Método Simple: Incrusta subtítulos permanentemente con estilo mejorado\n"
    "• Subtítulos como Pista: Añade subtítulos opcionales (se pueden activar/desactivar)\n"
    "• NOTA: Tu archivo SRT será corregido automáticamente al formato estándar\n"
    "• Si un método falla, prueba otro. El método temporal es el más confiable.")
info_text.config(state="disabled")

ventana.mainloop()