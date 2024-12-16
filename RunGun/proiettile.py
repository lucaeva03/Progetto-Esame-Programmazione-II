import pygame
from img import *
from sprite import *

# CLASSE PROIETTILE PER CREARLO, AGGIORNARLO E CONTROLLARE COLLISIONI
class Proiettile(pygame.sprite.Sprite):
    
    #FUNZIONE PER CREARE IL PROIETTILE
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self) 
        self.speed = 10 
        self.image = proiettile_img 
        self.rect = self.image.get_rect() 
        self.rect.center = (x,y) 
        self.direction = direction 

    # FUNZIONE PER AGGIORANTE STATO PROIETTILE
    def update(self, world, player, screen_scroll):
        # MOVIMENTO PROIETTILE
        self.rect.x += (self.direction * self.speed) + screen_scroll 
        # CONTROLLO SE IL PROIETTILE ESCE DALLO SCHERMO
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH: 
            self.kill() 
        # CONTROLLA COLLISIONI CON OSTACOLI
        for tile in world.obstacle_list: 
            if tile[1].colliderect(self.rect): 
                self.kill() 
        # CONTROLLA COLLISIONI CON ALTRI NEMICI
        if pygame.sprite.spritecollide(player, gruppo_proiettile, False): 
            if player.alive: 
                player.health -= 5 
                self.kill() 
        for enemy in gruppo_nemici: 
            if pygame.sprite.spritecollide(enemy, gruppo_proiettile, False): 
                if enemy.alive: 
                    enemy.health -= 25 
                    self.kill() 