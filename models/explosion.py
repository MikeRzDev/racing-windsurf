import pygame
from config.settings import RED

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 30
        self.growing = True
        self.alpha = 255
    
    def update(self):
        if self.growing:
            self.radius += 2
            if self.radius >= self.max_radius:
                self.growing = False
        else:
            self.alpha -= 10
        return self.alpha > 0
    
    def draw(self, screen):
        surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*RED, self.alpha), (self.radius, self.radius), self.radius)
        screen.blit(surf, (self.x - self.radius, self.y - self.radius))
