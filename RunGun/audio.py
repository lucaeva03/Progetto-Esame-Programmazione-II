import pygame

pygame.mixer.init() 

# CARICAMENTO FILE AUDIO
pygame.mixer.music.load('audio/music.mp3') 
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000) 
jump_fx = pygame.mixer.Sound('audio/jump.mp3')
jump_fx.set_volume(0.5) 
shot_fx = pygame.mixer.Sound('audio/shot.mp3') 
shot_fx.set_volume(0.5) 
grenade_fx = pygame.mixer.Sound('audio/grenade.wav') 
grenade_fx.set_volume(0.5) 
level_completed_fx = pygame.mixer.Sound('audio/level_completed.mp3') 
level_completed_fx.set_volume(1) 
dead_fx = pygame.mixer.Sound('audio/dead.mp3') 
dead_fx.set_volume(0.8) 