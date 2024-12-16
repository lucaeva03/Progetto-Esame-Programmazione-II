import pygame

#CLASSE PER ESPLOSIONE
class Esplosione(pygame.sprite.Sprite):

    #FUNZIONE PER CREARE e AGGIORNARE L'ANIMAZIONE DI ESPLOSIONE
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        for num in range (1,6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha() 
            img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale))) 
            self.images.append(img) 
        self.frame_index = 0 
        self.image = self.images[self.frame_index] 
        self.rect = self.image.get_rect() 
        self.rect.center = (x,y) 
        self.counter = 0 

    #FUNZIONE PER FERMARE E RIMUOVERE L'ANIMAZIONE DI ESPLOSIONE
    def update (self, screen_scroll):
        # AGGIORNAMENTO POSIZIONE ESPLOSIONE
        self.rect.x += screen_scroll 
        # ANIMAZIONE ESPLOSIONE
        EXPLOSION_SPEED = 4 
        self.counter += 1 
        if self.counter >= EXPLOSION_SPEED: 
            self.counter = 0 
            self.frame_index += 1 
            if self.frame_index >= len(self.images): 
                self.kill() 
            else:
                self.image = self.images[self.frame_index] 
