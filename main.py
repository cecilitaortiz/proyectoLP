import tkinter as tk
from tkinter import ttk

def analizar_codigo():
    return


# Ventana principal
ventana = tk.Tk()
ventana.title("Analizador Léxico y Semántico C#")
ventana.geometry("900x500")

# Marco principal
frame = ttk.Frame(ventana, padding=10)
frame.pack(expand=True, fill=tk.BOTH)

# Cuadro de entrada de código
label_entrada = ttk.Label(frame, text="Código C#:")
label_entrada.grid(column=0, row=0, sticky=tk.W)
text_entrada = tk.Text(frame, width=50, height=25, wrap=tk.NONE)
text_entrada.grid(column=0, row=1, padx=5, pady=5)

# Cuadro de resultados
label_resultado = ttk.Label(frame, text="Resultado del análisis:")
label_resultado.grid(column=1, row=0, sticky=tk.W)
text_resultado = tk.Text(frame, width=50, height=25, wrap=tk.NONE, foreground="blue")
text_resultado.grid(column=1, row=1, padx=5, pady=5)

# Botón para analizar
boton_analizar = ttk.Button(frame, text="Analizar", command=analizar_codigo)
boton_analizar.grid(column=0, row=2, columnspan=2, pady=10)

ventana.mainloop()