
import pygame
import sys
from scripts import *

def check_interface():
    try:
        # Initialize Pygame (if not already initialized in interface.py)
        if not pygame.get_init():
            pygame.init()
        
        # Check if screen is created
        if not pygame.display.get_surface():
            screen = pygame.display.set_mode((screen_width, screen_height))
        
        # Test draw_button function
        test_button = draw_button('Test', 100, 100, 100, 50, (200, 200, 200), (150, 150, 150))
        
        # Test character creation
        test_character = Character(screen_width // 2, screen_height // 2, 50, 50, RED)
        
        # Test movement function
        keys = pygame.key.get_pressed()
        move_character(test_character, keys, screen_width, screen_height)
        
        print("Interface, Character, and Movement modules work successfully")
        return True
    except Exception as e:
        print(f"Error in initialization: {e}")
        return False

def main():
    if check_interface():
        # If interface check passes, proceed with the game
        try:
            main_menu()  # Start the game with the main menu
        except Exception as e:
            print(f"Error during game execution: {e}")
    else:
        print("Initialization check failed. Exiting the game.")
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()