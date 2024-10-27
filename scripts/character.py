import pygame

class Character:
    def __init__(self, x, y, width, height, color, idle_image_paths, running_image_paths):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.idle_images = [pygame.image.load(path) for path in idle_image_paths]
        self.running_images = [pygame.image.load(path) for path in running_image_paths]
        self.frame_index = 0
        self.is_running = False
        self.animation_timer = 0  # Timer to control animation speed

    def draw(self, screen):
        if self.is_running:
            screen.blit(self.running_images[self.frame_index], self.rect)
        else:
            screen.blit(self.idle_images[self.frame_index], self.rect)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        if self.is_running:
            self.animation_timer += 1
            if self.animation_timer >= 5:  # Change image every 5 frames
                self.frame_index = (self.frame_index + 1) % len(self.running_images)
                self.animation_timer = 0
        else:
            self.frame_index = 0  # Reset to the first idle image

    def set_running(self, running):
        self.is_running = running