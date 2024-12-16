# ------------------------------------ VARIABILI GLOBALI -------------------------------

# DEFINIZIONE COSTANTI DI GIOCO
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
FPS = 60
GRAVITA = 0.40 
SCROLL_THRESH = 200 # soglia di scorrimento della mappa
ROWS = 16 # righe mappa
COLS = 150 # colonne mappa
TILE_SIZE = SCREEN_HEIGHT // ROWS # dimensione cella, dimensione tile, dimensione icona gioco
TYLE_TYPES = 21 # numero di tipi di tile 
MAX_LEVELS = 3

# DEFINIZIONE VARIABILI DI GIOCO
screen_scroll = 0 
screen_scrool_speed = 1.5 
bg_scroll = 0 
level = 1 
start_game = False 
start_trans = False 
dead_sound_played = False 

# DEFINIZIONE VARIABILI PLAYER
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_active = False

# DEFINIZIONI COLORI
BG = (144,201,120)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)