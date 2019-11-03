# -*- coding: UTF-8 -*-


class Bloco(object):
    """docstring for Block."""
    def __init__(self, pai, declaracoes):
        super(Bloco, self).__init__()
        self.pai = pai
        self.declaracoes = declaracoes

    def __str__(self):
        return "Bloco {0} : \n\tDeclarações: {1}".format(
            self.pai,
            str(self.declaracoes)
        )

    def __repr__(self):
        return "| \n\tDeclarações :\n {0} | ".format(
            str(self.declaracoes)
        )
