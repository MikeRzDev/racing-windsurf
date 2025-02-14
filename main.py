import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ROAD_WIDTH = 300
CAR_WIDTH = 40
CAR_HEIGHT = 60
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D Car Racing")
clock = pygame.time.Clock()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Fill background
        screen.fill(WHITE)
        
        # Draw road (temporary rectangle for now)
        road_x = (WINDOW_WIDTH - ROAD_WIDTH) // 2
        pygame.draw.rect(screen, GRAY, (road_x, 0, ROAD_WIDTH, WINDOW_HEIGHT))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
