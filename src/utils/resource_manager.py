import os
import pygame
from src.utils.debug_section import debug

class ResourceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of ResourceManager
        """
        if not hasattr(cls, '_instance') or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # Prevent re-initialization
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        # Initialize resources dictionaries
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        
        # Default screen dimensions
        self.screen_width = 800  # Default width
        self.screen_height = 600  # Default height
        
        # Base path for resources
        self.base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        
        # Load resources
        self.load_resources()
        
        self._initialized = True

    def set_screen_dimensions(self, width, height):
        """Set screen dimensions for resource scaling."""
        self.screen_width = width
        self.screen_height = height
        
        # Reload background with new dimensions
        self.reload_background()
    
    def reload_background(self):
        """Reload background image with current screen dimensions"""
        try:
            background_path = 'assets/Image/Background/background-image.png'
            if os.path.exists(background_path):
                background_image = pygame.image.load(background_path).convert_alpha()
                background_image = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))
                self.images['main_background'] = background_image
                debug.log('resources', "Background image reloaded with new dimensions")
        except Exception as e:
            debug.log('resources', f"Failed to reload background: {e}")

    def load_resources(self):
        """Load all game resources."""
        image_resources = {
            'character_idle': {
                'path': 'assets/Image/Character/Idle/knightt.png', 
                'size': (100, 100)
            },
            'character_run': {
                'path': 'assets/Image/Character/running/running1.png', 
                'size': (50, 50)
            },
            'main_background': {
                'path': 'assets/Image/Background/background-image.png', 
                'size': (self.screen_width, self.screen_height)
            },
            'blue_item': {
                'path': 'assets/Image/items/good_thing.jpg', 
                'size': (30, 30),
                'fallback_color': (0, 0, 255)
            },
            'green_item': {
                'path': 'assets/Image/items/tressure_thing.jpg', 
                'size': (30, 30),
                'fallback_color': (0, 255, 0)
            },
            'red_item': {
                'path': 'assets/Image/items/bad_thing.jpg', 
                'size': (30, 30),
                'fallback_color': (255, 0, 0)
            }
        }
        
        sound_resources = {
            'collect': 'assets/sounds/collect-sound.m4a',
            'hit': 'assets/sounds/hit-sound.m4a'
        }
        
        for key, resource in image_resources.items():
         self.load_image(key, resource['path'], resource.get('size'))
        self.load_sounds(sound_resources)

    def load_images(self, image_resources):
        """
        Load multiple images with optional fallback mechanism.
        
        Args:
            image_resources (dict): Dictionary of image resources to load
        """
        for key, resource in image_resources.items():
            path = resource['path']
            size = resource.get('size')
            fallback_color = resource.get('fallback_color')
            
            self.load_image(key, path, size, fallback_color)
        
        try:
            # Remove the problematic lines
            # idle_image = self.resource_manager.get_image('character_idle')
            # run_image = self.resource_manager.get_image('character_run')
            # Instead, directly use the loaded images
            idle_image = self.get_image('character_idle')
            run_image = self.get_image('character_run')
            
            # Store images with multiple key types
            self.idle_image = idle_image
            self.run_image = run_image
        except KeyError as e:
            debug.log('character', f"Image loading error: {e}")
            # Use fallback methods or default images

    def load_image(self, key, path, size=None, fallback_color=None):
        debug.log('resources', f"Attempting to load image: {key} from {path}")
        
        # Ensure key is always a string
        key = str(key)
        
        if not os.path.exists(path):
            debug.log('resources', f"File not found: {path}")
            
            if fallback_color and size:
                debug.log('resources', f"Creating fallback surface for {key}")
                fallback_surface = pygame.Surface(size)
                fallback_surface.fill(fallback_color)
                self.images[key] = fallback_surface
            return False
        
        try:
            image = pygame.image.load(path).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            
            # Store only with string key
            self.images[key] = image
            
            debug.log('resources', f"Successfully loaded image: {key}")
            return True
        except Exception as e:
            debug.log('resources', f"Failed to load image {key}: {e}")
            return False

    def load_sounds(self, sound_resources):
        """
        Load multiple sound files.
        
        Args:
            sound_resources (dict): Dictionary of sound resources to load
        """
        for key, path in sound_resources.items():
            self.load_sound(key, path)

    def load_sound(self, key, path):
        """
        Load a single sound file with error handling.
        
        Args:
            key (str): Unique identifier for the sound
            path (str): Path to the sound file
        
        Returns:
            bool: True if sound loaded successfully, False otherwise
        """
        if not os.path.isfile(path):
            debug.log('resources', f"No sound file '{path}' found.")
            return False
        
        try:
            self.sounds[key] = pygame.mixer.Sound(path)
            debug.log('resources', f"Loaded sound: {key}")
            return True
        except Exception as e:
            debug.log('resources', f"Failed to load sound {key}: {e}")
            return False

    def get_image(self, key):
        """
        Retrieve an image by key with robust error handling
        
        Args:
            key (str or tuple): Key of the image to retrieve
        
        Returns:
            pygame.Surface: The requested image
        
        Raises:
            KeyError: If image is not found
        """
        # Ensure key is a string
        key = str(key)
        
        # Direct key lookup
        image = self.images.get(key)
        if image is not None:
            return image
        
        # If not found, raise a clear error
        raise KeyError(f"Image with key '{key}' not found in resources")

    def get_sound(self, key):
        """
        Retrieve a sound by key.
        
        Args:
            key (str): Key of the sound to retrieve
        
        Returns:
            pygame.mixer.Sound or None: The requested sound
        """
        return self.sounds.get(key)

    def play_sound(self, sound_key):
        """
        Play a sound by key.
        
        Args:
            sound_key (str): Key of the sound to play
        """
        sound = self.sounds.get(sound_key)
        if sound:
            sound.play()
        else:
            debug.log('game', f"Sound not found: {sound_key}")