import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ply import lex
import os
import re

# ---------------------------
# Definición de tokens y lexer para C#
# ---------------------------

tokens = (
    'ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'STRING', 'LT', 'GT',
    'INCREMENT', 'DECREMENT', 'AND', 'OR', 'ARROW', 'LBRACKET', 'RBRACKET', 'DOT',
    'COMMA', 'COLON', 'QUESTION', 'AMPERSAND', 'PIPE', 'MOD', 'NOT', 'QUOTE', 'APOSTROPHE', 'COMMENT',
    'LE', 'GE', 'EQ', 'NE',  # <=, >=, ==, !=
    'PLUSEQ', 'MINUSEQ', 'TIMESEQ', 'DIVEQ', 'MODEQ',  # +=, -=, *=, /=, %=
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
    'using': 'USING',
    'namespace': 'NAMESPACE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'do': 'DO',
    'while': 'WHILE',
    'try': 'TRY',
    'catch': 'CATCH',
    'finally': 'FINALLY',
    'throw': 'THROW',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
    'enum': 'ENUM',
    'const': 'CONST',
    'readonly': 'READONLY',
    'interface': 'INTERFACE',
    'override': 'OVERRIDE',
    'abstract': 'ABSTRACT',
    'virtual': 'VIRTUAL',
    'base': 'BASE',
    'object': 'OBJECT',
    'decimal': 'DECIMAL',
    'byte': 'BYTE',
    'short': 'SHORT',
    'long': 'LONG',
    'uint': 'UINT',
    'ulong': 'ULONG',
    'ushort': 'USHORT',
    'sbyte': 'SBYTE',
    'foreach': 'FOREACH',
    'out': 'OUT',
    'ref': 'REF',
    'params': 'PARAMS',
    'get': 'GET',
    'set': 'SET',
    'operator': 'OPERATOR',
    'event': 'EVENT',
    'delegate': 'DELEGATE',
    'struct': 'STRUCT',
    'sizeof': 'SIZEOF',
    'typeof': 'TYPEOF',
    'is': 'IS',
    'as': 'AS',
    'lock': 'LOCK',
    'checked': 'CHECKED',
    'unchecked': 'UNCHECKED',
    'fixed': 'FIXED',
    'stackalloc': 'STACKALLOC',
    'implicit': 'IMPLICIT',
    'explicit': 'EXPLICIT',
    'extern': 'EXTERN',
    'partial': 'PARTIAL',
    'yield': 'YIELD',
    'add': 'ADD',
    'remove': 'REMOVE'
}

tokens += tuple(reserved.values())

# Expresiones regulares para los tokens (orden: primero los de mayor longitud)
t_INCREMENT   = r'\+\+'
t_DECREMENT   = r'--'
t_AND         = r'&&'
t_OR          = r'\|\|'
t_ARROW       = r'->'
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_EQUALS      = r'='
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_LBRACKET    = r'\['
t_RBRACKET    = r'\]'
t_SEMICOLON   = r';'
t_COMMA       = r','
t_COLON       = r':'
t_QUESTION    = r'\?'
t_AMPERSAND   = r'&'
t_PIPE        = r'\|'
t_DOT         = r'\.'
t_LT          = r'<'
t_GT          = r'>'
t_MOD         = r'%'
t_NOT         = r'!'
t_QUOTE       = r'"'
t_APOSTROPHE  = r"'"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
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
    t.value = t.value[1:-1]
    return t

def t_ignore_whitespace(t):
    r'[ \t]+'
    pass

def t_newline(t):
    r'(\r\n|\r|\n)+'
    t.lexer.lineno += t.value.count('\n')

def t_COMMENT(t):
    r'//.*'
    pass

def t_multiline_comment(t):
    r'/\*[\s\S]*?\*/'
    pass

def t_ignore_unicode(t):
    r'[^\x00-\x7F]'
    pass

