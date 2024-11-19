import pygame

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