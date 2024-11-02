import pygame
import sys
from .game_state import current_game_state

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

class PauseMenu(Menu):
    def __init__(self, screen, current_screen):
        super().__init__(screen)
        self.current_screen = current_screen

    def display(self):
        menu_width = 300
        menu_height = 400
        menu_x = self.screen.get_width()//2 - menu_width//2
        menu_y = self.screen.get_height()//2 - menu_height//2

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None

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

            exit_text = 'Exit Game' if self.current_screen == 'main_menu' else 'Main Menu'
            if self.draw_button(exit_text, button_x, menu_y + 240, 
                          button_width, button_height, (180, 180, 180), (150, 150, 150)):
                return 'exit'

            pygame.display.flip()