# -*- coding: UTF-8 -*-

# Autor 1: Eliane Isadora Faveron Maciel
# Autora 2: Guilherme Menin Stedile
from ply import lex, yacc
from analisador_lexico import AnaliserLexer
from grammar import *


if __name__ == '__main__':
    file_open = open("fonte.txt", "r")
    lines = file_open.readlines()
    lexer = AnaliserLexer()
    lexer.build()
    tokens = lexer.tokens
    parser = yacc.yacc(debug=True)
    for line in lines:
        lexer.lexer.input(line)
        print(lexer.token())

    result = parser.parse(file_open.read(), lexer=lexer, debug=True)
    print(result)

    file_open.close()

    lexer.transform_tokens()
    file_open = open("Saida.txt", "w")
    file_open.write("\n".join(lexer.tokens_result_str))
    file_open.close()
