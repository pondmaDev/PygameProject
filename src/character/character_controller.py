import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.system.lane_system import LaneManager  
    from src.character.character import Character  
    from config.setting import Settings  

import pygame

class CharacterController:
    def __init__(
        self, 
        character: 'Character', 
        lane_manager: 'LaneManager', 
        settings: 'Settings'
    ):
        """
        Initialize the character controller.

        Args:
            character: The game character being controlled
            lane_manager: Manages lane switching logic
            settings: Game settings containing speed and other parameters
        """
        self.game_speed = 1.0  # Default game speed
        self.character = character
        self.lane_manager = lane_manager
        self.settings = settings

    def handle_input(self, keys_pressed):
        """
        Handle lane switching based on key presses.
        
        Args:
            keys_pressed: Pygame key state dictionary
        """
        if not (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT]):
            self.lane_manager.can_switch = True  # Reset the switch flag when keys are released
        
        if keys_pressed[pygame.K_LEFT] and self.lane_manager.can_switch:
            if self.lane_manager.switch_lane(-1):
                self.character.is_switching_lanes = True
                self.character.target_x = self.lane_manager.current_lane_position
        
        elif keys_pressed[pygame.K_RIGHT] and self.lane_manager.can_switch:
            if self.lane_manager.switch_lane(1):
                self.character.is_switching_lanes = True
                self.character.target_x = self.lane_manager.current_lane_position  # Use property
    
    def update(self, dt: float, game_speed: float = None):
        """
        Update the character's position during lane switching.
        
        Args:
            dt (float): Delta time since last frame
            game_speed (float, optional): Game speed to adjust movement
        """
        # Update game speed if provided
        if game_speed is not None:
            self.game_speed = game_speed
        
        # If character is switching lanes, update position
        if self.character.is_switching_lanes:
            self._update_position(dt)
        
        # Add basic movement (if needed)
        # Use character's speed or settings speed
        movement_speed = getattr(self.character, 'speed', self.settings.character_speed)
        self.character.x += movement_speed * self.game_speed * dt

    def _update_position(self, dt: float):
        """
        Update the character's position during lane switching.
        Smoothly moves the character to the target x position.
        
        Args:
            dt (float): Delta time since last frame
        """
        # Adjust speed based on game speed and delta time
        adjusted_speed = self.settings.character_speed * self.game_speed * dt

        dx = self.character.target_x - self.character.x
        if abs(dx) < adjusted_speed:
            # Snap to target if very close
            self.character.x = self.character.target_x
            self.character.is_switching_lanes = False
        else:
            # Move towards target
            move_direction = 1 if dx > 0 else -1
            self.character.x += move_direction * adjusted_speed

    def move_towards_target(self, target_x: float, speed: float, dt: float):
        """
        Smoothly move the character towards a target x position.
        
        Args:
            target_x: The target x coordinate
            speed: Movement speed
            dt: Delta time since last frame
        """
        current_x = self.character.x
        distance = target_x - current_x
        
        # Adjust speed with delta time
        adjusted_speed = speed * dt

        if abs(distance) < adjusted_speed:
            # Snap to target if very close
            self.character.x = target_x
            self.character.is_switching_lanes = False
        else:
            # Move towards target
            direction = 1 if distance > 0 else -1
            self.character.x += adjusted_speed * direction

    def set_game_speed(self, speed: float):
        """
        Set the game speed multiplier
        
        Args:
            speed (float): Game speed multiplier
        """
        self.game_speed = speed