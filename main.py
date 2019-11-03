# -*- coding: UTF-8 -*-

# Autor 1: Eliane Isadora Faveron Maciel
# Autora 2: Guilherme Menin Stedile
from ply import lex, yacc
from analisador_lexico import AnaliserLexer


if __name__ == '__main__':
    file = open("fonte.txt", "r")
    lexer = AnaliserLexer()
    lexer.build()
    for line in file:
        lexer.lexer.input(line)
        print(lexer.token())

    file.close()

    lexer.transform_tokens()
    file = open("Saida.txt", "w")
    file.write("\n".join(lexer.tokens_result_str))
    file.close()
