import pygame
from img import *

# CLASSE PER TRANSIZIONE    
class Transizione():

    # FUNZIONE PER CREARE LA CLASSE
    def __init__(self, direction, colour, speed):
        self.direction = direction 
        self.colour = colour 
        self.speed = speed 
        self.fade_counter = 0 

    # FUNZIONE PER CREARE I VARI TIPI DI TRANSIZIONE
    def fade(self):
        fade_complete = False 
        self.fade_counter += self.speed 
        # FADE IN ORIZZONTALE VERSO DESTRA
        if self.direction == 1: 
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        # FADE IN VERTICALE VERSO BASSO
        if self.direction == 2: 
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 - self.fade_counter))
        # CONTROLLO VALORE CONTATORE (400 per completare animazione) e RITORNO (animazione completata)
        if self.fade_counter >= 400: 
            fade_complete = True 
        return fade_complete 
