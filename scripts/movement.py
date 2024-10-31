import pygame
from scripts.character import Character

def move_character(character, keys_pressed, screen_width, screen_height, settings):  # Add settings parameter
    speed = settings.character_speed
    if keys_pressed[pygame.K_LEFT]:
        character.x -= speed
        character.set_running(True)
    elif keys_pressed[pygame.K_RIGHT]:
        character.x += speed
        character.set_running(True)
    elif keys_pressed[pygame.K_UP]:
        character.y -= speed
        character.set_running(True)
    elif keys_pressed[pygame.K_DOWN]:
        character.y += speed
        character.set_running(True)
    else:
        character.set_running(False)  # Stop running when no key is pressed

    character.x = max(0, min(character.x, screen_width - character.width))
    character.y = max(0, min(character.y, screen_height - character.height))