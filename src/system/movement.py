import pygame
from src.character.character import Character
# src/movement.py
import pygame

def move_character(character, keys_pressed, lane_manager, settings):
    """
    Legacy function for character movement
    
    :param character: The character object to move
    :param keys_pressed: Pygame key press state
    :param lane_manager: Lane management object
    :param settings: Game settings
    """
    # Check for lane switching
    if not (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT]):
        lane_manager.can_switch = True  # Reset the switch flag when keys are released
    
    if keys_pressed[pygame.K_LEFT] and lane_manager.can_switch:
        if lane_manager.switch_lane(-1):
            character.is_switching_lanes = True
            character.target_x = lane_manager.get_current_lane_position()
    
    elif keys_pressed[pygame.K_RIGHT] and lane_manager.can_switch:
        if lane_manager.switch_lane(1):
            character.is_switching_lanes = True
            character.target_x = lane_manager.get_current_lane_position()
    
    # Update character position during lane switching
    if character.is_switching_lanes:
        dx = character.target_x - character.x
        if abs(dx) < settings.character_speed:
            character.x = character.target_x
            character.is_switching_lanes = False
        else:
            move_direction = 1 if dx > 0 else -1
            character.x += move_direction * settings.character_speed