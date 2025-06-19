import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ply import lex
import os
import re
from analizador_sintactico import analizar_sintaxis_basica
from analizador_semantico import analizar_semantica

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

errores_lexicos = []  # Lista global para almacenar errores léxicos

def t_error(t):
    if not re.match(r'\s', t.value[0]):
        mensaje = f"Error de análisis en la línea {t.lineno}: {t.value[0]}"
        errores_lexicos.append(mensaje)
        print(mensaje)
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

def analizar_lexico_y_sintaxis():
    """
    Analiza el código ingresado en la interfaz y muestra los tokens y errores sintácticos.
    """
    entrada = text_entrada.get("1.0", tk.END)
    # --- Análisis Léxico ---
    lexer.lineno = 1
    lexer.input(entrada)
    resultado_lexico = []
    errores_lexicos.clear()
    while True:
        tok = lexer.token()
        if not tok:
            break
        resultado_lexico.append(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")

    # --- Análisis Sintáctico Básico ---
    lineas = entrada.splitlines()
    pila_llaves = []
    pila_parentesis = []
    clase_abierta = False
    metodo_abierta = False

    for idx, linea in enumerate(lineas, start=1):
        stripped = linea.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if re.match(r'(public|private|protected)?\s*class\s+\w+', stripped):
            clase_abierta = True
            if '{' not in stripped:
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Falta '{{' en declaración de clase")
            continue
        for i, c in enumerate(linea):
            if c == '{':
                pila_llaves.append((idx, i))
            elif c == '}':
                if pila_llaves:
                    pila_llaves.pop()
                else:
                    errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Llave de cierre '}}' sin abrir")
        for i, c in enumerate(linea):
            if c == '(':
                pila_parentesis.append((idx, i))
            elif c == ')':
                if pila_parentesis:
                    pila_parentesis.pop()
                else:
                    errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Paréntesis de cierre ')' sin abrir")
        if re.match(r'(public|private|protected|static|\s)*\s*\w+\s+\w+\s*\(.*\)\s*', stripped):
            metodo_abierta = True
            if '{' not in stripped:
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Falta '{{' en declaración de método")
            continue
        if (not stripped.endswith(';') and
            not stripped.endswith('{') and
            not stripped.endswith('}') and
            not re.match(r'(public|private|protected)?\s*class\s+\w+', stripped) and
            not re.match(r'(public|private|protected|static|\s)*\s*\w+\s+\w+\s*\(.*\)\s*', stripped)):
            if ('=' in stripped or '(' in stripped or ')' in stripped) and not stripped.startswith("//"):
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Falta punto y coma ';'")
    for idx, _ in pila_llaves:
        errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Llave de apertura '{{' sin cerrar")
    for idx, _ in pila_parentesis:
        errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Paréntesis de apertura '(' sin cerrar")
    if not clase_abierta:
        errores_lexicos.append("Error de estructura: No se encontró ninguna declaración de clase en el código.")

    # --- Mostrar resultados ---
    text_resultado.delete("1.0", tk.END)
    text_resultado.insert(tk.END, "Tokens reconocidos:\n")
    for linea in resultado_lexico:
        text_resultado.insert(tk.END, linea + "\n")
    if errores_lexicos:
        text_resultado.insert(tk.END, "\nErrores de sintaxis encontrados:\n")
        for err in errores_lexicos:
            text_resultado.insert(tk.END, err + "\n")
    else:
        text_resultado.insert(tk.END, "\nEstructura sintáctica básica correcta.\n")
    guardar_log(resultado_lexico + ([""] if resultado_lexico else []) + (["Errores de sintaxis encontrados:"] + errores_lexicos if errores_lexicos else ["Estructura sintáctica básica correcta."]))

def analizar_lexico_sintaxis_semantica():
    """
    Analiza el código ingresado en la interfaz y muestra tokens, errores sintácticos y semánticos.
    """
    entrada = text_entrada.get("1.0", tk.END)
    # --- Análisis Léxico ---
    lexer.lineno = 1
    lexer.input(entrada)
    resultado_lexico = []
    errores_lexicos.clear()
    while True:
        tok = lexer.token()
        if not tok:
            break
        resultado_lexico.append(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")

    # --- Análisis Sintáctico ---
    errores_sintacticos = analizar_sintaxis_basica(entrada)

    # --- Análisis Semántico ---
    errores_semanticos = analizar_semantica(entrada)

    # --- Mostrar resultados ---
    text_resultado.delete("1.0", tk.END)
    text_resultado.insert(tk.END, "Tokens reconocidos:\n")
    for linea in resultado_lexico:
        text_resultado.insert(tk.END, linea + "\n")
    if errores_sintacticos:
        text_resultado.insert(tk.END, "\nErrores de sintaxis encontrados:\n")
        for err in errores_sintacticos:
            text_resultado.insert(tk.END, err + "\n")
    else:
        text_resultado.insert(tk.END, "\nEstructura sintáctica básica correcta.\n")
    if errores_semanticos:
        text_resultado.insert(tk.END, "\nErrores semánticos encontrados:\n")
        for err in errores_semanticos:
            text_resultado.insert(tk.END, err + "\n")
    else:
        text_resultado.insert(tk.END, "\nSemántica básica correcta.\n")
    guardar_log(
        resultado_lexico +
        ([""] if resultado_lexico else []) +
        (["Errores de sintaxis encontrados:"] + errores_sintacticos if errores_sintacticos else ["Estructura sintáctica básica correcta."]) +
        (["Errores semánticos encontrados:"] + errores_semanticos if errores_semanticos else ["Semántica básica correcta."])
    )

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

def cargar_archivo_prueba():
    """
    Carga el contenido de los archivos de prueba Thomas_prueba.cs y Cecilia_prueba.cs en el área de entrada.
    No realiza análisis, solo muestra el contenido.
    """
    archivos = ["Thomas_prueba.cs", "Cecilia_prueba.cs"]
    contenido_total = ""
    for ruta in archivos:
        if not os.path.exists(ruta):
            continue
        with open(ruta, "r", encoding="utf-8") as f:
            entrada = f.read()
        contenido_total += f"// Archivo: {ruta}\n{entrada}\n\n"
    text_entrada.delete("1.0", tk.END)
    text_entrada.insert(tk.END, contenido_total)
    text_resultado.delete("1.0", tk.END)

# ---------------------------
# Interfaz gráfica principal
# ---------------------------

class TextWithLineNumbers(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.text = tk.Text(self, **kwargs)
        self.linenumbers = tk.Canvas(self, width=40, background='lightgray', highlightthickness=0)
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        self.text.bind("<KeyRelease>", self._on_change)
        self.text.bind("<MouseWheel>", self._on_change)
        self.text.bind("<Button-1>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        self.text.bind("<FocusIn>", self._on_change)
        self.text.bind("<ButtonRelease-1>", self._on_change)
        self.text['yscrollcommand'] = self._on_textscroll
        self._on_change()

    def _on_change(self, event=None):
        self._update_line_numbers()

    def _on_textscroll(self, *args):
        # Solo pasar los argumentos válidos a yview
        if args and args[0] in ("moveto", "scroll"):
            self.linenumbers.yview(*args)
        self._update_line_numbers()

    def _update_line_numbers(self):
        self.linenumbers.delete("all")
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.linenumbers.create_text(35, y, anchor="ne", text=linenum, font=self.text['font'], fill="black")
            i = self.text.index(f"{i}+1line")

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def bind(self, *args, **kwargs):
        return self.text.bind(*args, **kwargs)

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

# Reemplazar text_entrada por widget con numeración de líneas
text_entrada_widget = TextWithLineNumbers(frame, wrap=tk.NONE)
text_entrada_widget.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
text_entrada = text_entrada_widget.text  # para compatibilidad con el resto del código

label_resultado = ttk.Label(frame, text="Resultados del análisis:")
label_resultado.grid(column=1, row=0, sticky=tk.W)
text_resultado = tk.Text(frame, wrap=tk.NONE, foreground="blue")
text_resultado.grid(column=1, row=1, padx=5, pady=5, sticky="nsew")

# Botones para mostrar resultados separados
frame_botones = ttk.Frame(frame)
frame_botones.grid(column=1, row=2, padx=5, pady=5, sticky="ew")

boton_lexico = ttk.Button(frame_botones, text="Léxico", command=analizar_lexico)
boton_lexico.pack(side=tk.LEFT, padx=2)
boton_sintactico = ttk.Button(frame_botones, text="Sintáctico", command=analizar_sintactico)
boton_sintactico.pack(side=tk.LEFT, padx=2)
boton_semantico = ttk.Button(frame_botones, text="Semántico", command=analizar_semantico)
boton_semantico.pack(side=tk.LEFT, padx=2)

# Botón Cargar Archivo de Prueba (solo carga el contenido)
boton_archivo = ttk.Button(frame, text="Cargar Archivo de Prueba", command=cargar_archivo_prueba)
boton_archivo.grid(column=0, row=2, padx=5, pady=10, sticky="ew")

# Botón Limpiar
boton_limpiar = ttk.Button(frame, text="Limpiar", command=limpiar_campos)
boton_limpiar.grid(column=0, row=3, columnspan=1, padx=5, pady=5, sticky="ew")

ventana.mainloop()