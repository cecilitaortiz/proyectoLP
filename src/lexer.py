import re
from ply import lex

# ---------------------------
# Definición de tokens y lexer para C#
# ---------------------------

# Solo define los tokens que realmente usas en las reglas del parser
tokens = (
    'ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'LT', 'GT',
    'COMMA', 'MOD', 'NOT', 'DOT',
    'LE', 'GE', 'EQ', 'NE',
    'CONSOLE', 'WRITELINE', 'READLINE',
    'INT', 'DOUBLE', 'FLOAT', 'BOOL', 'STRING', 'CHAR', 'VAR', 'LIST',
    'FOR', 'IF', 'ELSE', 'CLASS', 'PUBLIC', 'RETURN', 'VOID', 'USING', 'TRUE', 'FALSE',
    'AND', 'OR', 'NEW', 'PRIVATE', 'PROTECTED',
    'PLUSPLUS', 'MINUSMINUS', 'PLUSEQUAL', 'MINUSEQUAL',
    'LBRACKET', 'RBRACKET', 'COLON', 'ADD', 'PARSE',
    'INT_CONST', 'FLOAT_CONST', 'STRING_CONST'
)

reserved = {
    'int': 'INT',
    'double': 'DOUBLE',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'string': 'STRING',
    'char': 'CHAR',
    'var': 'VAR',
    'List': 'LIST',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'class': 'CLASS',
    'public': 'PUBLIC',
    'return': 'RETURN',
    'void': 'VOID',
    'using': 'USING',
    'true': 'TRUE',
    'false': 'FALSE',
    'Console': 'CONSOLE',
    'WriteLine': 'WRITELINE',
    'ReadLine': 'READLINE',
    'new': 'NEW',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'Parse': 'PARSE'
}

# No sumes los tokens de reserved, ya están incluidos arriba

t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_ASSIGN      = r'='
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_SEMICOLON   = r';'
t_COMMA       = r','
t_DOT         = r'\.'
t_LT          = r'<'
t_GT          = r'>'
t_MOD         = r'%'
t_NOT         = r'!'
t_LE          = r'<='
t_GE          = r'>='
t_EQ          = r'=='
t_NE          = r'!='
t_AND         = r'&&'
t_OR          = r'\|\|'
t_PLUSPLUS    = r'\+\+'
t_MINUSMINUS  = r'--'
t_PLUSEQUAL   = r'\+='
t_MINUSEQUAL  = r'-='
t_LBRACKET    = r'\['
t_RBRACKET    = r'\]'
t_COLON       = r':'
t_ADD         = r'Add'
t_PARSE       = r'Parse'

def t_STRING_CONST(t):
    r'"([^"\n])*"'
    t.value = t.value[1:-1]
    t.lineno = t.lexer.lineno
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    t.lineno = t.lexer.lineno  # Asegura que todos los tokens, incluidos los reservados, tengan número de línea
    return t

def t_FLOAT_CONST(t):
    r'\d+\.\d+([fF])?'
    t.value = float(t.value[:-1]) if t.value.endswith(('f', 'F')) else float(t.value)
    t.lineno = t.lexer.lineno
    return t

def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    t.lineno = t.lexer.lineno
    return t

def t_ignore_whitespace(t):
    r'[ \t]+'
    pass

def t_newline(t):
    r'(\r\n|\r|\n)+'
    t.lexer.lineno += t.value.count('\n')

def t_COMMENT(t):
    r'//.*'
    pass

def t_multiline_comment(t):
    r'/\*[\s\S]*?\*/'
    pass

def t_ignore_unicode(t):
    r'[^\x00-\x7F]'
    pass

def t_error(t):
    if not re.match(r'\s', t.value[0]):
        print(f"Este caracter no está definido: '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()