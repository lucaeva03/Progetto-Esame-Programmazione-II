import pygame
import os
import random
from data import *
from sprite import *
from proiettile import *
from audio import *

# CLASSE SOLDATO PER CREARLO, POSIZIONARLO, ANIMARLO
class Soldato(pygame.sprite.Sprite):

    # FUNZIONE PER CREAZIONE DEL SOLDATO e INIZIALIZZAZIONE VARIABILI
    def __init__(self,char_type,x,y,scale,speed,ammo,grenades):
        pygame.sprite.Sprite.__init__(self) 

        #VARIABILI SOLDATO
        self.alive = True 
        self.char_type = char_type 
        self.speed = speed 
        self.ammo = ammo 
        self.start_ammo = ammo 
        self.shoot_cooldown = 0 
        self.grenades = grenades 
        self.health = 100 
        self.max_health = self.health 
        self.direction = 1 
        self.vel_y = 0 
        self.in_air = True 
        self.jump = False 
        self.flip = False 
        self.animation_list = [] 
        self.frame_index = 0 
        self.action = 0 
        self.update_time = pygame.time.get_ticks() 

        #VARIABILI SPECIFICHE PER IA
        self.move_counter = 0 
        self.vision = pygame.Rect(0,0,150,20) 
        self.idliing = False 
        self.idling_counter = 0 

        #CARICAMENTO IMMAGINI ANIMAZIONE SOLDATO
        animation_types = ['Idle', 'Run','Jump','Death'] 
        for animation in animation_types: 
            temp_list = [] 
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}')) 
            for i in range(num_of_frames): 
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha() 
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) 
                temp_list.append(img) 
            self.animation_list.append(temp_list)         
        self.image = self.animation_list[self.action][self.frame_index] 
        self.rect = self.image.get_rect() 
        self.rect.center = (x,y) 
        self.width = self.image.get_width() 
        self.height = self.image.get_height() 

    # FUNZIONE PER AGGIORNARE ANIMAZIONE E STATO SOLDATO
    def aggiorna(self):
        self.aggiorna_animazione() 
        self.check_alive() 
      # AGGIORNAMENTO TEMPO DI RICARICA SPARO
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    # FUNZIONE PER MUOVERE IL SOLDATO
    def movimento(self, moving_left, moving_right,world,screen_scroll):
        
        # RESETTA VARIABILE SCORRIMENTO MAPPA
        screen_scroll = 0 

        # RESETTA  VARIABILI MOVIMENTO 
        dx = 0
        dy = 0
        
        # MOVIMENTO GIOCATORE
        if moving_left:
            dx = -self.speed 
            self.flip = True 
            self.direction = -1 
        if moving_right:
            dx = self.speed 
            self.flip = False 
            self.direction = 1 
        
        # SALTO
        if self.jump == True and self.in_air == False: 
            self.vel_y = -10 
            self.jump = False 
            self.in_air = True 
        
        # APPLICAZIONE GRAVITA'
        self.vel_y += GRAVITA 
        if self.vel_y > 10: 
            self.vel_y = 10
        dy += self.vel_y 
        
        # CONTROLLO COLLISIONI 
        for tile in world.obstacle_list:  
            # CONTROLLO COLLISIONE ORIZZONTALE
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):  
                dx = 0  
                if self.char_type == 'enemy': 
                    self.direction *= -1 
                    self.move_counter = 0 
            # CONTROLLO COLLISIONE VERTICALE
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):  
              # CONTROLLO SALTO  
              if self.vel_y < 0:  
                    self.vel_y = 0  
                    dy = tile[1].bottom - self.rect.top  
              # CONTROLLO CADUTA  
              elif self.vel_y >= 0:  
                    self.vel_y = 0  
                    self.in_air = False  
                    dy = tile[1].top - self.rect.bottom 

        # CONTROLLO COLLISIONI CON ACQUA
        if pygame.sprite.spritecollide(self, gruppo_acqua, False): 
            self.health = 0 

        # CONTROLLO COLLISIONI CON EXIT 
        level_complete = False 
        if pygame.sprite.spritecollide(self, gruppo_exit, False): 
            level_complete = True 

        # CONTROLLO SE IL GIOCATORE CADE
        if self.rect.bottom > SCREEN_HEIGHT: 
            self.health = 0 

        # CONTROLLO SE IL GIOCATORE ESCE DALLA MAPPA
        if self.char_type == 'player': 
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH: 
                dx = 0 

        # AGGIORNAMENTO POSIZIONE DEL BOX DEL SOLDATO
        self.rect.x += dx 
        self.rect.y += dy 

        # SCORRIMENTO MAPPA IN BASE ALLA POSIZIONE DEL PLAYER e CONTROLLO LIMITI
        if self.char_type == 'player': 
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH ) or (self.rect.left < SCROLL_THRESH): 
                self.rect.x -= dx 
                screen_scroll = -dx 
        return screen_scroll * screen_scrool_speed, level_complete 

    # DEFINIZIONE FUNZIONE INTELIGENZA ARTIFICIALE ESCLUSIVAMENTE PER I NEMICI
    def IA(self, player, world, screen_scroll):
        if self.alive and player.alive: 
            
            # GENERATORE DI MOMENTI IN CUI IL NEMICO SI FERMA
            if self.idliing == False and random.randint(1, 200) == 1: 
                self.aggiorna_azione(0)                 
                self.idliing = True 
                self.idling_counter = 50 
            
            # SPARO AUTOMATICO DEL NEMICO quando SI MUOVE e ha nel raggio il player 
            if self.vision.colliderect(player.rect):
                self.aggiorna_azione(0) 
                self.spara() 
            
            # SE IL NEMICO NON HA IL PLAYER NEL RAGGIO DI SPARO SI MUOVE AUTOMATICAMENTE 
            else: 
                # MOVIMENTO AUTOMATICO NEMICO
                if self.idliing == False: 
                    if self.direction == 1: 
                        ai_moving_right = True 
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right 
                    self.movimento(ai_moving_left, ai_moving_right, world, screen_scroll) 
                    self.aggiorna_azione(1) 
                    self.move_counter +=1 
                    if self.move_counter >= TILE_SIZE: 
                        self.direction *= -1 
                        self.move_counter = -1 
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery) 

                # CONTATATORE STATO DI FERMO DEL NEMICO
                else:
                    self.idling_counter -= 1 
                    if self.idling_counter <= 0: 
                        self.idliing = False 
        
        # AGGIORNAMENTO POSIZIONE DEL BOX DEL NEMICO in base allo scorrimento della mappa
        self.rect.x += screen_scroll 

    # FUNZIONE PER SPARARE DEL SOLDATO
    def spara(self):
        if self.shoot_cooldown == 0 and self.ammo > 0: 
            self.shoot_cooldown = 20 
            proiettile = Proiettile(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction) 
            gruppo_proiettile.add(proiettile) 
            self.ammo -= 1 
            shot_fx.play() 
    
    # FUNZIONE PER AGGIORNARE ANIMAZIONE SOLDATO
    def aggiorna_animazione(self):
        ANIMATION_COOLDOWN = 120 
        self.image = self.animation_list[self.action][self.frame_index] 
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN: 
            self.update_time = pygame.time.get_ticks() 
            self.frame_index += 1 
        if self.frame_index >= len(self.animation_list[self.action]): 
            if self.action == 3: 
                self.frame_index = len(self.animation_list[self.action]) - 1 
            else: 
                self.frame_index = 0 

    # FUNZIONE PER CONTROLLARE E AGGIORNARE STATO AZIONE SOLDATO
    def aggiorna_azione(self, new_action):
        if new_action != self.action:
            self.action = new_action 
            self.frame_index = 0 
            self.update_time = pygame.time.get_ticks() 

    # FUNZIONE PER CONTROLLARE STATO VITA SOLDATO
    def check_alive(self): 
        if self.health <= 0: 
            self.health = 0 
            self.speed = 0 
            self.alive = False 
            self.aggiorna_azione(3) 
    
    # FUNZIONE POSIZIONE SOLDATO 
    def posiziona(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) 
        # pygame.draw.rect (screen, RED, self.rect, 1) # disegna il box collider del soldato (utile per controllare collisioni con item)

