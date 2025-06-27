# Tabla de símbolos
symbol_table = {}

def validar_declaracion_variable(tipo, nombre, valor):
    # Ejemplo simple: solo verifica si el nombre ya existe y si el tipo es válido
    if nombre in symbol_table:
        print(f"Error semántico: La variable '{nombre}' ya está declarada.")
        return False
    if tipo not in ['int', 'float', 'bool', 'string', 'char', 'var']:
        print(f"Error semántico: Tipo '{tipo}' no válido para variable '{nombre}'.")
        return False
    # Puedes agregar más validaciones de tipo aquí
    symbol_table[nombre] = {'tipo': tipo, 'valor': valor}
    print(f"Variable declarada correctamente: {tipo} {nombre} = {valor}")
    return True

def validar_declaracion_funcion(modificadores, tipo_retorno, nombre, parametros):
    # Ejemplo simple: verifica si la función ya existe
    if nombre in symbol_table:
        print(f"Error semántico: La función '{nombre}' ya está declarada.")
        return False
    # Puedes agregar más validaciones de tipo y parámetros aquí
    symbol_table[nombre] = {
        'tipo': 'funcion',
        'modificadores': modificadores,
        'tipo_retorno': tipo_retorno,
        'parametros': parametros
    }
    print(f"Función declarada correctamente: {' '.join(modificadores)} {tipo_retorno} {nombre}({parametros})")
    return True