def t_error(t):
    if not re.match(r'\s', t.value[0]):
        print(f"Error de análisis en la línea {t.lineno}: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# ---------------------------
# Funciones de análisis y log
# ---------------------------

def analizar_codigo():
    """Analiza el código ingresado en la interfaz y muestra los tokens."""
    entrada = text_entrada.get("1.0", tk.END)
    lexer.lineno = 1  # <-- Inicializar el número de línea antes de analizar
    lexer.input(entrada)
    resultado = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        resultado.append(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")
    text_resultado.delete("1.0", tk.END)
    for linea in resultado:
        text_resultado.insert(tk.END, linea + "\n")
    guardar_log(resultado)

def guardar_log(resultado):
    """Guarda el resultado del análisis en un archivo de log."""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"logs/lexico-{usuario_git}-{fecha_hora}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("Tokens reconocidos:\n")
        f.write("\n".join(resultado))
    print(f"Log guardado: {nombre_archivo}")

def limpiar_campos():
    """Limpia el contenido de los cuadros de texto de entrada y resultado."""
    text_entrada.delete("1.0", tk.END)
    text_resultado.delete("1.0", tk.END)

# ---------------------------
# Obtener nombre de usuario de Git
# ---------------------------

import subprocess
try:
    usuario_git = subprocess.check_output(["git", "config", "user.name"]).strip().decode('utf-8')
except subprocess.CalledProcessError:
    usuario_git = "desconocido"

# ---------------------------
# Análisis de archivos de prueba
# ---------------------------

def analizar_archivo_prueba():
    """Lee y analiza los archivos de prueba Thomas_prueba.cs y Cecilia_prueba.cs."""
    archivos = ["Thomas_prueba.cs", "Cecilia_prueba.cs"]
    contenido_total = ""
    resultado_total = []
    for ruta in archivos:
        if not os.path.exists(ruta):
            print(f"El archivo {ruta} no existe. Crea tu algoritmo de prueba en ese archivo.")
            continue
        with open(ruta, "r", encoding="utf-8") as f:
            entrada = f.read()
        contenido_total += f"// Archivo: {ruta}\n{entrada}\n\n"
        lexer.lineno = 1  # <-- Inicializar el número de línea antes de analizar cada archivo
        lexer.input(entrada)
        resultado_total.append(f"--- Tokens para {ruta} ---")
        while True:
            tok = lexer.token()
            if not tok:
                break
            resultado_total.append(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")
        resultado_total.append("")
    text_entrada.delete("1.0", tk.END)
    text_entrada.insert(tk.END, contenido_total)
    text_resultado.delete("1.0", tk.END)
    for linea in resultado_total:
        text_resultado.insert(tk.END, linea + "\n")
    guardar_log(resultado_total)
    print("Análisis completado. Revisa el archivo log generado en la carpeta logs.")

# ---------------------------
# Interfaz gráfica principal
# ---------------------------

ventana = tk.Tk()
ventana.title("Analizador Léxico de C# ")
ventana.geometry("900x400")  # Pantalla más pequeña

frame = ttk.Frame(ventana, padding=10)
frame.pack(expand=True, fill=tk.BOTH)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(1, weight=1)

label_entrada = ttk.Label(frame, text="Código C#:")
label_entrada.grid(column=0, row=0, sticky=tk.W)
text_entrada = tk.Text(frame, wrap=tk.NONE)
text_entrada.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

label_resultado = ttk.Label(frame, text="Tokens:")
label_resultado.grid(column=1, row=0, sticky=tk.W)
text_resultado = tk.Text(frame, wrap=tk.NONE, foreground="blue")
text_resultado.grid(column=1, row=1, padx=5, pady=5, sticky="nsew")

# Distribuir los botones horizontalmente en la parte inferior
boton_analizar = ttk.Button(frame, text="Analizar", command=analizar_codigo)
boton_analizar.grid(column=0, row=2, padx=5, pady=10, sticky="ew")

boton_archivo = ttk.Button(frame, text="Analizar archivo de prueba", command=analizar_archivo_prueba)
boton_archivo.grid(column=1, row=2, padx=5, pady=10, sticky="ew")

boton_limpiar = ttk.Button(frame, text="Limpiar", command=limpiar_campos)
boton_limpiar.grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky="ew")

ventana.mainloop()