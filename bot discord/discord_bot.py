import discord
from programmi_appoggio import lancio_moneta as lm
from programmi_appoggio import codice_morse_bot as cm
from programmi_appoggio import lancio_dadi_bot as ld    
from programmi_appoggio import battute as bt
from programmi_appoggio import orario as ora
from programmi_appoggio import gatti_im as gt
from discord.ext import commands
import requests
import asyncio
from programmi_appoggio import meteo
from programmi_appoggio import esericizi_palestra as ep
from programmi_appoggio import cane 
from programmi_appoggio import nasa
from programmi_appoggio import fortnite_shop
import random as r

token = ""

#configuriamo intents
intents = discord.Intents().all()
#intents.message_content = True  #permesso per i messaggi

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
    await bot.add_cog(Musica(bot))
    await bot.add_cog(Palestra(bot))
    await bot.add_cog(ForFun(bot))
    await bot.add_cog(Aiuto(bot))
    

#################  SEZIONE MUSICA   #################    
from programmi_appoggio import musica
from programmi_appoggio import lista_canzoni
import os

class Musica(commands.Cog, description = "comandi per la gestione della musica"):
    def __init__(self,bot):
        self.bot = bot
    #lista canzoni
    @commands.command(name="listacanzoni", description = "mostra le canzoni già scaricate")
    async def canzoni(self,ctx):
        available = lista_canzoni.lista()
        i = 0
        messaggio = ""
        await ctx.send('usa il comando $riproducicanzone <id_canzone> per far martire quella canzone')
        for canzone in available:
            messaggio += f"{i}: {canzone}\n"
            i += 1
        await ctx.send(messaggio)

    #riproduce canzone random della lista
    @commands.command(name="canzonerandom", description ="riproduce una canzone random dalla lista delle canzoni disponibili")
    async def random(self,ctx):
        canzoni = lista_canzoni.lista()
        titolo = r.choice(canzoni)
        voice_channel = ctx.author.voice.channel
        voice_channel = await voice_channel.connect()
    
        voice_channel.play(discord.FFmpegPCMAudio(f'D:/folder/bot discord/canzoni/{titolo}.mp3'), after=lambda e: print('done', e))
        await ctx.send(f"Sto riproducendo: **{titolo}**")

        while voice_channel.is_playing():
            await asyncio.sleep(1)
        await voice_channel.disconnect()  

    #musica random
    @commands.command(name="shuffle", description ="riproduce tutte le canzoni presenti in maniera randomica")
    async def shuffle(self,ctx):
        canzoni = lista_canzoni.lista()
        voice_channel = ctx.author.voice.channel
        voice_channel = await voice_channel.connect()
        for _ in range(len(canzoni)+1):
            titolo = r.choice(canzoni)
            voice_channel.play(discord.FFmpegPCMAudio(f'D:/folder/bot discord/canzoni/{titolo}.mp3'), after=lambda e: print('done', e))
            canzoni.remove(titolo)
            await ctx.send(f"Sto riproducendo: **{titolo}**")
    
            while voice_channel.is_playing():
                await asyncio.sleep(1)
            if canzoni == []:
                await ctx.send("**Canzoni finite**!!")
                break
        await voice_channel.disconnect()


    #musica tramite id
    @commands.command(name = "riproducicanzone", description = "Inseisci l'id associato alla canzone, vedi la lista con $canzoni")
    async def riproduci(self,ctx,numero : int):
        canzoni = lista_canzoni.lista()
        if numero <= len(canzoni):
            voice_channel = ctx.author.voice.channel
            voice_channel = await voice_channel.connect()
            voice_channel.play(discord.FFmpegPCMAudio(f'D:/folder/bot discord/canzoni/{canzoni[numero]}.mp3'), after = lambda e: print('done',e))
            await ctx.send(f'Sto riproducendo : {canzoni[numero]}')
            while voice_channel.is_playing():
                await asyncio.sleep(1)
            await voice_channel.disconnect()
        else:
            await ctx.send(f"nessuna canzone associata all'id: {numero}")
    
    
    #loop una canzone
    @commands.command(name = 'loop', description = 'loop di una canzone tramite id')
    async def loop(self,ctx,numero : int):
        canzoni = lista_canzoni.lista()
        voice_channel = ctx.author.voice.channel
        voice_channel = await voice_channel.connect()
        await ctx.send(f'Sto riproducendo : {canzoni[numero]}')
        while True:
            if numero <= len(canzoni):
                voice_channel.play(discord.FFmpegPCMAudio(f'D:/folder/bot discord/canzoni/{canzoni[numero]}.mp3'), after = lambda e: print('done',e))
            while voice_channel.is_playing():
                await asyncio.sleep(1)
            else:
                await ctx.send(f"nessuna canzone associata all'id: {numero}")
    
    #entrata bot con musica
    @commands.command(name="play", description ="inserisic URL della canzone o nome (vedi lista delle canzoni disponibili)")
    async def play(self,ctx,url_video):
    
        voice_channel = ctx.author.voice.channel
        #pezzo del controllo se canzone giù presente
        titolo = musica.titolo(url_video)
        voice_channel = await voice_channel.connect()
        lista_canzoni = []
        #creo una lista di canzoni per poi controllare  se è gia presente la canzone
        for canzone in os.listdir("D:/folder/bot discord/canzoni"):
            lista_canzoni.append(canzone)
        
        if f"{titolo}.mp3" in lista_canzoni:
            voice_channel.play(discord.FFmpegPCMAudio(f'D:/folder/bot discord/canzoni/{titolo}.mp3'), after=lambda e: print('done', e))
            await ctx.send(f"Sto riproducendo: **{titolo}**")
            
        else: #non è presente me la scarica
            await ctx.send("Sto scaricando la canzone,attendi qualche secondo")
            musica.scarica_audio_da_youtube(url_video)
            voice_channel.play(discord.FFmpegPCMAudio(f'D:/folder/bot discord/canzoni/{titolo}.mp3'), after=lambda e: print('done', e))
            await ctx.send(f"Sto riproducendo: **{titolo}**")
                      
        while voice_channel.is_playing():
            await asyncio.sleep(1)
        await voice_channel.disconnect()
       
    #uscire bot col comando
    @commands.command(name="leave", description ="fai uscire il bot")
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()

