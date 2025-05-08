import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
import subprocess
import sys
import tempfile
import threading
import openpyxl # Para leer archivos Excel
from xml.sax.saxutils import escape # Para escapar caracteres especiales XML

# --- Configuración ---
VOCES = {}  # Se llenará dinámicamente desde Balcon

def obtener_voces_balcon():
    """Obtiene la lista de voces disponibles desde Balcon."""
    try:
        # Asegúrate de que Balcon esté en el PATH o proporciona la ruta completa
        result = subprocess.run(["balcon", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, encoding='utf-8')
        voces_raw = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        # Limpiar posibles prefijos numéricos que Balcon a veces añade
        voces_limpias = []
        for voz in voces_raw:
            # Intenta quitar "N) " si está al principio
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

def leer_datos_excel(ruta_archivo):
    """Lee las dos primeras columnas de la primera hoja de un archivo Excel."""
    datos = []
    try:
        workbook = openpyxl.load_workbook(ruta_archivo)
        sheet = workbook.active  # Obtiene la primera hoja activa
        for row in sheet.iter_rows(min_row=1): # Puedes ajustar min_row si tienes encabezados
            celda1_valor = str(row[0].value) if row[0].value is not None else ""
            celda2_valor = str(row[1].value) if len(row) > 1 and row[1].value is not None else ""
            # Solo añadir si al menos una celda tiene contenido
            if celda1_valor or celda2_valor:
                datos.append((celda1_valor, celda2_valor))
    except Exception as e:
        messagebox.showerror("Error de Excel", f"No se pudo leer el archivo Excel: {str(e)}")
        return None
    return datos

def excel_a_ssml(datos_excel, voz_columna1, voz_columna2):
    """Convierte los datos de Excel (dos columnas) a SSML."""
    ssml_parts = []
    for texto_col1, texto_col2 in datos_excel:
        if texto_col1.strip():
            ssml_parts.append(f'<voice required="Name={escape(voz_columna1)}">{escape(texto_col1.strip())}</voice>')
        if texto_col2.strip():
            ssml_parts.append(f'<voice required="Name={escape(voz_columna2)}">{escape(texto_col2.strip())}</voice>')
        # Podrías añadir una pausa entre filas si lo deseas:
        # if texto_col1.strip() or texto_col2.strip():
        #     ssml_parts.append('<break time="500ms"/>')

    return f'<?xml version="1.0" encoding="UTF-8"?>\n<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-ES">\n{"".join(ssml_parts)}\n</speak>'
    # Cambiado xml:lang a "es-ES" asumiendo contenido en español, ajusta si es necesario

def verificar_balcon():
    """Verifica si Balcon está instalado y disponible en el sistema"""
    try:
        subprocess.run(["balcon", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError: # Balcon podría no tener --version pero existir
        try:
            subprocess.run(["balcon", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True # Si -l funciona, está bien
        except:
            return False


def generar_wav_desde_ssml(texto_ssml, archivo_wav):
    """Genera un archivo WAV a partir de SSML usando Balcon"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="utf-8") as temp_file:
        temp_file.write(texto_ssml)
        archivo_ssml = temp_file.name

    comando_balcon = [
        "balcon",
        "-f", archivo_ssml,
        "-w", archivo_wav,
        "-m",  # Interpretar como SSML
        "-enc", "UTF-8" # Asegurar que Balcon interprete el archivo SSML como UTF-8
    ]

    try:
        # Especificar encoding para la salida de Balcon puede ayudar a depurar
        result = subprocess.run(comando_balcon, check=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        os.unlink(archivo_ssml)
        return True, ""
    except subprocess.CalledProcessError as e:
        os.unlink(archivo_ssml)
        error_message = f"Error al ejecutar Balcon.\nComando: {' '.join(e.cmd)}\nSalida: {e.stdout}\nError: {e.stderr}"
        return False, error_message
    except Exception as e: # Captura otras excepciones
        if os.path.exists(archivo_ssml):
            os.unlink(archivo_ssml)
        return False, f"Error inesperado durante la generación de WAV: {str(e)}"


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

class ConversorExcelAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Excel a Audio (SSML)")
        self.root.geometry("800x650")
        self.archivo_excel_seleccionado = None
        self.voces_disponibles = obtener_voces_balcon()

        self.voz_columna1 = tk.StringVar(root)
        self.voz_columna2 = tk.StringVar(root)

        if self.voces_disponibles:
            default_voice1 = "Microsoft Helena Desktop" # Ajusta según tus voces en español
            default_voice2 = "Microsoft Sabina Desktop" # Ajusta según tus voces en español

            if default_voice1 in self.voces_disponibles:
                self.voz_columna1.set(default_voice1)
            elif self.voces_disponibles:
                self.voz_columna1.set(self.voces_disponibles[0])

            if default_voice2 in self.voces_disponibles:
                self.voz_columna2.set(default_voice2)
            elif len(self.voces_disponibles) > 1:
                self.voz_columna2.set(self.voces_disponibles[1])
            elif self.voces_disponibles: # Si solo hay una voz, usa la misma
                self.voz_columna2.set(self.voces_disponibles[0])
        else:
            messagebox.showwarning("Voces no encontradas", "No se encontraron voces de Balcon. La funcionalidad de selección de voz estará limitada.")


        self.balcon_disponible = verificar_balcon()
        self.configurar_interfaz()

    def configurar_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        self.btn_abrir = ttk.Button(toolbar, text="Abrir archivo Excel (.xlsx)", command=self.abrir_archivo_excel)
        self.btn_abrir.pack(side=tk.LEFT, padx=(0, 5))

        self.lbl_archivo_cargado = ttk.Label(toolbar, text="Archivo: Ninguno")
        self.lbl_archivo_cargado.pack(side=tk.LEFT, padx=(20, 0))

        frame_voces = ttk.LabelFrame(main_frame, text="Selección de Voces SAPI")
        frame_voces.pack(fill=tk.X, pady=(0, 5))

        lbl_voz_col1 = ttk.Label(frame_voces, text="Voz Columna 1:")
        lbl_voz_col1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_voz_col1 = ttk.Combobox(frame_voces, textvariable=self.voz_columna1, values=self.voces_disponibles, state="readonly" if self.voces_disponibles else "disabled")
        self.combo_voz_col1.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        lbl_voz_col2 = ttk.Label(frame_voces, text="Voz Columna 2:")
        lbl_voz_col2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_voz_col2 = ttk.Combobox(frame_voces, textvariable=self.voz_columna2, values=self.voces_disponibles, state="readonly" if self.voces_disponibles else "disabled")
        self.combo_voz_col2.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        frame_voces.columnconfigure(1, weight=1)


        frame_preview = ttk.LabelFrame(main_frame, text="Información del Archivo Excel")
        frame_preview.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        self.texto_preview = scrolledtext.ScrolledText(frame_preview, wrap=tk.WORD, font=("Consolas", 10))
        self.texto_preview.pack(fill=tk.BOTH, expand=True)
        self.texto_preview.config(state=tk.DISABLED)

        frame_audio_botones = ttk.Frame(main_frame)
        frame_audio_botones.pack(fill=tk.X, pady=(5, 0))

        self.btn_generar_audio = ttk.Button(frame_audio_botones, text="Generar Audio del Excel",
                                            command=self.generar_audio_excel,
                                            state=tk.DISABLED) # Se activa al cargar archivo
        self.btn_generar_audio.pack(side=tk.LEFT, padx=(0, 5))

        self.barra_estado = ttk.Label(main_frame, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(fill=tk.X, side=tk.BOTTOM)

        if not self.balcon_disponible:
            self.barra_estado.config(text="ADVERTENCIA: Balcon no está instalado o no funciona. La generación de audio no estará disponible.")
            self.btn_generar_audio.config(state=tk.DISABLED)
        elif not self.voces_disponibles:
            self.barra_estado.config(text="ADVERTENCIA: No se encontraron voces de Balcon. Verifica la instalación.")
            self.btn_generar_audio.config(state=tk.DISABLED)


    def abrir_archivo_excel(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.archivo_excel_seleccionado = archivo
            self.lbl_archivo_cargado.config(text=f"Archivo: {os.path.basename(self.archivo_excel_seleccionado)}")
            if self.balcon_disponible and self.voces_disponibles:
                 self.btn_generar_audio.config(state=tk.NORMAL)

            self.texto_preview.config(state=tk.NORMAL)
            self.texto_preview.delete(1.0, tk.END)
            try:
                datos_excel = leer_datos_excel(self.archivo_excel_seleccionado)
                if datos_excel is not None:
                    preview_text = f"Archivo cargado: {os.path.basename(self.archivo_excel_seleccionado)}\n"
                    preview_text += f"{len(datos_excel)} filas con datos encontradas (en las primeras dos columnas).\n\n"
                    preview_text += "Vista previa de las primeras filas (Columna 1 | Columna 2):\n"
                    for i, (c1, c2) in enumerate(datos_excel[:5]): # Vista previa de las primeras 5 filas
                        preview_text += f"- {c1[:50]}{'...' if len(c1)>50 else ''} | {c2[:50]}{'...' if len(c2)>50 else ''}\n"
                    self.texto_preview.insert(tk.END, preview_text)
                else:
                    self.texto_preview.insert(tk.END, "No se pudieron leer datos del archivo Excel o está vacío.")
                    self.btn_generar_audio.config(state=tk.DISABLED)

            except Exception as e:
                self.texto_preview.insert(tk.END, f"Error al previsualizar el archivo Excel: {str(e)}")
                self.btn_generar_audio.config(state=tk.DISABLED)
            self.texto_preview.config(state=tk.DISABLED)
        else:
            self.archivo_excel_seleccionado = None
            self.lbl_archivo_cargado.config(text="Archivo: Ninguno")
            self.texto_preview.config(state=tk.NORMAL)
            self.texto_preview.delete(1.0, tk.END)
            self.texto_preview.config(state=tk.DISABLED)
            self.btn_generar_audio.config(state=tk.DISABLED)

    def generar_audio_excel(self):
        if not self.balcon_disponible:
            messagebox.showerror("Error", "Balcon no está instalado o no es funcional.")
            return
        if not self.archivo_excel_seleccionado:
            messagebox.showinfo("Información", "No se ha seleccionado ningún archivo Excel.")
            return
        if not self.voces_disponibles:
            messagebox.showerror("Error", "No hay voces de Balcon disponibles. No se puede generar audio.")
            return

        voz_col1 = self.voz_columna1.get()
        voz_col2 = self.voz_columna2.get()

        if not voz_col1 or not voz_col2:
            messagebox.showerror("Error", "Por favor, selecciona las voces para ambas columnas.")
            return

        try:
            datos_excel = leer_datos_excel(self.archivo_excel_seleccionado)
            if datos_excel is None or not datos_excel: # Si leer_datos_excel falló o no hay datos
                messagebox.showinfo("Información", "El archivo Excel está vacío, no contiene datos en las primeras dos columnas o no se pudo leer.")
                self.barra_estado.config(text="Operación cancelada: archivo Excel vacío o ilegible.")
                return

            ssml_completo = excel_a_ssml(datos_excel, voz_col1, voz_col2)

            # Guardar el SSML generado para depuración (opcional)
            # with open("debug_ssml.xml", "w", encoding="utf-8") as f_debug:
            # f_debug.write(ssml_completo)

            nombre_base_audio = os.path.splitext(os.path.basename(self.archivo_excel_seleccionado))[0]
            # Obtener el directorio del archivo Excel para guardar el WAV allí
            directorio_salida = os.path.dirname(self.archivo_excel_seleccionado)
            archivo_wav = os.path.join(directorio_salida, f"{nombre_base_audio}.wav")


            self.barra_estado.config(text=f"Generando audio para: {os.path.basename(self.archivo_excel_seleccionado)}...")
            self.root.update_idletasks() # Forzar actualización de la UI

            # Deshabilitar botón mientras se genera
            self.btn_generar_audio.config(state=tk.DISABLED)

            def proceso_generar(ssml, wav_file):
                exito, mensaje_error_o_info = generar_wav_desde_ssml(ssml, wav_file)
                self.root.after(0, lambda e=exito, msg=mensaje_error_o_info, file=wav_file: self.actualizar_ui_generar(e, msg, file))

            thread = threading.Thread(target=proceso_generar, args=(ssml_completo, archivo_wav))
            thread.daemon = True # Permite que el programa cierre aunque el hilo esté corriendo
            thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el archivo Excel: {str(e)}")
            self.barra_estado.config(text=f"Error al procesar Excel: {str(e)}")
            # Habilitar botón de nuevo si falla antes del hilo
            if self.balcon_disponible and self.voces_disponibles and self.archivo_excel_seleccionado:
                self.btn_generar_audio.config(state=tk.NORMAL)


    def actualizar_ui_generar(self, exito, mensaje_error_o_info, archivo_generado):
        if exito:
            self.barra_estado.config(text=f"Audio generado con éxito: {os.path.basename(archivo_generado)}")
            if messagebox.askyesno("Éxito", f"Se generó el audio: {os.path.basename(archivo_generado)}\n¿Deseas reproducirlo?"):
                reproducir_audio(archivo_generado)
        else:
            messagebox.showerror("Error de Generación", f"Error al generar audio para {os.path.basename(archivo_generado)}:\n{mensaje_error_o_info}")
            self.barra_estado.config(text=f"Error al generar audio. Revisa los detalles.")
        
        # Rehabilitar el botón de generar audio si es apropiado
        if self.balcon_disponible and self.voces_disponibles and self.archivo_excel_seleccionado:
            self.btn_generar_audio.config(state=tk.NORMAL)


if __name__ == "__main__":
    # Necesitas instalar openpyxl: pip install openpyxl
    if sys.version_info[0] < 3:
        messagebox.showerror("Error de Versión", "Este script requiere Python 3.")
        sys.exit(1)
    try:
        import openpyxl
    except ImportError:
        messagebox.showerror("Dependencia Faltante", "La biblioteca 'openpyxl' es necesaria. Por favor, instálala ejecutando: pip install openpyxl")
        sys.exit(1)

    root = tk.Tk()
    app = ConversorExcelAudio(root)
    root.mainloop()