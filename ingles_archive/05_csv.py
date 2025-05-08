import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
import subprocess
import sys
import tempfile
import threading
import csv # Para leer archivos CSV
import random # Para desordenar las filas
from xml.sax.saxutils import escape # Para escapar caracteres especiales XML

# --- Configuración ---
# VOCES se llenará dinámicamente
DELIMITADORES = {
    "Coma (,)": ",",
    "Punto y Coma (;)": ";",
    "Tabulador (TSV)": "\t"
}
DELIMITADORES_DISPLAY = list(DELIMITADORES.keys())


def obtener_voces_balcon():
    """Obtiene la lista de voces disponibles desde Balcon."""
    try:
        result = subprocess.run(["balcon", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, encoding='utf-8')
        voces_raw = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        voces_limpias = []
        for voz in voces_raw:
            parts = voz.split(") ", 1)
            if len(parts) > 1 and parts[0].isdigit():
                voces_limpias.append(parts[1])
            else:
                voces_limpias.append(voz)
        return voces_limpias
    except FileNotFoundError:
        messagebox.showerror("Error", "Balcon no se encuentra. Asegúrate de que esté instalado y en el PATH del sistema.")
        return []
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al listar voces de Balcon: {e.stderr}")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado al obtener voces: {str(e)}")
        return []

def leer_datos_csv(ruta_archivo, delimitador):
    """Lee las dos primeras columnas de un archivo CSV/TXT."""
    datos = []
    try:
        # Intentar con UTF-8, luego con latin-1 si falla (común en algunos CSVs)
        encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1']
        file_content_decoded = False
        for encoding in encodings_to_try:
            try:
                with open(ruta_archivo, mode='r', newline='', encoding=encoding) as csvfile:
                    csv_reader = csv.reader(csvfile, delimiter=delimitador)
                    for row in csv_reader:
                        if not row: # Saltar filas vacías
                            continue
                        celda1_valor = str(row[0]) if len(row) > 0 else ""
                        celda2_valor = str(row[1]) if len(row) > 1 else ""
                        if celda1_valor or celda2_valor: # Solo añadir si hay contenido
                            datos.append((celda1_valor, celda2_valor))
                file_content_decoded = True
                break # Salir del bucle si la decodificación fue exitosa
            except UnicodeDecodeError:
                continue # Probar con el siguiente encoding
            except csv.Error as e: # Capturar errores específicos de CSV
                messagebox.showerror("Error de CSV", f"Error al parsear el CSV con delimitador '{delimitador}' en la línea {csv_reader.line_num}: {e}\nPrueba con otro delimitador o revisa el archivo.")
                return None
        
        if not file_content_decoded:
            messagebox.showerror("Error de Codificación", f"No se pudo decodificar el archivo '{os.path.basename(ruta_archivo)}' con las codificaciones probadas (UTF-8, Latin-1, ISO-8859-1).")
            return None

    except FileNotFoundError:
        messagebox.showerror("Error de Archivo", f"Archivo no encontrado: {ruta_archivo}")
        return None
    except Exception as e:
        messagebox.showerror("Error de Lectura", f"No se pudo leer el archivo: {str(e)}")
        return None
    return datos

def datos_a_ssml(datos_columnas, voz_columna1, voz_columna2):
    """Convierte los datos de dos columnas (lista de tuplas) a SSML."""
    ssml_parts = []
    for texto_col1, texto_col2 in datos_columnas:
        # Limpiar y escapar texto
        texto_col1_limpio = escape(texto_col1.strip())
        texto_col2_limpio = escape(texto_col2.strip())

        if texto_col1_limpio:
            ssml_parts.append(f'<voice required="Name={escape(voz_columna1)}">{texto_col1_limpio}</voice>')
        if texto_col2_limpio:
            ssml_parts.append(f'<voice required="Name={escape(voz_columna2)}">{texto_col2_limpio}</voice>')
        # Pausa entre "filas" del CSV si ambas columnas de la fila original tenían texto.
        if texto_col1_limpio or texto_col2_limpio:
             ssml_parts.append('<break time="300ms"/>')


    return f'<?xml version="1.0" encoding="UTF-8"?>\n<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-ES">\n{"".join(ssml_parts)}\n</speak>'
    # xml:lang="es-ES" asumiendo contenido en español, ajusta si es necesario

