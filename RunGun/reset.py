import pygame
from data import *
from sprite import *

# FUNZIONE PER RESETTARE LIVELLO
def resetta_livello():
    gruppo_nemici.empty() 
    gruppo_proiettile.empty() 
    gruppo_granata.empty() 
    gruppo_esplosione.empty()
    gruppo_item.empty()
    gruppo_decorazioni.empty() 
    gruppo_acqua.empty() 
    gruppo_exit.empty() 

    # CREAZIONE LISTA VUOTA NUOVA PER I NUOVI DATI DELLA MAPPA
    data = [] 
    for row in range(ROWS): 
        r = [-1] * COLS 
        data.append(r) 
    return data 