
# ---------------------------------------------
# semantic.py
# Módulo de análisis semántico para el analizador de C#
# Aquí valido tipos, declaraciones, asignaciones y listas.
# ---------------------------------------------

# Tabla de símbolos global para almacenar información de variables declaradas
symbol_table = {}

# Esta función valida la declaración de una variable, su tipo y valor inicial.
# Permite tipos simples y listas (List<T>), impide la redeclaración,
# valida el tipo y almacena la variable en la tabla de símbolos si es válida.
# Devuelve mensajes de éxito o error.
def validar_declaracion_variable(tipo, nombre, valor, valor_tipo=None):
    """
    Valida la declaración de una variable, su tipo y valor inicial.
    - Permite tipos simples y listas (List<T>).
    - Impide la redeclaración de variables.
    - Valida que el tipo de la variable sea permitido.
    - Si hay valor inicial, valida que el tipo del valor coincida o sea compatible (casting implícito).
    - Para listas, valida que no sean listas de listas y que el tipo de los elementos sea válido.
    - Almacena la variable en la tabla de símbolos si es válida.
    - Devuelve mensajes de éxito o error.
    """
    tipos_validos = ["int", "float", "bool", "string", "char", "var", "double"]
    mensajes = []
    # Detecta si el tipo es una lista (por ejemplo, ('list_type', 'int'))
    es_lista = False
    tipo_lista_str = None
    if isinstance(tipo, tuple) and tipo[0] == 'list_type':
        es_lista = True
        tipo_interno = tipo[1]
        # No se permiten listas de listas
        if isinstance(tipo_interno, tuple) and tipo_interno[0] == 'list_type':
            mensajes.append(f"Error semántico: No se permiten listas de listas para la variable '{nombre}'.")
            return mensajes
        if tipo_interno not in tipos_validos:
            mensajes.append(f"Error semántico: Tipo de elemento '{tipo_interno}' no válido en la lista para variable '{nombre}'.")
            return mensajes
        tipo_lista_str = f"list<{tipo_interno}>"
    # Impide redeclaración
    if nombre in symbol_table:
        mensajes.append(f"Error semántico: La variable '{nombre}' ya está declarada. No se permite redeclaración.")
        return mensajes
    # Valida tipo permitido
    if not es_lista and tipo not in tipos_validos:
        mensajes.append(f"Error semántico: Tipo '{tipo}' no válido para variable '{nombre}'. Solo se permiten: {', '.join(tipos_validos)}.")
        return mensajes
    # Validación de tipo para literales, identificadores y expresiones
    if valor is not None:
        tipo_valor = None
        # Si es una expresión compleja, infiere el tipo
        if valor_tipo is None or valor_tipo == 'EXPR':
            tipo_valor = inferir_tipo_expresion(valor)
        elif valor_tipo == "ID":
            if valor not in symbol_table:
                mensajes.append(f"Error semántico: La variable '{valor}' usada en la inicialización de '{nombre}' no está declarada.")
                return mensajes
            tipo_valor = symbol_table[valor]["tipo"]
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
        # Validación para listas
        if es_lista:
            # Permite solo asignación de listas del mismo tipo
            if isinstance(tipo_valor, str) and tipo_valor.startswith("list<"):
                if tipo_valor != tipo_lista_str:
                    mensajes.append(f"Error semántico: No se puede asignar valor de tipo {tipo_valor} a variable {tipo_lista_str} '{nombre}'.")
                    return mensajes
            elif tipo_valor != tipo_interno:
                mensajes.append(f"Error semántico: No se puede asignar valor de tipo {tipo_valor} a variable {tipo_lista_str} '{nombre}'. Solo se permiten listas del tipo correcto.")
                return mensajes
        else:
            # Permite casting implícito de int a float/double
            if tipo == "float" and tipo_valor == "int":
                mensajes.append(f"Casting implícito: Variable '{nombre}' de tipo float inicializada con int. Se convierte automáticamente a float.")
            elif tipo == "double" and tipo_valor == "int":
                mensajes.append(f"Casting implícito: Variable '{nombre}' de tipo double inicializada con int. Se convierte automáticamente a double.")
            elif tipo_valor != tipo:
                mensajes.append(f"Error semántico: No se puede asignar valor de tipo {tipo_valor} a variable {tipo} '{nombre}'.")
                return mensajes
    # Guarda la variable en la tabla de símbolos
    if es_lista:
        symbol_table[nombre] = {"tipo": tipo_lista_str, "valor": valor}
        mensajes.append(f"Variable declarada correctamente: {tipo_lista_str} {nombre} = {valor}")
    else:
        symbol_table[nombre] = {"tipo": tipo, "valor": valor}
        mensajes.append(f"Variable declarada correctamente: {tipo} {nombre} = {valor}")
    return mensajes

