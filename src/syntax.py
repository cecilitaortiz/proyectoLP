import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT'),
    ('right', 'UMINUS'),
)

def p_program(p):
    '''program : using_list class_list'''
    p[0] = ("program", p[1], p[2])

def p_using_list(p):
    '''using_list : using_list using_stmt
                  | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_using_stmt(p):
    '''using_stmt : USING ID SEMICOLON'''
    p[0] = ("using", p[2])

def p_class_list(p):
    '''class_list : class_list class_decl
                  | class_decl'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_class_decl(p):
    '''class_decl : PUBLIC CLASS ID LBRACE member_list RBRACE'''
    p[0] = ("class", p[3], p[5])

def p_member_list(p):
    '''member_list : member_list member
                   | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_member(p):
    '''member : method_decl
              | var_decl'''
    p[0] = p[1]

def p_method_decl(p):
    '''method_decl : PUBLIC type ID LPAREN param_list RPAREN LBRACE stmt_list RBRACE'''
    p[0] = ("method", p[3], p[2], p[5], p[8])

def p_var_decl(p):
    '''var_decl : type ID EQUALS expr SEMICOLON
                | type ID SEMICOLON'''
    if len(p) == 6:
        p[0] = ("var_decl", p[1], p[2], p[4])
    else:
        p[0] = ("var_decl", p[1], p[2], None)

def p_param_list(p):
    '''param_list : param_list COMMA param
                  | param
                  | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_param(p):
    '''param : type ID'''
    p[0] = ("param", p[1], p[2])

def p_type(p):
    '''type : INT
            | FLOAT
            | DOUBLE
            | STRINGTYPE
            | BOOL
            | CHAR
            | VOID
            | VAR'''
    p[0] = p[1]

def p_type_list(p):
    '''type : LIST LT type GT'''
    p[0] = ("list", p[3])

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_stmt(p):
    '''stmt : var_decl
            | assign_stmt
            | if_stmt
            | return_stmt
            | for_stmt'''
    p[0] = p[1]

def p_assign_stmt(p):
    '''assign_stmt : ID EQUALS expr SEMICOLON'''
    p[0] = ("assign", p[1], p[3])

def p_if_stmt(p):
    '''if_stmt : IF LPAREN expr RPAREN LBRACE stmt_list RBRACE else_part'''
    p[0] = ("if", p[3], p[6], p[8])

def p_else_part(p):
    '''else_part : ELSE LBRACE stmt_list RBRACE
                 | empty'''
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = []

def p_return_stmt(p):
    '''return_stmt : RETURN expr SEMICOLON'''
    p[0] = ("return", p[2])

def p_for_stmt(p):
    '''for_stmt : FOR LPAREN assign_stmt expr SEMICOLON assign_stmt RPAREN LBRACE stmt_list RBRACE'''
    p[0] = ("for", p[3], p[4], p[6], p[9])

def p_expr_cast(p):
    '''expr : LPAREN type RPAREN expr'''
    p[0] = ("cast", p[2], p[4])

def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr MOD expr
            | expr EQ expr
            | expr NE expr
            | expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr AND expr
            | expr OR expr'''
    p[0] = ("binop", p[2], p[1], p[3])

def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_expr_not(p):
    '''expr : NOT expr'''
    p[0] = ("not", p[2])

def p_expr_uminus(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = ("uminus", p[2])

def p_expr_id(p):
    '''expr : ID'''
    p[0] = ("var", p[1])

def p_expr_literal(p):
    '''expr : INT
            | FLOAT
            | DOUBLE
            | STRING
            | TRUE
            | FALSE
            | CHAR'''
    p[0] = ("const", p[1])

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}: Token inesperado '{p.value}'")
    else:
        print("Error de sintaxis: Fin de entrada inesperado.")

parser = yacc.yacc()

