import pygame
import sys
from .game_state import current_game_state

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Debug function
def debug_print(message):
    print(f"[DEBUG] {message}")
#draw button
def draw_button(screen, text, x, y, width, height, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Create a rectangle for the button
    button_rect = pygame.Rect(x, y, width, height)
    
    # Debug print for mouse position and button boundaries
    # print(f"Button {text}: x={x}-{x+width}, y={y}-{y+height}, Mouse: {mouse}")
    
    # Check if mouse is over the button using rect.collidepoint
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, active_color, button_rect)
        if click[0] == 1:
            print(f"{text} button clicked! Mouse pos: {mouse}")
            return True
    else:
        pygame.draw.rect(screen, inactive_color, button_rect)
    
    # Draw the text
    font = pygame.font.Font(None, 30)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = button_rect.center
    screen.blit(text_surf, text_rect)
    
    # Debug: Draw button boundaries
    # pygame.draw.rect(screen, (255, 0, 0), button_rect, 1)  # Red outline for debugging
    
    return False

#main menu screen
def main_menu(screen):
    current_game_state.set_screen('main_menu')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_menu(screen, current_game_state.get_screen()) #current_screen is not define
                    if result == 'exit':
                        pygame.quit()
                        sys.exit()
                    elif result == 'settings':
                        # Implement settings screen
                        pass

        # back ground image
        background_image = pygame.image.load('data/raw/Background/background-image.png')
        background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
        screen.blit(background_image, (0, 0))

        # Title/Header
        font = pygame.font.Font(None, 74)
        title_text = font.render('CollectCat', True, BLACK)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 20))

        # Buttons
        if draw_button(screen, 'Start Game', screen.get_width()//2 - 100, 200, 200, 50, (200, 200, 200), (150, 150, 150)):
            pygame.time.wait(200)  # Add a small delay because It will colision when no delay
            return 'start_game'
        draw_button(screen, 'Settings', screen.get_width()//2 - 100, 300, 200, 50, (200, 200, 200), (150, 150, 150))
        draw_button(screen, 'Credits', screen.get_width()//2 - 100, 400, 200, 50, (200, 200, 200), (150, 150, 150))

        pygame.display.flip()


def level_selection(screen):
    current_game_state.set_screen('level_selection')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Get screen dimensions
        screen_width = screen.get_width()
        
        # Button dimensions
        button_width = 150
        button_height = 50
        
        # Calculate button positions with even spacing
        spacing = (screen_width - (3 * button_width)) // 4
        x1 = spacing
        x2 = 2 * spacing + button_width
        x3 = 3 * spacing + 2 * button_width
        y_position = 200

        font = pygame.font.Font(None, 74)
        title_text = font.render('Select Level', True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        # Draw buttons with calculated positions
        level1_clicked = draw_button(screen, 'Level 1', x1, y_position, button_width, button_height, (200, 200, 200), (150, 150, 150))
        level2_clicked = draw_button(screen, 'Level 2', x2, y_position, button_width, button_height, (200, 200, 200), (150, 150, 150))
        level3_clicked = draw_button(screen, 'Level 3', x3, y_position, button_width, button_height, (200, 200, 200), (150, 150, 150))

        if level1_clicked:
            debug_print("Level 1 selected")
            return 1
        elif level2_clicked:
            debug_print("Level 2 selected")
            return 2
        elif level3_clicked:
            debug_print("Level 3 selected")
            return 3

        pygame.display.flip()

def pause_menu(screen, current_screen):
    """
    Display pause menu when ESC is pressed
    current_screen: string indicating which screen the game is currently on
    ('main_menu', 'game', etc.)
    """
    menu_width = 300
    menu_height = 400
    menu_x = screen.get_width()//2 - menu_width//2
    menu_y = screen.get_height()//2 - menu_height//2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC again to resume
                    return None

        # Semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)  # 128 is half transparent
        screen.blit(overlay, (0, 0))

        # Pause menu background
        pygame.draw.rect(screen, (200, 200, 200), 
                        (menu_x, menu_y, menu_width, menu_height))

        # Title
        font = pygame.font.Font(None, 48)
        title_text = font.render('Pause Menu', True, BLACK)
        screen.blit(title_text, (menu_x + menu_width//2 - title_text.get_width()//2, 
                                menu_y + 20))

        # Buttons
        button_width = 200
        button_height = 50
        button_x = menu_x + (menu_width - button_width)//2
        
        # Level Selection button
        if draw_button(screen, 'Level Selection', button_x, menu_y + 100, 
                      button_width, button_height, (180, 180, 180), (150, 150, 150)):
            return 'level_selection'

        # Settings button
        if draw_button(screen, 'Settings', button_x, menu_y + 170, 
                      button_width, button_height, (180, 180, 180), (150, 150, 150)):
            return 'settings'

        # Exit button (context-sensitive)
        exit_text = 'Exit Game' if current_screen == 'main_menu' else 'Main Menu'
        if draw_button(screen, exit_text, button_x, menu_y + 240, 
                      button_width, button_height, (180, 180, 180), (150, 150, 150)):
            return 'exit'

        pygame.display.flip()