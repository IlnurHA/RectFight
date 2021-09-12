import pygame
import func

mouse = pygame.sprite.Sprite()
mouse.image = func.load_image('arrow.png')

mouse_clicked = pygame.sprite.Sprite()
mouse_clicked.image = func.load_image('arrow_clicked.png')

button_sprite = []

button_sprite_nonclicked = pygame.sprite.Sprite()
button_sprite_nonclicked.image = func.load_image('button-nonclicked.png')

button_sprite_clicked = pygame.sprite.Sprite()
button_sprite_clicked.image = func.load_image('button-clicked.png')
