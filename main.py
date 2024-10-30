import pygame
import sys
from scripts.character import Character
from scripts.movement import move_character
from scripts.interface import main_menu, level_selection, pause_menu
from scripts.game_state import current_game_state

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

 # Debug and Error 
def error_print(message):
    print(f"[ERROR] {message}")

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CollectCat')


# Example paths for idle and running images
idle_image_paths = [
    'data/raw/Character/Idle/pixil-frame-0.png', 
    'data/raw/Character/Idle/pixil-frame-0 (1).png'
]
running_image_paths = [
    'data/raw/Character/running/pixil-frame-0 (2).png', 
    'data/raw/Character/running/pixil-frame-0 (3).png'
]

def debug_print(message):
    print(f"[DEBUG] {message}")

def error_print(message):
    print(f"[ERROR] {message}")

def start_game(level):
    global character
    debug_print("Starting the game...")
    
    current_game_state.set_screen('game')
    current_game_state.set_level(level)
    
    try:
        character = Character(screen_width // 2, screen_height // 2, 50, 50, RED, 
                              idle_image_paths, running_image_paths)
        debug_print("Character initialized successfully.")
    except Exception as e:
        error_print(f"Failed to initialize character: {e}")
        return

    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        result = pause_menu(screen, current_game_state.get_screen())
                        if result == 'exit':
                            return  # Return to main menu
                        elif result == 'level_selection':
                            return 'level_selection'
                        elif result == 'settings':
                            # Implement settings
                            pass

            keys_pressed = pygame.key.get_pressed()
            move_character(character, keys_pressed, screen_width, screen_height)

            screen.fill(WHITE)
            character.update()  
            character.draw(screen)  

            font = pygame.font.Font(None, 36)
            level_text = font.render(f'Level {level}', True, BLACK)
            screen.blit(level_text, (10, 10))

            pygame.display.flip()
        
        except Exception as e:
            error_print(f"An error occurred during the game loop: {e}")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    current_game_state.set_screen('main_menu')
    
    while True:
        try:
            menu_option = main_menu(screen)
            debug_print(f"Menu option selected: {menu_option}")
            if menu_option == 'start_game':
                level = level_selection(screen)
                debug_print(f"Level selected: {level}")
                result = start_game(level)
                if result == 'level_selection':
                    continue
        except Exception as e:
            error_print(f"An error occurred in the main loop: {e}")


if __name__ == "__main__":
    while True:
        try:
            menu_option = main_menu(screen)
            debug_print(f"Menu option selected: {menu_option}")
            if menu_option == 'start_game':
                level = level_selection(screen)  # Ensure level selection is called here
                debug_print(f"Level selected: {level}")
                start_game(level)  # Start the game with the selected level
        except Exception as e:
            error_print(f"An error occurred in the main loop: {e}")