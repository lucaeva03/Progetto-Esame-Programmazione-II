import pygame
from data import *
from img import *

# CLASSE ITEM PER CREARLO, AGGIORNARLO E CONTROLLARE COLLISIONI
class Item(pygame.sprite.Sprite):
    
    #FUNZIONE PER CREARE L'ITEM
    def __init__(self,item_type,x,y,):
        pygame.sprite.Sprite.__init__(self) 
        self.item_type = item_type 
        self.image = item_boxes[self.item_type] 
        self.rect = self.image.get_rect() 
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) 

    #FUNZIONE PER AGGIORNARE STATO ITEM
    def update(self,player,screen_scroll):
        # AGGIORNAMENTO POSIZIONE ITEM
        self.rect.x += screen_scroll 
        # CONTROLLO COLLISIONI CON IL GIOCATORE e AGGIORNAMENTO SALUTE, MUNIZIONI, GRANATE GIOCATORE
        if pygame.sprite.collide_rect(self, player): 
            if self.item_type == 'Medikit':
                player.health += 25 
                if player.health > player.max_health: 
                    player.health = player.max_health 
            elif self.item_type == 'Munizioni': 
                player.ammo += 15 
            elif self.item_type == 'Granate': 
                player.grenades += 3 
            self.kill() 