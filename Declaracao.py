# -*- coding: UTF-8 -*-


class Declaracao(object):
    """docstring for Declaration."""
    name = ''

    def __init__(self):
        super(Declaracao, self).__init__()

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name
