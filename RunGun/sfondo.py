import pygame
from img import *

# FUNZIONE PER POSIZIONARE IMMAGINI SFONDO
def posiziona_bg():
    screen.fill(BG)
    width = sky_img.get_width() 
    for x in range(5): 
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0)) 
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300)) 
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150)) 
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height())) 