# Esta función infiere el tipo de una expresión (nodo del AST).
# Soporta literales, identificadores, operaciones aritméticas, lógicas y relacionales.
# Para operaciones, valida compatibilidad de tipos y retorna el tipo resultante.
# Para llamadas a función y acceso a listas, retorna un tipo por defecto (mejorable).
# Si no puede inferir el tipo, retorna un mensaje de error.
def inferir_tipo_expresion(expr):
    """
    Dada una expresión (nodo del AST), infiere y retorna su tipo:
    - Soporta literales, identificadores, operaciones aritméticas, lógicas y relacionales.
    - Para operaciones, valida compatibilidad de tipos y retorna el tipo resultante.
    - Para llamadas a función y acceso a listas, retorna un tipo por defecto (mejorable).
    - Si no puede inferir el tipo, retorna un mensaje de error.
    """
    if isinstance(expr, int):
        return 'int'
    if isinstance(expr, float):
        return 'float'
    if isinstance(expr, str):
        return 'string'
    if isinstance(expr, bool):
        return 'bool'
    if isinstance(expr, tuple):
        op = expr[0]
        # Operaciones binarias aritméticas
        if op in ['+', '-', '*', '/']:
            tipo_izq = inferir_tipo_expresion(expr[1])
            tipo_der = inferir_tipo_expresion(expr[2])
            if tipo_izq == tipo_der:
                return tipo_izq
            # Permite int + float = float, int + double = double, float + double = double
            if 'double' in (tipo_izq, tipo_der):
                if tipo_izq in ['int', 'float', 'double'] and tipo_der in ['int', 'float', 'double']:
                    return 'double'
            if 'float' in (tipo_izq, tipo_der):
                if tipo_izq in ['int', 'float'] and tipo_der in ['int', 'float']:
                    return 'float'
            return f"Error: Operación entre tipos incompatibles: {tipo_izq} y {tipo_der}"
        # Operadores lógicos
        if op in ['and', 'or']:
            tipo_izq = inferir_tipo_expresion(expr[1])
            tipo_der = inferir_tipo_expresion(expr[2])
            if tipo_izq == tipo_der == 'bool':
                return 'bool'
            return f"Error: Operador lógico requiere booleanos, se recibió {tipo_izq} y {tipo_der}"
        # Operador not
        if op == 'not':
            tipo = inferir_tipo_expresion(expr[1])
            if tipo == 'bool':
                return 'bool'
            return f"Error: Operador 'not' requiere booleano, se recibió {tipo}"
        # Operadores relacionales
        if op in ['>', '<', '>=', '<=', '==', '!=']:
            tipo_izq = inferir_tipo_expresion(expr[1])
            tipo_der = inferir_tipo_expresion(expr[2])
            if tipo_izq == tipo_der or (tipo_izq in ['int', 'float', 'double'] and tipo_der in ['int', 'float', 'double']):
                return 'bool'
            return f"Error: Comparación entre tipos incompatibles: {tipo_izq} y {tipo_der}"
        # Operador unario negativo
        if op == 'neg':
            tipo = inferir_tipo_expresion(expr[1])
            if tipo in ['int', 'float', 'double']:
                return tipo
            return f"Error: Operador unario '-' requiere tipo numérico, se recibió {tipo}"
        # Llamada a función (por defecto retorna int, mejorable)
        if op == 'func_call':
            return 'int'
        # Acceso a lista (por defecto retorna int, mejorable)
        if op == 'list_access':
            return 'int'
        # Parseo de tipo (ej: int.Parse)
        if op == 'parse':
            return expr[1]
        # Lectura de consola
        if op == 'readline':
            return 'string'
    # Si es un identificador declarado, retorna su tipo
    if isinstance(expr, str) and expr in symbol_table:
        return symbol_table[expr]['tipo']
    return f"Error: No se puede inferir el tipo de la expresión {expr}"

