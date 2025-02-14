import pygame

class Bullet:
    def __init__(self, x, y):
        self.radius = 5
        self.x = x
        self.y = y
        self.speed = 7
        self.color = (255, 0, 0)  # Red color
    
    def move(self):
        self.y -= self.speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                         self.radius * 2, self.radius * 2)
    
    def is_off_screen(self):
        return self.y < -self.radius
