import ply.lex as lex


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
        'MINUSEQUALS', 'TIMESEQUALS', 'DIVIDEEQUALS', 'MOD'
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
    t_TIMESEQUALS  = r'\*='
    t_DIVIDEEQUALS = r'/='
    t_ASSIGN = r'='
    
    def __init__(self):
        self.lexer = None

    def t_NUMBER(self,t):
        r'\d+'
        t.value = int(t.value)    
        return t
 
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    
    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value in RESERVED:# Check for reserved words
            t.type = RESERVED[t.value]
        return t

    def t_NORMALSTRING(self, t):
	    r'\"([^\\\n]|(\\.))*?\"'
        #	print(t)
	    return t

    def t_COMMENT_MONOLINE(self, t):
        r'//.*'
        pass

    def t_ccode_comment(self,   t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        pass

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
     
    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            print(tok)