# Tabla de símbolos global para almacenar información de variables declaradas
symbol_table = {}

def validar_declaracion_variable(tipo, nombre, valor, valor_tipo=None):
    """
    Valida la declaración de una variable, su tipo y valor inicial.
    - Permite tipos simples y listas (List<T>).
    - Impide la redeclaración de variables.
    - Valida que el tipo de la variable sea permitido.
    - Si hay valor inicial, valida que el tipo del valor coincida o sea compatible (casting implícito).
    - Para listas, valida que no sean listas de listas y que el tipo de los elementos sea válido.
    - Almacena la variable en la tabla de símbolos si es válida.
    - Devuelve mensajes de éxito o error.
    """
    tipos_validos = ["int", "float", "bool", "string", "char", "var", "double"]
    mensajes = []
    # Detecta si el tipo es una lista (por ejemplo, ('list_type', 'int'))
    es_lista = False
    tipo_lista_str = None
    if isinstance(tipo, tuple) and tipo[0] == 'list_type':
        es_lista = True
        tipo_interno = tipo[1]
        # No se permiten listas de listas
        if isinstance(tipo_interno, tuple) and tipo_interno[0] == 'list_type':
            mensajes.append(f"Error semántico: No se permiten listas de listas para la variable '{nombre}'.")
            return mensajes
        if tipo_interno not in tipos_validos:
            mensajes.append(f"Error semántico: Tipo de elemento '{tipo_interno}' no válido en la lista para variable '{nombre}'.")
            return mensajes
        tipo_lista_str = f"list<{tipo_interno}>"
    # Impide redeclaración
    if nombre in symbol_table:
        mensajes.append(f"Error semántico: La variable '{nombre}' ya está declarada. No se permite redeclaración.")
        return mensajes
    # Valida tipo permitido
    if not es_lista and tipo not in tipos_validos:
        mensajes.append(f"Error semántico: Tipo '{tipo}' no válido para variable '{nombre}'. Solo se permiten: {', '.join(tipos_validos)}.")
        return mensajes
    # Validación de tipo para literales, identificadores y expresiones
    if valor is not None:
        tipo_valor = None
        # Si es una expresión compleja, infiere el tipo
        if valor_tipo is None or valor_tipo == 'EXPR':
            tipo_valor = inferir_tipo_expresion(valor)
        elif valor_tipo == "ID":
            if valor not in symbol_table:
                mensajes.append(f"Error semántico: La variable '{valor}' usada en la inicialización de '{nombre}' no está declarada.")
                return mensajes
            tipo_valor = symbol_table[valor]["tipo"]
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
        # Validación para listas
        if es_lista:
            # Permite solo asignación de listas del mismo tipo
            if isinstance(tipo_valor, str) and tipo_valor.startswith("list<"):
                if tipo_valor != tipo_lista_str:
                    mensajes.append(f"Error semántico: No se puede asignar valor de tipo {tipo_valor} a variable {tipo_lista_str} '{nombre}'.")
                    return mensajes
            elif tipo_valor != tipo_interno:
                mensajes.append(f"Error semántico: No se puede asignar valor de tipo {tipo_valor} a variable {tipo_lista_str} '{nombre}'. Solo se permiten listas del tipo correcto.")
                return mensajes
        else:
            # Permite casting implícito de int a float/double
            if tipo == "float" and tipo_valor == "int":
                mensajes.append(f"Casting implícito: Variable '{nombre}' de tipo float inicializada con int. Se convierte automáticamente a float.")
            elif tipo == "double" and tipo_valor == "int":
                mensajes.append(f"Casting implícito: Variable '{nombre}' de tipo double inicializada con int. Se convierte automáticamente a double.")
            elif tipo_valor != tipo:
                mensajes.append(f"Error semántico: No se puede asignar valor de tipo {tipo_valor} a variable {tipo} '{nombre}'.")
                return mensajes
    # Guarda la variable en la tabla de símbolos
    if es_lista:
        symbol_table[nombre] = {"tipo": tipo_lista_str, "valor": valor}
        mensajes.append(f"Variable declarada correctamente: {tipo_lista_str} {nombre} = {valor}")
    else:
        symbol_table[nombre] = {"tipo": tipo, "valor": valor}
        mensajes.append(f"Variable declarada correctamente: {tipo} {nombre} = {valor}")
    return mensajes


    """
    Dada una expresión (nodo del AST), infiere y retorna su tipo:
    - Soporta literales, identificadores, operaciones aritméticas, lógicas y relacionales.
    - Para operaciones, valida compatibilidad de tipos y retorna el tipo resultante.
    - Para llamadas a función y acceso a listas, retorna un tipo por defecto (mejorable).
    - Si no puede inferir el tipo, retorna un mensaje de error.
    """
    if isinstance(expr, int):
        return 'int'
    if isinstance(expr, float):
        return 'float'
    if isinstance(expr, str):
        return 'string'
    if isinstance(expr, bool):
        return 'bool'
    if isinstance(expr, tuple):
        op = expr[0]
        # Operaciones binarias aritméticas
        if op in ['+', '-', '*', '/']:
            tipo_izq = inferir_tipo_expresion(expr[1])
            tipo_der = inferir_tipo_expresion(expr[2])
            if tipo_izq == tipo_der:
                return tipo_izq
            # Permite int + float = float, int + double = double, float + double = double
            if 'double' in (tipo_izq, tipo_der):
                if tipo_izq in ['int', 'float', 'double'] and tipo_der in ['int', 'float', 'double']:
                    return 'double'
            if 'float' in (tipo_izq, tipo_der):
                if tipo_izq in ['int', 'float'] and tipo_der in ['int', 'float']:
                    return 'float'
            return f"Error: Operación entre tipos incompatibles: {tipo_izq} y {tipo_der}"
        # Operadores lógicos
        if op in ['and', 'or']:
            tipo_izq = inferir_tipo_expresion(expr[1])
            tipo_der = inferir_tipo_expresion(expr[2])
            if tipo_izq == tipo_der == 'bool':
                return 'bool'
            return f"Error: Operador lógico requiere booleanos, se recibió {tipo_izq} y {tipo_der}"
        # Operador not
        if op == 'not':
            tipo = inferir_tipo_expresion(expr[1])
            if tipo == 'bool':
                return 'bool'
            return f"Error: Operador 'not' requiere booleano, se recibió {tipo}"
        # Operadores relacionales
        if op in ['>', '<', '>=', '<=', '==', '!=']:
            tipo_izq = inferir_tipo_expresion(expr[1])
            tipo_der = inferir_tipo_expresion(expr[2])
            if tipo_izq == tipo_der or (tipo_izq in ['int', 'float', 'double'] and tipo_der in ['int', 'float', 'double']):
                return 'bool'
            return f"Error: Comparación entre tipos incompatibles: {tipo_izq} y {tipo_der}"
        # Operador unario negativo
        if op == 'neg':
            tipo = inferir_tipo_expresion(expr[1])
            if tipo in ['int', 'float', 'double']:
                return tipo
            return f"Error: Operador unario '-' requiere tipo numérico, se recibió {tipo}"
        # Llamada a función (por defecto retorna int, mejorable)
        if op == 'func_call':
            return 'int'
        # Acceso a lista (por defecto retorna int, mejorable)
        if op == 'list_access':
            return 'int'
        # Parseo de tipo (ej: int.Parse)
        if op == 'parse':
            return expr[1]
        # Lectura de consola
        if op == 'readline':
            return 'string'
    # Si es un identificador declarado, retorna su tipo
    if isinstance(expr, str) and expr in symbol_table:
        return symbol_table[expr]['tipo']
    return f"Error: No se puede inferir el tipo de la expresión {expr}"

