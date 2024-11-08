import pygame
from src.utils.debug_section import debug

class Character:
    def __init__(self, x, y, width, height, color, idle_images=None, running_images=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.game_speed = 0
        
        # Create default surface if no images provided
        default_surface = pygame.Surface((width, height))
        default_surface.fill(color)
        
        self.idle_images = idle_images if idle_images else [default_surface]
        self.running_images = running_images if running_images else [default_surface]
        self.current_animation = self.idle_images
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        self.is_switching_lanes = False

    def update(self, game_speed):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
        
        # Update position based on game speed

    def draw(self, screen):
        try:
            current_image = self.current_animation[self.current_frame]
            screen.blit(current_image, (self.x - self.width//2, self.y - self.height//2))
        except:
            # Fallback to drawing a rectangle if image drawing fails
            pygame.draw.rect(screen, self.color, 
                           (self.x - self.width//2, self.y - self.height//2, 
                            self.width, self.height))
    
    def load_character_images(self):
        """Load and scale character images"""
        debug.log('character', "Starting to load character images")
        
        # Clear existing images
        self.idle_images = []
        self.running_images = []
        
        # Load idle images
        for path in self.idle_image_paths:
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (50, 50))
                self.idle_images.append(image)
                debug.debug_print(f"Loaded idle image: {path}")
                debug.log('character', f"Loaded idle image: {path}")
            except Exception as e:
                debug.error_print(f"Failed to load idle image {path}: {e}")
                debug.error('character', f"Failed to load idle image {path}: {e}")
                
        # Load running images
        for path in self.running_image_paths:
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (50, 50))
                self.running_images.append(image)
                debug.debug_print(f"Loaded running image: {path}")
                debug.log('character', f"Loaded running image: {path}")
            except Exception as e:
                debug.error_print(f"Failed to load running image {path}: {e}")
                debug.error('character', f"Failed to load running image {path}: {e}")
                
        # If no images were loaded, create fallback images
        if not self.idle_images:
            fallback = pygame.Surface((50, 50))
            fallback.fill(self.RED)
            self.idle_images = [fallback]
            debug.debug_print("Using fallback idle image")
            debug.log('character', "Using fallback idle image")
            
        if not self.running_images:
            fallback = pygame.Surface((50, 50))
            fallback.fill(self.RED)
            self.running_images = [fallback]
            debug.debug_print("Using fallback running image")
            debug.log('character', "Using fallback running image")
        
        debug.log('character', "Character images loading completed")