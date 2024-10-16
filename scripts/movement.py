import pygame
from .character import Character

def move_character(character, keys_pressed, screen_width, screen_height):
    speed = 5
    if keys_pressed[pygame.K_LEFT] and character.x - speed > 0:
        character.x -= speed
    if keys_pressed[pygame.K_RIGHT] and character.x + speed + character.width < screen_width:
        character.x += speed
    if keys_pressed[pygame.K_UP] and character.y - speed > 0:
        character.y -= speed
    if keys_pressed[pygame.K_DOWN] and character.y + speed + character.height < screen_height:
        character.y += speed