import pygame

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