import pygame
from typing import TYPE_CHECKING
from src.utils.debug_section import debug
if TYPE_CHECKING:
    from src.system.lane_system import LaneManager  
    from src.character.character import Character  
    from config.setting import Settings  

class CharacterController:
    def __init__(
        self, 
        character: 'Character', 
        lane_manager: 'LaneManager', 
        settings: 'Settings'
    ):
        """
        Initialize the character controller.

        Args:
            character: The game character being controlled
            lane_manager: Manages lane switching logic
            settings: Game settings containing speed and other parameters
        """
        self.character = character
        self.lane_manager = lane_manager
        self.settings = settings
        self.lane_switch_start_time = 0
        self.lane_switch_duration = 0.2  # Duration of lane switch in seconds
        self.is_lane_switch_in_progress = False
        
        # New attributes to control lane switching
        self.lane_switch_start_time = 0
        self.lane_switch_duration = 0.2  # Duration of lane switch in seconds
        self.is_lane_switch_in_progress = False

    def handle_input(self, keys_pressed):
        if not (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT]):
            self.lane_manager.can_switch = True  # Reset the switch flag when keys are released
        
        if keys_pressed[pygame.K_LEFT] and self.lane_manager.can_switch:
            if self.lane_manager.switch_lane(-1):
                self._start_lane_switch()
        
        elif keys_pressed[pygame.K_RIGHT] and self.lane_manager.can_switch:
            if self.lane_manager.switch_lane(1):
                self._start_lane_switch()
    
    def _start_lane_switch(self):
        """
        Initialize lane switching process
        """
        # Calculate precise lane center accounting for character width
        target_x = self.lane_manager.get_lane_center(self.lane_manager.current_lane, self.character.width)
        self.character.target_x = target_x
        self.is_lane_switch_in_progress = True
        self.lane_switch_start_time = pygame.time.get_ticks()

        debug.log('movement', 
            f"Lane Switch Details:\n"
            f"  Current Lane: {self.lane_manager.current_lane}\n"
            f"  Current Position: {self.character.x}\n"
            f"  Target Position: {target_x}\n"
            f"  Character Width: {self.character.width}"
        )

        self.character.is_switching_lanes = True
        
    def update(self, dt: float, game_speed: float = None):
        """
        Update the character's position during lane switching.
        
        Args:
            dt (float): Delta time since last frame
            game_speed (float, optional): Game speed to adjust movement
        """
        # Update game speed if provided
        if game_speed is not None:
            self.game_speed = game_speed

        # Check and update lane switching state
        if self.is_lane_switch_in_progress:
            self._update_lane_switch(dt)

        # Prevent continuous movement after lane switch
        if not self.is_lane_switch_in_progress:
            self.character.is_switching_lanes = False

    def _update_lane_switch(self, dt: float):
        """
        Smoothly update character position during lane switching.
        
        Args:
            dt (float): Delta time since last frame
        """
        # Calculate elapsed time
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.lane_switch_start_time) / 1000.0
        
        # Calculate movement progress
        progress = min(elapsed_time / self.lane_switch_duration, 1.0)
        
        # Use a more precise easing function
        smooth_progress = self._cubic_ease_in_out(progress)
        
        # Interpolate position with more precise calculation
        start_x = self.character.x
        end_x = self.lane_manager.get_lane_center(
            self.lane_manager.current_lane, 
            self.character.width
        )
        
        # Calculate new position
        new_x = start_x + (end_x - start_x) * smooth_progress
        
        # Set character position
        self.character.x = new_x
        
        # End lane switching with precise positioning
        if progress >= 1.0:
            self.character.force_position(end_x)
            self.is_lane_switch_in_progress = False
            self.character.is_switching_lanes = False
    
    def _cubic_ease_in_out(self, t: float) -> float:
        """
        Cubic ease-in-out interpolation for smoother movement
        
        Args:
            t (float): Progress from 0 to 1
        
        Returns:
            float: Interpolated progress
        """
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2

    def set_game_speed(self, speed: float):
        """
        Set the game speed multiplier
        
        Args:
            speed (float): Game speed multiplier
        """
        self.game_speed = speed
    
    