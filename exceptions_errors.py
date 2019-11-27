# -*- coding: UTF-8 -*-


class SinalDesconhecido(Exception):

    def __init__(self, token):
        self.message = "Sinal não reconhecido '{0}', linha {1} , coluna {2}!".format(
            token.value, token.lineno, token.lexpos
        )


class SyntaxeError(Exception):

    def __init__(self, token):
        self.message = "Erro sintaxe '{0}', linha {1} , coluna {2}".format(
                token.value, token.lineno, token.lexpos
            )
