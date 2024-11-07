import pygame
import random

class Item:
    def __init__(self, lane, color, is_good=True):
        self.lane = lane
        self.lane_width = 800 // 3  # Screen width divided by number of lanes
        self.x = (lane * self.lane_width) + (self.lane_width // 2)
        self.y = -50  # Start above the screen
        self.size = 30
        self.color = color
        self.is_good = is_good

    def fall(self): #This function make item fall
        self.y += self.speed

    
    def update(self, game_speed):
        # Update position based on game speed
        self.y += game_speed


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.size//2, self.y, self.size, self.size))
        
    def get_points(self):  # Renamed from get_points(self, color) to get_points(self)
        if self.color == (0, 0, 255):  # Blue
            return 1
        elif self.color == (0, 255, 0):  # Green
            return 5
        elif self.color == (255, 0, 0):  # Red
            return -3
        else:
            return 0