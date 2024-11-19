import pygame
from src.utils.debug_section import debug
from src.utils.constant import Colors
from src.utils.resource_manager import ResourceManager

class Character:
    def __init__(
        self, 
        x, 
        y, 
        width=80,  # Default width
        height=80,  # Default height
        color='RED', 
        idle_image_key='character_idle', 
        running_image_key='character_run'
    ):
        # Get resource manager instance
        self.resource_manager = ResourceManager.get_instance()
        
        # Use the Colors dictionary to get the color tuple
        self.color = Colors.get(color)
        
        # Position and dimensions
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Image keys for resource management
        self.idle_image_key = idle_image_key
        self.run_image_key = running_image_key
        
        # Animation and state variables
        self.game_speed = 0
        self.idle_images = []
        self.running_images = []
        
        # Create default surface if no images provided
        default_surface = pygame.Surface((width, height))
        default_surface.fill(self.color)
        
        self.current_animation = [default_surface]
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        self.is_switching_lanes = False
        
        # Load character images
        self.load_character_images()

    def load_character_images(self):
        """
        Load and resize character images with comprehensive error handling
        """
        debug.log('character', "Starting to load character images")
        
        # Clear existing images
        self.idle_images = []
        self.running_images = []
        
        # Image keys
        idle_key = 'character_idle'
        run_key = 'character_run'
        
        # Try to load and resize idle image
        try:
            idle_image = self.resource_manager.get_image(idle_key)
            resized_idle = pygame.transform.scale(idle_image, (self.width, self.height))
            self.idle_images = [resized_idle]
            debug.log('character', f"Loaded and resized idle image: {idle_key}")
        except Exception as e:
            debug.warning('character', f"Error loading idle image: {e}")
            # Create fallback idle image
            fallback = pygame.Surface((self.width, self.height))
            fallback.fill(self.color)
            self.idle_images = [fallback]
        
        # Try to load and resize running image
        try:
            running_image = self.resource_manager.get_image(run_key)
            resized_running = pygame.transform.scale(running_image, (self.width, self.height))
            self.running_images = [resized_running]
            debug.log('character', f"Loaded and resized running image: {run_key}")
        except Exception as e:
            debug.warning('character', f"Error loading running image: {e}")
            # Create fallback running image
            fallback = pygame.Surface((self.width, self.height))
            fallback.fill(self.color)
            self.running_images = [fallback]
        
        # Set default animation to idle
        self.current_animation = self.idle_images
        
        debug.log('character', "Character images loading completed")

    def animate(self):
        """
        Animate character images
        Cycles through available animation frames
        """
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.animation_timer = 0

    def force_position(self, x):
        """
        Force the character to a specific x-position.
        
        Args:
            x (float): The exact x-coordinate to move to
        """
        self.x = x
        self.target_x = x

    def get_current_image(self):
        """
        Get the current animation frame
        
        Returns:
            pygame.Surface: Current animation frame
        """
        return self.current_animation[self.current_frame]

    def set_animation_state(self, is_running):
        """
        Set character animation state
        
        Args:
            is_running (bool): Whether character is running
        """
        self.current_animation = self.running_images if is_running else self.idle_images
        self.current_frame = 0
        self.animation_timer = 0
    
    def draw(self, screen):
        """
        Draw the character on the screen with resizing support
        
        Args:
            screen (pygame.Surface): The surface to draw the character on
        """
        # Get the current animation frame
        current_image = self.get_current_image()
        
        # Ensure image is scaled to current width and height
        scaled_image = pygame.transform.scale(current_image, (self.width, self.height))
        
        # Draw the character image
        screen.blit(scaled_image, (self.x, self.y))
        
        # Optional: Draw debug information
        if debug.sections.get('character', False):
            # Draw a rectangle around the character
            pygame.draw.rect(screen, Colors.RED, 
                            (self.x, self.y, self.width, self.height), 
                            2)  # 2 pixel border
            
            # Draw center point
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            pygame.draw.circle(screen, Colors.GREEN, (center_x, center_y), 3)
        
        debug.log('character', f"Drawing character at ({self.x}, {self.y})")
    
    def resize_character(self, new_width, new_height):
        """
        Dynamically resize the character
        
        Args:
            new_width (int): New width of the character
            new_height (int): New height of the character
        """
        debug.log('character', f"Resizing character to {new_width}x{new_height}")
        
        # Update dimensions
        self.width = new_width
        self.height = new_height
        
        # Reload images with new size
        self.load_character_images()