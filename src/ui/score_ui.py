import pygame
from src.utils.debug_section import debug
from src.game.game_state import current_game_state
class ScoreUI:
    def __init__(self, screen_width, screen_height):
        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        
        # Screen dimensions
        self.screen_width = screen_width
        
        # Score variables
        self.total_score = 0
        self.visible_score = 0
        self.score_transition_speed = 0.1
        
        # Colors
        self.text_color = (255, 215, 0)  # Gold color
        self.background_color = (0, 0, 0)  # Black background

        # Win scores for each level
        self.win_scores = {
            1: 100,
            2: 1000,
            3: 2500
        }

    def update(self, time_delta):
        """Smooth score transition"""
        # Simple linear interpolation
        if abs(self.visible_score - self.total_score) > 1:
            self.visible_score += (self.total_score - self.visible_score) * self.score_transition_speed
        else:
            self.visible_score = self.total_score
    
    def add_score(self, amount):
        """Add score"""
        self.total_score += amount
    
    def reset_score(self):
        """Reset score to zero"""
        self.total_score = 0
        self.visible_score = 0
    
    def draw(self, screen):
        """Draw score on the screen"""
        # Create score text surface
        score_text = self.font.render(f'Score: {int(self.visible_score)}', True, self.text_color)
        
        # Position the score text
        text_rect = score_text.get_rect(center=(self.screen_width // 2, 50))
        
        # Optional: Draw a semi-transparent background
        background_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5, 
                                      text_rect.width + 20, text_rect.height + 10)
        s = pygame.Surface(background_rect.size, pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(s, background_rect)
        
        # Draw the score text
        screen.blit(score_text, text_rect)
    
    def is_winning_score(self, current_level):
        """
        Check if the current score meets the winning condition for the given level.

        Args:
            current_level (int): The current level of the game.

        Returns:
            bool: True if the score meets or exceeds the winning score, False otherwise.
        """
        return self.total_score >= self.win_scores.get(current_level, 0)

    def add_score(self, score_change):
        """
        Add score to the total score and check for win condition.

        Args:
            score_change (int): The amount of score to add.
        """
        self.total_score += score_change
        current_level = current_game_state.get_level()
        
        debug.log('score_ui', f"Score updated. Current score: {self.total_score}, Level: {current_level}")
        
        if self.is_winning_score(current_level):
            debug.log('score_ui', f"Winning score reached: {self.total_score}")
            # Explicitly trigger win condition
            current_game_state.trigger_win_condition()
            return True
        return False