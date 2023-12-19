import discord
import lancio_moneta as lm
import codice_morse_bot as cm
import lancio_dadi_bot as ld    
import battute as bt
import orario as ora
import gatti_im as gt
from discord.ext import commands
import requests


token = "MTE4NjYzOTYzMjk5ODM0MjY1Nw.GxKpUl.Gs6-c6mTRBWk_4ao2Hio4wLP7c3Pk5n3R79k-A"

#configuriamo intents
intents = discord.Intents.default()
intents.message_content = True  #permesso per i messaggi

bot = commands.Bot(command_prefix="$",intents=intents)



#creiamo la lista dei comandi nuova
class NewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)
            
bot.help_command = NewHelp()

#avvio del bot
@bot.event
async def on_ready():
    print(f"Bot avviato correttamente, {bot.user}")


#somma fra due nuemri
@bot.command(name="somma", description ="Inserisci due numeri e li somma")    #name mettiam il nome del comando
async def somma(ctx, arg1, arg2):
    somma = int(arg1) + int(arg2)
    await ctx.send(somma)


#nome1 da schiaffo a nom2
@bot.command(name="schiaffo", description = "Il primo nome inserito tira lo schiaffo al secondo nome")
async def schiaffo(ctx,nome1: str, nome2: str):
    await ctx.send(f"{nome1} ha tirato una schiaffo a {nome2}")


#converte morse in normale
@bot.command(name="morse", description = "inserisci il codice morse e verrà tradotto. Lascia uno spazio fra un codice e l'altro.")
async def morse(ctx,*,morse: str):
    diz = cm.diz
    tradotto = cm.traduzione_morse_to_normal(diz,morse)
    await ctx.send(f"Traduzione: {tradotto}")

#lancio dadi
@bot.command(name="dadi", description = "Inserisci come primo valore il tipo di dado da lanciare e come secondo valore quanti dadi vuoi lanciare")
async def dadi(ctx, tipo_dado: int, quanti_dadi:int):
    ris = ld.lancia(tipo_dado,quanti_dadi)
    await ctx.send(f"Hai lanciato un D{tipo_dado} per {quanti_dadi} volte\nRisultato: {ris}")

#scrive una freddura
@bot.command(name="freddura")
async def chatbot(ctx):
    await ctx.send(f"{bt.battuta('D:/folder/bot discord/battute.txt')}")

#testa o croce
@bot.command(name="moneta", description = "Lancio della moneta per testa o croce")
async def lancio_mon(ctx):
    await ctx.send(f"E' uscito: {lm.lancio()}")

#mostra orario di vari paesi
@bot.command(name="orario", description = "Scrivi 1 per Europe/Rome\nScrivi 2 per America/New_York\nScrivi 3 per America/Los_Angeles\nScrivi 4 per Japan")
async def orario(ctx,scelta: int):
    await ctx.send(ora.ora_attuale(scelta))
    
#mostra foto di gattini random
@bot.command(name="gatto", description = "Mostra foto di gattini")
async def gatto(ctx):
    immagine = discord.File(gt.estrai_caso())
    await ctx.send(file=immagine)

#mostra tutte le informazioni su un champion di genshin
@bot.command(name="build", description = "Inserisci il nome di un personaggio di genshin e avrai tutto quello di cui hai bisogno!")
async def build(ctx,nome_personaggio: str):
    
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
        for diz in lista_info:
            ris = (f"Nome: {diz['name']}\nRarità: {diz['rarity'].replace('_',' ')}\nArma: {diz['weapon']}\nTipo: {diz['vision']}\nWiki: {diz['wiki_url']}")
        await ctx.send(ris)
        
        
bot.run(token)
