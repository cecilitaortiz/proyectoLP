import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from lexer import lexer
from main import analizar_codigo, guardar_log
from tkcode import CodeEditor

# Obtener nombre de usuario de Git
try:
    usuario_git = subprocess.check_output(["git", "config", "user.name"]).strip().decode('utf-8')
except subprocess.CalledProcessError:
    usuario_git = "desconocido"

def listar_archivos_test():
    carpeta = "test"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    return [f for f in os.listdir(carpeta) if f.endswith(".cs")]

def cargar_archivo_test(nombre_archivo):
    ruta = os.path.join("test", nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

class ModalArchivos(tk.Toplevel):
    def __init__(self, master, callback_cargar):
        super().__init__(master)
        self.title("Selecciona o sube un archivo de prueba (.cs)")
        self.callback_cargar = callback_cargar
        self.geometry("400x200")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        ttk.Label(self, text="Archivos en test/").pack(pady=(10, 2))
        self.archivos_var = tk.StringVar()
        self.archivos_dropdown = ttk.Combobox(self, textvariable=self.archivos_var, values=listar_archivos_test(), state="readonly")
        self.archivos_dropdown.pack(fill="x", padx=20)
        ttk.Button(self, text="Cargar archivo seleccionado", command=self.cargar_archivo).pack(pady=5)

        ttk.Label(self, text="Subir archivo .cs").pack(pady=(10, 2))
        ttk.Button(self, text="Seleccionar archivo...", command=self.subir_archivo).pack()
        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

    def cargar_archivo(self):
        nombre = self.archivos_var.get()
        if nombre:
            self.callback_cargar(nombre)
            self.destroy()

    def subir_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos C#", "*.cs")])
        if ruta:
            destino = os.path.join("test", os.path.basename(ruta))
            with open(ruta, "rb") as src, open(destino, "wb") as dst:
                dst.write(src.read())
            self.archivos_dropdown['values'] = listar_archivos_test()

class AnalizadorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Léxico de C#")
        self.geometry("1100x600")
        self.resizable(True, True)

        # Título
        ttk.Label(self, text="Analizador Léxico de C#", font=("Arial", 18, "bold")).pack(pady=10)

        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Editor de código con numeración de líneas y resaltado para C#
        editor_frame = ttk.Frame(main_frame)
        editor_frame.pack(side="left", fill="both", expand=True)
        ttk.Label(editor_frame, text="Código fuente:").pack(anchor="w")
        self.editor = CodeEditor(
            editor_frame,
            width=60,
            height=25,
            language="csharp",  # <-- Cambia aquí a "csharp"
            font=("Consolas", 12),
            blockcursor=True,
            background="white",
            highlighter="dracula"
        )
        self.editor.pack(fill="both", expand=True)

        # Panel de resultados y botones
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="left", fill="y", padx=(10,0))

        # Botones de selección de resultado
        botones_frame = ttk.Frame(right_frame)
        botones_frame.pack(fill="x", pady=(0,5))
        self.btn_tokens = ttk.Button(botones_frame, text="Tokens", command=self.mostrar_tokens)
        self.btn_tokens.grid(row=0, column=0, padx=2)
        self.btn_semantico = ttk.Button(botones_frame, text="Semántico", command=self.mostrar_semantico)
        self.btn_semantico.grid(row=0, column=1, padx=2)
        self.btn_sintactico = ttk.Button(botones_frame, text="Sintáctico", command=self.mostrar_sintactico)
        self.btn_sintactico.grid(row=0, column=2, padx=2)

        # Áreas de resultados
        self.resultado_tokens = ScrolledText(right_frame, width=50, height=15, font=("Consolas", 11), state="normal")
        self.resultado_tokens.pack(fill="x")
        self.resultado_semantico = ScrolledText(right_frame, width=50, height=15, font=("Consolas", 11), state="normal")
        self.resultado_semantico.pack(fill="x")
        self.resultado_sintactico = ScrolledText(right_frame, width=50, height=15, font=("Consolas", 11), state="normal")
        self.resultado_sintactico.pack(fill="x")
        self.resultado_semantico.pack_forget()
        self.resultado_sintactico.pack_forget()

        # Mensaje de log
        self.mensaje_log = ttk.Label(right_frame, text="", foreground="green")
        self.mensaje_log.pack(pady=5)

        # Botones de acción
        acciones_frame = ttk.Frame(self)
        acciones_frame.pack(pady=5)
        ttk.Button(acciones_frame, text="Analizar", command=self.analizar).pack(side="left", padx=5)
        ttk.Button(acciones_frame, text="Analizar archivo de prueba", command=self.abrir_modal_archivos).pack(side="left", padx=5)
        ttk.Button(acciones_frame, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

    def mostrar_tokens(self):
        self.resultado_tokens.pack(fill="x")
        self.resultado_semantico.pack_forget()
        self.resultado_sintactico.pack_forget()

    def mostrar_semantico(self):
        self.resultado_tokens.pack_forget()
        self.resultado_semantico.pack(fill="x")
        self.resultado_sintactico.pack_forget()

    def mostrar_sintactico(self):
        self.resultado_tokens.pack_forget()
        self.resultado_semantico.pack_forget()
        self.resultado_sintactico.pack(fill="x")

    def analizar(self):
        entrada = self.editor.get("1.0", "end-1c")
        try:
            resultado = analizar_codigo(entrada)
            self.resultado_tokens.config(state="normal")
            self.resultado_tokens.delete("1.0", "end")
            self.resultado_tokens.insert("1.0", "\n".join(resultado))
            self.resultado_tokens.config(state="disabled")
            log_path = guardar_log(resultado)
            self.mensaje_log.config(text=f"✅ Log guardado exitosamente en '{log_path}'", foreground="green")
            self.mostrar_tokens()
        except Exception as e:
            self.mensaje_log.config(text=f"❌ Error: {str(e)}", foreground="red")

    def limpiar(self):
        self.editor.delete("1.0", "end")
        for area in [self.resultado_tokens, self.resultado_semantico, self.resultado_sintactico]:
            area.config(state="normal")
            area.delete("1.0", "end")
            area.config(state="disabled")
        self.mensaje_log.config(text="")
        self.mostrar_tokens()

    def abrir_modal_archivos(self):
        ModalArchivos(self, self.cargar_archivo_test)

    def cargar_archivo_test(self, nombre_archivo):
        try:
            contenido = cargar_archivo_test(nombre_archivo)
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", contenido)
            self.analizar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

if __name__ == "__main__":
    # Solo intenta lanzar la GUI si hay entorno gráfico disponible
    if os.environ.get("DISPLAY") or os.name == "nt":
        app = AnalizadorApp()
        app.mainloop()
    else:
        print("No se detectó entorno gráfico. Ejecuta este programa en un entorno con GUI.")


# Nota:
# El componente gr.Code ya incluye scroll automático y numeración de líneas por defecto.
# No es necesario ni posible agregar 'autoscroll=True' como argumento.
