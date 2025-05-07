import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import markdown
import os
import subprocess
import sys
import tempfile
import threading

# --- Configuración ---
VOCES = {}  # Se llenará dinámicamente desde Balcon

def obtener_voces_balcon():
    """Obtiene la lista de voces disponibles desde Balcon."""
    try:
        result = subprocess.run(["balcon", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        voces = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return voces
    except FileNotFoundError:
        messagebox.showerror("Error", "Balcon no se encuentra instalado.")
        return []
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al listar voces de Balcon: {e.stderr}")
        return []

def markdown_a_ssml(md, voz_principal, voz_secundaria):
    """Convierte Markdown a SSML, etiquetando el texto en <em> con la voz secundaria."""
    html_content = markdown.markdown(md)
    ssml_parts = []
    cursor = 0
    for match in re.finditer(r'<(/?)em>', html_content):
        tag_type = match.group(1)
        tag_start = match.start()
        tag_end = match.end()

        # Texto antes de la etiqueta <em>
        if tag_start > cursor:
            texto_principal = html_content[cursor:tag_start]
            texto_principal_limpio = re.sub(r'<[^>]+>', '', texto_principal).strip()
            if texto_principal_limpio:
                ssml_parts.append(f'<voice required="Name={voz_principal}">{texto_principal_limpio}</voice>')

        if tag_type == '':  # Opening <em> tag
            cursor = tag_end
            cierre_match = re.search(r'</em>', html_content[cursor:])
            if cierre_match:
                texto_secundario = html_content[cursor : cursor + cierre_match.start()]
                texto_secundario_limpio = texto_secundario.strip()
                if texto_secundario_limpio:
                    ssml_parts.append(f'<voice required="Name={voz_secundaria}">{texto_secundario_limpio}</voice>')
                cursor += cierre_match.end()
            else:
                texto_principal_final = html_content[cursor:]
                texto_principal_final_limpio = re.sub(r'<[^>]+>', '', texto_principal_final).strip()
                if texto_principal_final_limpio:
                    ssml_parts.append(f'<voice required="Name={voz_principal}">{texto_principal_final_limpio}</voice>')
                break
        elif tag_type == '/':  # Closing </em> tag
            cursor = tag_end

    # Texto después de la última etiqueta </em>
    if cursor < len(html_content):
        texto_principal_final = html_content[cursor:]
        texto_principal_final_limpio = re.sub(r'<[^>]+>', '', texto_principal_final).strip()
        if texto_principal_final_limpio:
            ssml_parts.append(f'<voice required="Name={voz_principal}">{texto_principal_final_limpio}</voice>')

    return f'<?xml version="1.0" encoding="UTF-8"?>\n<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">\n{"".join(ssml_parts)}\n</speak>'

def verificar_balcon():
    """Verifica si Balcon está instalado y disponible en el sistema"""
    try:
        subprocess.run(["balcon", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
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
        "-enc", "UTF-8"
    ]

    try:
        subprocess.run(comando_balcon, check=True, capture_output=True, text=True, encoding='utf-8')
        os.unlink(archivo_ssml)
        return True, ""
    except subprocess.CalledProcessError as e:
        os.unlink(archivo_ssml)
        return False, f"Error al ejecutar Balcon: {e.stderr}"

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

class ConversorMarkdownAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Markdown a Audio")
        self.root.geometry("800x650")
        self.archivos_seleccionados = []
        self.voces_disponibles = obtener_voces_balcon()
        self.voz_principal = tk.StringVar(root)
        self.voz_secundaria = tk.StringVar(root)
        if self.voces_disponibles:
            # Establecer voces predeterminadas si están disponibles
            if "Microsoft Helena Desktop" in self.voces_disponibles:
                self.voz_principal.set("Microsoft Helena Desktop")
            elif self.voces_disponibles:
                self.voz_principal.set(self.voces_disponibles[0])

            if "Microsoft David Desktop" in self.voces_disponibles:
                self.voz_secundaria.set("Microsoft David Desktop")
            elif len(self.voces_disponibles) > 1:
                self.voz_secundaria.set(self.voces_disponibles[1])
            elif self.voces_disponibles:
                self.voz_secundaria.set(self.voces_disponibles[0])

        self.balcon_disponible = verificar_balcon()
        self.configurar_interfaz()

    def configurar_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        self.btn_abrir = ttk.Button(toolbar, text="Abrir archivos MD", command=self.abrir_archivos)
        self.btn_abrir.pack(side=tk.LEFT, padx=(0, 5))

        self.lbl_archivos = ttk.Label(toolbar, text="Archivos: Ninguno")
        self.lbl_archivos.pack(side=tk.LEFT, padx=(20, 0))

        frame_idiomas = ttk.LabelFrame(main_frame, text="Selección de Voces")
        frame_idiomas.pack(fill=tk.X, pady=(0, 5))

        lbl_principal = ttk.Label(frame_idiomas, text="Voz Principal:")
        lbl_principal.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_voz_principal = ttk.Combobox(frame_idiomas, textvariable=self.voz_principal, values=self.voces_disponibles)
        self.combo_voz_principal.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        lbl_secundario = ttk.Label(frame_idiomas, text="Voz Secundaria (énfasis):")
        lbl_secundario.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_voz_secundaria = ttk.Combobox(frame_idiomas, textvariable=self.voz_secundaria, values=self.voces_disponibles)
        self.combo_voz_secundaria.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        frame_texto = ttk.LabelFrame(main_frame, text="Vista Previa del Primer Archivo Markdown")
        frame_texto.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        self.texto_markdown = scrolledtext.ScrolledText(frame_texto, wrap=tk.WORD, font=("Consolas", 10))
        self.texto_markdown.pack(fill=tk.BOTH, expand=True)
        self.texto_markdown.config(state=tk.DISABLED)

        frame_audio_botones = ttk.Frame(main_frame)
        frame_audio_botones.pack(fill=tk.X, pady=(5, 0))

        self.btn_generar_audio = ttk.Button(frame_audio_botones, text="Generar Audio para Seleccionados",
                                            command=self.generar_audio_seleccionados,
                                            state=tk.DISABLED if not self.balcon_disponible or not self.archivos_seleccionados else tk.NORMAL)
        self.btn_generar_audio.pack(side=tk.LEFT, padx=(0, 5))

        self.barra_estado = ttk.Label(main_frame, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(fill=tk.X, side=tk.BOTTOM)

        if not self.balcon_disponible:
            self.barra_estado.config(text="ADVERTENCIA: Balcon no está instalado. La generación de audio no estará disponible.")
        elif not self.voces_disponibles:
            self.barra_estado.config(text="ADVERTENCIA: No se encontraron voces de Balcon.")

    def abrir_archivos(self):
        archivos = filedialog.askopenfilenames(
            title="Seleccionar archivos Markdown",
            filetypes=[("Archivos Markdown", "*.md"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if archivos:
            self.archivos_seleccionados = list(archivos)
            self.lbl_archivos.config(text=f"Archivos: {len(self.archivos_seleccionados)} seleccionados")
            self.btn_generar_audio.config(state=tk.NORMAL if self.balcon_disponible and self.archivos_seleccionados else tk.DISABLED)
            # Mostrar el contenido del primer archivo para vista previa
            if self.archivos_seleccionados:
                try:
                    with open(self.archivos_seleccionados[0], "r", encoding="utf-8") as f:
                        contenido = f.read()
                    self.texto_markdown.config(state=tk.NORMAL)
                    self.texto_markdown.delete(1.0, tk.END)
                    self.texto_markdown.insert(tk.END, contenido)
                    self.texto_markdown.config(state=tk.DISABLED)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir el archivo para vista previa: {str(e)}")
            else:
                self.texto_markdown.config(state=tk.DISABLED)
                self.texto_markdown.delete(1.0, tk.END)

    def generar_audio_seleccionados(self):
        if not self.balcon_disponible:
            messagebox.showerror("Error", "Balcon no está instalado.")
            return
        if not self.archivos_seleccionados:
            messagebox.showinfo("Información", "No se han seleccionado archivos para generar audio.")
            return

        voz_principal = self.voz_principal.get()
        voz_secundaria = self.voz_secundaria.get()

        if not voz_principal or not voz_secundaria:
            messagebox.showerror("Error", "Por favor, selecciona las voces principal y secundaria.")
            return

        for archivo_md in self.archivos_seleccionados:
            try:
                with open(archivo_md, "r", encoding="utf-8") as f:
                    contenido_markdown = f.read()

                ssml_completo = markdown_a_ssml(contenido_markdown, voz_principal, voz_secundaria)
                nombre_base_audio = os.path.splitext(os.path.basename(archivo_md))[0]
                archivo_wav = f"{nombre_base_audio}.wav"

                self.barra_estado.config(text=f"Generando audio para: {os.path.basename(archivo_md)}...")
                self.root.update()

                def proceso_generar(ssml, wav_file):
                    exito, mensaje_error = generar_wav_desde_ssml(ssml, wav_file)
                    self.root.after(0, lambda e=exito, msg=mensaje_error, file=wav_file: self.actualizar_ui_generar(e, msg, file))

                thread = threading.Thread(target=proceso_generar, args=(ssml_completo, archivo_wav))
                thread.daemon = True
                thread.start()

            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar {os.path.basename(archivo_md)}: {str(e)}")

    def actualizar_ui_generar(self, exito, mensaje_error, archivo_generado):
        if exito:
            self.barra_estado.config(text=f"Audio generado con éxito: {os.path.basename(archivo_generado)}")
            messagebox.showinfo("Éxito", f"Se generó el audio para {os.path.basename(archivo_generado)}.")
        else:
            messagebox.showerror("Error", f"Error al generar audio para {os.path.basename(archivo_generado)}: {mensaje_error}")
            self.barra_estado.config(text=f"Error al generar audio para {os.path.basename(archivo_generado)}: {mensaje_error}. Verifique la instalación de Balcon y las voces.")

    def reproducir_audio(self):
        messagebox.showinfo("Información", "Por favor, reproduce los archivos de audio generados manualmente.")
        if hasattr(self, 'archivo_wav') and os.path.exists(self.archivo_wav):
            reproducir_audio(self.archivo_wav)
        else:
            messagebox.showinfo("Información", "No se ha generado ningún archivo de audio recientemente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorMarkdownAudio(root)
    root.mainloop()