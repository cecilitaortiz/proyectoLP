from semantic import validar_declaracion_variable, validar_uso_variable, validar_declaracion_funcion, validar_retorno_funcion

# Ejemplo 1: Declaración de variable correcta
validar_declaracion_variable('int', 'x', 5)

# Ejemplo 2: Declaración de variable con tipo incorrecto
validar_declaracion_variable('int', 'y', "hola")

# Ejemplo 3: Uso de variable no declarada
validar_uso_variable('z')

# Ejemplo 4: Declaración de función y retorno correcto
validar_declaracion_funcion(['public'], 'int', 'Sumar', [('int', 'a'), ('int', 'b')])
validar_retorno_funcion('Sumar', 10)

# Ejemplo 5: Retorno incorrecto en función
validar_retorno_funcion('Sumar', "hola")
