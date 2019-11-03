# -*- coding: UTF-8 -*-

import ply.yacc as yacc
from exceptions_errors import sintaxe_erro, sinal_desconhecido
from Variavel import Variavel
from Declaracao import Declaracao
from Bloco import Bloco
# from mylexer import tokens


precedence = (
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'AND', 'OR'),
    ('left', 'MAIOR', 'MENOR', 'MAIOREQUALS', 'MENOREQUALS', 'EQUALS', 'DIFF'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'NOT', 'TERNARY'),
)


def p_binary_operators(p):
    '''expression : expression PLUS term
                   | expression MINUS term
        term       : term TIMES factor
                   | term DIVIDE factor'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    else:
        sinal_desconhecido(p)


def p_expression_logop(p):
    '''expression : expression MAIOR expression
                  | expression MENOR expression
                  | expression MAIOREQUALS expression
                  | expression MENOREQUALS expression
                  | expression EQUALS expression
                  | expression DIFF expression
                  | expression AND expression
                  | expression OR expression'''
    if p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == 'and':
        p[0] = p[1] and p[3]
    elif p[2] == 'or':
        p[0] = p[1] or p[3]
    else:
        sinal_desconhecido(p)


def p_var_especification(p):
    '''var_Especification   : NAME LCOLC NUMBER RCOLC
                            | NAME ASSIGN expression
                            | NAME
                            | NAME LCOLC NUMBER RCOLC ASSIGN LBRACE sequence_literal RBRACE'''
    if len(p) == 2:
        p[0] = Variavel(p[1], None)
    elif len(p) == 4:
        p[0] = Variavel(p[1], p[3])


def p_expression_not(p):
    'expression : EXPLAMATION expression %prec NOT'
    p[0] = not p[2]


def p_expression(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_sequence_expression(p):
    '''sequence_expression : expression COMMA sequence_expression
                            | expression'''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        [p[1]]


def p_assign(p):
    '''assignment :   variavel ASSIGN expression
                  |   variavel MOD expression
                  |   variavel SUMEQUALS expression
                  |   variavel MINUSEQUALS expression
                  |   variavel TIMESEQUALS expression
                  |   variavel DIVIDEEQUALS expression
    '''

    # if p[2] == '=':
    #     p[0] = Variavel(p[1], p[3])
    # elif p[2] == '%=':
    #     (p[1], var_global.show(p[1]) /p[3])
    # elif p[2] == '+=':
    #     var_global.change(p[1], var_global.show(p[1]) +p[3])
    # elif p[2] == '-=':
    #     var_global.change(p[1], var_global.show(p[1])-p[3])
    # elif p[2] == '*=':
    #     var_global.change(p[1], var_global.show(p[1]) *p[3])
    # elif p[2] == '/=':
    #     var_global.change(p[1], var_global.show(p[1])/p[3])
    # else:
    #     errors.unknownSignal(t)
    # p[0]=var_global.show(p[1])


# Build the parser
parser = yacc.yacc()


while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
