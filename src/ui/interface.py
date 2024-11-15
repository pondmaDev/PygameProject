import pygame
import sys
import time
from src.game.game_state import current_game_state
from config.setting import current_settings
from src.utils.constant import Colors
from src.utils.resource_manager import ResourceManager  # Make sure to import ResourceManager
from src.utils.debug_section import debug
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
        if screen is None:
            raise ValueError("Screen cannot be None")

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
            
            # More comprehensive event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'quit'
                
                # Add mouse click event handling
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Reset button clicked state
                    self.button_clicked = False

            self.screen.fill(Colors.WHITE)

            if background_image:
                self.screen.blit(background_image, (0, 0))

            screen_width = self.screen.get_width()
            button_width = 200
            button_height = 50
            button_x = screen_width // 2 - button_width // 2
            
            # Title
            font = pygame.font.Font('assets/font/River Adventurer.ttf', 100)
            title_text = font.render('Collect Cat', True, Colors.BLACK)
            if int(time.time() * 2) % 2 == 0:  # กระพริบข้อความทุกๆ ครึ่งวินาที
                title_text = font.render('Collect Cat', True, pygame.Color(50, 50, 50))
            else:
                title_text = font.render('Collect Cat', True,  pygame.Color(139, 69, 19))

            title_rect = title_text.get_rect(center=(screen_width // 2, 100))
            mouse_x, mouse_y = pygame.mouse.get_pos()
            text_color = pygame.Color(128, 128, 128) if title_rect.collidepoint(mouse_x, mouse_y) else Colors.BLACK  
            self.screen.blit(title_text, title_rect)


            # Button positions
            start_button_y = 250
            settings_button_y = start_button_y + button_height + 20
            quit_button_y = settings_button_y + button_height + 20

            # Start Game Button
            if self.draw_button('Start Game', button_x, start_button_y, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                debug.log('menu', "Start Game selected")
                return 'start_game'

            # Settings Button
            if self.draw_button('Settings', button_x, settings_button_y, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                # font = pygame.font.Font(None, 36)  # ตั้งค่าฟอนต์และขนาด
                # text = font.render('Settings', True, (50, 200, 200))  # สีข้อความ
                # text_rect = text.get_rect(center=(button_x + button_width // 2, settings_button_y + button_height // 2))
                # self.screen.blit(text, text_rect)

                debug.log('menu', "Settings selected")
                return 'settings'

            # Quit Button
            if self.draw_button('Quit', button_x, quit_button_y, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                debug.log('menu', "Quit selected")
                return 'quit'

            pygame.display.flip()
            clock.tick(60)

class LevelSelectionMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.last_click_time = 0
        self.click_delay =  300
        self.button_clicked = False

    def display(self):
        current_game_state.set_screen('level_selection')
        clock = pygame.time.Clock()
        
        pygame.event.clear()
        pygame.time.wait(200)
        
       # Load the background image from ResourceManager
        try:
            background_image = self.resource_manager.get_image('main_background')
        except Exception as e:
            debug.error('menu', f"Failed to load background image: {e}")
            background_image = None
        try:
            while True:
                current_time = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'quit'
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return 'main_menu'
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Reset button clicked state
                        self.button_clicked = False

                self.screen.fill(Colors.WHITE)

                # Draw the background image
                if background_image:
                    self.screen.blit(background_image, (0, 0))

                screen_width = self.screen.get_width()
                button_width = 150
                button_height = 50
                spacing = (screen_width - (3 * button_width)) // 4
                x1 = spacing
                x2 = 2 * spacing + button_width
                x3 = 3 * spacing + 2 * button_width
                y_position = 200

                back_button_x = screen_width // 2 - button_width // 2
                back_button_y = self.screen.get_height() - 100

                font = pygame.font.Font(None, 74)
                title_text = font.render('Select Level', True, Colors.BLACK)
                self.screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

                 # Modify button handling to use mouse events instead of click state
                mouse_pos = pygame.mouse.get_pos()
                mouse_clicked = pygame.mouse.get_pressed()[0]

                # Level 1 Button
                level1_rect = pygame.Rect(x1, y_position, button_width, button_height)
                if self.draw_button('Level 1', x1, y_position, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                    if mouse_clicked and level1_rect.collidepoint(mouse_pos):
                        pygame.event.clear()
                        return 1

                # Level 2 Button
                level2_rect = pygame.Rect(x2, y_position, button_width, button_height)
                if self.draw_button('Level 2', x2, y_position, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                    if mouse_clicked and level2_rect.collidepoint(mouse_pos):
                        pygame.event.clear()
                        return 2

                # Level 3 Button
                level3_rect = pygame.Rect(x3, y_position, button_width, button_height)
                if self.draw_button('Level 3', x3, y_position, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                    if mouse_clicked and level3_rect.collidepoint(mouse_pos):
                        pygame.event.clear()
                        return 3

                # Back Button
                back_rect = pygame.Rect(back_button_x, back_button_y, button_width, button_height)
                if self.draw_button(BUTTON_TEXTS['back'], back_button_x, back_button_y, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                    if mouse_clicked and back_rect.collidepoint(mouse_pos):
                        pygame.event.clear()
                        return 'main_menu'

                pygame.display.flip()
                clock.tick(60)
        except Exception as e:
            debug.error('menu', f"Level selection error: {e}")
            return 'main_menu' 

class SettingsMenu(Menu):
    def __init__(self, screen, settings, from_pause=False):
        super().__init__(screen)
        self.settings = settings
        self.from_pause = from_pause
        
        # Input handling attributes
        self.input_active = False
        self.current_input_field = None
        self.input_text = ""
        
        # Define input configurations with more detailed validation
        self.setting_configs = {
            'bg_music_volume': {
                'label': 'Music Volume',
                'min': 0,
                'max': 100,
                'type': int,
                'description': 'Enter volume (0-100)'
            },
            'character_speed': {
                'label': 'Character Speed',
                'min': 1,
                'max': 10,
                'type': float,
                'description': 'Enter speed (1-10)'
            }
        }
        
        # Store original settings for potential reset
        self.original_settings = {
            key: getattr(settings, key) 
            for key in self.setting_configs.keys()
        }
        
        # Input rect tracking
        self.input_rects = {}
        self.input_font = pygame.font.Font(None, 36)
        self.description_font = pygame.font.Font(None, 24)

    def validate_and_clamp_input(self, value, config):
        """
        Validate and clamp input to the specified range
        
        Args:
            value (str): Input value
            config (dict): Setting configuration
        
        Returns:
            tuple: (processed_value, is_valid)
        """
        try:
            # Remove any non-numeric characters except decimal point and minus sign
            cleaned_value = re.sub(r'[^\d.-]', '', value)
            
            # Convert to appropriate type
            processed_value = config['type'](cleaned_value)
            
            # Clamp the value to the specified range
            clamped_value = max(config['min'], min(processed_value, config['max']))
            
            return clamped_value, True
        
        except (ValueError, TypeError):
            # If conversion fails, return the minimum value
            return config['min'], False

    def display(self):
        """
        Display the settings menu with text input
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
                    if self.input_active:
                        if event.key == pygame.K_RETURN:
                            # Validate and update the setting
                            self.update_setting()
                            self.input_active = False
                            self.current_input_field = None
                        elif event.key == pygame.K_BACKSPACE:
                            # Remove last character
                            self.input_text = self.input_text[:-1]
                        else:
                            # Add typed character
                            self.input_text += event.unicode
                
                # Mouse click handling for input fields
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a setting input field was clicked
                    for setting_key, config in self.setting_configs.items():
                        input_rect = self.input_rects.get(setting_key)
                        if input_rect and input_rect.collidepoint(event.pos):
                            self.input_active = True
                            self.current_input_field = setting_key
                            self.input_text = str(getattr(self.settings, setting_key))
                        else:
                            # Deactivate input if clicked outside
                            self.input_active = False
                            self.current_input_field = None
            
            # Clear screen
            self.screen.fill(Colors.WHITE)
            
            # Title
            title = self.input_font.render("Settings", True, Colors.BLACK)
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(title, title_rect)
            
            # Render settings
            y_start = 150
            spacing = 100
            
            for i, (setting_key, config) in enumerate(self.setting_configs.items()):
                current_value = getattr(self.settings, setting_key)
                
                # Label
                label = self.input_font.render(config['label'], True, Colors.BLACK)
                self.screen.blit(label, (self.screen.get_width() // 2 - 250, y_start + i * spacing))
                
                # Input field
                input_rect = pygame.Rect(
                    self.screen.get_width() // 2 - 100, 
                    y_start + i * spacing + 50, 
                    200, 
                    40
                )
                self.input_rects[setting_key] = input_rect
                
                # Draw input field
                input_color = Colors.LIGHTGRAY if self.current_input_field == setting_key else Colors.GRAY
                pygame.draw.rect(self.screen, input_color, input_rect)
                
                # Render current value or input text
                display_text = (self.input_text if self.current_input_field == setting_key 
                                else str(current_value))
                text_surface = self.input_font.render(display_text, True, Colors.BLACK)
                text_rect = text_surface.get_rect(center=input_rect.center)
                self.screen.blit(text_surface, text_rect)
                
                # Description
                description = self.description_font.render(
                    config['description'], 
                    True, 
                    Colors.GRAY
                )
                description_rect = description.get_rect(
                    center=(self.screen.get_width() // 2, y_start + i * spacing + 100)
                )
                self.screen.blit(description, description_rect)
            
            # Back button
            back_text = 'Back to Game' if self.from_pause else 'Back'
            if self.draw_button(
                back_text, 
                self.screen.get_width() // 2 - 100, 
                self.screen.get_height() - 100, 
                200, 50, 
                (200, 200, 200), 
                (150, 150, 150)
            ):
                return self.handle_exit()
            
            pygame.display.flip()
            clock.tick(60)

    def update_setting(self):
        """
        Update the setting with validated input
        """
        if self.current_input_field:
            config = self.setting_configs[self.current_input_field]
            
            # Validate and clamp input
            clamped_value, is_valid = self.validate_and_clamp_input(self.input_text, config)
            
            # Update the setting
            setattr(self.settings, self.current_input_field, clamped_value)
            
            # Special handling for music volume
            if self.current_input_field == 'bg_music_volume':
                try:
                    import pygame
                    pygame.mixer.music.set_volume(clamped_value / 100)
                except Exception as e:
                    debug.log('settings', f"Failed to adjust music volume: {e}")
            if not is_valid:
                debug.log('settings', f"Invalid input for {self.current_input_field}. "
                        f"Value clamped to {clamped_value}")
                
    def handle_exit(self):
        """
        Handle exiting the settings menu
        
        Returns:
            str: Screen to return to
        """
        debug.log('settings', "Saving settings")
        # Save settings before exiting
        self.settings.save()
        return 'pause' if self.from_pause else 'main_menu'

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