import pygame
import sys
from scripts.game_state import current_game_state
from scripts.setting import current_settings

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def debug_print(message):
    print(f"[DEBUG] {message}")

class Menu:
    def __init__(self, screen):
        self.screen = screen

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
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect()
        text_rect.center = button_rect.center
        self.screen.blit(text_surf, text_rect)
        
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return None

class MainMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.last_click_time = 0
        self.click_delay = 300
        self.button_clicked = False

    def display(self):
        current_game_state.set_screen('main_menu')
        clock = pygame.time.Clock()
        
        while True:
            current_time = pygame.time.get_ticks()
            
            # Handle all events first
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.button_clicked = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu = PauseMenu(self.screen, current_game_state.get_screen())
                        return pause_menu.display()

            background_image = pygame.image.load('data/raw/Background/background-image.png')
            background_image = pygame.transform.scale(background_image, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(background_image, (0, 0))

            font = pygame.font.Font(None, 74)
            title_text = font.render('CollectCat', True, BLACK)
            self.screen.blit(title_text, (self.screen.get_width() // 2 - title_text.get_width() // 2, 20))

            # Start Game button with delay check
            if self.draw_button('Start Game', self.screen.get_width()//2 - 100, 200, 200, 50, (200, 200, 200), (150, 150, 150)):
                if not self.button_clicked and current_time - self.last_click_time > self.click_delay:
                    self.button_clicked = True
                    self.last_click_time = current_time
                    # Clear all pending events before transition
                    pygame.event.clear()
                    pygame.time.wait(300)  # Wait before transition
                    return 'start_game'

            # Settings button with delay check
            if self.draw_button('Settings', self.screen.get_width()//2 - 100, 300, 200, 50, (200, 200, 200), (150, 150, 150)):
                if not self.button_clicked and current_time - self.last_click_time > self.click_delay:
                    self.button_clicked = True
                    self.last_click_time = current_time
                    return 'settings'

            self.draw_button('Credits', self.screen.get_width()//2 - 100, 400, 200, 50, (200, 200, 200), (150, 150, 150))

            pygame.display.flip()
            clock.tick(60)

class LevelSelectionMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.last_click_time = 0
        self.click_delay = 300
        self.button_clicked = False

    def display(self):
        current_game_state.set_screen('level_selection')
        clock = pygame.time.Clock()
        
        # Clear any pending events and wait before accepting input
        pygame.event.clear()
        pygame.time.wait(200)
        
        while True:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.button_clicked = False

            self.screen.fill(WHITE)

            screen_width = self.screen.get_width()
            button_width = 150
            button_height = 50
            spacing = (screen_width - (3 * button_width)) // 4
            x1 = spacing
            x2 = 2 * spacing + button_width
            x3 = 3 * spacing + 2 * button_width
            y_position = 200

            # Back button position (centered horizontally and near bottom of screen)
            back_button_x = screen_width // 2 - button_width // 2
            back_button_y = self.screen.get_height() - 100  # 100 pixels from bottom

            font = pygame.font.Font(None, 74)
            title_text = font.render('Select Level', True, BLACK)
            self.screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

            # Get current mouse state
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            # Level buttons with delay checks
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

            # Back button with same styling and delay check
            if self.draw_button('Back', back_button_x, back_button_y, button_width, button_height, (200, 200, 200), (150, 150, 150)):
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
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.last_click_time = 0
        self.click_delay = 200  # 200 milliseconds delay between clicks
        self.from_pause = from_pause

    def display(self):
        clock = pygame.time.Clock()
        
        while True:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'main_menu'

            self.screen.fill(self.WHITE)

            # Draw title
            font = pygame.font.Font(None, 48)
            title_text = font.render("Settings", True, self.BLACK)
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(title_text, title_rect)

            y_start = 150
            spacing = 60

            # Music Volume
            self.draw_setting_label("Music Volume:", y_start)
            volume_value = f"{int(self.settings.bg_music_volume)}%"
            if self.draw_button(volume_value, self.screen.get_width()//2 + 50, y_start, 100, 40, (200, 200, 200), (150, 150, 150)):
                if current_time - self.last_click_time > self.click_delay:
                    self.settings.bg_music_volume = (self.settings.bg_music_volume + 10) % 110
                    self.last_click_time = current_time

            # Window Mode
            self.draw_setting_label("Window Mode:", y_start + spacing)
            mode_text = "Fullscreen" if not self.settings.window_mode else "Windowed"
            if self.draw_button(mode_text, self.screen.get_width()//2 + 50, y_start + spacing, 150, 40, (200, 200, 200), (150, 150, 150)):
                if current_time - self.last_click_time > self.click_delay:
                    self.settings.toggle_window_mode()
                    self.last_click_time = current_time

            # Character Speed
            self.draw_setting_label("Character Speed:", y_start + spacing * 2)
            speed_value = f"{self.settings.character_speed:.1f}x"
            if self.draw_button(speed_value, self.screen.get_width()//2 + 50, y_start + spacing * 2, 100, 40, (200, 200, 200), (150, 150, 150)):
                if current_time - self.last_click_time > self.click_delay:
                    new_speed = round(self.settings.character_speed + 0.5, 1)
                    if new_speed > 10:
                        new_speed = 1.0
                    self.settings.adjust_character_speed(new_speed)
                    self.last_click_time = current_time

            # Back button
            back_text = 'Back to Game' if self.from_pause else 'Back'
            if self.draw_button(back_text, self.screen.get_width()//2 - 100, self.screen.get_height() - 100, 200, 50, (200, 200, 200), (150, 150, 150)):
                if current_time - self.last_click_time > self.click_delay:
                    return 'resume' if self.from_pause else 'main_menu'

            pygame.display.flip()
            clock.tick(60)

    def draw_setting_label(self, text, y):
        font = pygame.font.Font(None, 36)
        label = font.render(text, True, self.BLACK)
        self.screen.blit(label, (50, y))

class PauseMenu:
    def __init__(self, screen, previous_screen, settings):
        self.screen = screen
        self.previous_screen = previous_screen
        self.settings = settings
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Define button dimensions and positions
        button_width = 200
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        spacing = 20  # Space between buttons
        
        # Create button rectangles with proper centering
        self.resume_button = pygame.Rect(button_x, 200, button_width, button_height)
        self.settings_button = pygame.Rect(button_x, 200 + button_height + spacing, button_width, button_height)
        self.main_menu_button = pygame.Rect(button_x, 200 + (button_height + spacing) * 2, button_width, button_height)
        
    def display(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if mouse is over any button
            resume_hover = self.resume_button.collidepoint(mouse_pos)
            settings_hover = self.settings_button.collidepoint(mouse_pos)
            main_menu_hover = self.main_menu_button.collidepoint(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'resume'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Use the full button rectangles for click detection
                    if self.resume_button.collidepoint(event.pos):
                        return 'resume'
                    elif self.settings_button.collidepoint(event.pos):
                        return 'settings'
                    elif self.main_menu_button.collidepoint(event.pos):
                        return 'main_menu'
            
            # Draw semi-transparent background
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            # Draw buttons with hover effect
            self.draw_button(self.resume_button, "Resume", resume_hover)
            self.draw_button(self.settings_button, "Settings", settings_hover)
            self.draw_button(self.main_menu_button, "Main Menu", main_menu_hover)
            
            pygame.display.flip()
    
    def draw_button(self, rect, text, hovered):
        # Draw button background
        color = (200, 200, 200) if not hovered else (180, 180, 180)
        pygame.draw.rect(self.screen, color, rect)
        
        # Add a border to make the button more visible
        pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)
        
        # Draw text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)