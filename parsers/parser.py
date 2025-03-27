import ply.yacc as yacc
from lexer import tokens
def p_expressao_binaria(p):
    '''expressao : expressao OPERADOR expressao'''
    p[0] = ('op', p[2], p[1], p[3])