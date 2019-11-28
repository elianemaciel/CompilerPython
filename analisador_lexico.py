from sly import Lexer
import copy


class AnaliserLexer(Lexer):

    tokens = {
        ID, NAME, NUMBER, NORMALSTRING, PLUS, MINUS,
        TIMES, DIVIDE, ASSIGN, RPAREN, LPAREN,
        RCOLC, LCOLC, RBRACE, LBRACE,
        COLON, EQUALS, DIFF, MENOR, MAIOR,
        MENOREQUALS, MAIOREQUALS, SUMEQUALS,
        MINUSEQUALS, TIMESEQUALS, DIVIDEEQUALS,
        WHITESPACE, EOF, BREAK, FOR, FALSE, IF, ELIF, ELSE,
        RETURN, TRUE, WHILE, PASS, DEF, CLASS, NONE, AND,
        CONTINUE, FROM, IMPORT, IN, NOT, OR
    }

    ignore = ' \t'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    RPAREN = r'\)'
    LPAREN = r'\('
    RCOLC = r'\]'
    LCOLC = r'\['
    RBRACE = r'\}'
    LBRACE = r'\{'
    COLON = r':'
    EQUALS = r'=='
    DIFF = r'!='
    MENOR = r'<'
    MAIOR = r'>'
    MENOREQUALS = r'<='
    MAIOREQUALS = r'>='
    SUMEQUALS = r'\+='
    MINUSEQUALS = r'-='
    TIMESEQUALS = r'\*='
    DIVIDEEQUALS = r'/='
    ASSIGN = r'='
    EOF = r'$\(?![\r\n]\)'
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    # IF = r'if'
    # ELSE = r'else'
    # WHILE = r'while'
    FOR = r'for'
    BREAK = r'breack'
    FALSE = r'false'
    ELIF = r'elif'
    RETURN = r'return'
    TRUE = r'True'
    PASS = r'pass'
    DEF = r'def'
    CLASS = r'class'
    NONE = r'None'
    AND = r'and'
    CONTINUE = r'continue'
    FROM = r'from'
    IMPORT = r'import'
    IN = r'in'
    NOT = r'not'
    OR = r'or'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Special cases
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE

    def __init__(self, eoftoken='EOF', **kwargs):

        self.indents = [0]  # indentation stack
        self.tokens_result = []    # token queue
        self.tokens_result_str = []    # token queue

        self.end = False
        self.eof = eoftoken

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

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Error handling rule
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    @_(r'\"([^\\\n]|(\\.))*?\"')
    def NORMALSTRING(self, t):
        # print(t)
        return t

    @_(r'\s\s+')
    def WHITESPACE(self, t):
        whitespace = t.value
        change = self.calc_indent(whitespace)

        if change == 1:
            t.type = 'INDENT'

        if change < 0:
            # dedenting one or more times
            change += 1
            t.type = 'DEDENT'

            # buffer any additional DEDENTs
            while change:
                self.tokens.append(copy.copy(t))
                change += 1

    def eof(self, t):
        if t is None:
            return None

    def tokenize_data(self, data):
        # loop until we find a valid token
        import ipdb; ipdb.set_trace()
        for tok in self.tokenize(data):

            self.tokens_result.append(tok)
            print('type=%r, value=%r' % (tok.type, tok.value))

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
