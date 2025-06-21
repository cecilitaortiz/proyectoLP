from datetime import datetime
import os
import subprocess
from lexer import lexer  # Importa el lexer desde lexer.py

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

def guardar_log(resultado):
    """Guarda el resultado del análisis en un archivo de log."""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"logs/lexico-{usuario_git}-{fecha_hora}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("Tokens reconocidos:\n")
        f.write("\n".join(resultado))
    return nombre_archivo

def analizar_codigo(entrada):
    """Analiza el código ingresado y retorna los tokens."""
    lexer.lineno = 1
    lexer.input(entrada)
    resultado = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        resultado.append(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")
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

# Nota: Ya no hay interfaz gráfica aquí.