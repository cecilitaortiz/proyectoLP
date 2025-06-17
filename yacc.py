import ply.lex as lex

reserved = {"if":"IF",
            "for":"FOR",
            "while":"WHILE",
            "continue":"CONTINUE",
            "in":"IN",
            "fn":"FUNCTION",
            "let":"LET",
            "String":"STRING",
            "Array":"ARRAY"
            }

# List of token names.   This is always required
tokens = (
   'INTEGER',
   'FLOAT',
   'STR',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
    'MODULE',
    'LBRACKET',
    'RBRACKET',
   'LSBRACKET',
   'RSBRACKET',
    'ID',
    'EQUALS',
    'SEMICOLON',
    'COMMA',
    'CONSTANT',
    'COLON',
   'DOT',
    'PRINTLN'
)+tuple(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_MODULE = r'%'
t_LSBRACKET = r'\['
t_RSBRACKET = r'\]'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_COMMA = r','
t_COLON = r':'
t_DOT = r'\.'
#t_PRINTLN = r'println!'
# A regular expression rule with some action code

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STR(t):
    r'"[^"]*"|\'[^"]*\''
    t.value = str(t.value)
    return t

def t_PRINTLN(t):
    r'[a-z_]+!'
    return t

def t_ID(t):
    r'[a-z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_CONSTANT(t):
    r'[A-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'CONSTANT')
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_COMMENTS(t):
    '//.*'
    pass
# Error handling rule
def t_error(t):
    print("Léxico no válido '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
archivo = open("codigo.rs")
data = archivo.read()
archivo.close()
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)