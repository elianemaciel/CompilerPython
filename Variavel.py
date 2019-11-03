# -*- coding: UTF-8 -*-
from Declaracao import Declaracao


class Variavel(Declaracao):
    """Exclusive class for control variables"""
    """docstring for Variable."""
    name = ''
    tipo = ''
    value = None

    def __init__(self, name, value):
        super(Variavel, self).__init__()
        self.name = name
        self.value = value
        self.set_tipo()

    def set_tipo(self):
        self.tipo = type(self.value)

    def __str__(self):
        return "Variavel: {0} \n\tType: {1} \n\tValue: {2}".format(
                self.name,
                str(self.tipo),
                str(self.value)
            )

    def __repr__(self):
        return "| {0} , {1} , {2} |".format(
            self.name,
            str(self.tipo),
            str(self.value)
        )
