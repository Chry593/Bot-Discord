import random

def lancia(tipo_dado,quanti_dadi):
    assert type(tipo_dado) == int and type(quanti_dadi) == int,"non è un numero valido"
    tot = 0
    for i in range(0,quanti_dadi):
    
        ris = random.randint(1,tipo_dado)
        tot += ris
    return tot
