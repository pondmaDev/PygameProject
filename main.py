import pygame
import sys
from src.game.game import Game as GameImplementation
from src.utils.debug_section import debug

def main():
    """
    Main game loop with robust error handling and screen management
    """
    pygame_initialized = False
    
    try:
        pygame.init()
        pygame_initialized = True
        
        game = GameImplementation()
        
        current_screen = 'main_menu'
        
        while True:
            try:
                if current_screen == 'main_menu':
                    menu_option = game.main_menu.display()
                    debug.log('game', f"MAIN: Menu option selected: {menu_option}")
                    
                    if menu_option == 'start_game':
                        current_screen = 'level_selection'
                    elif menu_option == 'settings':
                        current_screen = 'settings'
                    elif menu_option == 'quit':
                        break
                
                elif current_screen == 'level_selection':
                    level = game.level_menu.display()
                    debug.log('game', f"MAIN: Level selected: {level}")
                    
                    if level == 'main_menu':
                        current_screen = 'main_menu'
                    elif level == 'quit':
                        break
                    elif isinstance(level, int):
                        try:
                            pygame.event.clear()
                            debug.log('game', f"MAIN: Attempting to start game with level {level}")
                            game_result = game.start_game(level)
                            debug.log('game', f"MAIN: Game result: {game_result}")
                            
                            if game_result == 'quit':
                                debug.log('game', "MAIN: Quit game")
                                break
                            elif game_result == 'restart':
                                debug.log('game', "MAIN: Restarting game")
                                continue
                            elif game_result == 'main_menu':
                                debug.log('game', "MAIN: Returning to main menu")
                                current_screen = 'main_menu'
                            elif game_result == 'level_selection':
                                debug.log('game', "MAIN: Returning to level selection")
                                current_screen = 'level_selection'
                            else:
                                debug.warning('game', f"MAIN: Unexpected game result: {game_result}")
                                current_screen = 'main_menu'
                        
                        except Exception as game_start_error:
                            debug.error('game', f"MAIN: Error starting game: {game_start_error}")
                            import traceback
                            debug.error('game', f"Full traceback: {traceback.format_exc()}")
                            current_screen = 'main_menu'
                
                elif current_screen == 'settings':
                    try:
                        settings_result = game.show_settings()
                        debug.log('game', f"Settings result: {settings_result}")
                        
                        if settings_result == 'quit':
                            break
                        elif settings_result == 'main_menu':
                            current_screen = 'main_menu'
                        elif settings_result == 'resume':
                            current_screen = 'main_menu'
                    except Exception as settings_error:
                        debug.error('game', f"Error in settings: {settings_error}")
                        current_screen = 'main_menu'
                
                else:
                    debug.error('game', f"Unexpected screen state: {current_screen}")
                    current_screen = 'main_menu'
                
                pygame.time.delay(10)
                
            except KeyboardInterrupt:
                debug.log('game', "Game interrupted by user")
                break
            except Exception as screen_error:
                debug.error('game', f"Screen management error: {screen_error}")
                current_screen = 'main_menu'
    
    except pygame.error as pygame_error:
        debug.error('init', f"Pygame initialization error: {pygame_error}")
    
    except Exception as init_error:
        debug.error('init', f"Initialization error: {init_error}")
    
    finally:
        # Comprehensive cleanup
        try:
            if pygame_initialized:
                pygame.mixer.quit()
                pygame.display.quit()
                pygame.quit()
        except Exception as cleanup_error:
            debug.error('cleanup', f"Error during cleanup: {cleanup_error}")
        
        sys.exit(0)

# Optional: Wrap main in a function to catch any unhandled exceptions
def run_game():
    try:
        main()
    except Exception as unexpected_error:
        debug.error('critical', f"Unexpected critical error: {unexpected_error}")
        # Log to file or send error report
        sys.exit(1)

# Entry point
if __name__ == "__main__":
    run_game()