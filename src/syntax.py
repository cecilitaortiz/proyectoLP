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


def p_using_list(p):
    '''using_list : using_list using_stmt
                  | empty'''


def p_using_stmt(p):
    '''using_stmt : USING ID SEMICOLON'''


def p_class_list(p):
    '''class_list : class_list class_decl
                  | class_decl'''


def p_class_decl(p):
    '''class_decl : PUBLIC CLASS ID LBRACE member_list RBRACE'''


def p_member_list(p):
    '''member_list : member_list member
                   | empty'''


def p_member(p):
    '''member : method_decl
              | var_decl'''


def p_method_decl(p):
    '''method_decl : PUBLIC type ID LPAREN param_list RPAREN LBRACE stmt_list RBRACE'''


def p_var_decl(p):
    '''var_decl : type ID EQUALS expr SEMICOLON
                | type ID SEMICOLON'''


def p_param_list(p):
    '''param_list : param_list COMMA param
                  | param
                  | empty'''


def p_param(p):
    '''param : type ID'''


def p_type(p):
    '''type : INT
            | FLOAT
            | DOUBLE
            | STRINGTYPE
            | BOOL
            | CHAR
            | VOID
            | VAR'''


def p_type_list(p):
    '''type : LIST LT type GT'''


def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | empty'''


def p_stmt(p):
    '''stmt : var_decl
            | assign_stmt
            | if_stmt
            | return_stmt
            | for_stmt'''


def p_assign_stmt(p):
    '''assign_stmt : ID EQUALS expr SEMICOLON'''


def p_if_stmt(p):
    '''if_stmt : IF LPAREN expr RPAREN LBRACE stmt_list RBRACE else_part'''


def p_else_part(p):
    '''else_part : ELSE LBRACE stmt_list RBRACE
                 | empty'''


def p_return_stmt(p):
    '''return_stmt : RETURN expr SEMICOLON'''


def p_for_stmt(p):
    '''for_stmt : FOR LPAREN assign_stmt expr SEMICOLON assign_stmt RPAREN LBRACE stmt_list RBRACE'''


def p_expr_cast(p):
    '''expr : LPAREN type RPAREN expr'''


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


def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''


def p_expr_not(p):
    '''expr : NOT expr'''


def p_expr_uminus(p):
    '''expr : MINUS expr %prec UMINUS'''


def p_expr_id(p):
    '''expr : ID'''
  

def p_expr_literal(p):
    '''expr : INT
            | FLOAT
            | DOUBLE
            | STRING
            | TRUE
            | FALSE
            | CHAR'''
 

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}: Token inesperado '{p.value}'")
    else:
        print("Error de sintaxis: Fin de entrada inesperado.")

parser = yacc.yacc()

