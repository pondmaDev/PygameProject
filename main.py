from scripts import interface
import pygame
import sys

def check_interface():
    try:
        # Initialize Pygame (if not already initialized in interface.py)
        if not pygame.get_init():
            pygame.init()
        
        # Check if screen is created
        if not pygame.display.get_surface():
            interface.screen = pygame.display.set_mode((interface.screen_width, interface.screen_height))
        
        # Test draw_button function
        test_button = interface.draw_button('Test', 100, 100, 100, 50, (200, 200, 200), (150, 150, 150))
        
        # Test main_menu function (just call it without entering the loop)
        interface.main_menu()
        
        # Test level_selection function (just call it without entering the loop)
        interface.level_selection()
        
        print("Section 1 : Interface : Works Successfully")
        return True
    except Exception as e:
        print(f"Error in interface.py: {e}")
        return False

def main():
    if check_interface():
        # If interface check passes, proceed with the rest of the game
        try:
            interface.main_menu()  # Start the game with the main menu
        except Exception as e:
            print(f"Error during game execution: {e}")
    else:
        print("Interface check failed. Exiting the game.")
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()