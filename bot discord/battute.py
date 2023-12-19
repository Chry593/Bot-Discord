import random

def battuta(path_file):
    with open (path_file,mode="r",encoding="utf-8") as f:
        righe = f.readlines()
        
    return random.choice(righe)
