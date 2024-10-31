import pygame
import sys
from scripts.character import Character
from scripts.movement import move_character
from scripts.interface import MainMenu, LevelSelectionMenu, PauseMenu
from scripts.game_state import current_game_state
from scripts.setting import Setting

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Setting()
        # Remove the character initialization from here
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.menu = MainMenu(self.screen)
        pygame.display.set_caption('CollectCat')
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        
        # Initialize menu classes
        self.main_menu = MainMenu(self.screen)
        self.level_menu = LevelSelectionMenu(self.screen)
        
        self.idle_image_paths = [
            'data/raw/Character/Idle/pixil-frame-0.png', 
            'data/raw/Character/Idle/pixil-frame-0 (1).png'
        ]
        self.running_image_paths = [
            'data/raw/Character/running/pixil-frame-0 (2).png', 
            'data/raw/Character/running/pixil-frame-0 (3).png'
        ]
        
        self.character = None  # Initialize as None

    def debug_print(self, message):
        print(f"[DEBUG] {message}")

    def error_print(self, message):
        print(f"[ERROR] {message}")

    def start_game(self, level):
        self.debug_print("Starting the game...")
        
        current_game_state.set_screen('game')
        current_game_state.set_level(level)
        
        try:
            self.character = Character(self.screen_width // 2, self.screen_height // 2, 50, 50, self.RED, 
                                self.idle_image_paths, self.running_image_paths)
            self.debug_print("Character initialized successfully.")
        except Exception as e:
            self.error_print(f"Failed to initialize character: {e}")
            return

        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'quit'
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pause_menu = PauseMenu(self.screen, current_game_state.get_screen())
                            result = pause_menu.display()
                            if result == 'exit':
                                return 'main_menu'
                            elif result == 'level_selection':
                                return 'level_selection'
                            elif result == 'settings':
                                self.show_settings()

                keys_pressed = pygame.key.get_pressed()
                move_character(self.character, keys_pressed, self.screen_width, self.screen_height, self.settings)

                self.screen.fill(self.WHITE)
                self.character.update()  
                self.character.draw(self.screen)  

                font = pygame.font.Font(None, 36)
                level_text = font.render(f'Level {level}', True, self.BLACK)
                self.screen.blit(level_text, (10, 10))

                pygame.display.flip()
            
            except Exception as e:
                self.error_print(f"An error occurred during the game loop: {e}")

    def show_settings(self):
        self.debug_print("Entering settings menu...")
        running = True
        clock = pygame.time.Clock()

        input_active = None
        input_text = {
            'volume': str(int(self.settings.bg_music_volume)),
            'speed': f"{self.settings.character_speed:.1f}"
        }
        temp_text = {
            'volume': str(int(self.settings.bg_music_volume)),
            'speed': f"{self.settings.character_speed:.1f}"
        }

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif input_active:
                        if event.key == pygame.K_RETURN:
                            try:
                                if input_active == 'volume':
                                    new_value = int(temp_text['volume'])
                                    if 0 <= new_value <= 100:
                                        self.settings.bg_music_volume = new_value
                                        input_text['volume'] = str(new_value)
                                    else:
                                        temp_text['volume'] = input_text['volume']
                                elif input_active == 'speed':
                                    new_value = float(temp_text['speed'])
                                    if 0 <= new_value <= 10:
                                        self.settings.character_speed = new_value
                                        input_text['speed'] = f"{new_value:.1f}"
                                    else:
                                        temp_text['speed'] = input_text['speed']
                            except ValueError:
                                # If conversion fails, revert to previous valid value
                                temp_text[input_active] = input_text[input_active]
                            input_active = None
                        elif event.key == pygame.K_BACKSPACE:
                            temp_text[input_active] = temp_text[input_active][:-1]
                        else:
                            # Only allow numbers and decimal point
                            if event.unicode.isnumeric() or (event.unicode == '.' and input_active == 'speed' and '.' not in temp_text['speed']):
                                temp_text[input_active] += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if volume_input_rect.collidepoint(mouse_pos):
                        input_active = 'volume'
                        temp_text['volume'] = input_text['volume']
                    elif speed_input_rect.collidepoint(mouse_pos):
                        input_active = 'speed'
                        temp_text['speed'] = input_text['speed']
                    else:
                        input_active = None

            self.screen.fill(self.WHITE)

            # Draw title
            font = pygame.font.Font(None, 48)
            title_text = font.render("Settings", True, self.BLACK)
            title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
            self.screen.blit(title_text, title_rect)

            settings_font = pygame.font.Font(None, 36)
            y_position = 150

            # Music Volume
            volume_text = settings_font.render("Music Volume (0-100):", True, self.BLACK)
            volume_rect = volume_text.get_rect(left=50, top=y_position)
            self.screen.blit(volume_text, volume_rect)

            volume_input_rect = pygame.Rect(volume_rect.right + 20, y_position, 100, 40)
            pygame.draw.rect(self.screen, 
                            (170, 170, 170) if input_active == 'volume' else (200, 200, 200), 
                            volume_input_rect)
            volume_surface = settings_font.render(
                temp_text['volume'] if input_active == 'volume' else input_text['volume'], 
                True, 
                self.BLACK
            )
            self.screen.blit(volume_surface, (volume_input_rect.x + 5, volume_input_rect.y + 5))

            # Window Mode
            y_position += 60
            window_text = settings_font.render("Window Mode:", True, self.BLACK)
            window_rect = window_text.get_rect(left=50, top=y_position)
            self.screen.blit(window_text, window_rect)

            mode_text = "Fullscreen" if not self.settings.window_mode else "Windowed"
            if self.menu.draw_button(mode_text, window_rect.right + 20, y_position, 150, 40, (200, 200, 200), (150, 150, 150)):
                self.settings.toggle_window_mode()

            # Character Speed
            y_position += 60
            speed_text = settings_font.render("Character Speed (0-10):", True, self.BLACK)
            speed_rect = speed_text.get_rect(left=50, top=y_position)
            self.screen.blit(speed_text, speed_rect)

            speed_input_rect = pygame.Rect(speed_rect.right + 20, y_position, 100, 40)
            pygame.draw.rect(self.screen, 
                            (170, 170, 170) if input_active == 'speed' else (200, 200, 200), 
                            speed_input_rect)
            speed_surface = settings_font.render(
                temp_text['speed'] if input_active == 'speed' else input_text['speed'], 
                True, 
                self.BLACK
            )
            self.screen.blit(speed_surface, (speed_input_rect.x + 5, speed_input_rect.y + 5))

            # Back button
            back_y = self.screen_height - 100
            if self.menu.draw_button("Back", self.screen_width // 2 - 100, back_y, 200, 50, (200, 200, 200), (150, 150, 150)):
                running = False

            pygame.display.flip()
            clock.tick(60)

        self.debug_print("Exiting settings menu...")

        if not self.settings.window_mode:
            pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((self.screen_width, self.screen_height))

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        current_game_state.set_screen('main_menu')
        
        while True:
            try:
                # Use MainMenu class
                menu_option = self.main_menu.display()
                self.debug_print(f"Menu option selected: {menu_option}")
                
                if menu_option == 'start_game':
                    # Use LevelSelectionMenu class
                    level = self.level_menu.display()
                    self.debug_print(f"Level selected: {level}")
                    
                    result = self.start_game(level)
                    if result == 'quit':
                        break
                    elif result == 'main_menu':
                        continue
                    elif result == 'level_selection':
                        continue
                    elif result == 'settings':
                        self.show_settings()
                elif menu_option == 'settings':
                    self.show_settings()
                elif menu_option == 'quit':
                    break
                    
            except Exception as e:
                self.error_print(f"An error occurred in the main loop: {e}")

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()