# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()


# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])



# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Create a surface and pass in a tuple containing its length and width
    surf = pygame.Surface((50, 50))

    # Give the surface a color to separate it from the background
    surf.fill((0, 0, 0))
    rect = surf.get_rect()

    # This line says "Draw surf onto the screen at the center"
    screen.blit(surf, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()