def verificar_balcon():
    """Verifica si Balcon está instalado y disponible en el sistema"""
    try:
        subprocess.run(["balcon", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=5)
        return True
    except FileNotFoundError:
        return False
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        try: # Balcon podría no tener --version pero existir
            subprocess.run(["balcon", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=5)
            return True
        except:
            return False


def generar_wav_desde_ssml(texto_ssml, archivo_wav):
    """Genera un archivo WAV a partir de SSML usando Balcon"""
    temp_ssml_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(texto_ssml)
            temp_ssml_file = temp_file.name

        comando_balcon = [
            "balcon",
            "-f", temp_ssml_file,
            "-w", archivo_wav,
            "-m",  # Interpretar como SSML
            "-enc", "UTF-8"
        ]
        result = subprocess.run(comando_balcon, check=True, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120) # Timeout de 2 mins
        return True, ""
    except subprocess.CalledProcessError as e:
        error_message = f"Error al ejecutar Balcon.\nComando: {' '.join(e.cmd)}\nSalida: {e.stdout}\nError: {e.stderr}"
        return False, error_message
    except subprocess.TimeoutExpired:
        return False, "Error: Balcon tardó demasiado en responder. El proceso fue terminado."
    except Exception as e:
        return False, f"Error inesperado durante la generación de WAV: {str(e)}"
    finally:
        if temp_ssml_file and os.path.exists(temp_ssml_file):
            os.unlink(temp_ssml_file)


def reproducir_audio(archivo_wav):
    """Reproduce el archivo de audio generado"""
    if os.path.exists(archivo_wav):
        try:
            if sys.platform.startswith('win'):
                os.startfile(archivo_wav)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', archivo_wav], check=True)
            elif sys.platform.startswith('linux'):
                subprocess.run(['xdg-open', archivo_wav], check=True)
            return True
        except Exception as e:
            messagebox.showerror("Error al reproducir", f"No se pudo reproducir el archivo de audio: {str(e)}")
            return False
    else:
        messagebox.showerror("Error", "El archivo de audio no se encuentra.")
        return False

class ConversorCsvAudio:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Conversor de CSV/TXT a Audio (SSML)")
        self.root.geometry("800x700") # Aumentado un poco la altura para nuevas opciones
        self.archivo_seleccionado = None
        self.voces_disponibles = obtener_voces_balcon()

        self.voz_columna1 = tk.StringVar(self.root)
        self.voz_columna2 = tk.StringVar(self.root)
        self.delimitador_seleccionado = tk.StringVar(self.root)
        self.desordenar_filas_var = tk.BooleanVar(self.root, value=False) # Por defecto no desordenar

        if self.voces_disponibles:
            default_voice1 = "Microsoft Helena Desktop"
            default_voice2 = "Microsoft Sabina Desktop"
            if default_voice1 in self.voces_disponibles: self.voz_columna1.set(default_voice1)
            elif self.voces_disponibles: self.voz_columna1.set(self.voces_disponibles[0])
            if default_voice2 in self.voces_disponibles: self.voz_columna2.set(default_voice2)
            elif len(self.voces_disponibles) > 1: self.voz_columna2.set(self.voces_disponibles[1])
            elif self.voces_disponibles: self.voz_columna2.set(self.voces_disponibles[0])
        else:
            messagebox.showwarning("Voces no encontradas", "No se encontraron voces de Balcon. La funcionalidad de selección de voz estará limitada.")

        self.delimitador_seleccionado.set(DELIMITADORES_DISPLAY[0]) # Coma por defecto

        self.balcon_disponible = verificar_balcon()
        self.configurar_interfaz()

    def configurar_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Toolbar (Abrir Archivo) ---
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        self.btn_abrir = ttk.Button(toolbar, text="Abrir CSV/TXT", command=self.abrir_archivo_csv_txt)
        self.btn_abrir.pack(side=tk.LEFT, padx=(0, 5))
        self.lbl_archivo_cargado = ttk.Label(toolbar, text="Archivo: Ninguno")
        self.lbl_archivo_cargado.pack(side=tk.LEFT, padx=(20, 0))

        # --- Opciones de CSV ---
        frame_csv_opciones = ttk.LabelFrame(main_frame, text="Opciones de CSV/TXT")
        frame_csv_opciones.pack(fill=tk.X, pady=5)
        
        lbl_delimitador = ttk.Label(frame_csv_opciones, text="Separador:")
        lbl_delimitador.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_delimitador = ttk.Combobox(frame_csv_opciones, textvariable=self.delimitador_seleccionado, values=DELIMITADORES_DISPLAY, state="readonly", width=18)
        self.combo_delimitador.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.check_desordenar = ttk.Checkbutton(frame_csv_opciones, text="Desordenar filas", variable=self.desordenar_filas_var)
        self.check_desordenar.grid(row=0, column=2, padx=15, pady=5, sticky=tk.W)


        # --- Selección de Voces ---
        frame_voces = ttk.LabelFrame(main_frame, text="Selección de Voces SAPI")
        frame_voces.pack(fill=tk.X, pady=5)
        lbl_voz_col1 = ttk.Label(frame_voces, text="Voz Columna 1:")
        lbl_voz_col1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_voz_col1 = ttk.Combobox(frame_voces, textvariable=self.voz_columna1, values=self.voces_disponibles, state="readonly" if self.voces_disponibles else "disabled")
        self.combo_voz_col1.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        lbl_voz_col2 = ttk.Label(frame_voces, text="Voz Columna 2:")
        lbl_voz_col2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_voz_col2 = ttk.Combobox(frame_voces, textvariable=self.voz_columna2, values=self.voces_disponibles, state="readonly" if self.voces_disponibles else "disabled")
        self.combo_voz_col2.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        frame_voces.columnconfigure(1, weight=1)

        # --- Vista Previa ---
        frame_preview = ttk.LabelFrame(main_frame, text="Información del Archivo")
        frame_preview.pack(fill=tk.BOTH, expand=True, pady=5)
        self.texto_preview = scrolledtext.ScrolledText(frame_preview, wrap=tk.WORD, font=("Consolas", 10))
        self.texto_preview.pack(fill=tk.BOTH, expand=True)
        self.texto_preview.config(state=tk.DISABLED)

        # --- Botones de Acción ---
        frame_audio_botones = ttk.Frame(main_frame)
        frame_audio_botones.pack(fill=tk.X, pady=(5, 0))
        self.btn_generar_audio = ttk.Button(frame_audio_botones, text="Generar Audio del Archivo",
                                            command=self.generar_audio_csv_txt,
                                            state=tk.DISABLED)
        self.btn_generar_audio.pack(side=tk.LEFT, padx=(0, 5))

        # --- Barra de Estado ---
        self.barra_estado = ttk.Label(main_frame, text="Listo.", relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(fill=tk.X, side=tk.BOTTOM)

        if not self.balcon_disponible:
            self.barra_estado.config(text="ADVERTENCIA: Balcon no está instalado o no funciona. La generación de audio no estará disponible.")
            self.btn_generar_audio.config(state=tk.DISABLED)
        elif not self.voces_disponibles:
            self.barra_estado.config(text="ADVERTENCIA: No se encontraron voces de Balcon. Verifica la instalación.")
            self.btn_generar_audio.config(state=tk.DISABLED)


    def abrir_archivo_csv_txt(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV o TXT",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.archivo_seleccionado = archivo
            self.lbl_archivo_cargado.config(text=f"Archivo: {os.path.basename(self.archivo_seleccionado)}")
            if self.balcon_disponible and self.voces_disponibles:
                 self.btn_generar_audio.config(state=tk.NORMAL)

            self.texto_preview.config(state=tk.NORMAL)
            self.texto_preview.delete(1.0, tk.END)
            
            delimitador_actual = DELIMITADORES[self.delimitador_seleccionado.get()]
            datos_leidos = leer_datos_csv(self.archivo_seleccionado, delimitador_actual)

            if datos_leidos is not None:
                preview_text = f"Archivo cargado: {os.path.basename(self.archivo_seleccionado)}\n"
                preview_text += f"Delimitador actual para vista previa: '{self.delimitador_seleccionado.get()}'\n"
                preview_text += f"{len(datos_leidos)} filas con datos encontradas (en las primeras dos columnas).\n\n"
                preview_text += "Vista previa de las primeras filas (Columna 1 | Columna 2):\n"
                for i, (c1, c2) in enumerate(datos_leidos[:5]):
                    preview_text += f"- {c1[:50]}{'...' if len(c1)>50 else ''} | {c2[:50]}{'...' if len(c2)>50 else ''}\n"
                self.texto_preview.insert(tk.END, preview_text)
                if not datos_leidos: # Si se leyó pero no hay datos válidos
                     self.texto_preview.insert(tk.END, "\nEl archivo parece estar vacío o no tiene datos en el formato esperado con el delimitador actual.")
            else: # leer_datos_csv devolvió None (error)
                self.texto_preview.insert(tk.END, "Error al leer o previsualizar el archivo. Revisa el delimitador o el contenido del archivo.")
                self.btn_generar_audio.config(state=tk.DISABLED)
            self.texto_preview.config(state=tk.DISABLED)
        else: # No se seleccionó archivo
            self.archivo_seleccionado = None
            self.lbl_archivo_cargado.config(text="Archivo: Ninguno")
            self.texto_preview.config(state=tk.NORMAL)
            self.texto_preview.delete(1.0, tk.END)
            self.texto_preview.config(state=tk.DISABLED)
            self.btn_generar_audio.config(state=tk.DISABLED)

    def generar_audio_csv_txt(self):
        if not self.balcon_disponible:
            messagebox.showerror("Error", "Balcon no está instalado o no es funcional.")
            return
        if not self.archivo_seleccionado:
            messagebox.showinfo("Información", "No se ha seleccionado ningún archivo.")
            return
        if not self.voces_disponibles:
            messagebox.showerror("Error", "No hay voces de Balcon disponibles. No se puede generar audio.")
            return

        voz_col1 = self.voz_columna1.get()
        voz_col2 = self.voz_columna2.get()
        delimitador_real = DELIMITADORES[self.delimitador_seleccionado.get()]
        desordenar = self.desordenar_filas_var.get()

        if not voz_col1 or not voz_col2:
            messagebox.showerror("Error", "Por favor, selecciona las voces para ambas columnas.")
            return

        try:
            datos_columnas = leer_datos_csv(self.archivo_seleccionado, delimitador_real)
            if datos_columnas is None or not datos_columnas:
                messagebox.showinfo("Información", f"El archivo está vacío, no contiene datos válidos con el delimitador '{delimitador_real}', o no se pudo leer.")
                self.barra_estado.config(text="Operación cancelada: archivo vacío, ilegible o delimitador incorrecto.")
                return

            if desordenar:
                random.shuffle(datos_columnas)
                self.barra_estado.config(text="Filas desordenadas.")
                self.root.update_idletasks()


            ssml_completo = datos_a_ssml(datos_columnas, voz_col1, voz_col2)
            
            # Guardar el SSML generado para depuración (opcional)
            # debug_ssml_path = os.path.join(os.path.dirname(self.archivo_seleccionado), "debug_ssml_output.xml")
            # with open(debug_ssml_path, "w", encoding="utf-8") as f_debug:
            #    f_debug.write(ssml_completo)
            # self.barra_estado.config(text=f"SSML de depuración guardado en {debug_ssml_path}")
            # self.root.update_idletasks()


            nombre_base_audio = os.path.splitext(os.path.basename(self.archivo_seleccionado))[0]
            directorio_salida = os.path.dirname(self.archivo_seleccionado)
            archivo_wav = os.path.join(directorio_salida, f"{nombre_base_audio}.wav")

            self.barra_estado.config(text=f"Generando audio para: {os.path.basename(self.archivo_seleccionado)}...")
            self.root.update_idletasks()
            self.btn_generar_audio.config(state=tk.DISABLED)

            def proceso_generar(ssml, wav_file):
                exito, mensaje_error_o_info = generar_wav_desde_ssml(ssml, wav_file)
                # Llamar a la actualización de UI en el hilo principal de Tkinter
                self.root.after(0, self.actualizar_ui_generar, exito, mensaje_error_o_info, wav_file)


            thread = threading.Thread(target=proceso_generar, args=(ssml_completo, archivo_wav))
            thread.daemon = True
            thread.start()

        except Exception as e:
            messagebox.showerror("Error General", f"Error al procesar el archivo: {str(e)}")
            self.barra_estado.config(text=f"Error al procesar archivo: {str(e)}")
            if self.balcon_disponible and self.voces_disponibles and self.archivo_seleccionado:
                self.btn_generar_audio.config(state=tk.NORMAL)


    def actualizar_ui_generar(self, exito, mensaje_error_o_info, archivo_generado):
        if exito:
            self.barra_estado.config(text=f"Audio generado con éxito: {os.path.basename(archivo_generado)}")
            if messagebox.askyesno("Éxito", f"Se generó el audio: {os.path.basename(archivo_generado)}\n¿Deseas reproducirlo?"):
                reproducir_audio(archivo_generado)
        else:
            messagebox.showerror("Error de Generación", f"Error al generar audio para {os.path.basename(archivo_generado)}:\n{mensaje_error_o_info}")
            self.barra_estado.config(text=f"Error al generar audio. Revisa los detalles.")
        
        if self.balcon_disponible and self.voces_disponibles and self.archivo_seleccionado:
            self.btn_generar_audio.config(state=tk.NORMAL)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        messagebox.showerror("Error de Versión", "Este script requiere Python 3.")
        sys.exit(1)
    
    # No se necesita openpyxl para esta versión, así que quitamos la comprobación.

    root = tk.Tk()
    app = ConversorCsvAudio(root)
    root.mainloop()