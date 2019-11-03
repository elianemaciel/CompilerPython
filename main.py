# -*- coding: UTF-8 -*-

# Autor 1: Eliane Isadora Faveron Maciel
# Autora 2: Guilherme Menin Stedile

from analisador_lexico import AnaliserLexer


if __name__ == '__main__':
    file = open("fonte.txt", "r")
    m = AnaliserLexer()
    m.build()           # Build the lexer
    for line in file:
        print(m.run(line))

    file.close()
