import pygame
from img import *
from data import *

# INIZIALIZZAZIONE DI PYGAME
pygame.init()  

# DEFINIZIONE FONT
font = pygame.font.SysFont('Future', 30) 

# FUNZIONE PER CREARE TESTO
def testo(text, font, text_color, x, y): 
    img = font.render(text, True, text_color) 
    screen.blit(img, (x,y)) 