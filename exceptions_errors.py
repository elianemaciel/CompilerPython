# -*- coding: UTF-8 -*-


def sinal_desconhecido(t):
    print(
        u"Sinal não reconhecido '{0}', linha {1} , coluna {2}!".format(
            t.value, t.lineno, t.lexpos
        )
    )


def sintaxe_erro(t):
    if t:
        print(
            "Erro sintaxe '{0}', linha {1} , coluna {2}".format(
                t.value, t.lineno, t.lexpos
            )
        )
    else:
        print("Errp de sintaxe EOF")
        raise SystemExit
