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
            
class CharacterController:
    def __init__(self, character, lane_manager, settings):
        self.character = character
        self.lane_manager = lane_manager
        self.settings = settings

    def handle_input(self, keys_pressed):
        """Handle lane switching based on key presses."""
        if not (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT]):
            self.lane_manager.can_switch = True  # Reset the switch flag when keys are released
        
        if keys_pressed[pygame.K_LEFT] and self.lane_manager.can_switch:
            if self.lane_manager.switch_lane(-1):
                self.character.is_switching_lanes = True
                self.character.target_x = self.lane_manager.get_current_lane_position()
        
        elif keys_pressed[pygame.K_RIGHT] and self.lane_manager.can_switch:
            if self.lane_manager.switch_lane(1):
                self.character.is_switching_lanes = True
                self.character.target_x = self.lane_manager.get_current_lane_position()

    def update(self):
        """Update the character's position."""
        if self.character.is_switching_lanes:
            self._update_position()

    def _update_position(self):
        """Update the character's position during lane switching."""
        dx = self.character.target_x - self.character.x
        if abs(dx) < self.settings.character_speed:
            self.character.x = self.character.target_x
            self.character.is_switching_lanes = False
        else:
            move_direction = 1 if dx > 0 else -1
            self.character.x += move_direction * self.settings.character_speed

    def move_towards_target(self, target_x, speed):
        """Smoothly move the character towards a target x position."""
        current_x = self.character.x
        distance = target_x - current_x

        if abs(distance) < speed:
            self.character.x = target_x
            self.character.is_switching_lanes = False
        else:
            direction = 1 if distance > 0 else -1
            self.character.x += speed * direction