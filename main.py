# -*- coding: UTF-8 -*-

# Autor 1: Eliane Isadora Faveron Maciel
# Autora 2: Guilherme Menin Stedile
from ply import lex, yacc
from analisador_lexico import AnaliserLexer
from grammar import MyParser
import logging


if __name__ == '__main__':

    file_open = open("fonte.txt", "r")
    # lines = file_open.readlines()
    # lexer = AnaliserLexer()

    # for line in lines:
    #     lexer.lexer.input(line)
    #     print(lexer.token())

    parser = MyParser()
    parser.run(file_open.read())
    file_open.close()

    # lexer.transform_tokens()
    # file_open = open("Saida.txt", "w")
    # file_open.write("\n".join(lexer.tokens_result_str))
    # file_open.close()
