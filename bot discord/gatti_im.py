import os
import random

def estrai_caso():
    lista_im = []
    direct = "D:/folder/bot discord/gatti"
    for file in os.listdir(direct):
        path_completo = direct + "/" + file
        lista_im.append(path_completo)

    return random.choice(lista_im)

