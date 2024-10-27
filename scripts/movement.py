import pygame
from .character import Character

SPEED = 0.5 # Editting speed of character

def move_character(character, keys_pressed, screen_width, screen_height):
    if keys_pressed[pygame.K_LEFT]:
        character.x -= SPEED
        character.set_running(True)
    elif keys_pressed[pygame.K_RIGHT]:
        character.x += SPEED
        character.set_running(True)
    elif keys_pressed[pygame.K_UP]:
        character.y -= SPEED
        character.set_running(True)
    elif keys_pressed[pygame.K_DOWN]:
        character.y += SPEED
        character.set_running(True)
    else:
        character.set_running(False)  # Stop running when no key is pressed

    character.x = max(0, min(character.x, screen_width - character.width))
    character.y = max(0, min(character.y, screen_height - character.height))