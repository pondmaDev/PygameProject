# src/ui/game_over_screen.py
import pygame
import sys
from src.utils.constant import Colors
from src.utils.debug_section import debug

class GameOverScreen:
    def __init__(self, screen, final_score=0):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Colors
        self.BACKGROUND_COLOR = (20, 20, 40)  # Deep blue-black
        self.TEXT_COLOR = Colors.WHITE
        self.HIGHLIGHT_COLOR = (255, 100, 100)  # Soft red
        
        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font('assets/font/River Adventurer.ttf', 100)
        self.subtitle_font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 40)
        
        # Final score
        self.final_score = final_score
        
        # Buttons
        self.buttons = [
            {"text": "Restart", "action": "restart"},
            {"text": "Main Menu", "action": "main_menu"},
            {"text": "Quit", "action": "quit"}
        ]
        
        # Button properties
        self.button_width = 250
        self.button_height = 60
        self.button_spacing = 20
        
        # Button state
        self.selected_button = 0
    
    def draw_background(self):
        # Gradient background
        for y in range(self.screen_height):
            # Create a gradient from dark blue to almost black
            r = int(20 * (1 - y / self.screen_height))
            g = int(20 * (1 - y / self.screen_height))
            b = int(40 * (1 - y / self.screen_height))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen_width, y))
    
    def create_button(self, text, is_hover=False):
        # Button with hover effect
        button_surface = pygame.Surface((self.button_width, self.button_height), pygame.SRCALPHA)
        
        if is_hover:
            # Semi-transparent highlight
            button_surface.fill((*self.HIGHLIGHT_COLOR, 150))
            text_color = self.BACKGROUND_COLOR
        else:
            # Semi-transparent white
            button_surface.fill((255, 255, 255, 100))
            text_color = self.TEXT_COLOR
        
        # Rounded corners
        pygame.draw.rect(button_surface, text_color, 
                         button_surface.get_rect(), 2, border_radius=10)
        
        # Render text
        text_surface = self.button_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_surface.get_rect().center)
        button_surface.blit(text_surface, text_rect)
        
        return button_surface
    
    def display(self):
        """
        Display the game over screen
        
        Returns:
            str: Selected action ('restart', 'main_menu', or 'quit')
        """
        clock = pygame.time.Clock()
        
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_button = (self.selected_button - 1) % len(self.buttons)
                    elif event.key == pygame.K_DOWN:
                        self.selected_button = (self.selected_button + 1) % len(self.buttons)
                    elif event.key == pygame.K_RETURN:
                        # Log the selected action
                        debug.log('game_over', f"Selected action: {self.buttons[self.selected_button]['action']}")
                        return self.buttons[self.selected_button]["action"]
                
                # Mouse support
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, button_info in enumerate(self.buttons):
                        button_x = (self.screen_width - self.button_width) // 2
                        button_y = start_y + i * (self.button_height + self.button_spacing)
                        button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
                        
                        if button_rect.collidepoint(mouse_pos):
                            debug.log('game_over', f"Clicked action: {button_info['action']}")
                            return button_info['action']
            
            # Clear screen
            self.screen.fill(self.BACKGROUND_COLOR)
            
            # Draw background with subtle effects
            self.draw_background()
            
            # Game Over Title with shadow effect
            title = self.title_font.render("GAME OVER", True, self.TEXT_COLOR)
            # Shadow effect
            shadow = self.title_font.render("GAME OVER", True, (50, 50, 50))
            title_rect = title.get_rect(centerx=self.screen_width//2, centery=100)
            shadow_rect = shadow.get_rect(centerx=self.screen_width//2 + 3, centery=103)
            
            # Draw shadow first, then title
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(title, title_rect)
            
            # Score Display
            score_text = self.subtitle_font.render(f"Final Score: {self.final_score}", True, self.TEXT_COLOR)
            score_rect = score_text.get_rect(centerx=self.screen_width//2, centery=200)
            self.screen.blit(score_text, score_rect)
            
            # Buttons
            total_buttons_height = (self.button_height + self.button_spacing) * len(self.buttons)
            start_y = (self.screen_height - total_buttons_height) // 2 + 100
            
            for i, button_info in enumerate(self.buttons):
                button = self.create_button(button_info["text"], i == self.selected_button)
                button_x = (self.screen_width - self.button_width) // 2
                button_y = start_y + i * (self.button_height + self.button_spacing)
                
                self.screen.blit(button, (button_x, button_y))
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            clock.tick(30)