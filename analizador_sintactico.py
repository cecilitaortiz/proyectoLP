import re

def analizar_sintaxis_basica(codigo):
    """
    Analiza la sintaxis básica del código C# recibido como string.
    Retorna una lista de errores sintácticos encontrados.
    - Verifica declaraciones de clase, métodos, variables, if/else, llaves y paréntesis.
    - Detecta errores comunes como declaraciones inválidas, sentencias incompletas, etc.
    """
    lineas = codigo.splitlines()
    errores_lexicos = []
    pila_llaves = []
    pila_parentesis = []
    clase_abierta = False

    tipo_regex = r'(int|double|float|bool|string|char|var|List<.*?>)'

    for idx, linea in enumerate(lineas, start=1):
        stripped = linea.strip()
        # Ignorar líneas vacías y comentarios
        if not stripped or stripped.startswith("//"):
            continue

        # Verificar declaración de clase
        if re.match(r'(public|private|protected)?\s*class\s+\w+', stripped):
            clase_abierta = True
            # Permitir llave en la misma línea o en la siguiente
            if '{' not in stripped:
                siguiente = lineas[idx] if idx < len(lineas) else ""
                if '{' not in siguiente.strip():
                    errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Falta '{{' en declaración de clase")
            continue

        # Verificar if con llaves
        if re.match(r'if\s*\(.*\)\s*$', stripped):
            siguiente = lineas[idx] if idx < len(lineas) else ""
            if not (stripped.endswith("{") or siguiente.strip().startswith("{")):
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Falta '{{' después de if")
            continue

        # Verificar else con llaves
        if re.match(r'else\s*$', stripped):
            siguiente = lineas[idx] if idx < len(lineas) else ""
            if not (stripped.endswith("{") or siguiente.strip().startswith("{")):
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Falta '{{' después de else")
            continue

        # Verificar declaración de variable válida
        # Casos inválidos: "int = 4;", "int;", "float numero = ;"
        match_decl = re.match(rf'^{tipo_regex}\s*([a-zA-Z_][a-zA-Z0-9_]*)?\s*(=\s*[^;]+)?;$', stripped)
        if match_decl:
            tipo = match_decl.group(1)
            nombre = match_decl.group(2)
            valor = match_decl.group(3)
            if nombre is None:
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Declaración de variable sin nombre.")
            elif valor is not None and re.match(r'=\s*$', valor):
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Inicialización de variable incompleta.")
            continue
        # Detectar declaración de tipo sin nombre ni asignación
        if re.match(rf'^{tipo_regex}\s*;$', stripped):
            errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Declaración de variable sin nombre.")
            continue
        # Detectar declaración de tipo con igual pero sin nombre
        if re.match(rf'^{tipo_regex}\s*=\s*[^;]+;$', stripped):
            errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Declaración de variable sin nombre.")
            continue

        # Verificar apertura/cierre de llaves
        for i, c in enumerate(linea):
            if c == '{':
                pila_llaves.append((idx, i))
            elif c == '}':
                if pila_llaves:
                    pila_llaves.pop()
                else:
                    errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Llave de cierre '}}' sin abrir")

        # Verificar apertura/cierre de paréntesis
        for i, c in enumerate(linea):
            if c == '(':
                pila_parentesis.append((idx, i))
            elif c == ')':
                if pila_parentesis:
                    pila_parentesis.pop()
                else:
                    errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Paréntesis de cierre ')' sin abrir")

        # Verificar declaración de método
        if re.match(r'(public|private|protected|static|\s)*\s*\w+\s+\w+\s*\(.*\)\s*', stripped):
            if '{' not in stripped:
                siguiente = lineas[idx] if idx < len(lineas) else ""
                if '{' not in siguiente.strip():
                    errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Falta '{{' en declaración de método")
            continue

        # Verificar punto y coma en sentencias simples (no en llaves, declaraciones de clase/método, ni bloques, ni if/else)
        if (not stripped.endswith(';') and
            not stripped.endswith('{') and
            not stripped.endswith('}') and
            not re.match(r'(public|private|protected)?\s*class\s+\w+', stripped) and
            not re.match(r'(public|private|protected|static|\s)*\s*\w+\s+\w+\s*\(.*\)\s*', stripped) and
            not re.match(r'if\s*\(.*\)\s*$', stripped) and
            not re.match(r'else\s*$', stripped)):
            # Si la línea parece una instrucción (contiene '=' o llamada a método)
            if ('=' in stripped or '(' in stripped or ')' in stripped) and not stripped.startswith("//"):
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Falta punto y coma ';'")
            # Si la línea contiene solo identificadores o palabras no válidas (ejemplo: sdfsfsf)
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', stripped):
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Sentencia no válida o incompleta: '{stripped}'")
            # Si la línea contiene tokens pero no es una sentencia válida
            else:
                errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Sentencia no válida: '{stripped}'")

    # Verificar si quedan llaves o paréntesis sin cerrar
    for idx, _ in pila_llaves:
        errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Llave de apertura '{{' sin cerrar")
    for idx, _ in pila_parentesis:
        errores_lexicos.append(f"Línea {idx}: Error de sintaxis - Paréntesis de apertura '(' sin cerrar")

    # Validar que exista al menos una clase
    if not clase_abierta:
        errores_lexicos.append("Error de estructura: No se encontró ninguna declaración de clase en el código.")

    return errores_lexicos

# --- INTEGRACIÓN DE REGLAS SINTÁCTICAS CON PLY ---

from ply import yacc

# Deben coincidir con los tokens definidos en el lexer principal
tokens = [
    'ID', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'INT', 'DOUBLE', 'FLOAT', 'BOOL', 'STRINGTYPE', 'VOID'
    # ...agrega más tokens según tu lexer...
]

# Reglas de precedencia (si es necesario)
precedence = ()

# Reglas de producción para funciones en C#
def p_function_empty_body(p):
    'function : type ID LPAREN RPAREN LBRACE RBRACE'
    pass

def p_function_with_body(p):
    'function : type ID LPAREN RPAREN LBRACE body RBRACE'
    pass

def p_type(p):
    '''type : INT
            | DOUBLE
            | FLOAT
            | BOOL
            | STRINGTYPE
            | VOID'''
    pass

def p_body(p):
    '''body : statement_list'''
    pass

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    pass

def p_statement(p):
    '''statement : SEMICOLON'''
    pass

def p_error(p):
    if p:
        raise SyntaxError(f"Error de sintaxis en la línea {p.lineno}: token inesperado '{p.value}'")
    else:
        raise SyntaxError("Error de sintaxis: Fin de archivo inesperado")

parser = yacc.yacc()

def analizar_sintaxis_ply(codigo, lexer):
    """
    Analiza la sintaxis usando PLY y retorna una lista de errores sintácticos.
    """
    errores = []
    try:
        parser.parse(codigo, lexer=lexer)
    except SyntaxError as e:
        errores.append(str(e))
    return errores
