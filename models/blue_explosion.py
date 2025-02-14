import pygame
from models.explosion import Explosion
from config.settings import METEOR_BLUE

class BlueExplosion(Explosion):
    def draw(self, screen):
        # Calculate progress (0 to 1)
        progress = (self.radius - self.min_radius) / (self.max_radius - self.min_radius)
        
        if progress < 0.3:  # First phase: white to light blue
            p = progress * 3.33
            r = 255 - (p * 75)  # 255 to 180
            g = 255 - (p * 55)  # 255 to 200
            b = 255
        elif progress < 0.6:  # Second phase: light blue to medium blue
            p = (progress - 0.3) * 3.33
            r = 180 - (p * 100)  # 180 to 80
            g = 200 - (p * 100)  # 200 to 100
            b = 255
        else:  # Final phase: medium blue to dark blue
            p = (progress - 0.6) * 2.5
            r = 80 - (p * 50)   # 80 to 30
            g = 100 - (p * 70)  # 100 to 30
            b = 255 - (p * 55)  # 255 to 200
        
        # Draw main explosion circle
        color = (int(r), int(g), int(b))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.radius))
        
        # Draw inner glow
        inner_radius = max(self.radius * 0.6, self.min_radius)
        inner_color = (min(r + 50, 255), min(g + 50, 255), min(b + 50, 255))
        pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), int(inner_radius))
