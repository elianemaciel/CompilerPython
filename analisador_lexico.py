from ply import lex
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

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_RPAREN = r'\)'
    t_LPAREN = r'\('
    t_RCOLC = r'\]'
    t_LCOLC = r'\['
    t_RBRACE = r'\}'
    t_LBRACE = r'\{'
    t_COMMA = r','
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
    t_WHITESPACE = r'\s\s+'
    t_ignore = r'[\s]*\n'

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

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_ccode_comment(self,   t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        pass

    # Regular expression rules for simple tokens

    def __init__(self, **kwargs):

        self.lexer = None
        self.indents = [0]  # indentation stack
        self.tokens_result = []    # token queue
        self.tokens_result_str = []    # token queue

    def input(self, *args, **kwds):
        self.lexer.input(*args, **kwds)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def transform_tokens(self):

        for token in self.tokens_result:
            self.tokens_result_str.append(
                "{0}, {1}, {2}, {3}".format(
                    token.type,
                    token.lineno,
                    token.value,
                    token.lexpos
                )
            )

    def token(self):
        # loop until we find a valid token
        while 1:
            change = None
            # grab the next from first stage
            token = self.lexer.token()
            if token:
                self.tokens_result.append(token)
                print(token)
            # we only care about whitespace
            if token and token.type != 'WHITESPACE':
                continue

            if not token:
                break

            # check for new indent/dedent
            whitespace = token.value
            change = self.calc_indent(whitespace)

            if change == 1:
                token.type = 'INDENT'

            if change < 0:
                # dedenting one or more times
                change += 1
                token.type = 'DEDENT'

                # buffer any additional DEDENTs
                while change:
                    self.tokens.append(copy.copy(token))
                    change += 1

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