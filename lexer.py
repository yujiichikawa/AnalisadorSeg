import ply.lex as lex

# Definição dos tokens
tokens = [
    'PALAVRA_RESERVADA',
    'IDENTIFICADOR',
    'NUMERO',
    'OPERADOR'
]

# Regras para os tokens
t_PALAVRA_RESERVADA = r'if|else|while|for|return'
t_IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMERO = r'\d+'
t_OPERADOR = r'[+\-*/=]'


t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()