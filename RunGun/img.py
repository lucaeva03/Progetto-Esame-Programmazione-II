import pygame
from data import *

# INIZIALIZZAZIONE FINESTRA DI GIOCO
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Run & Gun') 

#CARICAMENTO TITOLO, POWERED MENU e DEAD
title_img = pygame.image.load('img/title/Run&Gun.png').convert_alpha() 
powered_by_img = pygame.image.load('img/title/powered_by.png').convert_alpha() 
dead_img = pygame.image.load('img/title/dead.png').convert_alpha() 

#CARICAMENTO IMMMAGINI BOTTONI
start_img = pygame.image.load('img/button/start.png').convert_alpha() 
restart_img = pygame.image.load('img/button/restart.png').convert_alpha() 
exit_img = pygame.image.load('img/button/exit.png').convert_alpha() 

#CARICAMENTO IMMAGINI BACKGROUND
pine1_img = pygame.image.load('img/background/pine1.png').convert_alpha() 
pine2_img = pygame.image.load('img/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/background/mountain.png').convert_alpha() 
sky_img = pygame.image.load('img/background/sky_cloud.png').convert_alpha()

#CARICAMENTO IMMAGINI TILE PER LA MAPPA
img_list = [] 
for x in range(TYLE_TYPES): 
    img = pygame.image.load(f'img/tile/{x}.png') 
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) 
    img_list.append(img) 

#CARICAMENTO IMMAGINI PROIETTILE E GRANATA
proiettile_img = pygame.image.load('img/icons/bullet.png').convert_alpha() 
granata_img = pygame.image.load('img/icons/grenade.png').convert_alpha() 

#CARICAMENTO IMMAGINI BOX RIFORNIMENTO e DIZIONARIO ITEM
medikit_img = pygame.image.load('img/icons/health_box.png').convert_alpha() 
munizoni_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha() 
granate_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha() 
item_boxes = { 
    'Medikit': medikit_img,
    'Munizioni': munizoni_img,
    'Granate': granate_img
}

#CARICAMENTO IMMAGINI MENU
background_menu_img = pygame.image.load('img/background/menu.png').convert_alpha() 
