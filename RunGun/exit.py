import pygame
from data import *

# CLASSE PER EXIT 
class Exit(pygame.sprite.Sprite):
    
    #FUNZIONE PER CREARE LA DECORAZIONE
    def __init__(self,img,x,y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = img 
        self.rect = self.image.get_rect() 
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    # FUNZIONE PER AGGIORNARE LA POSIZIONE DELL'EXIT
    def update(self, screen_scroll): 
        self.rect.x += screen_scroll 
