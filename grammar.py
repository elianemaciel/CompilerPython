# -*- coding: UTF-8 -*-

from sly import Parser
from exceptions_errors import SyntaxeError, SinalDesconhecido
from analisador_lexico import AnaliserLexer


class MyParser(Parser):
    tokens = AnaliserLexer.tokens

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

    def __init__(self):
        self.debug = True
        self.lexer = AnaliserLexer()
        self.parser = yacc.yacc(
            module=self,
            start='expression',
            debug=self.debug
        )

    # Definição
    def p_pass(self, p):
        'empty : PASS'

        if p[1] == 'pass':
            pass

    def p_literal(self, p):
        '''literal : NUMBER
                | TRUE
                | FALSE
                | NORMALSTRING
        '''
        p[0] = p[1]

    def p_sequence_literal(self, p):
        '''sequence_literal : literal COMMA sequence_literal
                            | literal'''

    def p_variavel(self, p):
        '''variavel : NAME
                    | NAME LCOLC expression RCOLC'''
        p[0] = p[1]

    def p_binary_operators(self, p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
        expression    : literal TIMES literal
                      | literal DIVIDE literal
        '''
        if p[1] and p[3]:
            if p[2] == '+':
                p[0] = p[1] + p[3]
            elif p[2] == '-':
                p[0] = p[1] - p[3]
            elif p[2] == '*':
                p[0] = p[1] * p[3]
            elif p[2] == '/':
                if p[3] == 0:
                    print("Can't divide by 0")
                    raise ZeroDivisionError('integer division by 0')
                else:
                    p[0] = p[1] / p[3]
            else:
                raise SinalDesconhecido(p)
        else:
            SyntaxeError(p)

    def p_operators(self, p):
        ''' expression : SUMEQUALS expression
                    | MINUSEQUALS expression
                    | TIMESEQUALS expression
                    | DIVIDEEQUALS expression'''

        if p[2]:
            if p[1] == '+=':
                p[0] += p[2]
            elif p[1] == '-=':
                p[0] -= p[2]
            elif p[1] == '*=':
                p[0] *= p[2]
            elif p[1] == '/=':
                p[0] /= p[2]
        else:
            sintaxe_erro(p)

    def p_assign(self, p):
        ''' assign : ASSIGN expression'''

        if p[1] == '=':
            p[0] = p[2]
        else:
            sintaxe_erro(p)

    def p_expression_logop(self, p):
        '''comparison : literal MAIOR literal
                    | literal MENOR literal
                    | literal MAIOREQUALS literal
                    | literal MENOREQUALS literal
                    | literal EQUALS literal
                    | literal DIFF literal
                    | literal AND literal
                    | literal OR literal'''
        if p[1] and p[3]:
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
        else:
            print(p)
            sintaxe_erro(p)

    def p_define_expression_literal(self,  p):
        'expression : literal'
        p[0] = p[1]

    # statements
    def p_statement(self, p):
        '''statement    : for_statement
        '''
        p[0] = p[1]

    def p_list_statement(self, p):
        '''list_statement : statement list_statement
                            | empty'''

    def p_statement_eof(self, p):
        '''eof_statement : expression EOF'''
        '''              | EOF'''

        print("parsed:", p)

    def p_import(self, p):
        '''import : FROM NAME IMPORT NAME
                  | IMPORT NAME'''

        from_p = p[2]
        if p[1] == 'from':
            import_p = p[4]
            from from_p import import_p
        elif p[1] == 'import':
            import_p = p[2]
            import import_p

    def p_define_end_of_instruction(self, p):
        'end : EOF'
        return '$end'

    def p_colon(self, p):
        'colon  : expression COLON'

    def p_brace(self, p):
        'dict  : RBRACE expression LBRACE'
        if p[1] == '{' and p[3] == '}':
            p[0] = {p[2]}

    def p_none(self, p):
        'none  : assign NONE'
        if p[2] == 'None':
            p[0] = p[2]

    def p_not(self, p):
        '''not  : NOT expression
                | NOT literal'''
        if p[1] == 'not':
            p[0] = not p[2]

    # block
    def p_block(self, p):
        '''block : list_statement'''
        p[0] = [p[1], p[2]]

    def p_statement_for(self, p):
        'for_statement  : FOR expression COLON block'

    def p_statement_if(self, p):
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

    def p_empty(self, p):
        '''empty : '''

    def p_statement_while(self, p):
        'while_statement : WHILE expression COLON block'
        while(p[3]):
            p[5]

    def p_statement_return(self, p):
        '''return_statement : RETURN
                            | RETURN variavel'''

    def p_statement_break(self, p):
        '''break_statement : BREAK'''

    def p_statement_def(self, p):
        '''def_statement : DEF NAME COLON block'''

    def p_statement_class(self, p):
        '''class_statement : CLASS NAME COLON block'''

    def p_statement_continue(self, p):
        '''continue_statement : CONTINUE'''

    def p_expression(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    # variable name literal expression: <expression> -> NAME
    def p_expression_name(self, p):
        'expression : NAME'
        # attempt to lookup variable in current dictionary, throw error if not found
        try:
            p[0] = self.names[p[1]]
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

    # Error rule for syntax errors
    def p_error(self, p):
        if p:
            self.parser.errok()
            raise SyntaxError(p)
        else:
            print("Syntax error at EOF")

    def run(self, code):
        result = self.parser.parse(
            code + '\n',
            lexer=self.lexer,
            debug=self.debug
        )
        print(result)