##################################################### 


######################## Palestra Ilaria ############

from programmi_appoggio import dieta

class Palestra(commands.Cog, description = "comandi per la palestra e la dieta"):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command(name="palestra", description = "inserisci il giorno")
    async def palestra(self,ctx,giorno):
        settimana = ep.diz_giorni
        es_giorno = list(settimana[giorno].keys())
        lista_esercizi = ep.es(giorno)
        await ctx.send(f"**{es_giorno[0]}**")
        for esercizio in lista_esercizi:
            if esercizio.startswith("https"):
                await ctx.send(esercizio)
            else:
                await ctx.send(file=discord.File(esercizio))

    #dieta ila
    @commands.command(name = "valori", description = "inserisci il nome del cibo, vedi la lista con $listacibo")
    async def valori (self,ctx,*,nome_cibo):
        try:
            await ctx.send(dieta.valore_nutrizionale(nome_cibo))
        except KeyError:
            await ctx.send(f'{nome_cibo} non presente')

    #lista cibi
    @commands.command(name = "listacibo", description = "mostra la lista dei cibi disponibili")
    async def listacibo(self,ctx):
        await ctx.send(dieta.lista_c())

#####################################################


######################## For Fun ####################

from programmi_appoggio import fusione_nomi
class ForFun(commands.Cog, description = "comandi per lo svago"):
    def __init__(self,bot):
        self.bot = bot

    #mostra tutte le informazioni su un champion di genshin
    @commands.command(name="build", description = "Inserisci il nome di un personaggio di genshin e avrai tutto quello di cui hai bisogno!")
    async def build(self,ctx,nome_personaggio: str):
    
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


    #foto giorno nasa
    @commands.command(name="apod", description = "apod (Astronomy Picture of the Day), foto del giorno riguardante lo spazio")
    async def apod(self,ctx):
        dati = nasa.pianeta()
        await ctx.send(f"**Spiegazione:**\n{dati['explanation']}")
        await ctx.send(dati["url"])
        
    #meteo
    @commands.command(name="meteo", description = "mostra temperatura e precipitazioni a Latina")
    async def tempo(self,ctx):
        await ctx.send(meteo.t())

    #foto cani
    @commands.command(name="cane",description="foto di cagnolini!")
    async def cagnolino(self,ctx):
        await ctx.send(cane.cagnolino())



    #mostra foto di gattini random
    @commands.command(name="gatto", description = "Mostra foto di gattini")
    async def gatto(self,ctx):
        immagine = discord.File(gt.estrai_caso())
        await ctx.send(file=immagine)

    #mostra orario di vari paesi
    @commands.command(name="orario", description = "Scrivi 1 per Europe/Rome\nScrivi 2 per America/New_York\nScrivi 3 per America/Los_Angeles\nScrivi 4 per Japan")
    async def orario(self,ctx,scelta: int):
        await ctx.send(ora.ora_attuale(scelta))

    #somma fra due nuemri
    @commands.command(name="somma", description ="Inserisci due numeri e li somma")    #name mettiam il nome del comando
    async def somma(self,ctx, arg1, arg2):
        somma = int(arg1) + int(arg2)
        await ctx.send(somma)


    #nome1 da schiaffo a nom2
    @commands.command(name="schiaffo", description = "Il primo nome inserito tira lo schiaffo al secondo nome")
    async def schiaffo(self,ctx,nome1: str, nome2: str):
        await ctx.send(f"{nome1} ha tirato una schiaffo a {nome2}")


    #converte morse in normale
    @commands.command(name="morse", description = "inserisci il codice morse e verrà tradotto. Lascia uno spazio fra un codice e l'altro.")
    async def morse(self,ctx,*,morse: str):
        diz = cm.diz
        tradotto = cm.traduzione_morse_to_normal(diz,morse)
        await ctx.send(f"Traduzione: {tradotto}")

    #lancio dadi
    @commands.command(name="dadi", description = "Inserisci come primo valore il tipo di dado da lanciare e come secondo valore quanti dadi vuoi lanciare")
    async def dadi(self,ctx, tipo_dado: int, quanti_dadi:int):
        ris = ld.lancia(tipo_dado,quanti_dadi)
        await ctx.send(f"Hai lanciato un D{tipo_dado} per {quanti_dadi} volte\nRisultato: {ris}")

    #scrive una freddura
    @commands.command(name="freddura")
    async def chatbot(self,ctx):
        await ctx.send(f"{bt.battuta('D:/folder/bot discord/battute.txt')}")

    #testa o croce
    @commands.command(name="moneta", description = "Lancio della moneta per testa o croce")
    async def lancio_mon(self,ctx):
        await ctx.send(f"E' uscito: {lm.lancio()}")

    #fusione di due nomi
     
    @commands.command(nome = 'fusione', description = "inserisci un nome e poi l' altro per avere un la fusione dei due" )
    async def fusione(self,ctx,nome1,nome2):
        await ctx.send(f"la fusione fra {nome1} e {nome2} e' {fusione_nomi.genera_nome(nome1,nome2)}", tts = True)
        
    @commands.command(nome = 'shop', description = 'Mostra lo shop di fornite')
    async def shop(self,ctx):
        immagine = discord.File(fortnite_shop.shop())
        await ctx.send(file=immagine)

        
          
   
#####################################################


######################## Aiuto ######################

class Aiuto(commands.Cog,description = "sezione aiuto per i comandi complessi"):
    
    #aiuto comandi difficili
    @commands.command(name="aiuto", description = "spiegazione dei comandi più complessi")
    async def aiuto(self,ctx):
        with open("D:/folder/bot discord/aiuto.txt",mode = "r", encoding="utf-8") as f:
            testo = f.read()
        await ctx.send(testo)

#####################################################    




                 
bot.run(token)
