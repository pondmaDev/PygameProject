# src/ui/game_over_screen.py
import pygame
import sys
import time
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
        self.BUTTON_COLORS = {
            'normal': (200, 200, 200),
            'hover': (180, 180, 180),
            'text_normal': (0, 0, 0),
            'text_hover': (255, 255, 255)
        }
        
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
        
        # Interaction management
        self.input_cooldown = 250  # 250 ms cooldown
        self.last_input_time = 0
        
        # Hover management
        self.hover_button = None
    
    def draw_button(self, text, x, y, is_selected=False, is_hovered=False):
        """
        Draw a button with advanced hover and selection effects
        
        Args:
            text (str): Button text
            x (int): X position
            y (int): Y position
            is_selected (bool): Whether the button is currently selected
            is_hovered (bool): Whether the button is being hovered
        
        Returns:
            pygame.Rect: Button rectangle for click detection
        """
        # Determine button colors based on state
        if is_selected or is_hovered:
            button_color = self.BUTTON_COLORS['hover']
            text_color = self.BUTTON_COLORS['text_hover']
        else:
            button_color = self.BUTTON_COLORS['normal']
            text_color = self.BUTTON_COLORS['text_normal']
        
        # Create button rectangle
        button_rect = pygame.Rect(x, y, self.button_width, self.button_height)
        
        # Draw button with rounded corners
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
        
        # Render button text
        text_surface = self.button_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        
        # Blit text onto screen
        self.screen.blit(text_surface, text_rect)
        
        return button_rect

    def handle_input(self):
        """
        Handle user input with advanced interaction management and input delay
        
        Returns:
            str or None: Action to take, or None if no action
        """
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            # Quit events
            if event.type == pygame.QUIT:
                return 'quit'
            
            # Mouse motion for hover effects
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                # Check which button is being hovered
                for i, button_info in enumerate(self.buttons):
                    button_x = (self.screen_width - self.button_width) // 2
                    button_y = self.calculate_button_y(i)
                    button_rect = pygame.Rect(
                        button_x, button_y, 
                        self.button_width, self.button_height
                    )
                    
                    if button_rect.collidepoint(mouse_pos):
                        self.hover_button = i
                        break
                else:
                    self.hover_button = None
            
            # Keyboard navigation
            if event.type == pygame.KEYDOWN:
                # Prevent rapid input with extended cooldown
                if current_time - self.last_input_time < self.input_cooldown:
                    continue
                
                # Navigation
                if event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                    self.last_input_time = current_time
                elif event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                    self.last_input_time = current_time
                
                # Select button with a slight delay
                elif event.key == pygame.K_RETURN:
                    # Add a small delay before action
                    pygame.time.delay(200)  # 200 ms delay
                    return self.buttons[self.selected_button]["action"]
            
            # Mouse click with delay
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, button_info in enumerate(self.buttons):
                    button_x = (self.screen_width - self.button_width) // 2
                    button_y = self.calculate_button_y(i)
                    button_rect = pygame.Rect(
                        button_x, button_y, 
                        self.button_width, self.button_height
                    )
                    
                    if button_rect.collidepoint(mouse_pos):
                        # Add a small delay before action
                        pygame.time.delay(200)  # 200 ms delay
                        return button_info["action"]
        
        return None

    def calculate_button_y(self, button_index):
        """
        Calculate the Y position for a specific button
        
        Args:
            button_index (int): Index of the button
        
        Returns:
            int: Y position for the button
        """
        total_buttons_height = (self.button_height + self.button_spacing) * len(self.buttons)
        start_y = (self.screen_height - total_buttons_height) // 2 + 100
        return start_y + button_index * (self.button_height + self.button_spacing)

    def display(self):
        """
        Display the game over screen with enhanced interaction
        
        Returns:
            str: Selected action ('restart', 'main_menu', or 'quit')
        """
        clock = pygame.time.Clock()
        
        while True:
            # Handle input
            action = self.handle_input()
            
            # Check for specific actions with additional safeguard
            if action:
                # Add a final small delay to ensure visual feedback
                pygame.time.delay(250)  # Additional 250 ms delay
                
                debug.log('game_over', f"Selected action: {action}")
                return action
            
            # Clear screen
            self.screen.fill(self.BACKGROUND_COLOR)
            
            # Game Over Title with shadow effect
            title = self.title_font.render("GAME OVER", True, self.TEXT_COLOR)
            shadow = self.title_font.render("GAME OVER", True, (50, 50, 50))
            title_rect = title.get_rect(centerx=self.screen_width//2, centery=100)
            shadow_rect = shadow.get_rect(centerx=self.screen_width//2 + 3, centery=103)
            
            # Draw shadow first, then title
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(title, title_rect)
            
            # Score Display
            score_text = self.subtitle_font.render(f"Final Score: {self.final_score}", True, self.TEXT_COLOR)
            score_rect = score_text.get_rect(centerx=self.screen_width // 2, centery=200)
            self.screen.blit(score_text, score_rect)

            # Draw buttons
            for i, button_info in enumerate(self.buttons):
                button_x = (self.screen_width - self.button_width) // 2
                button_y = self.calculate_button_y(i)
                is_selected = (i == self.selected_button)
                is_hovered = (i == self.hover_button)
                self.draw_button(button_info["text"], button_x, button_y, is_selected, is_hovered)

            # Update display
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 frames per second