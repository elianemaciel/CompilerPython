# -*- coding: UTF-8 -*-

from sly import Parser
from exceptions_errors import SyntaxeError, SinalDesconhecido
from analisador_lexico import AnaliserLexer


class MyParser(Parser):
    tokens = AnaliserLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ('left', AND, OR),
        ('left', MAIOR, MENOR, MAIOREQUALS, MENOREQUALS, EQUALS, DIFF),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('left', IF, ELSE),
        ('right', NOT),
    )

    def __init__(self):
        self.debug = True
        self.names = {}

    @_('ID ASSIGN expr')
    def statement(self, p):
        self.names[p.ID] = p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('term')
    def expr(self, p):
        return p.term

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    # @_('IF expr COLON block ELSE block')
    # def expr(self, p):
    #     if expr0:
    #         return self.function.block_start()

    @_('ID')
    def expr(self, p):
        try:
            return self.names[p.ID]
        except LookupError:
            print("Undefined name '%s'" % p.ID)
            return 0

    @_('expr DIVIDE term')
    def expr(self, p):
        if p.term == 0:
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')
        return (p[1], p.expr, p.term)

    @_('ID')
    def term(self, p):
        return p.ID

    @_('PASS')
    def term(self, p):
        pass

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('ID SUMEQUALS NUMBER')
    def sumequals(self, p):
        return (p[1], p[2])

    @_('ID MINUSEQUALS NUMBER')
    def minusequals(self, p):
        return (p[1], p[2])

    @_('ID ASSIGN NUMBER')
    def assign(self, p):
        return p[2]

    @_('IF expr COLON expr')
    def assign(self, p):
        return p.expr1

    @_('IF expr')
    def assign(self, p):
        return p[4]

    def error(self, p):
        if p:
            # print(p)
            print("Syntax error at {0}, in line {1}, colum {2}".format(
                    p.type,
                    p.lineno,
                    p.index
                )
            )
            # Just discard the token and tell the parser it's okay.
            self.errok()
        else:
            print("End of File!")
            return
        self.restart()
