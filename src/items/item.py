import pygame
import random
from src.utils.debug_section import debug

class Item:
    def __init__(
        self, 
        lane: int, 
        color: tuple = (0, 255, 0), 
        is_good: bool = True, 
        size: int = 40,
        fall_speed: float = 5,  # Base fall speed
        level: int = 1  # Game level
    ):
        """
        Initialize an item in the game
        
        Args:
            lane (int): The lane the item is in
            color (tuple): RGB color of the item
            is_good (bool): Whether the item is beneficial
            size (int): Size of the item
            fall_speed (float): Base speed at which the item falls
            level (int): Current game level
        """
        self.lane = lane
        self.x = 0  # Will be set by spawner
        self.y = 0  # Will be set by spawner
        self.color = color
        self.is_good = is_good
        self.size = size
        
        # Calculate dynamic fall speed based on level
        self.base_speed = fall_speed
        self.level = level
        self.speed = self._calculate_speed()

    def _calculate_speed(self) -> float:
        """
        Calculate dynamic fall speed based on level with more aggressive progression
        
        Returns:
            float: Calculated fall speed
        """
        # Base speed increases exponentially with level
        # Adjust these multipliers to fine-tune difficulty progression
        base_speed_multiplier = 1.0  # Starting point
        level_speed_multiplier = 1 + (self.level * 0.5)  # 50% speed increase per level
        
        # Optional: Add some randomness to speed variation
        speed_variation = random.uniform(0.9, 1.1)
        
        return self.base_speed * level_speed_multiplier * speed_variation

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
            
            # Update position with dynamic speed
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
        Draw the item on the screen with dynamic size
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        pygame.draw.rect(
            screen, 
            self.color, 
            (self.x - self.size // 2, self.y, self.size, self.size)
        )