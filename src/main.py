
# -------------------------------------------------------------
# main.py - Módulo principal del Analizador C# en Python (usando PLY)
#
# Este archivo orquesta el análisis léxico, sintáctico y semántico,
# gestiona la interfaz gráfica y el registro de logs.
# Incluye funciones para analizar código fuente, guardar resultados
# y ejecutar pruebas automáticas.
# -------------------------------------------------------------

from datetime import datetime
import os
import subprocess
from lexer import lexer  # Analizador léxico (definido en lexer.py)
from syntax import parser  # Analizador sintáctico (definido en syntax.py)
from semantic import validar_declaracion_variable, symbol_table  # Funciones y tabla semántica


# ---------------------------
# Obtener nombre de usuario de Git para logs
# ---------------------------
try:
    usuario_git = subprocess.check_output(["git", "config", "user.name"]).strip().decode('utf-8')
except subprocess.CalledProcessError:
    usuario_git = "desconocido"


# ---------------------------
# Funciones de análisis y log
# ---------------------------

# ------------ Léxico -------------------
def guardar_log_lexico(resultado):
    """
    Guarda el resultado del análisis léxico en un archivo de log.
    El nombre del archivo incluye el usuario y la fecha/hora.
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"logs/lexico-{usuario_git}-{fecha_hora}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("Tokens reconocidos:\n")
        f.write("\n".join(resultado))
    return nombre_archivo

def analizar_lexico(entrada):
    """
    Analiza el código fuente recibido y retorna una lista de tokens reconocidos.
    Si encuentra caracteres no definidos, los reporta con su línea.
    """
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



# ------------ Sintáctico -------------------
def guardar_log_sintactico(resultado):
    """
    Guarda el resultado del análisis sintáctico en un archivo de log.
    El nombre del archivo incluye el usuario y la fecha/hora.
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"logs/sintactico-{usuario_git}-{fecha_hora}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("Sintaxis:\n")
        f.write("\n".join(resultado))
    return nombre_archivo

def analizar_sintactico(entrada):
    """
    Realiza el análisis sintáctico del código fuente usando el parser de syntax.py.
    Captura reglas reconocidas y errores, y retorna el resultado como lista de strings.
    """
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
    resultado.extend(reglas_y_errores)
    if not resultado:
        resultado.append("Análisis sintáctico exitoso.")
    else:
        if not any("Error de sintaxis" in r or "Excepción" in r for r in resultado):
            resultado.append("Análisis sintáctico exitoso.")
    return resultado


