import ply.yacc as yacc
from lexer import tokens

# Precedencia para expresiones simples
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Regla inicial: lista de declaraciones

def p_program(p):
    '''program : declarations'''
    p[0] = p[1]

# Lista de declaraciones

def p_declarations_multiple(p):
    '''declarations : declarations declaration'''
    p[0] = p[1] + [p[2]]

def p_declarations_single(p):
    '''declarations : declaration'''
    p[0] = [p[1]]

def p_declarations_empty(p):
    '''declarations : '''
    p[0] = []

# Declaración de variable (con o sin inicialización)

def _msg(p, regla):
    # Busca el primer elemento que sea un objeto token (PLY usa objetos LexToken)
    lineno = None
    for i in range(1, len(p)):
        try:
            lineno = p.lineno(i)
            if lineno and lineno > 0:
                break
        except Exception:
            continue
    if not lineno:
        lineno = getattr(p.slice[1], 'lineno', 0) if len(p.slice) > 1 else 0
    print(f"Línea {lineno}: {regla}")

def p_declaration_init(p):
    '''declaration : type ID ASSIGN expression SEMICOLON'''
    _msg(p, f"declaracion_variable : {p[1]} {p[2]} = {p[4]}")
    p[0] = ('decl_var_init', p[1], p[2], p[4])

def p_declaration_noinit(p):
    '''declaration : type ID SEMICOLON'''
    _msg(p, f"declaracion_variable : {p[1]} {p[2]}")
    p[0] = ('decl_var', p[1], p[2])

# Reglas para impresión por pantalla (Console.WriteLine)

def p_declaration_print(p):
    '''declaration : CONSOLE DOT WRITELINE LPAREN expression RPAREN SEMICOLON'''
    _msg(p, f"impresion : Console.WriteLine({p[5]})")
    p[0] = ('print', p[5])

# Estructura if-else y else if

def p_declaration_if_else(p):
    '''declaration : IF LPAREN expression RPAREN LBRACE declarations RBRACE else_part'''
    _msg(p, f"if : if ({p[3]}) {{ ... }} {p[7]}")
    p[0] = ('if_else', p[3], p[6], p[8])

def p_else_part_else(p):
    '''else_part : ELSE LBRACE declarations RBRACE'''
    _msg(p, f"else : else {{ ... }}")
    p[0] = ('else', p[3])

def p_else_part_elseif(p):
    '''else_part : ELSE IF LPAREN expression RPAREN LBRACE declarations RBRACE else_part'''
    _msg(p, f"else if : else if ({p[4]}) {{ ... }} {p[8]}")
    p[0] = ('elseif', p[4], p[7], p[9])

def p_else_part_empty(p):
    '''else_part : '''
    p[0] = None

# Tipos soportados

def p_type(p):
    '''type : INT
           | FLOAT
           | BOOL
           | STRINGTYPE'''
    p[0] = p[1]

# Expresiones simples

def p_expression_binop(p):
    '''expression : expression PLUS expression
                 | expression MINUS expression
                 | expression TIMES expression
                 | expression DIVIDE expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_relop(p):
    '''expression : expression GT expression
                 | expression LT expression
                 | expression GE expression
                 | expression LE expression
                 | expression EQ expression
                 | expression NE expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : INT_CONST
                 | FLOAT_CONST'''
    p[0] = p[1]

def p_expression_bool(p):
    '''expression : TRUE
                 | FALSE'''
    p[0] = p[1]

def p_expression_string(p):
    '''expression : STRING_CONST'''
    p[0] = p[1]

def p_expression_id(p):
    '''expression : ID'''
    p[0] = p[1]

# Manejo de errores

def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}: token '{p.value}'")
    else:
        print("Error de sintaxis al final del archivo")


# Construir el parser
parser = yacc.yacc()
