import pygame
import sys
from src.game.game_state import current_game_state
from config.setting import current_settings
from src.utils.constant import Colors
from src.utils.resource_manager import ResourceManager  # Make sure to import ResourceManager

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

    def draw_button(self, text, x, y, width, height, inactive_color, active_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        button_rect = pygame.Rect(x, y, width, height)
        
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, active_color, button_rect)
            if click[0] == 1:
                print(f"{text} button clicked! Mouse pos: {mouse}")
                return True
        else:
            pygame.draw.rect(self.screen, inactive_color, button_rect)
        
        font = pygame.font.Font(None, 30)
        text_surf = font.render(text, True, Colors.BLACK)
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return False

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
        
        # Load the background image from ResourceManager
        background_image = self.resource_manager.get_image('main_background')

        while True:
            current_time = pygame.time.get_ticks()

            # Handle events
            event_result = self.handle_events()
            if event_result == 'resume':
                pause_menu = PauseMenu(self.screen, current_game_state.get_screen())
                return pause_menu.display()

            # Draw the background image
            if background_image:
                self.screen.blit(background_image, (0, 0))

            # Draw title
            font = pygame.font.Font(None, 74)
            title_text = font.render('CollectCat', True, Colors.BLACK)
            self.screen.blit(title_text, (self.screen.get_width() // 2 - title_text.get_width() // 2, 20))

            # Start Game button with delay check
            if self.draw_button(BUTTON_TEXTS['start_game'], self.screen.get_width() // 2 - 100, 200, 200, 50, (200, 200, 200), (150, 150, 150)):
                if not self.button_clicked and current_time - self.last_click_time > self.click_delay:
                    self.button_clicked = True
                    self.last_click_time = current_time
                    pygame.event.clear()
                    pygame.time.wait(300)  # Wait before transition
                    return 'start_game'

            # Settings button with delay check
            if self.draw_button(BUTTON_TEXTS['settings'], self.screen.get_width() // 2 - 100, 300, 200, 50, (200, 200, 200), (150, 150, 150)):
                if not self.button_clicked and current_time - self.last_click_time > self.click_delay:
                    self.button_clicked = True
                    self.last_click_time = current_time
                    return 'settings'

            self.draw_button(BUTTON_TEXTS['credits'], self.screen.get_width() // 2 - 100, 400, 200, 50, (200, 200, 200), (150, 150, 150))

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
        background_image = self.resource_manager.get_image('main_background')

        while True:
            current_time = pygame.time.get_ticks()
            self.handle_events()

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

            if self.draw_button('Level 1', x1, y_position, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                if not self.button_clicked and current_time - self.last_click_time > self.click_delay:
                    self.button_clicked = True
                    self.last_click_time = current_time
                    pygame.event.clear()
                    return 1

            if self.draw_button('Level 2', x2, y_position, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                if not self.button_clicked and current_time - self.last_click_time > self.click_delay:
                    self.button_clicked = True
                    self.last_click_time = current_time
                    pygame.event.clear()
                    return 2

            if self.draw_button('Level 3', x3, y_position, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                if not self.button_clicked and current_time - self.last_click_time > self.click_delay:
                    self.button_clicked = True
                    self.last_click_time = current_time
                    pygame.event.clear()
                    return 3

            if self.draw_button(BUTTON_TEXTS['back'], back_button_x, back_button_y, button_width, button_height, (200, 200, 200), (150, 150, 150)):
                if not self.button_clicked and current_time - self.last_click_time > self.click_delay:
                    self.button_clicked = True
                    self.last_click_time = current_time
                    pygame.event.clear()
                    return 'main_menu'

            pygame.display.flip()
            clock.tick(60)

class SettingsMenu(Menu):
    def __init__(self, screen, settings, from_pause=False):
        super().__init__(screen)
        self.settings = settings
        self.last_click_time = 0
        self.click_delay = 200
        self.from_pause = from_pause

    def display(self):
        clock = pygame.time.Clock()
        
        while True:
            current_time = pygame.time.get_ticks()
            self.handle_events()

            self.screen.fill(Colors.WHITE)

            # Load the background image from ResourceManager
            background_image = self.resource_manager.get_image('main_background')
            if background_image:
                self.screen.blit(background_image, (0, 0))

            font = pygame.font.Font(None, 48)
            title_text = font.render("Settings", True, Colors.BLACK)
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(title_text, title_rect)

            y_start = 150
            spacing = 60

            self.draw_setting_label("Music Volume:", y_start)
            volume_value = f"{int(self.settings.bg_music_volume)}%"
            if self.draw_button(volume_value, self.screen.get_width() // 2 +  50, y_start, 100, 40, (200, 200, 200), (150, 150, 150)):
                if current_time - self.last_click_time > self.click_delay:
                    self.settings.bg_music_volume = (self.settings.bg_music_volume + 10) % 110
                    self.last_click_time = current_time

            self.draw_setting_label("Window Mode:", y_start + spacing)
            mode_text = "Fullscreen" if not self.settings.window_mode else "Windowed"
            if self.draw_button(mode_text, self.screen.get_width() // 2 + 50, y_start + spacing, 150, 40, (200, 200, 200), (150, 150, 150)):
                if current_time - self.last_click_time > self.click_delay:
                    self.settings.toggle_window_mode()
                    self.last_click_time = current_time

            self.draw_setting_label("Character Speed:", y_start + spacing * 2)
            speed_value = f"{self.settings.character_speed:.1f}x"
            if self.draw_button(speed_value, self.screen.get_width() // 2 + 50, y_start + spacing * 2, 100, 40, (200, 200, 200), (150, 150, 150)):
                if current_time - self.last_click_time > self.click_delay:
                    new_speed = round(self.settings.character_speed + 0.5, 1)
                    if new_speed > 10:
                        new_speed = 1.0
                    self.settings.adjust_character_speed(new_speed)
                    self.last_click_time = current_time

            back_text = 'Back to Game' if self.from_pause else 'Back'
            if self.draw_button(back_text, self.screen.get_width() // 2 - 100, self.screen.get_height() - 100, 200, 50, (200, 200, 200), (150, 150, 150)):
                if current_time - self.last_click_time > self.click_delay:
                    return 'resume' if self.from_pause else 'main_menu'

            pygame.display.flip()
            clock.tick(60)

    def draw_setting_label(self, text, y):
        font = pygame.font.Font(None, 36)
        label = font.render(text, True, Colors.BLACK)
        self.screen.blit(label, (50, y))

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
            
            resume_hover = self.resume_button.collidepoint(mouse_pos)
            settings_hover = self.settings_button.collidepoint(mouse_pos)
            main_menu_hover = self.main_menu_button.collidepoint(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'resume'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.resume_button.collidepoint(event.pos):
                        return 'resume'
                    elif self.settings_button.collidepoint(event.pos):
                        return 'settings'
                    elif self.main_menu_button.collidepoint(event.pos):
                        return 'main_menu'
            
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            self.draw_button(self.resume_button, "Resume", resume_hover)
            self.draw_button(self.settings_button, "Settings", settings_hover)
            self.draw_button(self.main_menu_button, "Main Menu", main_menu_hover)
            
            pygame.display.flip()