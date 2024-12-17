import pygame
from data import *
from img import *

# CLASSE BARRA SALUTE
class BarraSalute():

    def __init__(self,x,y,health,max_health):
        self.x = x 
        self.y = y
        self.health = health
        self.max_health = max_health

    # FUNZIONE PER AGGIORNARE BARRA SALUTE
    def update(self, health):
        self.health = health 
        ratio = self.health/self.max_health 
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20)) 
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 150, 20), 2) 
