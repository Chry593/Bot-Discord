
import pytz
from datetime import datetime


def ora_attuale(scelta: int):
    
    formato_desiderato = '%d-%m-%Y %H:%M:%S' 
    
    if scelta == 1:
        zona = "Europe/Rome"
        tz = pytz.timezone(zona)
        ora = datetime.now(tz).strftime(formato_desiderato)
        
    if scelta == 2:
        zona = "America/New_York"
        tz = pytz.timezone(zona)
        ora = datetime.now(tz).strftime(formato_desiderato)
        
    if scelta == 3:
        zona = "America/Los_Angeles"
        tz = pytz.timezone(zona)
        ora = datetime.now(tz).strftime(formato_desiderato)
        
    if scelta == 4:
        zona = "Japan"
        tz = pytz.timezone(zona)
        ora = datetime.now(tz).strftime(formato_desiderato)

    return f"{zona}: {ora}"
