import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ply import lex, yacc
import os

#Código Cecilia Ortiz (deficinión de tokens y definiciones lexicas básicas)

tokens = (
    'ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'STRING', 'LT', 'GT',
)

reserved = {
    'int': 'INT',
    'double': 'DOUBLE',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'string': 'STRINGTYPE',
    'char': 'CHAR',
    'var': 'VAR',
    'List': 'LIST',

    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',

    'class': 'CLASS',
    'public': 'PUBLIC',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'static': 'STATIC',
    'new': 'NEW',
    'this': 'THIS',
    
    'return': 'RETURN',
    'void': 'VOID',
}

tokens += tuple(reserved.values())

# Definición de los tokens
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_EQUALS     = r'='
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_SEMICOLON  = r';'
t_LT         = r'<'
t_GT         = r'>'
t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es una palabra reservada
    return t

def t_FLOAT(t):
    r'\d+\.\d+' 
    t.value = float(t.value) 
    return t
    
def t_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value) 
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value) 
    return t    

def t_STRING(t):
    r'"[^"\n]*"'  
    t.value = t.value[1:-1]  # Eliminar las comillas
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error de análisis en la línea {t.lineno}: {t.value[0]}")
    t.lexer.skip(1)  # Ignorar el carácter no reconocido

lexer = lex.lex()




def analizar_codigo():
    entrada = text_entrada.get("1.0", tk.END)
    lexer.input(entrada)
    resultado = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        resultado.append(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")

    # Mostrar resultado en GUI
    text_resultado.delete("1.0", tk.END)
    for linea in resultado:
        text_resultado.insert(tk.END, linea + "\n")

    # Guardar log
    guardar_log(resultado)

def guardar_log(resultado):
    # Crear carpeta logs si no existe
    if not os.path.exists("logs"):
        os.makedirs("logs")
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"logs/lexico-{usuario_git}-{fecha_hora}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("Tokens reconocidos:\n")
        f.write("\n".join(resultado))
    print(f"Log guardado: {nombre_archivo}")

# Obtener el nombre de usuario de Git
import subprocess  
try:
    usuario_git = subprocess.check_output(["git", "config", "user.name"]).strip().decode('utf-8')
except subprocess.CalledProcessError:
    usuario_git = "desconocido" 




# ---------- VENTANA ----------
ventana = tk.Tk()
ventana.title("Analizador Léxico de C# ")
ventana.geometry("900x500")

frame = ttk.Frame(ventana, padding=10)
frame.pack(expand=True, fill=tk.BOTH)

label_entrada = ttk.Label(frame, text="Código C#:")
label_entrada.grid(column=0, row=0, sticky=tk.W)
text_entrada = tk.Text(frame, width=50, height=25, wrap=tk.NONE)
text_entrada.grid(column=0, row=1, padx=5, pady=5)

label_resultado = ttk.Label(frame, text="Tokens:")
label_resultado.grid(column=1, row=0, sticky=tk.W)
text_resultado = tk.Text(frame, width=50, height=25, wrap=tk.NONE, foreground="blue")
text_resultado.grid(column=1, row=1, padx=5, pady=5)

boton_analizar = ttk.Button(frame, text="Analizar", command=analizar_codigo)
boton_analizar.grid(column=0, row=2, columnspan=2, pady=10)

ventana.mainloop()