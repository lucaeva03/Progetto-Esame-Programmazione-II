import pygame
from data import *

# CLASSE PER ACQUA
class Acqua(pygame.sprite.Sprite):
    
    def __init__(self,img,x,y,):
        pygame.sprite.Sprite.__init__(self) 
        self.image = img 
        self.rect = self.image.get_rect() 
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height())) 

    # FUNZIONE PER AGGIORNARE LA POSIZIONE DELL'ACQUA
    def update(self,screen_scroll): 
        self.rect.x += screen_scroll 
