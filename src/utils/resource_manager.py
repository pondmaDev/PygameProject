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
                'size': (80, 80)
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
        for key, resource in image_resources.items():
         self.load_image(key, resource['path'], resource.get('size'))
        
        sound_resources = {
            'collect_good_item': 'assets/sounds/effect/good_thing.mp3',  # Positive sound
            'collect_bad_item': 'assets/sounds/effect/bad_thing.mp3',    # Negative sound
            'win_sound' : 'assets/sounds/effect/bad_thing.mp3',
            'lost_sound' : 'assets/sounds/effect/losing.mp3'
        }
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

    def load_sounds(self, sound_resources):
        """
        Load multiple sound files with error handling
        
        Args:
            sound_resources (dict): Dictionary of sound resources to load
        """
        for key, path in sound_resources.items():
            self.load_sound(key, path)

    def load_sound(self, key, path):
        """
        Load a single sound file with comprehensive error handling
        
        Args:
            key (str): Unique identifier for the sound
            path (str): Path to the sound file
        
        Returns:
            bool: True if sound loaded successfully, False otherwise
        """
        # Ensure pygame mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        if not os.path.exists(path):
            debug.warning('resources', f"Sound file not found: {path}")
            return False
        
        try:
            # Load sound with volume control
            sound = pygame.mixer.Sound(path)
            
            # Store the sound
            self.sounds[key] = sound
            
            debug.log('resources', f"Successfully loaded sound: {key}")
            return True
        
        except Exception as e:
            debug.warning('resources', f"Failed to load sound {key}: {e}")
            return False

    def play_sound(self, sound_key, volume=0.5):
        """
        Play a sound with volume control and error handling
        
        Args:
            sound_key (str): Key of the sound to play
            volume (float): Volume of the sound (0.0 to 1.0)
        """
        try:
            # Retrieve the sound
            sound = self.sounds.get(sound_key)
            
            if sound is None:
                debug.warning('resources', f"Sound not found: {sound_key}")
                return
            
            # Set volume and play
            sound.set_volume(volume)
            sound.play()
        
        except Exception as e:
            debug.error('resources', f"Error playing sound {sound_key}: {e}")