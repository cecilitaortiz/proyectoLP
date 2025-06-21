import re
from ply import lex

# ---------------------------
# Definición de tokens y lexer para C#
# ---------------------------

tokens = (
    'ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'STRING', 'LT', 'GT',
    'INCREMENT', 'DECREMENT', 'AND', 'OR', 'ARROW', 'LBRACKET', 'RBRACKET', 'DOT',
    'COMMA', 'COLON', 'QUESTION', 'AMPERSAND', 'PIPE', 'MOD', 'NOT', 'QUOTE', 'APOSTROPHE', 'COMMENT',
    'LE', 'GE', 'EQ', 'NE',  # <=, >=, ==, !=
    'PLUSEQ', 'MINUSEQ', 'TIMESEQ', 'DIVEQ', 'MODEQ',  # +=, -=, *=, /=, %=
)

reserved = {
    'int': 'INT',
    'double': 'DOUBLE',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'string': 'STRINGTYPE',
    'char': 'CHAR',
    'var': 'VAR',
    'List': 'LIST',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'class': 'CLASS',
    'public': 'PUBLIC',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'static': 'STATIC',
    'new': 'NEW',
    'this': 'THIS',
    'return': 'RETURN',
    'void': 'VOID',
    'using': 'USING',
     'switch': 'SWITCH',           # No usado
     'case': 'CASE',               # No usado
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'do': 'DO',
    'while': 'WHILE',
    'try': 'TRY',                 # No usado
     'catch': 'CATCH',             # No usado
    'finally': 'FINALLY',         # No usado
    'throw': 'THROW',             # No usado
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
     'enum': 'ENUM',               # No usado
     'const': 'CONST',             # No usado
     'readonly': 'READONLY',       # No usado
     'interface': 'INTERFACE',     # No usado
     'override': 'OVERRIDE',       # No usado
     'abstract': 'ABSTRACT',       # No usado
     'virtual': 'VIRTUAL',         # No usado
     'base': 'BASE',               # No usado
     'object': 'OBJECT',           # No usado

     'foreach': 'FOREACH',         # No usado
     'out': 'OUT',                 # No usado
     'ref': 'REF',                 # No usado
     'params': 'PARAMS',           # No usado
     'get': 'GET',                 # No usado
     'set': 'SET',                 # No usado
     'operator': 'OPERATOR',       # No usado
     'event': 'EVENT',             # No usado
    # 'sizeof': 'SIZEOF',           # No usado
    # 'typeof': 'TYPEOF',           # No usado
     'add': 'ADD',                 # No usado
    'remove': 'REMOVE'            # No usado
}

tokens += tuple(reserved.values())

# Expresiones regulares para los tokens (orden: primero los de mayor longitud)
t_INCREMENT   = r'\+\+'
t_DECREMENT   = r'--'
t_AND         = r'&&'
t_OR          = r'\|\|'
t_ARROW       = r'->'
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_EQUALS      = r'='
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_LBRACKET    = r'\['
t_RBRACKET    = r'\]'
t_SEMICOLON   = r';'
t_COMMA       = r','
t_COLON       = r':'
t_QUESTION    = r'\?'
t_AMPERSAND   = r'&'
t_PIPE        = r'\|'
t_DOT         = r'\.'
t_LT          = r'<'
t_GT          = r'>'
t_MOD         = r'%'
t_NOT         = r'!'
t_QUOTE       = r'"'
t_APOSTROPHE  = r"'"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
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
        print(f"Error de análisis en la línea {t.lineno}: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()