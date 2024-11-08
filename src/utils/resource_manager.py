# resource_manager.py
import pygame
from src.utils.debug_section import debug
import os

class ResourceManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if ResourceManager._instance is not None:
            raise Exception("ResourceManager is a singleton class!")
        
        ResourceManager._instance = self
        self.screen_width = 800  # Default values
        self.screen_height = 600
        self.images = {}
        self.sounds = {}
        self.load_resources()

    def set_screen_dimensions(self, width, height):
        self.screen_width = width
        self.screen_height = height

    def load_resources(self):
        # Define image resources with fallback colors
        image_resources = {
            'character_idle': ('assets/Image/Character/Idle/Idle_down.png', (50, 50)),
            'character_run': ('assets/Image/Character/running/running1.png', (50, 50)),
            'main_background': ('assets/Image/Background/background-image.png', (self.screen_width, self.screen_height)),
            'blue_item': ('assets/Image/items/good_thing.jpg', (30, 30), (0, 0, 255)),
            'green_item': ('assets/Image/items/tressure_thing.jpg', (30, 30), (0, 255, 0)),
            'red_item': ('assets/Image/items/bad_thing.jpg', (30, 30), (255, 0, 0))
        }
        
        self.load_images(image_resources)
        self.load_sounds({
            'collect': 'data/raw/sounds/collect.wav',
            'hit': 'data/raw/sounds/hit.wav'
        })

    def load_images(self, image_resources):
        for key, (path, size, *fallback_color) in image_resources.items():
            if self.load_image(key, path, size, fallback_color[0] if fallback_color else None):
                debug.log('resources', f"Loaded image: {key}")
            else:
                debug.log('resources', f"Failed to load image {key}")

    def load_sounds(self, sound_resources):
        for key, path in sound_resources.items():
            if self.load_sound(key, path):
                debug.log('resources', f"Loaded sound: {key}")
            else:
                debug.log('resources', f"Failed to load sound {key}")

    def get_image(self, key):
        return self.images.get(key)

    def load_image(self, key, path, size=None, fallback_color=None):
        if not os.path.isfile(path):
            debug.log('resources', f"No file '{path}' found.")
            if fallback_color:
                fallback_surface = pygame.Surface(size)
                fallback_surface.fill(fallback_color)
                self.images[key] = fallback_surface
                debug.log('resources', f"Created fallback color for {key}")
            return False
        
        try:
            image = pygame.image.load(path).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            self.images[key] = image
            return True
        except Exception as e:
            debug.log('resources', f"Failed to load image {key}: {e}")
            return False

    def get_sound(self, key):
        return self.sounds.get(key)

    def load_sound(self, key, path):
        if not os.path.isfile(path):
            debug.log('resources', f"No file '{path}' found.")
            return False
        
        try:
            self.sounds[key] = pygame.mixer.Sound(path)
            return True
        except Exception as e:
            debug.log('resources', f"Failed to load sound {key}: {e}")
            return False

    def play_sound(self, sound_key):
        if sound_key in self.sounds:
            self.sounds[sound_key].play()
        else:
            debug.log('game', f"Sound not found: {sound_key}")