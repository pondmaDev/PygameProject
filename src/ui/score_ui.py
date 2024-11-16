import pygame
import pygame_gui

class ScoreUI:
    def __init__(self, screen_width, screen_height):
        # Initialize Pygame GUI manager
        self.ui_manager = pygame_gui.UIManager((screen_width, screen_height))
        
        # Screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Score variables
        self.total_score = 0  # Total score accumulated
        self.visible_score = 0  # Score currently displayed
        self.score_transition_speed = 0.1  # Speed of score transition
        
        # Create Score display
        self.score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 100, screen_height // 4), (200, 50)),
            text=f'Score: {self.visible_score}',
            manager=self.ui_manager
        )
        
        # Score increase animation state
        self.is_score_animating = False
        self.target_score = 0  # Target score for animation
    
    def update(self, time_delta):
        """Update UI and handle smooth score transition"""
        # Update UI manager
        self.ui_manager.update(time_delta)
        
        # Handle smooth score transitions
        if self.is_score_animating:
            self.visible_score = self._lerp(self.visible_score, self.target_score, self.score_transition_speed)
            if abs(self.visible_score - self.target_score) < 1:  # Stop when close enough
                self.visible_score = self.target_score
                self.is_score_animating = False
            
            # Update score label
            self.score_label.set_text(f'Score: {int(self.visible_score)}')
    
    def _lerp(self, start, end, alpha):
        """Linear interpolation for smooth transitions"""
        return start + alpha * (end - start)
    
    def add_score(self, amount):
        """Add score and trigger animation"""
        self.total_score += amount
        self.target_score = self.total_score
        self.is_score_animating = True
    
    def reset_score(self):
        """Reset the score to zero"""
        self.total_score = 0
        self.visible_score = 0
        self.score_label.set_text('Score: 0')

    def draw(self, screen):
        """Draw UI elements"""
        # Draw UI manager
        self.ui_manager.draw_ui(screen)

