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
        self.color = (255, 0, 0)  # Red color
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                         self.radius * 2, self.radius * 2)
    
    def is_off_screen(self, height):
        return self.y > height
