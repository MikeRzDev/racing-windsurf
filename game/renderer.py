import pygame
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, ROAD_WIDTH,
    WHITE, GRAY, YELLOW
)

def draw_road(screen, offset):
    # Draw road background
    road_x = (WINDOW_WIDTH - ROAD_WIDTH) // 2
    pygame.draw.rect(screen, GRAY, (road_x, 0, ROAD_WIDTH, WINDOW_HEIGHT))
    
    # Draw road edges
    edge_width = 5
    pygame.draw.rect(screen, WHITE, (road_x, 0, edge_width, WINDOW_HEIGHT))
    pygame.draw.rect(screen, WHITE, (road_x + ROAD_WIDTH - edge_width, 0, edge_width, WINDOW_HEIGHT))
    
    # Draw dashed lines with movement
    dash_length = 30
    dash_width = 4
    dash_x = WINDOW_WIDTH // 2 - dash_width // 2
    
    for y in range((-dash_length + offset) % (dash_length * 2), WINDOW_HEIGHT + dash_length, dash_length * 2):
        pygame.draw.rect(screen, YELLOW, (dash_x, y, dash_width, dash_length))
