# -*- coding: UTF-8 -*-

import ply.yacc as yacc
from exceptions_errors import sintaxe_erro, sinal_desconhecido
from Variavel import Variavel
from Declaracao import Declaracao
from Bloco import Bloco
from analisador_lexico import AnaliserLexer


precedence = (
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'AND', 'OR'),
    ('left', 'MAIOR', 'MENOR', 'MAIOREQUALS', 'MENOREQUALS', 'EQUALS', 'DIFF'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'IF', 'ELSE'),
    ('right', 'NOT'),
)


# Definição
def p_pass(p):
    'empty : PASS'


def p_literal(t):
    '''literal : NUMBER
               | TRUE
               | FALSE
               | NORMALSTRING
    '''
    t[0] = t[1]


def p_sequence_literal(t):
    '''sequence_literal : literal COMMA sequence_literal
                        | literal'''


def p_variavel(t):
    '''variavel : NAME
                | NAME LCOLC expression RCOLC'''
    t[0] = t[1]


def p_binary_operators(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
       literal    : literal TIMES literal
                  | literal DIVIDE literal
    '''
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


def p_operators(p):
    ''' expression : SUMEQUALS expression
                   | MINUSEQUALS expression
                   | TIMESEQUALS expression
                   | DIVIDEEQUALS expression'''

    if p[1] == '+=':
        p[0] += p[2]
    elif p[1] == '-=':
        p[0] -= p[2]
    elif p[1] == '*=':
        p[0] *= p[2]
    elif p[1] == '/=':
        p[0] /= p[2]


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


def p_var_Especification(p):
    '''var_Especification   : NAME LCOLC NUMBER RCOLC
                            | NAME ASSIGN expression
                            | NAME
                            | NAME LCOLC NUMBER RCOLC ASSIGN LBRACE  RBRACE'''
    if len(p) == 2:
        p[0] = Variavel(p[1], None)
    elif len(p) == 4:
        p[0] = Variavel(p[1], p[3])


def p_define_expression_literal(t):
    'expression : literal'
    t[0] = t[1]


# statements
def p_statement(t):
    '''statement    : for_statement
    '''
    t[0] = t[1]

#  # | break_statement
#                 | return_statement
#                 | assignment end
#                 | subCall_statement end
#                 | write_statement end
#                 | read_statement end


def p_list_statement(t):
    '''list_statement : statement list_statement
                        | empty'''


def p_statement_eof(p):
    '''eof_statement : expression EOF'''

    print("parsed:", p)


# block
def p_block(t):
    '''block : list_statement'''
    t[0] = [t[1], t[2]]


def p_statement_for(t):
    'for_statement  : FOR expression COLON block'


def p_statement_if(t):
    '''if_statement : IF expression COLON block
                    | IF expression COLON block ELSE COLON block
                    | IF expression COLON block ELIF COLON block ELSE COLON block
                    | IF expression COLON block ELIF expression COLON block'''
    if t[3]:
        t[0] = t[6]
    elif len(t) > 10:  # with else
        t[0] = t[10]


def p_statement_while(p):
    'while_statement : WHILE expression COLON block'


def p_statement_return(p):
    '''return_statement : RETURN
                        | RETURN variavel'''


def p_statement_break(p):
    '''break_statement : BREAK'''


def p_statement_def(p):
    '''def_statement : DEF expression COLON block'''


def p_statement_class(p):
    '''class_statement : CLASS expression COLON block'''


def p_statement_continue(p):
    '''continue_statement : CONTINUE'''


def p_expression(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")

