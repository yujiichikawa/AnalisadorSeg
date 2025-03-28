import ply.lex as lex
import ply.yacc as yacc
import ast

# Definição dos tokens
tokens = ('ID', 'NUMBER', 'EQUALS', 'STRING')

t_literais = "=;"

def t_ID(t):
    r'[a-zA-Z_]\w*'
    return t

def t_NUMBER(t):
    r'\d+'
    return t

def t_STRING(t):
    r'".*?"'
    return t

t_ignore = ' \t\n'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

def p_statement_assign(p):
    'statement : ID EQUALS expression'
    p[0] = ('assign', p[1], p[3])

def p_expression(p):
    '''expression : ID
                  | NUMBER
                  | STRING'''
    p[0] = p[1]

parser = yacc.yacc()