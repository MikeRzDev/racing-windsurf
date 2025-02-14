import pygame
import random
from config.settings import WINDOW_WIDTH, ROAD_WIDTH

class PowerUp:
    def __init__(self):
        self.radius = 15
        road_left = (WINDOW_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH - self.radius * 2
        self.x = random.randint(road_left + self.radius, road_right)
        self.y = -self.radius
        self.speed = 3
        self.colors = {
            'border': (255, 255, 0),  # Yellow
            'fill': (0, 0, 0),       # Black
            'text': (255, 0, 0)       # Red
        }
        self.font = pygame.font.Font(None, int(self.radius * 1.5))
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        # Draw black filled circle
        pygame.draw.circle(screen, self.colors['fill'], (self.x, self.y), self.radius)
        # Draw yellow border (slightly smaller radius to fit within the circle)
        pygame.draw.circle(screen, self.colors['border'], (self.x, self.y), self.radius, 2)
        
        # Draw red "L"
        text = self.font.render("L", True, self.colors['text'])
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                         self.radius * 2, self.radius * 2)
    
    def is_off_screen(self, height):
        return self.y > height
