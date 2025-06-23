from datetime import datetime
import os
import subprocess
from lexer import lexer  # Importa el lexer desde lexer.py
from syntax import parser  # Importa el parser desde syntax.py

# ---------------------------
# Obtener nombre de usuario de Git
# ---------------------------

try:
    usuario_git = subprocess.check_output(["git", "config", "user.name"]).strip().decode('utf-8')
except subprocess.CalledProcessError:
    usuario_git = "desconocido"

# ---------------------------
# Funciones de análisis y log
# ---------------------------

def guardar_log_lexico(resultado):
    """Guarda el resultado del análisis léxico en un archivo de log."""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"logs/lexico-{usuario_git}-{fecha_hora}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("Tokens reconocidos:\n")
        f.write("\n".join(resultado))
    return nombre_archivo

def analizar_lexico(entrada):
    """Analiza el código ingresado y retorna los tokens."""
    lexer.lineno = 1
    lexer.input(entrada)
    resultado = []
    pos = 0
    length = len(entrada)
    while pos < length:
        tok = lexer.token()
        if tok:
            resultado.append(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")
            pos = lexer.lexpos
        else:
            # Si hay un carácter no reconocido, repórtalo y avanza uno
            if pos < length and not entrada[pos].isspace():
                linea_actual = entrada.count('\n', 0, pos) + 1
                resultado.append(f"<span style='color:red;'>Este caracter no está definido: '{entrada[pos]}' en la línea {linea_actual}</span>")
            pos += 1
            lexer.lexpos = pos
            # Reinicia el lexer para continuar desde el nuevo pos
            lexer.input(entrada[pos:])
    return resultado

def guardar_log_sintactico(resultado):
    """Guarda el resultado del análisis sintáctico en un archivo de log."""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"logs/sintactico-{usuario_git}-{fecha_hora}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("Sintaxis:\n")
        f.write("\n".join(resultado))
    return nombre_archivo

def analizar_sintactico(entrada):
    from syntax import parser
    resultado = []
    from lexer import lexer
    lexer.lineno = 1
    if hasattr(lexer, 'input'):
        lexer.input('')
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        parser.parse(entrada, lexer=lexer)
    except Exception as e:
        resultado.append(f"Excepción: {e}")
    sys.stdout = old_stdout
    reglas_y_errores = mystdout.getvalue().splitlines()
    for regla in reglas_y_errores:
        print(regla)
    resultado.extend(reglas_y_errores)
    if not resultado:
        resultado.append("Análisis sintáctico exitoso.")
    else:
        if not any("Error de sintaxis" in r or "Excepción" in r for r in resultado):
            resultado.append("Análisis sintáctico exitoso.")
    return resultado

def analizar_archivo_prueba():
    """Lee y analiza los archivos de prueba Thomas_prueba.cs y Cecilia_prueba.cs."""
    archivo1 = "src/Thomas_prueba.cs"
    archivo2 = "src/Cecilia_prueba.cs"
    archivos = [archivo1, archivo2]
    contenido_total = ""
    resultado_total = []
    for ruta in archivos:
        if not os.path.exists(ruta):
            resultado_total.append(f"El archivo {ruta} no existe. Crea tu algoritmo de prueba en ese archivo.")
            continue
        with open(ruta, "r", encoding="utf-8") as f:
            entrada = f.read()
        contenido_total += f"// Archivo: {ruta}\n{entrada}\n\n"
        lexer.lineno = 1
        lexer.input(entrada)
        resultado_total.append(f"--- Tokens para {ruta} ---")
        while True:
            tok = lexer.token()
            if not tok:
                break
            resultado_total.append(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")
        resultado_total.append("")
    return contenido_total, resultado_total

# Nota: Ya no hay interfaz gráfica

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from gui import AnalizadorApp
    import sys
    app = QApplication(sys.argv)
    ventana = AnalizadorApp()
    ventana.show()
    sys.exit(app.exec_())

    with open("archivo.cs") as f:
        data = f.read()

   
    # Permite ejecutar el análisis sintáctico directamente desde terminal
    import sys
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        with open(archivo, encoding="utf-8") as f:
            data = f.read()
        lexer.lineno = 1  # Reinicia el contador de líneas antes de analizar
        parser.parse(data, lexer=lexer)
    else:
        print("Uso: python src/main.py <archivo.cs>")