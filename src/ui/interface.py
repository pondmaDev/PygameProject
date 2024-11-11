import pygame
import sys
from src.game.game_state import current_game_state
from config.setting import current_settings
from src.utils.constant import Colors
from src.utils.resource_manager import ResourceManager  # Make sure to import ResourceManager
from src.utils.debug_section import debug
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
            font = pygame.font.Font(None, 74)
            title_text = font.render('Collect Cat', True, Colors.BLACK)
            title_rect = title_text.get_rect(center=(screen_width // 2, 100))
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
        try:
            super().__init__(screen)
            
            # Validate inputs
            if screen is None:
                raise ValueError("Screen cannot be None")
            if settings is None:
                raise ValueError("Settings cannot be None")
            
            # Use a deep copy to prevent direct modification of original settings
            self.settings = settings
            self.original_settings = {
                'bg_music_volume': settings.bg_music_volume,
                'window_mode': settings.window_mode,
                'character_speed': settings.character_speed
            }
            
            self.last_click_time = 0
            self.click_delay = 200
            self.from_pause = from_pause
            
        except Exception as init_error:
            debug.error('settings', f"Settings menu initialization error: {init_error}")
            raise

    def display(self):
        clock = pygame.time.Clock()
        
        try:
            # Set current game state
            current_game_state.set_screen('settings')
            
            # Load background image with error handling
            try:
                background_image = self.resource_manager.get_image('main_background')
            except Exception as bg_error:
                debug.warning('settings', f"Failed to load background image: {bg_error}")
                background_image = None

            while True:
                current_time = pygame.time.get_ticks()
                
                # Comprehensive event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'quit'
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Use the new handle_exit method
                            return self.handle_exit()

                # Render screen
                self.screen.fill(Colors.WHITE)

                # Draw background
                if background_image:
                    self.screen.blit(background_image, (0, 0))

                # Render title
                font = pygame.font.Font(None, 48)
                title_text = font.render("Settings", True, Colors.BLACK)
                title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
                self.screen.blit(title_text, title_rect)

                # Render settings options
                y_start = 150
                spacing = 60

                # Music Volume Setting
                self.render_setting_option(
                    "Music Volume:", 
                    f"{int(self.settings.bg_music_volume)}%", 
                    y_start, 
                    current_time,
                    self.adjust_volume
                )

                # Window Mode Setting
                self.render_setting_option(
                    "Window Mode:", 
                    "Fullscreen" if not self.settings.window_mode else "Windowed", 
                    y_start + spacing, 
                    current_time,
                    self.toggle_window_mode
                )

                # Character Speed Setting
                self.render_setting_option(
                    "Character Speed:", 
                    f"{self.settings.character_speed:.1f}x", 
                    y_start + spacing * 2, 
                    current_time,
                    self.adjust_character_speed
                )

                # Back button with dynamic text
                back_text = 'Back to Game' if self.from_pause else 'Back'
                if self.draw_button(
                    back_text, 
                    self.screen.get_width() // 2 - 100, 
                    self.screen.get_height() - 100, 
                    200, 50, 
                    (200, 200, 200), 
                    (150, 150, 150)
                ):
                    # Use the new handle_exit method
                    return self.handle_exit()

                pygame.display.flip()
                clock.tick(60)

        except Exception as display_error:
            debug.error('settings', f"Error in settings menu display: {display_error}")
            # Fallback to main menu or resume based on context
            return 'resume' if self.from_pause else 'main_menu'

    def render_setting_option(self, label, value, y_pos, current_time, action):
        """
        Render a single setting option with consistent error handling
        """
        try:
            # Draw label
            self.draw_setting_label(label, y_pos)
            
            # Draw value button
            if self.draw_button(
                value, 
                self.screen.get_width() // 2 + 50, 
                y_pos, 
                150, 40, 
                (200, 200, 200), 
                (150, 150, 150)
            ):
                if current_time - self.last_click_time > self.click_delay:
                    try:
                        action()
                        self.last_click_time = current_time
                    except Exception as action_error:
                        debug.error('settings', f"Error in setting action: {action_error}")
        except Exception as render_error:
            debug.error('settings', f"Error rendering setting option {label}: {render_error}")

    def adjust_volume(self):
        """Safely adjust volume"""
        try:
            new_volume = (self.settings.bg_music_volume + 10) % 110
            self.settings.adjust_bg_music_volume(new_volume)
            debug.log('settings', f"Volume adjusted to {new_volume}")
        except Exception as volume_error:
            debug.error('settings', f"Volume adjustment error: {volume_error}")

    def toggle_window_mode(self):
        """Safely toggle window mode"""
        try:
            self.settings.toggle_window_mode()
            debug.log('settings', f"Window mode changed to {self.settings.window_mode}")
        except Exception as mode_error:
            debug.error('settings', f"Window mode toggle error: {mode_error}")

    def adjust_character_speed(self):
        """Safely adjust character speed"""
        try:
            new_speed = round(self.settings.character_speed + 0.5, 1)
            if new_speed > 10:
                new_speed = 1.0
            self.settings.adjust_character_speed(new_speed)
            debug.log('settings', f"Character speed adjusted to {new_speed}")
        except Exception as speed_error:
            debug.error('settings', f"Character speed adjustment error: {speed_error}")

    def handle_exit(self):
        """
        Handle exiting the settings menu with change tracking
        
        Returns:
            str: Appropriate screen to return to
        """
        try:
            # Check if any settings were modified
            settings_changed = any([
                self.settings.bg_music_volume != self.original_settings['bg_music_volume'],
                self.settings.window_mode != self.original_settings['window_mode'],
                self.settings.character_speed != self.original_settings['character_speed']
            ])

            if settings_changed:
                # Optional: Add a confirmation dialog or auto-save
                try:
                    # Save settings to a default config file
                    self.settings.save_settings('config/user_settings.json')
                    debug.log('settings', "Settings saved successfully")
                except Exception as save_error:
                    debug.error('settings', f"Failed to save settings: {save_error}")

            # Explicitly return to the appropriate screen based on context
            debug.log('settings', f"Exiting settings from_pause: {self.from_pause}")
            
            # Key change: Always return 'resume' when from pause menu
            if self.from_pause:
                return 'resume'
            
            return 'main_menu'

        except Exception as exit_error:
            debug.error('settings', f"Error handling settings exit: {exit_error}")
            # Fallback to main menu if something goes wrong
            return 'main_menu'

    def draw_setting_label(self, text, y):
        """
        Draw setting label with error handling
        """
        try:
            font = pygame.font.Font(None, 36)
            label = font.render(text, True, Colors.BLACK)
            self.screen.blit(label, (50, y))
        except Exception as label_error:
            debug.error('settings', f"Error drawing setting label: {label_error}")

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