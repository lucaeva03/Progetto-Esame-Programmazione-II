import pygame
from data import *
from sprite import *
from img import *
from acqua import *
from decorazione import *
from soldato import *
from barrasalute import *
from item import *
from exit import *

# CLASSE MAPPA PER CREARLA, ASSOCIARE LE VARIE TILE ALLA LORO POSIZIONE
class Mappa():
    #FUNZIONE PER CREARE LA LISTA DELLE TILE VUOTA
    def __init__(self):
        self.obstacle_list = [] 

    #FUNZIONE PER PROCESSARE I DATI DELLA MAPPA
    def process_data(self, data):
        self.level_length = len(data[0]) 
        for y, row in enumerate(data): 
            for x, tile in enumerate(row): 
                if tile >= 0: 
                    img = img_list[tile] 
                    img_rect = img.get_rect() 
                    img_rect.x = x * TILE_SIZE 
                    img_rect.y = y * TILE_SIZE 
                    tile_data = (img, img_rect) 
                    # CONTROLLO TIPO DI TILE E AGGIUNTA ALLA LISTE OSTACOLI e DI SPRITE
                    if tile >= 0 and tile <= 8: 
                        self.obstacle_list.append(tile_data) 
                    elif tile >= 9 and tile <= 10: 
                        acqua = Acqua(img, x * TILE_SIZE, y * TILE_SIZE) 
                        gruppo_acqua.add(acqua) 
                    elif tile >= 11 and tile <= 14: 
                        decorazione = Decorazione(img, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE) 
                        gruppo_decorazioni.add(decorazione) 
                    elif tile == 15:
                        player = Soldato('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 4, 20, 5) 
                        barra_salute = BarraSalute(10,10,player.health,player.health) 
                    elif tile == 16: 
                        enemy = Soldato('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0) 
                        gruppo_nemici.add(enemy) 
                    elif tile == 17: 
                        item_box = Item('Munizioni', x * TILE_SIZE, y * TILE_SIZE) 
                        gruppo_item.add(item_box)
                    elif tile == 18: 
                        item_box = Item('Granate', x * TILE_SIZE, y * TILE_SIZE) 
                        gruppo_item.add(item_box)
                    elif tile == 19: 
                        item_box = Item('Medikit', x * TILE_SIZE, y * TILE_SIZE) 
                        gruppo_item.add(item_box)
                    elif tile == 20: 
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE) 
                        gruppo_exit.add(exit) 

        return player, barra_salute                   

    # POSIZIONA LE TILE DELLA MAPPA E AGGIORNA LA LORO POSIZIONE IN BASE ALLO SCORRIMENTO
    def posiziona(self, screen_scroll): 
        for tile in self.obstacle_list: 
            tile[1][0] += screen_scroll 
            screen.blit(tile[0], tile[1]) 