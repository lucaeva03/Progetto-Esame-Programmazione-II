import pygame
import csv
from data import *
from sprite import *
from img import *
from sfondo import *
from audio import *
from testo import *
from clock import *
from bottone import *
from soldato import *
from mappa import *
from decorazione import *
from acqua import *
from item import *
from exit import *
from barrasalute import * 
from proiettile import * 
from esplosione import * 
from granata import * 
from transizione import *
from reset import *

# ------------------------- DEFINIZIONE ISTANZE DI CLASSE  ---------------------------

# CREAZIONE TRANSIZIONE INIZIALE E TRA LIVELLI
trans_fade = Transizione(1, BLACK, 6)

# CREAZIONE BOTTONI
start_button = Bottone(275, SCREEN_HEIGHT // 2 - 130, start_img, 1) 
exit_button = Bottone(275, SCREEN_HEIGHT // 2 + 20, exit_img, 1) 
restart_button = Bottone(275, 230, restart_img, 1) 

# CREAZIONE LISTA PER LA MAPPA VUOTA (con tutti i valori a indice -1 che nei TILES è vuoto) 
world_data = [] 
for row in range(ROWS): 
    r = [-1] * COLS 
    world_data.append(r) 

# CARICAMENTO MAPPA DA FILE CSV
with open(f'levels/level{level}_data.csv', newline='') as csvfile: 
    reader = csv.reader(csvfile, delimiter=',') 
    for x, row in enumerate(reader): 
        for y, tile in enumerate(row): 
            world_data[x][y] = int(tile) 
world = Mappa() 
player, barra_salute = world.process_data(world_data)

# ------------------------------------ MAIN ----------------------------------------

# INIZIALIZZAZIONE 
run = True
while run:

    # VELOCITA' ESECUZIONE GIOCO
    clock.tick(FPS)

    # AVVIO MENU
    if start_game == False: 
        # MENU'
        screen.blit(background_menu_img, (0, 0))
        screen.blit(title_img, (SCREEN_WIDTH // 2 - title_img.get_width() // 2, 30)) 
        screen.blit(powered_by_img, (SCREEN_WIDTH // 2 - powered_by_img.get_width() // 2, 475)) 
        if start_button.draw(screen): 
            start_game = True 
            start_trans = True 
        if exit_button.draw(screen): 
            run = False 
    # AVVIO GIOCO
    else:
        # AGGIORNAMENTO BACKGROUND
        posiziona_bg()

        #POSIZIONA MAPPA
        world.posiziona(screen_scroll)

        # VISUALIZZA SALUTE, MUNIZIONI, GRANATE GIOCATORE
        barra_salute.update(player.health)
        testo('MUNIZIONI:', font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(proiettile_img, (130 + (x * 10), 40)) 
        testo('GRANATE:', font, WHITE, 10, 60)
        for x in range(player.grenades): 
            screen.blit(granata_img, (122 + (x * 15), 62)) 

        # INIZIALIZZAZIONE DEL PLAYER
        player.aggiorna()
        player.posiziona()

        # INIZIALIZZAZIONE DEI NEMICI UTILIZZANDO IL GRUPPO PERCHE SONO PIU' DI UNO E DEVONO ESSERE GESTITI E QUINDI CHIAMATI UNO INDIPENDENTEMENTE DALL'ALTRO
        for enemy in gruppo_nemici: 
            enemy.IA(player, world, screen_scroll) 
            enemy.aggiorna()
            enemy.posiziona()

        # AGGIORNA E POSIZIONA GRUPPI DI SPRITE - # chiama draw(screen) che è metodo definito all'interno di pygame.sprite.Group() e update che è definito nelle classi sopra ed è appartentente a grupo_proiettili/granata/... in quanto ogni gruppo è costituito da istanze di classi al cui interno sono definiti i vari update per ogni classe e di conseguenza per ogni istanza e quindi gruppo
        gruppo_proiettile.update(world, player, screen_scroll) 
        gruppo_granata.update(world, screen_scroll, player) 
        gruppo_esplosione.update(screen_scroll)
        gruppo_item.update(player, screen_scroll)
        gruppo_decorazioni.update(screen_scroll)
        gruppo_acqua.update(screen_scroll)
        gruppo_exit.update(screen_scroll)
        gruppo_proiettile.draw(screen) 
        gruppo_granata.draw(screen)
        gruppo_esplosione.draw(screen)
        gruppo_item.draw(screen)
        gruppo_decorazioni.draw(screen)
        gruppo_acqua.draw(screen)
        gruppo_exit.draw(screen)

        # GESTIONE TRANSIZIONE
        if start_trans == True: 
            if trans_fade.fade(): 
                start_trans = False 
                trans_fade.fade_counter = 0 

        # AGGIORNAMENTO AZIONI/STATO DEL PLAYER
        
        # PLAYER VIVO
        if player.alive:
            if shoot: 
                player.spara() 
            elif grenade and player.grenades > 0 and grenade_active == False: 
                grenade = Granata(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction) 
                gruppo_granata.add(grenade) 
                player.grenades -= 1        
                grenade_active = True 
            if player.in_air:
                player.aggiorna_azione(2) # 2 = salto
            elif moving_left or moving_right:
                player.aggiorna_azione(1) # 1 = corri
            else:
                player.aggiorna_azione(0) # 0 = fermo
            screen_scroll, level_complete = player.movimento(moving_left, moving_right, world, screen_scroll) 
            bg_scroll -= screen_scroll 
            # CONTROLLO DEL LIVELLO SE E' STATO COMPLETATO
            if level_complete:
                level_completed_fx.play()
                start_trans = True 
                level += 1
                bg_scroll = 0
                world_data = resetta_livello()
                # CARICAMENTO MAPPA LIVELLO SUCCESSIVO DA FILE
                if level <= MAX_LEVELS: 
                    with open(f'levels/level{level}_data.csv', newline='') as csvfile: 
                        reader = csv.reader(csvfile, delimiter=',') 
                        for x, row in enumerate(reader): 
                            for y, tile in enumerate(row): 
                                world_data[x][y] = int(tile) 
                    world = Mappa() 
                    player, barra_salute = world.process_data(world_data) 
        

        # QUANDO IL PLAYER E' MORTO
        else: 
            # SCHERMATA e SUONO MORTE
            if not dead_sound_played: 
                dead_fx.play() 
                dead_sound_played = True   
            screen_scroll = 0 
            screen.fill(RED) 
            screen.blit(dead_img, (SCREEN_WIDTH // 2 - dead_img.get_width() // 2, 50)) 
            # USCITA DAL GIOCO
            if exit_button.draw(screen): 
                run = False 
            # RIAVVIO LIVELLO
            if restart_button.draw(screen): 
                bg_scroll = 0 
                start_trans = True 
                world_data = resetta_livello() 
                # CARICAMENTO MAPPA DA FILE (come sopra)
                with open(f'levels/level{level}_data.csv', newline='') as csvfile: 
                    reader = csv.reader(csvfile, delimiter=',') 
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row): 
                            world_data[x][y] = int(tile) 
                world = Mappa() 
                player, barra_salute = world.process_data(world_data) 

        # RICHIAMO FUNZIONE MOVIMENTO PLAYER PER AGGIORNAMENTO POSIZIONE
        player.movimento(moving_left, moving_right, world, screen_scroll)
    
    # CONTROLLO DEGLI EVENTI - ITERAZIONI DI GIOCO PER IL PLAYER
    for event in pygame.event.get():        
        # CHIUSURA CON X DELLA FINESTRA
        if event.type == pygame.QUIT:
            run = False
        # COMANDI (quando vengono premuti)
        if event.type == pygame.KEYDOWN:            
            # MOVIMENTO GIOCATORE
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            # SPARO GIOCATORE
            if event.key == pygame.K_SPACE:
                shoot = True
            # LANCIO GRANATA
            if event.key == pygame.K_q:
                grenade = True           
            # SALTO GIOCATORE
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            # CHIUSURA CON [ESC]
            if event.key == pygame.K_ESCAPE:
                run = False

        # COMANDI (quando vengono rilasciati)
        if event.type == pygame.KEYUP:
            # MOVIMENTO GIOCATORE
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False         
            # SPARO GIOCATORE
            if event.key == pygame.K_SPACE:
                shoot = False
            # LANCIO GRANATA
            if event.key == pygame.K_q:
                grenade = False
                grenade_active = False # al rilascio diventa False possibilità di lanciare un'altra granata

    # AGGIORNAMENTO IN BASE AGLI EVENTI
    pygame.display.update()

# TERMINA PROGRAMMA
pygame.quit()