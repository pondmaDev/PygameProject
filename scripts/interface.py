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

            pygame.display.flip()
            clock.tick(60)

class SettingsMenu(Menu):
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.last_click_time = 0
        self.click_delay = 200  # 200 milliseconds delay between clicks

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
            if self.draw_button("Back", self.screen.get_width()//2 - 100, self.screen.get_height() - 100, 200, 50, (200, 200, 200), (150, 150, 150)):
                if current_time - self.last_click_time > self.click_delay:
                    return 'main_menu'

            pygame.display.flip()
            clock.tick(60)

    def draw_setting_label(self, text, y):
        font = pygame.font.Font(None, 36)
        label = font.render(text, True, self.BLACK)
        self.screen.blit(label, (50, y))

class PauseMenu(Menu):
    def __init__(self, screen, previous_screen):
        super().__init__(screen)
        self.previous_screen = previous_screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font = pygame.font.Font(None, 36)
        
        # Define buttons
        self.buttons = {
            'resume': pygame.Rect(self.width//2 - 100, self.height//2 - 60, 200, 50),
            'settings': pygame.Rect(self.width//2 - 100, self.height//2, 200, 50),
            'main_menu': pygame.Rect(self.width//2 - 100, self.height//2 + 60, 200, 50)
        }

    def display(self):
        menu_width = 300
        menu_height = 400
        menu_x = self.screen.get_width()//2 - menu_width//2
        menu_y = self.screen.get_height()//2 - menu_height//2

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'resume'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Resume button
                    if self.buttons['resume'].collidepoint(mouse_pos):
                        return 'resume'
                    
                    # Settings button
                    if self.buttons['settings'].collidepoint(mouse_pos):
                        return 'settings'
                    
                    # Main menu button
                    if self.buttons['main_menu'].collidepoint(mouse_pos):
                        return 'main_menu'

            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))

            pygame.draw.rect(self.screen, (200, 200, 200), 
                            (menu_x, menu_y, menu_width, menu_height))

            font = pygame.font.Font(None, 48)
            title_text = font.render('Pause Menu', True, BLACK)
            self.screen.blit(title_text, (menu_x + menu_width//2 - title_text.get_width()//2, 
                                    menu_y + 20))

            button_width = 200
            button_height = 50
            button_x = menu_x + (menu_width - button_width)//2
            
            if self.draw_button('Level Selection', button_x, menu_y + 100, 
                          button_width, button_height, (180, 180, 180), (150, 150, 150)):
                return 'level_selection'

            if self.draw_button('Settings', button_x, menu_y + 170, 
                          button_width, button_height, (180, 180, 180), (150, 150, 150)):
                return 'settings'

            exit_text = 'Exit Game' if self.previous_screen == 'main_menu' else 'Main Menu'
            if self.draw_button(exit_text, button_x, menu_y + 240, 
                          button_width, button_height, (180, 180, 180), (150, 150, 150)):
                return 'exit'

            pygame.display.flip()