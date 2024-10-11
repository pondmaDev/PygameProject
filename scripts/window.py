import pygame, sys
pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('First Game')


#this section of code is to set inf loop of display window
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the window with a color (optional)
    window.fill((0, 128, 255))  # Light blue background

    # Update the display
    pygame.display.flip()

# Quit Pygame properly
pygame.quit()
sys.exit()