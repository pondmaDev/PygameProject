# src/game/world.py
import pygame
import src.utils.debug_section as debug_section

class World:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Base scroll configuration
        self.base_scroll_speed = 5.0  # Default base speed
        self.max_scroll_speed = 10.0  # Maximum scroll speed
        self.min_scroll_speed = 2.0   # Minimum scroll speed
        
        # Scroll acceleration and deceleration
        self.scroll_acceleration = 0.1
        self.current_scroll_speed = self.base_scroll_speed

        # Background image handling
        try:
            self.bg_image = pygame.image.load('assets/Image/Background/3.jpg').convert()
            self.original_bg_image = self.bg_image  # Keep original image for scaling
            self.bg_image = pygame.transform.scale(self.bg_image, (screen_width, screen_height * 2))
            self.using_image = True
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load background image. Using white background instead. Error: {e}")
            self.bg_image = pygame.Surface((screen_width, screen_height * 2))
            self.bg_image.fill((255, 255, 255))  # RGB for white
            self.using_image = False
        
        self.bg_rect = self.bg_image.get_rect()
        self.scroll = 0
        self.zoom_factor = 1.0  # Default zoom
        self.tiles = []

    def update(self, dt: float, level: int = 1, settings=None, zoom_factor: float = 1.0):
        """
        Update world scroll with level-based progression and zoom factor.
        
        Args:
            dt (float): Delta time
            level (int): Current game level
            settings (optional): Game settings object
            zoom_factor (float): Desired zoom level for the background
        """
        try:
            # Use settings to get level multiplier if provided
            level_multiplier = 1.0
            if settings:
                level_multiplier = settings.get_level_scroll_multiplier(level)
            
            target_scroll_speed = self.base_scroll_speed * level_multiplier
            
            # Smooth acceleration/deceleration
            if self.current_scroll_speed < target_scroll_speed:
                self.current_scroll_speed += self.scroll_acceleration
            elif self.current_scroll_speed > target_scroll_speed:
                self.current_scroll_speed -= self.scroll_acceleration
            
            # Clamp scroll speed
            self.current_scroll_speed = max(
                self.min_scroll_speed, 
                min(self.current_scroll_speed, self.max_scroll_speed)
            )
            
            # Increment scroll
            self.scroll += self.current_scroll_speed * dt
            
            # Reset scroll when background is fully scrolled
            if self.scroll >= self.bg_rect.height:
                self.scroll = 0
            
            # Update zoom factor and rescale background
            self.zoom_factor = zoom_factor
            self.bg_image = pygame.transform.scale(
                self.original_bg_image, 
                (int(self.screen_width * self.zoom_factor), int(self.screen_height * 2 * self.zoom_factor))
            )
            self.bg_rect = self.bg_image.get_rect()

            debug_section.debug.log('world', 
                f"World scroll update: "
                f"speed={self.current_scroll_speed:.2f}, "
                f"level_multiplier={level_multiplier:.2f}, "
                f"current_scroll={self.scroll:.2f}, "
                f"zoom_factor={self.zoom_factor:.2f}"
            )
        except Exception as e:
            debug_section.debug.error('world', f"Error updating world scroll: {e}")

    def draw(self, screen):
        """
        Draw the scrolling background with zoom effect.
        
        Args:
            screen (pygame.Surface): Screen to draw background on
        """
        try:
            # Calculate offsets for centering the zoomed image
            offset_x = (self.screen_width - self.bg_rect.width) // 2
            offset_y = (self.screen_height - self.bg_rect.height) // 2

            # Draw background tiles to create continuous scrolling effect
            for i in range(3):
                screen.blit(
                    self.bg_image, 
                    (offset_x, -self.bg_rect.height + i * self.bg_rect.height + self.scroll + offset_y)
                )
        except Exception as e:
            debug_section.debug.error('world', f"Error drawing world background: {e}")

    def set_base_scroll_speed(self, speed: float):
        """
        Manually set the base scroll speed
        
        Args:
            speed (float): New base scroll speed
        """
        self.base_scroll_speed = max(self.min_scroll_speed, min(speed, self.max_scroll_speed))

    def get_current_scroll_speed(self) -> float:
        """
        Get the current scroll speed
        
        Returns:
            float: Current scroll speed
        """
        return self.current_scroll_speed