# ------------ Semántico -------------------
def guardar_log_semantico(resultado):
    """
    Guarda el resultado del análisis semántico en un archivo de log.
    El nombre del archivo incluye el usuario y la fecha/hora.
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")
    fecha_hora = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"logs/semantico-{usuario_git}-{fecha_hora}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("Análisis Semántico:\n")
        f.write("\n".join(resultado))
    return nombre_archivo

def analizar_semantico(entrada):
    """
    Realiza el análisis semántico del código fuente recibido.
    Valida declaraciones, inferencias de tipo, asignaciones y reporta errores.
    Utiliza la tabla de símbolos y funciones de semantic.py.
    """
    symbol_table.clear()
    resultado = []
    errores_semanticos = []
    try:
        lexer.lineno = 1
        lexer.input(entrada)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)
        tipo_actual = None
        en_declaracion = False
        nombre = None
        valor = None
        valor_tipo = None
        for i, tok in enumerate(tokens):
            # Detectar declaraciones de variables para cualquier tipo de dato reconocido por el lexer
            if tok.type in ["ID", "INT", "FLOAT", "BOOL", "CHAR", "DOUBLE", "VAR", "STRING"]:
                # Si es palabra reservada de tipo, usar su valor como tipo_actual
                if tok.type in ["INT", "FLOAT", "BOOL", "CHAR", "DOUBLE"]:
                    tipo_actual = tok.value
                    en_declaracion = True
                    resultado.append(f"Línea {tok.lineno}: Tipo '{tipo_actual}' detectado")
                elif tok.type == "STRING":
                    tipo_actual = "string"
                    en_declaracion = True
                    resultado.append(f"Línea {tok.lineno}: Tipo 'string' detectado")
                elif tok.type == "VAR":
                    tipo_actual = "var"
                    en_declaracion = True
                    resultado.append(f"Línea {tok.lineno}: Tipo 'var' detectado")
                # Si es un identificador y estamos en declaración, es el nombre de la variable
                elif en_declaracion and tok.type == "ID":
                    nombre = tok.value
                    valor = None
                    valor_tipo = None
                    # Busca inicialización en los siguientes tokens hasta el próximo punto y coma
                    j = i + 1
                    tiene_inicializacion = False
                    while j < len(tokens) and tokens[j].type != "SEMICOLON":
                        if tokens[j].type == "ASSIGN" and j + 1 < len(tokens):
                            siguiente = tokens[j + 1]
                            # Si es una expresión, intenta reconstruirla (solo para parser avanzado)
                            if siguiente.type in ["INT_CONST", "FLOAT_CONST", "STRING_CONST", "ID", "TRUE", "FALSE"]:
                                valor = siguiente.value
                                valor_tipo = siguiente.type if siguiente.type not in ["TRUE", "FALSE"] else "BOOL_CONST"
                            else:
                                # Si es una expresión compleja, reconstruir el AST (requiere integración con parser)
                                valor = siguiente.value
                                valor_tipo = 'EXPR'
                            tiene_inicializacion = True
                            break
                        j += 1
                    # Si no hay inicialización, igual registrar la variable
                    if not tiene_inicializacion:
                        valor = None
                        valor_tipo = None
                    # Si es var, permitir declaración sin inicialización (C#-like)
                    if tipo_actual == "var":
                        if valor is not None:
                            from semantic import inferir_tipo_expresion
                            tipo_inferido = inferir_tipo_expresion(valor)
                            tipo_actual = tipo_inferido
                            mensajes = validar_declaracion_variable(tipo_actual, nombre, valor, valor_tipo)
                        else:
                            # Registrar como pendiente de inferencia
                            if nombre not in symbol_table:
                                symbol_table[nombre] = {"tipo": "var", "valor": None, "pending_inference": True}
                            mensajes = [f"Línea {tok.lineno}: Variable 'var' declarada sin inicialización. El tipo se inferirá en la primera asignación."]
                    else:
                        mensajes = validar_declaracion_variable(tipo_actual, nombre, valor, valor_tipo)
                    if mensajes:
                        if isinstance(mensajes, str):
                            mensajes = [mensajes]
                        for msg in mensajes:
                            if msg and ("error" in msg.lower() or "no permitido" in msg.lower() or "no declarada" in msg.lower()):
                                errores_semanticos.append(f"Línea {tok.lineno}: {msg}")
                            resultado.append(f"Línea {tok.lineno}: {msg}")
                    else:
                        resultado.append(f"Línea {tok.lineno}: Variable '{nombre}' declarada como {tipo_actual}")
                        if valor is not None:
                            resultado.append(f"Línea {tok.lineno}: Variable '{nombre}' inicializada con valor {valor}")
                    en_declaracion = False
                    tipo_actual = None
            # Validar asignaciones fuera de declaración
            if tok.type == "ID" and i + 1 < len(tokens) and tokens[i + 1].type == "ASSIGN":
                nombre = tok.value
                if nombre in symbol_table:
                    valor = None
                    valor_tipo = None
                    siguiente = tokens[i + 2] if i + 2 < len(tokens) else None
                    if siguiente:
                        if siguiente.type in ["INT_CONST", "FLOAT_CONST", "STRING_CONST", "ID", "TRUE", "FALSE"]:
                            valor = siguiente.value
                            valor_tipo = siguiente.type if siguiente.type not in ["TRUE", "FALSE"] else "BOOL_CONST"
                        else:
                            valor = siguiente.value
                            valor_tipo = 'EXPR'
                        # Validar tipo de asignación
                        tipo_var = symbol_table[nombre]["tipo"]
                        from semantic import inferir_tipo_expresion
                        tipo_valor = None
                        if valor_tipo == 'EXPR':
                            tipo_valor = inferir_tipo_expresion(valor)
                        elif valor_tipo == "ID":
                            tipo_valor = symbol_table[valor]["tipo"] if valor in symbol_table else None
                        elif valor_tipo == "INT_CONST":
                            tipo_valor = "int"
                        elif valor_tipo == "FLOAT_CONST":
                            tipo_valor = "float"
                        elif valor_tipo == "STRING_CONST":
                            tipo_valor = "string"
                        elif valor_tipo == "BOOL_CONST":
                            tipo_valor = "bool"
                        else:
                            tipo_valor = valor_tipo
                        # Si la variable es var y pendiente de inferencia, infiere el tipo en la primera asignación
                        if tipo_var == "var" and symbol_table[nombre].get("pending_inference", False):
                            symbol_table[nombre]["tipo"] = tipo_valor
                            symbol_table[nombre]["pending_inference"] = False
                            tipo_var = tipo_valor
                            resultado.append(f"Línea {tok.lineno}: Tipo de 'var' inferido como {tipo_valor} en la primera asignación a '{nombre}'.")
                        if tipo_var == "float" and tipo_valor == "int":
                            resultado.append(f"Línea {tok.lineno}: Casting implícito: Variable '{nombre}' de tipo float asignada con int. Se convierte automáticamente a float.")
                        elif tipo_var == "double" and tipo_valor == "int":
                            resultado.append(f"Línea {tok.lineno}: Casting implícito: Variable '{nombre}' de tipo double asignada con int. Se convierte automáticamente a double.")
                        elif tipo_var != tipo_valor:
                            errores_semanticos.append(f"Línea {tok.lineno}: Error semántico: No se puede asignar valor de tipo {tipo_valor} a variable {tipo_var} '{nombre}'.")
                        else:
                            resultado.append(f"Línea {tok.lineno}: Asignación correcta: {nombre} = {valor}")
                else:
                    errores_semanticos.append(f"Línea {tok.lineno}: Error semántico: Variable '{nombre}' no declarada antes de la asignación.")
        if errores_semanticos:
            resultado.extend(["\n--- Errores Semánticos ---"] + errores_semanticos)
        if not errores_semanticos:
            resultado.append("\nAnálisis semántico exitoso - No se encontraron errores.")
        else:
            resultado.append(f"\nAnálisis semántico completado con {len(errores_semanticos)} error(es).")
    except Exception as e:
        resultado.append(f"Error durante el análisis semántico: {str(e)}")
    return resultado



# ------------ Pruebas automáticas -------------------
def analizar_archivo_prueba():
    """
    Lee y analiza los archivos de prueba Thomas_prueba.cs y Cecilia_prueba.cs.
    Retorna el contenido y los tokens reconocidos para cada archivo.
    """
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


# ---------------------------
# Ejecución principal y GUI
# ---------------------------
if __name__ == "__main__":
    # Si se ejecuta como script principal, lanza la interfaz gráfica (PyQt5)
    from PyQt5.QtWidgets import QApplication
    from gui import AnalizadorApp
    import sys
    app = QApplication(sys.argv)
    ventana = AnalizadorApp()
    ventana.show()
    sys.exit(app.exec_())

    # --- Ejecución por terminal (opcional) ---
    # Permite ejecutar el análisis sintáctico directamente desde terminal:
    # python src/main.py archivo.cs
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        with open(archivo, encoding="utf-8") as f:
            data = f.read()
        lexer.lineno = 1  # Reinicia el contador de líneas antes de analizar
        parser.parse(data, lexer=lexer)
    else:
        print("Uso: python src/main.py <archivo.cs>")