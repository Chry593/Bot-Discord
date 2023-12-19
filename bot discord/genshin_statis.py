import requests

def build(nome_personaggio: str):
    
    if nome_personaggio == "raiden":
        
        nome_personaggio = "Raiden%20Shogun"
        
        
    url = "https://gsi.fly.dev/characters/search?name="
    url_finale = url + nome_personaggio[0].upper() + nome_personaggio[1:]
    response = requests.get(url_finale)

    # Controlla lo stato della risposta
    if response.status_code == 200:
        # La richiesta è andata a buon fine
        dati_risposta = response.json()  
        lista_info = dati_risposta["results"]   #lista di dizionari
        print(lista_info)
        for diz in lista_info:
            print(f"Nome: {diz['name']}\nRarità: {diz['rarity'].replace('_',' ')}\nArma: {diz['weapon']}\nTipo: {diz['vision']}\nWiki: {diz['wiki_url']}")

build("mona")