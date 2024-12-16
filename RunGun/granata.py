import pygame
from img import *
from audio import *
from sprite import *
from esplosione import *

# CLASSE GRANATA PER CREARLA
class Granata(pygame.sprite.Sprite):

    #FUNZIONE PER CREARE LA GRANATA
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self) 
        self.timer = 100 
        self.vel_y = -11 
        self.speed = 7 
        self.image = granata_img 
        self.rect = self.image.get_rect() 
        self.rect.center = (x,y) 
        self.width = self.image.get_width() 
        self.height = self.image.get_height() 
        self.direction = direction 

    def update(self,world,screen_scroll,player):
        #MOVIMENTO GRANATA e SBATTE SUL BORDO SE ESCE DALLO SCHERMO
        self.vel_y += GRAVITA 
        dx = self.direction * self.speed 
        dy = self.vel_y 
        # CONTROLLO COLLISIONI CON OSTACOLI
        for tile in world.obstacle_list:
            # CONTROLLO COLLISIONE MURI
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height): 
                self.direction *= -1
                dx = self.direction * self.speed
            # CONTROLLO COLLISIONE SOFFITTO E PAVIMENTO
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):  
                self.speed = 0 
                # CONTROLLO SBATTE SOFFITTO
                if self.vel_y < 0:  
                    self.vel_y = 0  
                    dy = tile[1].bottom - self.rect.top  
                # CONTROLLO SBATTE PAVIMENTO
                elif self.vel_y >= 0:  
                    self.vel_y = 0  
                    dy = tile[1].top - self.rect.bottom 

        # AGGIORNAMENTO POSIZIONE e TIMER DELLA GRANATA
        self.rect.x += dx + screen_scroll 
        self.rect.y += dy 

        #CONTRLLO COLLISIONI CON NEMICI E CHIAMATA ANIMAZIONE ESPLOSIONE
        self.timer -= 1 
        if self.timer <= 0: 
            self.kill() 
            grenade_fx.play() 
            
            explosion = Esplosione(self.rect.x, self.rect.y, 0.5) 
            gruppo_esplosione.add(explosion) 
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2: 
                player.health -= 50 
            for enemy in gruppo_nemici: 
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2: # controlla se la distanza tra il centro della granata e il centro del giocatore è minore di due volte la dimensione di TILE_SIZE (il valore abs è per considerare anche il caso in cui la distanza risulti negativa) // Crea praticamente un raggio di danno intorno alla granat
                    enemy.health -= 50 
