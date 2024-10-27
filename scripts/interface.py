import pygame
import sys

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
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            print(f"{text} button clicked!")
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    
    font = pygame.font.Font(None, 30)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)
    return False

#main menu screen
def main_menu(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)  # Temporary, replace with background image

        # Title/Header
        font = pygame.font.Font(None, 74)
        title_text = font.render('CollectCat', True, BLACK)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 20))

        # Buttons
        if draw_button(screen, 'Start Game', screen.get_width()//2 - 100, 200, 200, 50, (200, 200, 200), (150, 150, 150)):
            return 'start_game'
        draw_button(screen, 'Settings', screen.get_width()//2 - 100, 300, 200, 50, (200, 200, 200), (150, 150, 150))
        draw_button(screen, 'Credits', screen.get_width()//2 - 100, 400, 200, 50, (200, 200, 200), (150, 150, 150))

        pygame.display.flip()


def level_selection(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        font = pygame.font.Font(None, 74)
        title_text = font.render('Select Level', True, BLACK)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 20))

        if draw_button(screen, 'Level 1', 100, 200, 150, 50, (200, 200, 200), (150, 150, 150)):
            debug_print("Level 1 selected")
            return 1

        if draw_button(screen, 'Level 2', 325, 200, 150, 50, (200, 200, 200), (150, 150, 150)):
            debug_print("Level 2 selected")
            return 2

        if draw_button(screen, 'Level 3', 550, 200, 150, 50, (200, 200, 200), (150, 150, 150)):
            debug_print("Level 3 selected")
            return 3
        
        pygame.display.flip()