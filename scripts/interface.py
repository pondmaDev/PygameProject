import pygame
import sys
from .character import Character
from .movement import move_character

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CollectCat')

# Load background music (placeholder)
# pygame.mixer.music.load('your_music_file.mp3')
# pygame.mixer.music.play(-1)

# Load background image (placeholder)
# background_image = pygame.image.load('your_background_image.png')
# background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


def draw_button(text, x, y, width, height, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    
    font = pygame.font.Font(None, 30)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)
    return False


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill screen with background image
        # screen.blit(background_image, (0, 0))
        screen.fill(WHITE)  # Temporary, replace with background image

        # Title/Header
        font = pygame.font.Font(None, 74)
        title_text = font.render('CollectCat', True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        # Buttons
        if draw_button('Start Game', screen_width//2 - 100, 200, 200, 50, (200, 200, 200), (150, 150, 150)):
            level_selection()
        draw_button('Settings', screen_width//2 - 100, 300, 200, 50, (200, 200, 200), (150, 150, 150))
        draw_button('Credits', screen_width//2 - 100, 400, 200, 50, (200, 200, 200), (150, 150, 150))

        pygame.display.flip()


def level_selection():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        font = pygame.font.Font(None, 74)
        title_text = font.render('Select Level', True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

        if draw_button('Level 1', 100, 200, 150, 50, (200, 200, 200), (150, 150, 150)):
            start_game(1)
        if draw_button('Level 2', 325, 200, 150, 50, (200,  200, 200), (150, 150, 150)):
            start_game(2)
        if draw_button('Level 3', 550, 200, 150, 50, (200, 200, 200), (150, 150, 150)):
            start_game(3)

        pygame.display.flip()


def start_game(level):
    global character
    character = Character(screen_width // 2, screen_height // 2, 50, 50, RED)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        move_character(character, keys_pressed, screen_width, screen_height)

        screen.fill(WHITE)
        character.update()
        character.draw(screen)

        font = pygame.font.Font(None,  36)
        level_text = font.render(f'Level {level}', True, BLACK)
        screen.blit(level_text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()