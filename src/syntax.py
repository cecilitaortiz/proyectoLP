import ply.yacc as yacc
from lexer import tokens

def p_start(p):
    '''start : var_decls'''
    print("Regla: start -> var_decls")

def p_var_decls(p):
    '''var_decls : var_decls var_decl
                 | var_decl'''
    # Permite varias declaraciones de variables seguidas

def p_type(p):
    '''type : INT
            | DOUBLE
            | FLOAT
            | BOOL
            | STRINGTYPE
            | CHAR
            | VAR
            | LIST'''
    print(f"Reconocido tipo: {p[1]}")
    p[0] = p[1]

def p_expr_int(p):
    'expr : INT'
    print(f"Reconocido expr: {p[1]}")
    p[0] = p[1]

def p_expr_float(p):
    'expr : FLOAT'
    print(f"Reconocido expr: {p[1]}")
    p[0] = p[1]

def p_expr_double(p):
    'expr : DOUBLE'
    print(f"Reconocido expr: {p[1]}")
    p[0] = p[1]

def p_expr_string(p):
    'expr : STRING'
    print(f"Reconocido expr: {p[1]}")
    p[0] = p[1]

def p_expr_char(p):
    'expr : CHAR'
    print(f"Reconocido expr: {p[1]}")
    p[0] = p[1]

def p_expr_true(p):
    'expr : TRUE'
    print(f"Reconocido expr: {p[1]}")
    p[0] = p[1]

def p_expr_false(p):
    'expr : FALSE'
    print(f"Reconocido expr: {p[1]}")
    p[0] = p[1]

def p_expr_id(p):
    'expr : ID'
    print(f"Reconocido expr: {p[1]}")
    p[0] = p[1]

def p_var_decl(p):
    '''var_decl : type ID EQUALS expr SEMICOLON
                | type ID SEMICOLON'''
    if len(p) == 6:
        print(f"Regla: var_decl -> {p[1]} {p[2]} = {p[4]};")
    else:
        print(f"Regla: var_decl -> {p[1]} {p[2]};")

def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}: Token inesperado '{p.value}'")
    else:
        print("Error de sintaxis: Fin de entrada inesperado.")

parser = yacc.yacc(start='start')