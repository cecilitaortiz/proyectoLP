import os
from datetime import datetime

symbol_table = {}

def validar_declaracion_variable(tipo, nombre, valor, valor_tipo=None):
    from semantic import inferir_tipo_expresion
    tipos_validos = ["int", "float", "bool", "string", "char", "var", "double"]
    mensajes = []
    if nombre in symbol_table:
        mensajes.append(f"Error semántico: La variable '{nombre}' ya está declarada. No se permite redeclaración.")
        return mensajes
    if tipo not in tipos_validos:
        mensajes.append(f"Error semántico: Tipo '{tipo}' no válido para variable '{nombre}'. Solo se permiten: {', '.join(tipos_validos)}.")
        return mensajes
    # Validación de tipo para literales, identificadores y expresiones
    if valor is not None:
        tipo_valor = None
        # Si es una expresión compleja, inferir tipo
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
        # Permitir casting implícito de int a float/double
        if tipo == "float" and tipo_valor == "int":
            mensajes.append(f"Casting implícito: Variable '{nombre}' de tipo float inicializada con int. Se convierte automáticamente a float.")
        elif tipo == "double" and tipo_valor == "int":
            mensajes.append(f"Casting implícito: Variable '{nombre}' de tipo double inicializada con int. Se convierte automáticamente a double.")
        elif tipo_valor != tipo:
            mensajes.append(f"Error semántico: No se puede asignar valor de tipo {tipo_valor} a variable {tipo} '{nombre}'.")
            return mensajes
    symbol_table[nombre] = {"tipo": tipo, "valor": valor}
    mensajes.append(f"Variable declarada correctamente: {tipo} {nombre} = {valor}")
    return mensajes

def inferir_tipo_expresion(expr):
    """
    Dado un nodo de expresión del parser, retorna el tipo inferido ('int', 'float', 'bool', 'string', 'char', 'double') o un mensaje de error.
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
        # Operaciones binarias
        if op in ['+', '-', '*', '/']:
            tipo_izq = inferir_tipo_expresion(expr[1])
            tipo_der = inferir_tipo_expresion(expr[2])
            if tipo_izq == tipo_der:
                return tipo_izq
            # Permitir int + float = float, int + double = double, float + double = double
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
        if op == 'neg':
            tipo = inferir_tipo_expresion(expr[1])
            if tipo in ['int', 'float', 'double']:
                return tipo
            return f"Error: Operador unario '-' requiere tipo numérico, se recibió {tipo}"
        if op == 'func_call':
            # No implementado: se asume que la función retorna int (puedes mejorar esto)
            return 'int'
        if op == 'list_access':
            # No implementado: se asume int
            return 'int'
        if op == 'parse':
            # int.Parse(Console.ReadLine())
            return expr[1]
        if op == 'readline':
            return 'string'
    # Si es un identificador
    if isinstance(expr, str) and expr in symbol_table:
        return symbol_table[expr]['tipo']
    return f"Error: No se puede inferir el tipo de la expresión {expr}"

