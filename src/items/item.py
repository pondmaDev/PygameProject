import random
from typing import Tuple
from src.utils.debug_section import debug

class ItemType:
    """Enum-like class to define item types"""
    GOOD_GREEN = {
        'color': (0, 255, 0),
        'is_good': True,
        'weight': 3,
        'size': 40
    }
    GOOD_BLUE = {
        'color': (0, 0, 255),
        'is_good': True,
        'weight': 3,
        'size': 40
    }
    BAD_RED = {
        'color': (255, 0, 0),
        'is_good': False,
        'weight': 1,
        'size': 40
    }

class Item:
    """Represents a game item that falls from the top of the screen"""
    
    def __init__(
        self, 
        lane: int, 
        color: Tuple[int, int, int] = ItemType.GOOD_GREEN['color'], 
        is_good: bool = True, 
        size: int = 40,
        fall_speed: float = 5,
        level: int = 1
    ):
        """
        Initialize an item with specific properties
        
        Args:
            lane (int): Lane the item is in
            color (Tuple[int,int,int]): RGB color of the item
            is_good (bool): Whether the item is beneficial
            size (int): Size of the item
            fall_speed (float): Base speed of falling
            level (int): Current game level
        """
        self.lane = lane
        self.x = 0  # Will be set by spawner
        self.y = 0  # Will be set by spawner
        self.color = color
        self.is_good = is_good
        self.size = size
        
        self.base_speed = fall_speed
        self.level = level
        self.speed = self._calculate_dynamic_speed()

    def _calculate_dynamic_speed(self) -> float:
        """
        Calculate fall speed with level-based progression
        
        Returns:
            float: Dynamically calculated speed
        """
        try:
            # Exponential speed increase with level
            level_multiplier = 1 + (self.level * 0.5)
            speed_variation = random.uniform(0.9, 1.1)
            
            calculated_speed = self.base_speed * level_multiplier * speed_variation
            
            # Ensure a minimum speed
            return max(2.0, calculated_speed)
        except Exception as e:
            debug.error('items', f"Speed calculation error: {e}")
            return self.base_speed

    def update(self, game_speed: float, screen_height: int) -> bool:
        """
        Update item position with error handling
        
        Args:
            game_speed (float): Current game speed
            screen_height (int): Screen height
        
        Returns:
            bool: Whether item is still on screen
        """
        try:
            safe_game_speed = max(0.1, game_speed)
            self.y += self.speed * safe_game_speed
            return self.y < screen_height
        except Exception as e:
            debug.error('items', f"Item update error: {e}")
            return False

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
        import pygame
        pygame.draw.rect(
            screen, 
            self.color, 
            (self.x - self.size // 2, self.y, self.size, self.size)
        )