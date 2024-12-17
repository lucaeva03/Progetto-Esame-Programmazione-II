import pygame
from img import *

# CLASSE PER TRANSIZIONE    
class Transizione():

    def __init__(self, colour, speed):
        self.colour = colour 
        self.speed = speed 
        self.fade_counter = 0 

    # FUNZIONE PER CREARE I VARI TIPI DI TRANSIZIONE
    def fade(self):
        fade_complete = False 
        self.fade_counter += self.speed 
        # FADE IN ORIZZONTALE DA CENTRO VERSO DESTRA E SINISTRA
        pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH // 2  - self.fade_counter, SCREEN_HEIGHT)) # (schermo, colore, (x,y,larghezza,altezza))
        pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH , SCREEN_HEIGHT))
        # CONTROLLO VALORE CONTATORE (400 per completare animazione) e RITORNO (animazione completata)
        if self.fade_counter >= 400: 
            fade_complete = True 
        return fade_complete
