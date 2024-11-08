import pygame
import sys
from src.game.game import Game as GameImplementation
from src.utils.debug_section import debug

def main():
    try:
        # Initialize Pygame
        pygame.init()

        # Create an instance of the game implementation
        game = GameImplementation()
        
        # Run the game loop
        current_screen = 'main_menu'
        
        while True:
            try:
                # Use the methods from the game implementation
                if current_screen == 'main_menu':
                    menu_option = game.main_menu.display()
                    debug.debug_print(f"Menu option selected: {menu_option}")
                    
                    if menu_option == 'start_game':
                        current_screen = 'level_selection'
                    elif menu_option == 'settings':
                        current_screen = 'settings'
                    elif menu_option == 'quit':
                        break
                
                elif current_screen == 'level_selection':
                    level = game.level_menu.display()
                    debug.debug_print(f"Level selected: {level}")
                    
                    if level == 'main_menu':
                        current_screen = 'main_menu'
                    elif isinstance(level, int):
                        # Start the game with the selected level
                        game_result = game.start_game(level)
                        debug.debug_print(f"Game result: {game_result}")
                        
                        if game_result == 'quit':
                            break
                        elif game_result == 'main_menu':
                            current_screen = 'main_menu'
                
                elif current_screen == 'settings':
                    settings_result = game.show_settings()
                    debug.debug_print(f"Settings result: {settings_result}")
                    
                    current_screen = 'main_menu'
                    
            except Exception as e:
                debug.error_print(f"An error occurred: {e}")
                break

    except Exception as e:
        debug.error_print(f"Initialization error: {e}")
    
    finally:
        # Cleanup
        pygame.quit()
        sys.exit()

# Remove the class definition entirely
# Remove the if __name__ == "__main__": block with the Game() instantiation

if __name__ == "__main__":
    main()