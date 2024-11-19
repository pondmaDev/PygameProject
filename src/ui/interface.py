import pygame
import sys
import time
from src.game.game_state import current_game_state
from config.setting import current_settings
from src.utils.constant import Colors
from src.utils.resource_manager import ResourceManager  # Make sure to import ResourceManager
from src.utils.debug_section import debug

import logging
import re
# Define button texts as constants
BUTTON_TEXTS = {
    'start_game': 'Start Game',
    'settings': 'Settings',
    'credits': 'Credits',
    'back': 'Back',
    'resume': 'Resume',
    'main_menu': 'Main Menu'
}

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.resource_manager = ResourceManager.get_instance()  # Get the ResourceManager instance

    def draw_button(self, 
                    text,  # First parameter is now the text
                    x,     # x position
                    y,     # y position
                    width=200,  # default width
                    height=50,  # default height
                    inactive_color=(200, 200, 200),  # default inactive color
                    active_color=(180, 180, 180)     # default active color
                    ):
        """
        Draw a button with customizable properties
        
        Args:
            text (str): Button text
            x (int): X position of button
            y (int): Y position of button
            width (int, optional): Button width
            height (int, optional): Button height
            inactive_color (tuple, optional): Color when not hovered
            active_color (tuple, optional): Color when hovered
        
        Returns:
            bool: Whether the button was clicked
        """
        # Create button rectangle
        button_rect = pygame.Rect(x, y, width, height)
        
        # Check if mouse is hovering
        mouse_pos = pygame.mouse.get_pos()
        hover_state = button_rect.collidepoint(mouse_pos)
        
        # Use provided or default colors and dimensions
        current_color = active_color if hover_state else inactive_color
        
        # Draw button background
        pygame.draw.rect(self.screen, current_color, button_rect)
        
        # Render text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        
        # Blit text onto screen
        self.screen.blit(text_surface, text_rect)
        
        # Check for button click
        mouse_clicked = pygame.mouse.get_pressed()[0]
        return hover_state and mouse_clicked

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'resume'  # Return resume to be handled by the calling method
        return None

class MainMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.last_click_time = 0
        self.click_delay = 300
        self.button_clicked = False
        self.screen = screen
        
        # Load custom font for buttons and title
        try:
            self.title_font = pygame.font.Font('assets/font/River Adventurer.ttf', 100)
            self.button_font = pygame.font.Font('assets/font/River Adventurer.ttf', 50)
        except Exception as e:
            debug.warning('menu', f"Failed to load custom font: {e}")
            # Fallback to default font
            self.title_font = pygame.font.Font(None, 100)
            self.button_font = pygame.font.Font(None, 50)
        
        # Button configuration
        self.buttons = [
            {
                'text': 'Start Game',
                'rect': None,
                'hover': False
            },
            {
                'text': 'Settings',
                'rect': None,
                'hover': False
            },
            {
                'text': 'Quit',
                'rect': None,
                'hover': False
            }
        ]

    def display(self):
        current_game_state.set_screen('main_menu')
        clock = pygame.time.Clock()
        
        try:
            background_image = self.resource_manager.get_image('main_background')
        except Exception as e:
            debug.warning('menu', f"Failed to load background image: {e}")
            background_image = None

        while True:
            current_time = pygame.time.get_ticks()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'quit'
                
                # Mouse motion for hover effects
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                    self._handle_mouse_hover(mouse_pos)
                
                # Mouse click handling
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    action = self._handle_mouse_click(mouse_pos)
                    if action:
                        # Add a small delay for visual feedback
                        pygame.time.delay(200)
                        return action

            # Clear screen
            self.screen.fill(Colors.WHITE)

            # Draw background if available
            if background_image:
                self.screen.blit(background_image, (0, 0))

            screen_width = self.screen.get_width()
            
            # Title with blinking effect
            title_text = self.title_font.render('Collect Cat', True, pygame.Color(139, 69, 19))
            if int(time.time() * 2) % 2 == 0:
                title_text = self.title_font.render('Collect Cat', True, pygame.Color(50, 50, 50))
            
            title_rect = title_text.get_rect(center=(screen_width // 2, 100))
            self.screen.blit(title_text, title_rect)

            # Button configuration
            button_width = 300
            button_height = 70
            button_x = screen_width // 2 - button_width // 2
            start_button_y = 250
            spacing = 20

            # Draw buttons
            for i, button in enumerate(self.buttons):
                # Calculate button position
                button_y = start_button_y + i * (button_height + spacing)
                
                # Create button surface
                button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                
                # Define colors
                base_color = (200, 200, 200, 200)  # Semi-transparent light gray
                hover_color = (180, 180, 180, 230)  # Semi-transparent darker gray
                text_color = Colors.BLACK
                
                # Apply hover effect
                current_color = hover_color if button['hover'] else base_color
                
                # Draw button background with rounded corners
                pygame.draw.rect(
                    button_surface, 
                    current_color, 
                    button_surface.get_rect(), 
                    border_radius=15
                )
                
                # Add border
                pygame.draw.rect(
                    button_surface, 
                    Colors.BLACK, 
                    button_surface.get_rect(), 
                    2, 
                    border_radius=15
                )
                
                # Render button text
                text_surface = self.button_font.render(button['text'], True, text_color)
                text_rect = text_surface.get_rect(center=(button_width // 2, button_height // 2))
                button_surface.blit(text_surface, text_rect)
                
                # Store button rect for click detection
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                button['rect'] = button_rect
                
                # Blit button
                self.screen.blit(button_surface, button_rect)

            pygame.display.flip()
            clock.tick(60)

    def _handle_mouse_hover(self, mouse_pos):
        """
        Handle mouse hover effects for buttons
        """
        for button in self.buttons:
            if button['rect'] and button['rect'].collidepoint(mouse_pos):
                button['hover'] = True
            else:
                button['hover'] = False

    def _handle_mouse_click(self, mouse_pos):
        """
        Handle mouse click events for buttons
        """
        for button in self.buttons:
            if button['rect'] and button['rect'].collidepoint(mouse_pos):
                if button['text'] == 'Start Game':
                    debug.log('menu', "Start Game selected")
                    return 'start_game'
                elif button['text'] == 'Settings':
                    debug.log('menu', "Settings selected")
                    return 'settings'
                elif button['text'] == 'Quit':
                    debug.log('menu', "Quit selected")
                    return 'quit'
        
        return None

# src/ui/interface.py (in the LevelSelectionMenu class)
class LevelSelectionMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.hover_level = None
        
        # Enhanced level design
        self.level_details = {
            1: {
                'name': 'Beginner\'s Path',
                'description': 'Start your adventure with easy challenges',
                'difficulty': 'Easy',
                'background_color': (100, 200, 100)  # Soft green
            },
            2: {
                'name': 'Challenging Route',
                'description': 'Test your skills with moderate obstacles',
                'difficulty': 'Medium',
                'background_color': (255, 165, 0)  # Orange
            },
            3: {
                'name': 'Master\'s Challenge',
                'description': 'Prove your mastery with ultimate challenges',
                'difficulty': 'Hard',
                'background_color': (220, 20, 60)  # Crimson
            }
        }

    def display(self):
        current_game_state.set_screen('level_selection')
        clock = pygame.time.Clock()
        
        # Load background image
        try:
            background_image = self.resource_manager.get_image('main_background')
        except Exception as e:
            debug.error('menu', f"Failed to load background image: {e}")
            background_image = None

        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'main_menu'
                
                # Mouse motion for hover effects
                if event.type == pygame.MOUSEMOTION:
                    self._handle_mouse_hover(event.pos)
                
                # Mouse click handling
                if event.type == pygame.MOUSEBUTTONDOWN:
                    level = self._handle_mouse_click(event.pos)
                    if level:
                        return level
            
            # Clear screen
            self.screen.fill(Colors.WHITE)

            # Draw background if available
            if background_image:
                self.screen.blit(background_image, (0, 0))

            # Screen dimensions
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()

            # Title
            title_font = pygame.font.Font('assets/font/River Adventurer.ttf', 64)
            title_text = title_font.render('Select Level', True, Colors.BLACK)
            title_rect = title_text.get_rect(center=(screen_width // 2, 80))
            self.screen.blit(title_text, title_rect)

            # Level button positioning (ROW pattern)
            button_width = 250
            button_height = 80
            spacing = (screen_width - (3 * button_width)) // 4
            start_y = 200

            # Draw level selection buttons
            for i in range(1, 4):
                # Button surface
                level_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                
                # Background color
                level_details = self.level_details[i]
                base_color = level_details['background_color']
                
                # Create gradient background
                for y in range(button_height):
                    r = int(base_color[0] * (1 - y / button_height))
                    g = int(base_color[1] * (1 - y / button_height))
                    b = int(base_color[2] * (1 - y / button_height))
                    pygame.draw.line(level_surface, (r, g, b), (0, y), (button_width, y))
                
                # Add border
                pygame.draw.rect(level_surface, Colors.BLACK, level_surface.get_rect(), 2)
                
                # Level number (smaller and centered)
                number_font = pygame.font.Font(None, 40)
                number_text = number_font.render(str(i), True, Colors.WHITE)
                number_rect = number_text.get_rect(center=(button_width // 2, button_height // 2))
                level_surface.blit(number_text, number_rect)
                
                # Position and draw the button (ROW pattern)
                button_rect = level_surface.get_rect(
                    center=((spacing * i) + (button_width * (i - 0.5)), start_y)
                )
                self.screen.blit(level_surface, button_rect)

            # Description Area
            if self.hover_level is not None:
                # Description background
                desc_surface = pygame.Surface((screen_width - 100, 100), pygame.SRCALPHA)
                desc_surface.fill((200, 200, 200, 200))
                pygame.draw.rect(desc_surface, Colors.BLACK, desc_surface.get_rect(), 2)
                
                # Description text (smaller font)
                desc_font = pygame.font.Font(None, 20)
                details = self.level_details[self.hover_level]
                
                # Render multiple lines of description
                name_text = desc_font.render(f"Level {self.hover_level}: {details['name']}", True, Colors.BLACK)
                difficulty_text = desc_font.render(f"Difficulty: {details['difficulty']}", True, Colors.BLACK)
                desc_text = desc_font.render(details['description'], True, Colors.BLACK)
                
                # Blit description texts (centered)
                desc_surface.blit(name_text, (desc_surface.get_width()//2 - name_text.get_width()//2, 10))
                desc_surface.blit(difficulty_text, (desc_surface.get_width()//2 - difficulty_text.get_width()//2, 40))
                desc_surface.blit(desc_text, (desc_surface.get_width()//2 - desc_text.get_width()//2, 70))
                
                # Position description
                desc_rect = desc_surface.get_rect(
                    center=(screen_width // 2, screen_height - 200)
                )
                self.screen.blit(desc_surface, desc_rect)

            # Back Button
            back_button_width = 200
            back_button_height = 50
            back_button_x = screen_width // 2 - back_button_width // 2
            back_button_y = screen_height - 100

            # Draw back button
            back_surface = pygame.Surface((back_button_width, back_button_height), pygame.SRCALPHA)
            back_surface.fill((200, 200, 200, 200))
            pygame.draw.rect(back_surface, Colors.BLACK, back_surface.get_rect(), 2, border_radius=10)
            
            back_font = pygame.font.Font(None, 36)
            back_text = back_font.render('Back', True, Colors.BLACK)
            back_text_rect = back_text.get_rect(center=(back_button_width // 2, back_button_height // 2))
            back_surface.blit(back_text, back_text_rect)
            
            self.screen.blit(back_surface, (back_button_x, back_button_y))

            # Update display
            pygame.display.flip()
            clock.tick(60)


    def _handle_mouse_hover(self, mouse_pos):
        """
        Handle mouse hover effects for levels with precise hit box calculation
        """
        screen_width = self.screen.get_width()
        button_width = 250
        button_height = 80
        spacing = (screen_width - (3 * button_width)) // 4
        start_y = 200

        # Reset hover level
        self.hover_level = None

        for i in range(1, 4):
            # Calculate precise button rect (ROW pattern)
            button_rect = pygame.Rect(
                (spacing * i) + (button_width * (i - 1)),  # Adjusted x-position calculation
                start_y, 
                button_width, 
                button_height
            )
            
            if button_rect.collidepoint(mouse_pos):
                self.hover_level = i
                debug.log('level_selection', f"Hovering over level {i}")
                break

        # Check back button hover
        back_button_rect = pygame.Rect(
            screen_width // 2 - 100,
            self.screen.get_height() - 100,
            200,
            50
        )
        if back_button_rect.collidepoint(mouse_pos):
            self.hover_back = True
        else:
            self.hover_back = False

    def _handle_mouse_click(self, mouse_pos):
        """
        Handle mouse click events for level selection with precise hit box
        """
        screen_width = self.screen.get_width()
        button_width = 250
        button_height = 80
        spacing = (screen_width - (3 * button_width)) // 4
        start_y = 200

        for i in range(1, 4):
            # Calculate precise button rect (ROW pattern)
            button_rect = pygame.Rect(
                (spacing * i) + (button_width * (i - 1)),  # Adjusted x-position calculation
                start_y, 
                button_width, 
                button_height
            )
            
            if button_rect.collidepoint(mouse_pos):
                return i  # Return the selected level

        # Check back button
        back_button_rect = pygame.Rect(
            screen_width // 2 - 100,
            self.screen.get_height() - 100,
            200,
            50
        )
        if back_button_rect.collidepoint(mouse_pos):
            return 'main_menu'

        return None

class SettingsMenu(Menu):

    def __init__(self, screen, settings, from_pause=False):
        super().__init__(screen)
        self.input_rects = {}
        self.settings = settings
        self.from_pause = from_pause
        
        # Input handling attributes
        self.input_active = False
        self.current_input_field = None
        self.input_text = ""
        
        # Import re for input validation
        import re
        self.re = re
        
        # Styling
        self.colors = {
            'background': (240, 240, 240),
            'input_inactive': (220, 220, 220),
            'input_active': (200, 200, 200),
            'text': (0, 0, 0),
            'label': (50, 50, 50),
            'description': (100, 100, 100),
            'button_base': (200, 200, 200),
            'button_hover': (180, 180, 180)
        }
        
        # Setting configurations
        self.setting_configs = {
            'bg_music_volume': {
                'label': 'Music Volume',
                'min': 0,
                'max': 100,
                'type': int,
                'description': 'Adjust background music volume (0-100)',
                'on_change': self._adjust_music_volume
            },
            'sound_effects_volume': {
                'label': 'Sound Effects',
                'min': 0,
                'max': 100,
                'type': int,
                'description': 'Adjust sound effects volume (0-100)',
                'on_change': self._adjust_sound_effects_volume
            }
        }
        
        # Buttons
        self.buttons = [
            {
                'text': 'Reset',
                'action': 'reset',
                'rect': None,
                'hover': False
            },
            {
                'text': 'Back',
                'action': 'back',
                'rect': None,
                'hover': False
            }
        ]
        
        # Fonts
        try:
            self.title_font = pygame.font.Font('assets/font/River Adventurer.ttf', 48)
            self.label_font = pygame.font.Font('assets/font/River Adventurer.ttf', 36)
            self.input_font = pygame.font.Font('assets/font/River Adventurer.ttf', 32)
            self.description_font = pygame.font.Font('assets/font/River Adventurer.ttf', 24)
            self.button_font = pygame.font.Font('assets/font/River Adventurer.ttf', 30)
        except Exception as e:
            debug.warning('settings', f"Failed to load custom font: {e}")
            # Fallback to default fonts
            self.title_font = pygame.font.Font(None, 48)
            self.label_font = pygame.font.Font(None, 36)
            self.input_font = pygame.font.Font(None, 32)
            self.description_font = pygame.font.Font(None, 24)
            self.button_font = pygame.font.Font(None, 30)

    def _render_settings_fields(self):
        """
        Render individual settings fields with input rectangles
        """
        y_start = 180
        spacing = 120
        
        for i, (setting_key, config) in enumerate(self.setting_configs.items()):
            current_value = getattr(self.settings, setting_key)
            
            # Render label
            label = self.label_font.render(config['label'], True, self.colors['label'])
            label_rect = label.get_rect(midleft=(
                self.screen.get_width() // 2 - 200, 
                y_start + i * spacing
            ))
            self.screen.blit(label, label_rect)
            
            # Create and store input rect
            input_rect = pygame.Rect(
                self.screen.get_width() // 2 + 20, 
                y_start + i * spacing - 15, 
                180, 
                40
            )
            self.input_rects[setting_key] = input_rect
            
            # Draw input field with rounded corners and dynamic coloring
            input_color = (
                self.colors['input_active'] if self.current_input_field == setting_key 
                else self.colors['input_inactive']
            )
            pygame.draw.rect(self.screen, input_color, input_rect, border_radius=10)
            
            # Render input text
            display_text = (
                self.input_text if self.current_input_field == setting_key 
                else str(current_value)
            )
            text_surface = self.input_font.render(display_text, True, self.colors['text'])
            text_rect = text_surface.get_rect(center=input_rect.center)
            self.screen.blit(text_surface, text_rect)
            
            # Render description
            description = self.description_font.render(
                config['description'], 
                True, 
                self.colors['description']
            )
            description_rect = description.get_rect(
                center=(self.screen.get_width() // 2, y_start + i * spacing + 50)
            )
            self.screen.blit(description, description_rect)

    def _handle_mouse_click(self, mouse_pos):
        """
        Handle mouse click events for input fields
        """
        # Check if an input field was clicked
        for setting_key, input_rect in self.input_rects.items():
            if input_rect.collidepoint(mouse_pos):
                self.input_active = True
                self.current_input_field = setting_key
                self.input_text = str(getattr(self.settings, setting_key))
                return

        # Deactivate input if clicked outside
        self.input_active = False
        self.current_input_field = None

    def handle_input(self, event):
        """
        Handle input events for settings menu
        """
        if not self.input_active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Validate and update setting
                self.update_setting()
                self.input_active = False
                self.current_input_field = None
            elif event.key == pygame.K_BACKSPACE:
                # Remove last character with safety check
                self.input_text = self.input_text[:-1]
            else:
                # Add typed character with input validation
                self.input_text += event.unicode

    def _adjust_music_volume(self, value):
        """
        Adjust the background music volume
        """
        debug.log('settings', f"Music volume adjusted to {value}")

    def _adjust_sound_effects_volume(self, value):
        """
        Adjust the sound effects volume
        """
        debug.log('settings', f"Sound effects volume adjusted to {value}")

    def update_setting(self):
        """
        Update the setting with input validation
        """
        if not self.current_input_field:
            return

        config = self.setting_configs[self.current_input_field]
        
        # Validate and process input
        processed_value, is_valid = self.validate_and_process_input(
            self.input_text, 
            config
        )
        
        # Update the setting
        setattr(self.settings, self.current_input_field, processed_value)
        
        # Call optional change handler
        if 'on_change' in config:
            config['on_change'](processed_value)
        
        # Log validation result
        if not is_valid:
            debug.warning(
                f"Input for {self.current_input_field} "
                f"clamped/adjusted to {processed_value}"
            )

    def validate_and_process_input(self, input_text: str, config):
        """
        Comprehensive input validation and processing
        
        Args:
            input_text (str): Raw input text
            config (dict): Setting configuration
        
        Returns:
            tuple: (processed_value, is_valid)
        """
        try:
            # Remove any non-numeric characters
            cleaned_value = self.re.sub(r'[^\d.-]', '', input_text)
            
            # Convert to appropriate type
            processed_value = config['type'](cleaned_value)
            
            # Clamp numeric values if min/max exist
            if 'min' in config and 'max' in config:
                processed_value = max(config['min'], min(processed_value, config['max']))
            
            return processed_value, True
        
        except (ValueError, TypeError) as e:
            debug.warning(f"Invalid input for {self.current_input_field}: {e}")
            # Return current value if conversion fails
            return getattr(self.settings, self.current_input_field), False

    def display(self):
        """
        Display the settings menu
        """
        clock = pygame.time.Clock()
        
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.handle_exit()
                
                # Handle input for active field
                self.handle_input(event)
                
                # Mouse click handling
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_click(event.pos)
            
            # Clear screen
            self.screen.fill(Colors.WHITE)
            
            # Render the settings fields
            self._render_settings_fields()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)

    def handle_exit(self):
        """
        Handle exit from settings menu
        """
        if self.from_pause:
            return 'pause_menu'
        return 'main_menu'

    def _process_event(self, event):
        """
        Process individual events with structured handling
        
        Returns:
            str or None: Screen to return or None if no specific action
        """
        # Quit event
        if event.type == pygame.QUIT:
            return 'quit'
        
        # Keyboard events
        if event.type == pygame.KEYDOWN:
            return self._handle_keyboard_event(event)
        
        # Mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_event(event)
        
        return None
    
    def _handle_keyboard_event(self, event):
        """
        Handle keyboard input for settings menu
        
        Returns:
            str or None: Screen to return or None
        """
        # Escape key handling
        if event.key == pygame.K_ESCAPE:
            return self.handle_exit()
        
        # Input field active handling
        if self.input_active:
            if event.key == pygame.K_RETURN:
                # Validate and update setting
                self.update_setting()
                self.input_active = False
                self.current_input_field = None
            elif event.key == pygame.K_BACKSPACE:
                # Remove last character with safety check
                self.input_text = self.input_text[:-1]
            else:
                # Add typed character with input validation
                self.input_text += event.unicode
        
        return None

    def _handle_mouse_event(self, event):
        """
        Handle mouse input for settings menu with additional button interactions
        """
        mouse_pos = event.pos
        
        # Check back button
        back_rect = pygame.Rect(
            self.screen.get_width() // 2 - 100, 
            self.screen.get_height() - 120, 
            200, 50
        )
        if back_rect.collidepoint(mouse_pos):
            return self.handle_exit()
        
        # Check reset button
        reset_rect = pygame.Rect(
            self.screen.get_width() // 2 - 250, 
            self.screen.get_height() - 120, 
            120, 50
        )
        if reset_rect.collidepoint(mouse_pos):
            self._reset_settings()
        
        # Handle input field selection
        for setting_key, config in self.setting_configs.items():
            input_rect = self.input_rects.get(setting_key)
            if input_rect and input_rect.collidepoint(mouse_pos):
                self.input_active = True
                self.current_input_field = setting_key
                self.input_text = str(getattr(self.settings, setting_key))
                break
        else:
            # Deactivate input if clicked outside
            self.input_active = False
            self.current_input_field = None
    
    def _render_settings_screen(self):
        """
        Comprehensive rendering of settings screen with improved UI
        """
        # Clear screen with soft background color
        self.screen.fill(self.colors['background'])
        
        # Render title with more prominent styling
        title = self.title_font.render("Game Settings", True, self.colors['text'])
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Render settings fields
        self._render_settings_fields()
        
        # Render action buttons
        self._render_action_buttons()

    def _render_title(self):
        """
        Render the settings menu title
        """
        title = self.input_font.render("Settings", True, Colors.BLACK)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)

    def _render_settings_fields(self):
        """
        Render individual settings fields with enhanced error handling
        """
        try:
            y_start = 180
            spacing = 120
            
            for i, (setting_key, config) in enumerate(self.setting_configs.items()):
                current_value = getattr(self.settings, setting_key)
                
                # Render label with improved styling
                label = self.label_font.render(config['label'], True, self.colors['label'])
                label_rect = label.get_rect(midleft=(
                    self.screen.get_width() // 2 - 200, 
                    y_start + i * spacing
                ))
                self.screen.blit(label, label_rect)
                
                # Create and store input rect with rounded look
                input_rect = pygame.Rect(
                    self.screen.get_width() // 2 + 20, 
                    y_start + i * spacing - 15, 
                    180, 
                    40
                )
                # Ensure input_rects is a dictionary before setting
                if not hasattr(self, 'input_rects'):
                    self.input_rects = {}
                self.input_rects[setting_key] = input_rect
                
                # Draw input field with rounded corners and dynamic coloring
                input_color = (
                    self.colors['input_active'] if self.current_input_field == setting_key 
                    else self.colors['input_inactive']
                )
                pygame.draw.rect(self.screen, input_color, input_rect, border_radius=10)
                
                # Render input text
                display_text = (
                    self.input_text if self.current_input_field == setting_key 
                    else str(current_value)
                )
                text_surface = self.input_font.render(display_text, True, self.colors['text'])
                text_rect = text_surface.get_rect(center=input_rect.center)
                self.screen.blit(text_surface, text_rect)
                
                # Render description with softer color
                description = self.description_font.render(
                    config['description'], 
                    True, 
                    self.colors['description']
                )
                description_rect = description.get_rect(
                    center=(self.screen.get_width() // 2, y_start + i * spacing + 50)
                )
                self.screen.blit(description, description_rect)
        
        except Exception as e:
            self.logger.error(f"Error in rendering settings fields: {e}")
            import traceback
            self.logger.error(traceback.format_exc())

    def _render_action_buttons(self):
        """
        Render action buttons with modern UI styling
        """
        # Back button
        back_text = 'Back to Game' if self.from_pause else 'Back'
        back_button_rect = pygame.Rect(
            self.screen.get_width() // 2 - 100, 
            self.screen.get_height() - 120, 
            200, 
            50
        )
        
        # Reset to default button
        reset_button_rect = pygame.Rect(
            self.screen.get_width() // 2 - 250, 
            self.screen.get_height() - 120, 
            120, 
            50
        )
        
        # Hover and click detection
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw Back button
        back_color = (180, 180, 180) if back_button_rect.collidepoint(mouse_pos) else (200, 200, 200)
        pygame.draw.rect(self.screen, back_color, back_button_rect, border_radius=10)
        back_button_text = self.label_font.render(back_text, True, self.colors['text'])
        back_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_button_text, back_text_rect)
        
        # Draw Reset button
        reset_color = (200, 100, 100) if reset_button_rect.collidepoint(mouse_pos) else (220, 120, 120)
        pygame.draw.rect(self.screen, reset_color, reset_button_rect, border_radius=10)
        reset_button_text = self.label_font.render('Reset', True, self.colors['text'])
        reset_text_rect = reset_button_text.get_rect(center=reset_button_rect.center)
        self.screen.blit(reset_button_text, reset_text_rect)
        
    def _render_back_button(self):
        """
        Render back button with dynamic text
        """
        back_text = 'Back to Game' if self.from_pause else 'Back'
        self.draw_button(
            back_text, 
            self.screen.get_width() // 2 - 100, 
            self.screen.get_height() - 100, 
            200, 50, 
            (200, 200, 200), 
            (150, 150, 150)
        )

    def update_setting(self):
        """
        Update the setting with input validation
        """
        if not self.current_input_field:
            return

        config = self.setting_configs[self.current_input_field]
        
        # Validate and process input
        processed_value, is_valid = self.validate_and_process_input(
            self.input_text, 
            config
        )
        
        # Update the setting
        setattr(self.settings, self.current_input_field, processed_value)
        
        # Call optional change handler
        if 'on_change' in config:
            config['on_change'](processed_value)
        
        # Log validation result
        if not is_valid:
            self.logger.warning(
                f"Input for {self.current_input_field} "
                f"clamped/adjusted to {processed_value}"
            )
    
    def _reset_settings(self):
        """
        Reset settings to their original values
        """
        for key in self.original_settings:
            setattr(self.settings, key, self.original_settings[key])
        self.logger.info("Settings have been reset to default values.")

    def handle_exit(self):
        """
        Handle exit from settings menu
        """
        if self.from_pause:
            return 'pause_menu'
        return 'main_menu'

    def draw_button(self, text, x, y, width, height, color, hover_color ):
        """
        Draw a button and handle hover effect
        
        Args:
            text (str): Button text
            x (int): X position
            y (int): Y position
            width (int): Button width
            height (int): Button height
            color (tuple): Button color
            hover_color (tuple): Color when hovered
        
        Returns:
            bool: True if button is clicked, False otherwise
        """
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(x, y, width, height)
        
        # Change color on hover
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_color, button_rect)
            if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(mouse_pos):
                return True
        else:
            pygame.draw.rect(self.screen, color, button_rect)
        
        # Render button text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, Colors.BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return False

    def reset_settings(self):
        """
        Reset settings to their original values
        """
        for key, original_value in self.original_settings.items():
            setattr(self.settings, key, original_value)
        debug.log('settings', "Settings reset to original values")

    def save_settings(self):
        """
        Save the current settings
        """
        self.settings.save()
        debug.log('settings', "Settings saved successfully")


class PauseMenu(Menu):
    def __init__(self, screen, previous_screen, settings):
        super().__init__(screen)
        self.previous_screen = previous_screen
        self.settings = settings
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        button_width = 200
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        spacing = 20
        
        self.resume_button = pygame.Rect(button_x, 200, button_width, button_height)
        self.settings_button = pygame.Rect(button_x, 200 + button_height + spacing, button_width, button_height)
        self.main_menu_button = pygame.Rect(button_x, 200 + (button_height + spacing) * 2, button_width, button_height)
        
    def display(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'resume'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.resume_button.collidepoint(event.pos):
                        debug.log('menu', "Pause Menu: Resuming game")
                        return 'resume'
                    elif self.settings_button.collidepoint(event.pos):
                        debug.log('menu', "Pause Menu: Entering Settings")
                        return 'settings'
                    elif self.main_menu_button.collidepoint(event.pos):
                        debug.log('menu', "Pause Menu: Returning to Main Menu")
                        return 'main_menu'
            
            # Create a semi-transparent overlay
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            # Draw buttons
            if self.draw_button("Resume", self.resume_button.x, self.resume_button.y, 
                                self.resume_button.width, self.resume_button.height, 
                                (200, 200, 200), (150, 150, 150)):
                return 'resume'
            
            if self.draw_button("Settings", self.settings_button.x, self.settings_button.y, 
                                self.settings_button.width, self.settings_button.height, 
                                (200, 200, 200), (150, 150, 150)):
                return 'settings'
            
            if self.draw_button("Main Menu", self.main_menu_button.x, self.main_menu_button.y, 
                                self.main_menu_button.width, self.main_menu_button.height, 
                                (200, 200, 200), (150, 150, 150)):
                return 'main_menu'
            
            pygame.display.flip()