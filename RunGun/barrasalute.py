import pygame
from data import *
from img import *

# CLASSE BARRA SALUTE, NB: non è necessario sprite group perchè non è un oggetto che si muove o che ha bisogno di essere controllato da pygame.sprite.Group
class BarraSalute():

    def __init__(self,x,y,health,max_health):
        self.x = x 
        self.y = y
        self.health = health
        self.max_health = max_health

    # FUNZIONE PER AGGIORNARE BARRA SALUTE
    def update(self, health):
        self.health = health # aggiorna la salute del giocatore
        ratio = self.health/self.max_health # calcola il rapporto tra la salute attuale e la salute massima
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20)) # disegna la barra rossa che sarà sotto alla barra della salute e indicherà la salute persa
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20)) # disegna la barra della salute in base alla salute attuale del giocatore che viene rappresentata da 150 * ratio dove ratio è la salute attuale divisa per la salute massima
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 150, 20), 2) # disegna il contorno (verso l'interno) della barra della salute dandogli le dimensioni del rettangolo e la dimensione del bordo (2)
