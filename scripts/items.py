import pygame
import random

class Item:
    def __init__(self, lane, color, size=50, is_good = True):
        self.lane = lane
        self.color = color
        self.size = size
        self.x = lane * (800 // 3) + (800 // 3 - size) // 2  # Center the item in the lane
        self.y = 0  # Start from the top of the screen
        self.speed = 5  # Falling speed
        self.points = self.get_points(color) # initial color as points
        self.is_good = is_good

    def fall(self): #This function make item fall
        self.y += self.speed

    def draw(self, screen): #Draw items
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
    def get_points(self, color): # set points for color of square
        if color == (0, 0, 255):  # Blue
            return 1
        elif color == (0, 255, 0):  # Green
            return 5
        elif color == (255, 0, 0):  # Red
            return -3
        else:
            return 0