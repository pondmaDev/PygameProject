import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CollectCat')

# Load background music (placeholder)
# pygame.mixer.music.load('your_music_file.mp3')
# pygame.mixer.music.play(-1)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen
    screen.fill(WHITE)

    # Title/Header
    font = pygame.font.Font(None, 74)
    title_text = font.render('CollectCat', True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

    # Buttons
    button_font = pygame.font.Font(None, 50)
    start_button = button_font.render('Start Game', True, BLACK)
    setting_button = button_font.render('Settings', True, BLACK)
    credit_button = button_font.render('Credits', True, BLACK)

    start_button_rect = start_button.get_rect(center=(screen_width // 2, 200))
    setting_button_rect = setting_button.get_rect(center=(screen_width // 2, 300))
    credit_button_rect = credit_button.get_rect(center=(screen_width // 2, 400))

    screen.blit(start_button, start_button_rect)
    screen.blit(setting_button, setting_button_rect)
    screen.blit(credit_button, credit_button_rect)

    # Placeholder for background GIF (you'll replace this with your actual GIF implementation)
    pygame.draw.rect(screen, BLACK, (50, 100, 700, 400), 2)

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
