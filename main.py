######           Analisador Lexico    ######
# Autor 1: Eliane Isadora Faveron Maciel
# Autora 2: Guilherme
# Implementacao do analisador lexico de um compilador
# Cada codigo citado a seguir representa um tipo de token
# Essa codificacao eh usada no arquivo de saida que contem os 
# resultados de operacao do analisador lexico
# tok1 - Operador
#   tok100 - .
#   tok101 - +
#   tok102 - -
#   tok103 - *
#   tok104 - /
#   tok105 - +=
#   tok106 - -=
#   tok107 - ==
#   tok108 - !=
#   tok109 - >
#   tok110 - >=
#   tok111 - <
#   tok112 - <=
#   tok113 - and
#   tok114 - or
#   tok115 - =

# tok2 - Delimitador
#   tok200 - :

# tok3 - Numero
# tok300 - Numero Inteiro
# tok301 - Numero Real

# tok400 - Caractere Constante

# tok500 - Identificador

# tok6 - Palavra reservada
#   tok600 - algoritmo
#   tok601 - variaveis
#   tok602 - constantes
#   tok603 - registro
#   tok604 - funcao
#   tok605 - retorno
#   tok606 - vazio
#   tok607 - se
#   tok608 - senao
#   tok609 - enquanto
#   tok610 - para
#   tok611 - leia
#   tok612 - escreva
#   tok613 - inteiro
#   tok614 - real
#   tok615 - booleano
#   tok616 - char
#   tok617 - cadeia
#   tok618 - verdadeiro
#   tok619 - falso

# tok700 - Cadeia constante
# ========================== ERROS LEXICOS
# Simbolo nao pertencente ao conjunto de simbolos terminais da linguagem
# Identificador Mal formado
# Tamanho do identificador
# Numero mal formado
# Fim de arquivo inesperado (comentario de bloco nao fechado)
# Caractere ou string mal formados
# ==============================================================================

# Incluindo caracteres especiais no programa
# -*- coding: utf-8 -*-

# Bibliotecas para entrada e saida de arquivos
import sys
import os.path
import string


# Declarando Classe do analisador Lexico

from analisador_lexico import AnaliserLexer


if __name__ == '__main__':
    # lex.runmain()
    m = AnaliserLexer()
    m.build()           # Build the lexer
    m.test("3 + 4")  