import pygame
import random
from typing import List, Optional
from src.utils.debug_section import debug

class Item:
    def __init__(
        self, 
        lane: int, 
        color: tuple = (0, 255, 0), 
        is_good: bool = True, 
        size: int = 30
    ):
        """
        Initialize an item in the game
        
        Args:
            lane (int): The lane the item is in
            color (tuple): RGB color of the item
            is_good (bool): Whether the item is beneficial
            size (int): Size of the item
        """
        self.lane = lane
        self.x = 0  # Will be set by spawner
        self.y = 0  # Will be set by spawner
        self.color = color
        self.is_good = is_good
        self.size = size
        self.speed = 5  # Configurable fall speed

    def update(self, game_speed: float, screen_height: int) -> bool:
        """
        Update item's position with robust error handling
        
        Args:
            game_speed (float): Current game speed
            screen_height (int): Height of the game screen
        
        Returns:
            bool: Whether item is still on screen
        """
        try:
            # Validate inputs
            safe_game_speed = max(0.1, game_speed)
            
            # Update position
            self.y += self.speed * safe_game_speed
            
            # Check if item is still on screen
            return self.y < screen_height
        
        except Exception as e:
            debug.error('items', f"Error updating item position: {e}")
            return False  # Remove item if update fails

    def get_points(self) -> int:
        """
        Calculate points based on item type
        
        Returns:
            int: Points for collecting the item
        """
        return 10 if self.is_good else -5

    def draw(self, screen):
        """
        Draw the item on the screen
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        pygame.draw.rect(
            screen, 
            self.color, 
            (self.x - self.size // 2, self.y, self.size, self.size)
        )