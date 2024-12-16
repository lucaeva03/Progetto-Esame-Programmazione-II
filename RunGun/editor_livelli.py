import pygame
import csv 
from bottone import * 

# INIZIALIZZAZIONE DI PYGAME
pygame.init()

# ------------------------------------ VARIABILI GLOBALI -------------------------------

# DEFINIZONE FRAME RATE PER CONTROLLO VELOCITA' ESECUZIONE GIOCO
clock = pygame.time.Clock() 
FPS = 60

# DEFINIZIONE E INIZIALIZZAZIONE FINESTRA DI GIOCO
SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100 # margine inferiore per la barra degli strumenti
SIDE_MARGIN = 300 # margine laterale per la barra degli strumenti
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Editor Livelli')

# DEFINIZIONE VARIABILI
ROWS = 16 
MAX_COLS = 150 
TILE_SIZE = SCREEN_HEIGHT // ROWS 
TILE_TYPES = 21 
level = 0 
current_tile = 0 
scroll_left = False 
scroll_right = False 
scroll = 0 
scroll_speed = 1 

# CARICAMENTO IMMAGINI
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

# METTERE LE IMMAGINI IN UNA LISTA
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png') 
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) 
    img_list.append(img) 

# CARICAMENTO IMMAGINI DEI BOTTONI
save_img = pygame.image.load('img/button/SALVA.png').convert_alpha() 
load_img = pygame.image.load('img/button/CARICA.png').convert_alpha() 

# CREAZIONE LISTA DI LISTE PER I DATI DEL LIVELLO
world_data = [] 
for row in range (ROWS) : 
    r = [-1] * MAX_COLS 
    world_data.append(r)

# CREAZIONE TERRENO BASE
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0 

#DEFINIZIONE FONT
font = pygame.font.SysFont('Future', 30)

# DEFINIZIONE COLORI
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#FUNZIONE PER SCRIVERE SU SCHERMO
def draw_text(text, font, text_col, x, y): 
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y)) 

# FUNZIONI PER IL POSIZIONARE LE IMMAGINI DEL BACKGROUND
def posiziona_bg():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for x in range (4): 
        screen.blit(sky_img, ((x * width) - scroll * 0.5, 0)) 
        screen.blit(mountain_img, ((x * width) - scroll * 0.6 , SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

# FUNZIONE PER disegnare griglia
def disegna_griglia():
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

#FUNZIONE PER POSIZIONARE LE IMMAGINI DEI TILE IN BASE ALLA LISTA world_data
def posiziona_world():
    for y, row in enumerate(world_data): 
        for x, tile in enumerate(row): 
            if tile >= 0: 
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE)) 

#CREAZIONE BOTTONI SALVATAGGIO E CARICAMENTO
save_button = Bottone(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN -50, save_img, 1) 
load_button = Bottone(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN -50, load_img, 1) 

#CREAZIONE  DEI BOTTONI PER LE IMMAGINI DEI TILE
button_list = []
button_col = 0 
button_row = 0
for i in range(len(img_list)): 
    tile_button = Bottone(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1) 
    button_list.append(tile_button) 
    button_col += 1 
    if button_col == 3: 
        button_row += 1 
        button_col = 0 

# ------------------------------------ MAIN ----------------------------------------

#INIZIALIZZAZIONE
run =  True
while run:

    # CONTROLLO DEL FRAME RATE
    clock.tick(FPS)

    # POSIZIONA BACKGROUND
    posiziona_bg()
    disegna_griglia()
    posiziona_world()
    draw_text(f'Livello: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    
    # SALVATAGGIO E CARICAMENTO DEI DATI --> USO LIBRERIA CSV --> APPROFONDIRE
    # SALVATAGGIO DEI DATI
    if save_button.draw(screen): 
        # SALVATAGGIO DEI DATI
        with open(f'levels/level{level}_data.csv', 'w', newline='') as csvfile: 
            writer = csv.writer(csvfile, delimiter=',') 
            for row in world_data: 
                writer.writerow(row) 
    # CARICAMENTO DEI DATI
    if load_button.draw(screen): 
        # CARICAMENTO DEI DATI
        scroll = 0 
        with open(f'levels/level{level}_data.csv', newline='') as csvfile: 
            reader = csv.reader(csvfile, delimiter=',') 
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # DISEGNA BOTTONI
    load_button.draw(screen)            

    #DISEGNA PANNELLO LATERALE PER LE IMMAGINI DEI TILE (QUI ALTRIMENTI SI VEDREBBERO SOPRA LE IMMAGINI DEL BACKGROUND)
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # DISEGNA BOTTONI TILE E MECCANISMO DI SELEZIONE DEL TILE
    button_count = 0
    for button_count, i in enumerate(button_list): 
        if i.draw(screen): 
            current_tile = button_count

    # EVIDENZIA IL TILE SELEZIONATO
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # SCROLLING DELLA MAPPA
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed 
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed 

    # AGGIUNGERE NUOVI TILE ALLO SCHERMO (CLICCANDO)
    pos = pygame.mouse.get_pos() 
    x = (pos[0] + scroll) // TILE_SIZE 
    y = pos[1] // TILE_SIZE 
    #controllo che le coordinate siano dentro allo schermo di gioco
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT: 
        #aggiornamento della cella con il tile corrente
        if pygame.mouse.get_pressed()[0] == 1: 
            if world_data[y][x] != current_tile: 
                world_data[y][x] = current_tile 
        if pygame.mouse.get_pressed()[2] == 1: 
            world_data[y][x] = -1 
        
    #print(x, y) --> STAMPA CELLA A CUI VIENE PUNTATO IL MOUSE

    # CONTROLLO DEGLI EVENTI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # COMANDI (quando vengono premuti i tasti)
        if event.type == pygame.KEYDOWN:
            # INCREMENTO DEL LIVELLO
            if event.key == pygame.K_UP:
                level += 1
            # DECREMENTO DEL LIVELLO
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            # SCROLLING DELLO SCHERMO
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            # SCROLLING VELOCIZZATO
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5  

        # COMANDI (quando vengono rilasciati i tasti)
        if event.type == pygame.KEYUP:
            # SCROLLING DELLO SCHERMO
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            # SCROLLING VELOCIZZATO
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1


    # AGGIORNAMENTO IN BASE AGLI EVENTI
    pygame.display.update()

pygame.quit()