# src/ui/game_over_screen.py
import pygame
import sys
import time
from src.utils.constant import Colors
from src.utils.debug_section import debug

class GameOverScreen:
    def __init__(self, screen, is_win=False, level=1):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Colors with more vibrant winning colors
        self.BACKGROUND_COLOR = (50, 200, 50) if is_win else (40, 40, 60)  # Green for win, dark blue for lose
        self.TEXT_COLOR = (255, 255, 255)
        self.HIGHLIGHT_COLOR = (255, 100, 100)
        
        # Button colors with more distinct styles
        self.BUTTON_COLORS = {
            'normal': (100, 200, 100) if is_win else (200, 200, 200),  # Green for win, light gray for lose
            'hover': (150, 230, 150) if is_win else (180, 180, 180),
            'text_normal': (0, 0, 0),
            'text_hover': (255, 255, 255)
        }

        # Fonts with custom loading
        try:
            self.title_font = pygame.font.Font('assets/font/River Adventurer.ttf', 64)
            self.subtitle_font = pygame.font.Font('assets/font/River Adventurer.ttf', 36)
            self.button_font = pygame.font.Font('assets/font/River Adventurer.ttf', 40)
        except Exception as e:
            debug.warning('game_over', f"Failed to load custom font: {e}")
            self.title_font = pygame.font.Font(None, 64)
            self.subtitle_font = pygame.font.Font(None, 36)
            self.button_font = pygame.font.Font(None, 40)
        
        # Win status and current level
        self.is_win = is_win
        self.current_level = level
        
        # Dynamically set buttons based on win/lose state
        self.buttons = (
            [
                {"text": "Next Level", "action": "next_level"},
                {"text": "Main Menu", "action": "main_menu"},
                {"text": "Quit", "action": "quit"}
            ] if is_win else
            [
                {"text": "Retry", "action": "restart"},
                {"text": "Main Menu", "action": "main_menu"},
                {"text": "Quit", "action": "quit"}
            ]
        )
        
        # Button properties
        self.button_width = 250
        self.button_height = 60
        self.button_spacing = 20
        
        # Button state management
        self.selected_button = 0
        self.hover_button = None
        
        # Input management
        self.input_cooldown = 250
        self.last_input_time = 0

    def display(self):
        clock = pygame.time.Clock()
        
        while True:
            # Handle input
            action = self.handle_input()
            
            # Check for specific actions with additional safeguard
            if action:
                pygame.time.delay(250)  # Additional 250 ms delay
                debug.log('game_over', f"Selected action: {action}")
                
                # Special handling for next level
                if action == 'next_level':
                    # Increment level, but cap at maximum level
                    next_level = min(self.current_level + 1, 3)
                    debug.log('game_over', f"Progressing to level {next_level}")
                    return next_level
                
                return action
            
            # Clear screen
            self.screen.fill(self.BACKGROUND_COLOR)
            
            # Determine title based on win/lose status
            if self.is_win:
                title_text = "CONGRATULATIONS!"
                subtitle_text = f"Level {self.current_level} Completed!"
            else:
                title_text = "GAME OVER"
                subtitle_text = "Better luck next time!"
            
            # Render title with shadow effect
            title = self.title_font.render(title_text, True, self.TEXT_COLOR)
            shadow = self.title_font.render(title_text, True, (50, 50, 50))
            title_rect = title.get_rect(centerx=self.screen_width//2, centery=100)
            shadow_rect = shadow.get_rect(centerx=self.screen_width//2 + 3, centery=103)
            
            # Draw shadow first, then title
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(title, title_rect)
            
            # Subtitle
            subtitle = self.subtitle_font.render(subtitle_text, True, self.TEXT_COLOR)
            subtitle_rect = subtitle.get_rect(centerx=self.screen_width // 2, centery=200)
            self.screen.blit(subtitle, subtitle_rect)
            
            # Draw buttons
            for i, button_info in enumerate(self.buttons):
                button_x = (self.screen_width - self.button_width) // 2
                button_y = self.calculate_button_y(i)
                is_selected = (i == self.selected_button)
                is_hovered = (i == self.hover_button)

                # Draw each button
                self.draw_button(button_info["text"], button_x, button_y, is_selected, is_hovered)

            # Update the display
            pygame.display.flip()
            clock.tick(60)

    def calculate_button_y(self, index):
        """
        Calculate the Y position for each button based on its index
        
        Args:
            index (int): Index of the button
        
        Returns:
            int: Calculated Y position
        """
        return 300 + index * (self.button_height + self.button_spacing)

    def handle_input(self):
        """
        Handle user input for navigating the game over screen
        
        Returns:
            str: Action to be taken based on input
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            # Mouse motion for hover effects
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                self._handle_mouse_hover(mouse_pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN:
                    return self.buttons[self.selected_button]["action"]
            
            # Mouse click handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                action = self._handle_mouse_click(mouse_pos)
                if action:
                    return action
        
        return None

    def _handle_mouse_hover(self, mouse_pos):
        """
        Handle mouse hover effects for buttons
        
        Args:
            mouse_pos (tuple): Current mouse position
        """
        for i, button_info in enumerate(self.buttons):
            button_x = (self.screen_width - self.button_width) // 2
            button_y = self.calculate_button_y(i)
            button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
            
            if button_rect.collidepoint(mouse_pos):
                self.hover_button = i
                return
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
        
        # Shadow layer
        shadow_rect = pygame.Rect(
            x + 2, 
            y + 2, 
            self.button_width, 
            self.button_height
        )
        pygame.draw.rect(
            self.screen, 
            (100, 100, 100, 100),  # Semi-transparent shadow 
            shadow_rect, 
            border_radius=10
        )
        
        # Main button layer
        pygame.draw.rect(
            self.screen, 
            button_color, 
            button_rect, 
            border_radius=10
        )
        
        # Optional: Add a subtle border for depth
        pygame.draw.rect(
            self.screen, 
            (50, 50, 50),  # Dark border color
            button_rect, 
            2,  # Border width
            border_radius=10
        )
        
        # Render button text with custom font
        text_surface = self.button_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        
        # Slight text offset when selected/hovered for press effect
        if is_selected or is_hovered:
            text_rect.y += 2
        
        # Blit text onto screen
        self.screen.blit(text_surface, text_rect)
        
        return button_rect

    def _handle_mouse_click(self, mouse_pos):
        """
        Handle mouse click events on buttons
        
        Args:
            mouse_pos (tuple): Current mouse position
        
        Returns:
            str: Action to be taken based on the clicked button
        """
        for i, button_info in enumerate(self.buttons):
            button_x = (self.screen_width - self.button_width) // 2
            button_y = self.calculate_button_y(i)
            button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
            
            if button_rect.collidepoint(mouse_pos):
                return button_info["action"]
        return None
