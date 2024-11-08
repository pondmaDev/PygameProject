import pygame
import src.utils.debug_section as debug_section

class World:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

         # Try to load the background image, create white surface if failed
        try:
            self.bg_image = pygame.image.load('assets/Image/Background/main_background.png').convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (screen_width, screen_height * 2))
            self.using_image = True
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load background image. Using white background instead. Error: {e}")
            # Create a white surface as fallback
            self.bg_image = pygame.Surface((screen_width, screen_height * 2))
            self.bg_image.fill((255, 255, 255))  # RGB for white
            self.using_image = False
        
        self.bg_rect = self.bg_image.get_rect()
        self.scroll = 0
        self.tiles = []

    def update(self, game_speed):
        self.scroll += game_speed
        if self.scroll >= self.bg_rect.height:
            self.scroll = 0

    def draw(self, screen):
        for i in range(3):
            screen.blit(self.bg_image, (0, -self.bg_rect.height + i * self.bg_rect.height + self.scroll))