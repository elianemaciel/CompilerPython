import ply.lex as lex
import copy


RESERVED = {
    'bool': 'BOOL',
    'break': 'BREAK',
    'for': 'FOR',
    'false': 'FALSE',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'int': 'INT',
    'return': 'RETURN',
    'string': 'STRING',
    'true': 'TRUE',
    'while': 'WHILE',
    'write': 'WRITE',
    'read': 'READ',
    'pass': 'PASS',
    'def': 'DEF',
    'class': 'CLASS',
    'none': 'NONE',
    'and': 'AND',
    'as': 'AS',
    'continue': 'CONTINUE',
    'del': 'DEL',
    'except': 'EXCEPT',
    'finally': 'FINALLY',
    'from': 'FROM',
    'global': 'GLOBAL',
    'import': 'IMPORT',
    'in': 'IN',
    'is': 'IS',
    'lambda': 'LAMBDA',
    'not': 'NOT',
    'or': 'OR',
    'raise': 'RAISE',
    'try': 'TRY',
    'with': 'WITH',
    'yield': 'YIELD'
}


class AnaliserLexer(object):
    tokens = [
        'NAME', 'NUMBER', 'NORMALSTRING', 'PLUS', 'MINUS',
        'TIMES', 'DIVIDE', 'ASSIGN', 'RPAREN', 'LPAREN',
        'RCOLC', 'LCOLC', 'RBRACE', 'LBRACE', 'COMMA',
        'SEMICOLON', 'EXPLAMATION', 'INTERROGATION',
        'COLON', 'EQUALS', 'DIFF', 'MENOR', 'MAIOR',
        'MENOREQUALS', 'MAIOREQUALS', 'SUMEQUALS',
        'MINUSEQUALS', 'TIMESEQUALS', 'DIVIDEEQUALS', 'MOD',
        'WHITESPACE'
    ] + list(RESERVED.values())

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_ignore = ' \t'
    t_RPAREN = r'\)'
    t_LPAREN = r'\('
    t_RCOLC = r'\]'
    t_LCOLC = r'\['
    t_RBRACE = r'\}'
    t_LBRACE = r'\{'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_OR = r'\|\|'
    t_AND = r'&&'
    t_EXPLAMATION = r'!'
    t_INTERROGATION = r'\?'
    t_COLON = r':'
    t_EQUALS = r'=='
    t_DIFF = r'!='
    t_MENOR = r'<'
    t_MAIOR = r'>'
    t_MENOREQUALS = r'<='
    t_MAIOREQUALS = r'>='
    t_SUMEQUALS = r'\+='
    t_MINUSEQUALS = r'-='
    t_TIMESEQUALS = r'\*='
    t_DIVIDEEQUALS = r'/='
    t_ASSIGN = r'='
    t_WHITESPACE = r'\n[ ]*'

    def __init__(self):
        self.lexer = None
        self.indents = [0]  # indentation stack
        # self.tokens = []    # token queue

    def input(self, *args, **kwds):
        self.lexer.input(*args, **kwds)

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value in RESERVED:  # Check for reserved words
            t.type = RESERVED[t.value]
        return t

    def t_NORMALSTRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        # print(t)
        return t

    def t_COMMENT_MONOLINE(self, t):
        r'//.*'
        pass

    def t_ccode_comment(self,   t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        pass

    def calc_indent(self, whitespace):
        "returns a number representing indents added or removed"
        n = len(whitespace)  # number of spaces
        indents = self.indents  # stack of space numbers
        if n > indents[-1]:
            indents.append(n)
            return 1

        # we are at the same level
        if n == indents[-1]:
            return 0

        # dedent one or more times
        i = 0
        while n < indents[-1]:
            indents.pop()
            if n > indents[-1]:
                raise SyntaxError("wrong indentation level")
            i -= 1
        return i

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def run(self, data):
        self.lexer.input(data)
        import ipdb; ipdb.set_trace()
        while True:
            token = self.lexer.token()

            if not token:
                break
            print(token)

            if token.type == 'WHITESPACE':
                # check for new indent/dedent
                whitespace = token.value[1:]  # strip \n
                change = self.calc_indent(whitespace)
                if change:
                    break
                # if not token:
                #     break
                # print(token)

                # indentation change
                if change == 1:
                    token.type = 'INDENT'
                    return token

                # dedenting one or more times
                assert change < 0
                change += 1
                token.type = 'DEDENT'

                # buffer any additional DEDENTs
                while change:
                    self.tokens.append(copy.copy(token))
                    change += 1
