# -*- coding: UTF-8 -*-

import ply.yacc as yacc
from exceptions_errors import sintaxe_erro, sinal_desconhecido


precedence = (
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'AND', 'OR'),
    ('left', 'MAIOR', 'MENOR', 'MAIOREQUALS', 'MENOREQUALS', 'EQUALS', 'DIFF'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'IF', 'ELSE'),
    ('right', 'NOT'),
)

# dictionary of names (for storing variables)
names = {}


# Definição
def p_pass(p):
    'empty : PASS'


def p_literal(p):
    '''literal : NUMBER
               | TRUE
               | FALSE
               | NORMALSTRING
    '''
    p[0] = p[1]


def p_sequence_literal(p):
    '''sequence_literal : literal COMMA sequence_literal
                        | literal'''


def p_variavel(p):
    '''variavel : NAME
                | NAME LCOLC expression RCOLC'''
    p[0] = p[1]


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
    '''comparison : literal MAIOR literal
                  | literal MENOR literal
                  | literal MAIOREQUALS literal
                  | literal MENOREQUALS literal
                  | literal EQUALS literal
                  | literal DIFF literal
                  | literal AND literal
                  | literal OR literal'''
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


# def p_var_Especification(p):
#     '''var_Especification   : NAME LCOLC NUMBER RCOLC
#                             | NAME ASSIGN expression
#                             | NAME
#                             | NAME LCOLC NUMBER RCOLC ASSIGN LBRACE  RBRACE'''
#     if len(p) == 2:
#         p[0] = Variavel(p[1], None)
#     elif len(p) == 4:
#         p[0] = Variavel(p[1], p[3])


def p_define_expression_literal(p):
    'expression : literal'
    p[0] = p[1]


# statements
def p_statement(p):
    '''statement    : for_statement
    '''
    p[0] = p[1]

#  # | break_statement
#                 | return_statement
#                 | assignment end
#                 | subCall_statement end
#                 | write_statement end
#                 | read_statement end


def p_list_statement(p):
    '''list_statement : statement list_statement
                        | empty'''


def p_statement_eof(p):
    '''eof_statement : expression EOF'''
    '''              : EOF'''

    print("parsed:", p)


def p_define_end_of_instruction(p):
    'end : EOF'
    return '$end'


# block
def p_block(p):
    '''block : list_statement'''
    p[0] = [p[1], p[2]]


def p_statement_for(p):
    'for_statement  : FOR expression COLON block'


def p_statement_if(p):
    '''if_statement : IF comparison COLON block
                    | IF comparison COLON block ELSE COLON block
                    | IF comparison COLON block ELIF comparison COLON block ELSE COLON block
                    | IF comparison COLON block ELIF comparison COLON block'''
    print(p)
    if p[3] == ':':
        if p[2]:
            p[0] = p[5]
        elif p[6] == 'else':
            p[0] = p[7]
        elif p[6] == 'elif' and p[7] and p[8] == ':':
            p[0] = p[9]


def p_empty(p):
    '''empty : '''


def p_statement_while(p):
    'while_statement : WHILE expression COLON block'
    while(p[3]):
        p[5]


def p_statement_return(p):
    '''return_statement : RETURN
                        | RETURN variavel'''


def p_statement_break(p):
    '''break_statement : BREAK'''


def p_statement_def(p):
    '''def_statement : DEF NAME COLON block'''


def p_statement_class(p):
    '''class_statement : CLASS NAME COLON block'''


def p_statement_continue(p):
    '''continue_statement : CONTINUE'''


def p_expression(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


# variable name literal expression: <expression> -> NAME
def p_expression_name(p):
    'expression : NAME'
    # attempt to lookup variable in current dictionary, throw error if not found
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        pass
        #print(p)
        #print("Syntax error at EOF")

