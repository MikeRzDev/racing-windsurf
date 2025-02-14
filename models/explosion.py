import pygame
import time

class Explosion:
    def __init__(self, x, y, target_size):
        self.x = x
        self.y = y
        self.min_radius = 5
        self.max_radius = target_size
        self.radius = self.min_radius
        self.start_time = time.time()
        self.duration = 2.0  # 2 seconds
        
    def update(self):
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        if elapsed >= self.duration:
            return False
        
        # Calculate progress (0 to 1)
        progress = elapsed / self.duration
        self.radius = self.min_radius + (self.max_radius - self.min_radius) * progress
        return True
    
    def draw(self, screen):
        # Create gradient colors from yellow to orange to red
        progress = (self.radius - self.min_radius) / (self.max_radius - self.min_radius)
        
        if progress < 0.5:
            # Yellow to orange
            p = progress * 2
            r = 255
            g = 255 - (p * 165)  # 255 to 90
            b = 0
        else:
            # Orange to red
            p = (progress - 0.5) * 2
            r = 255
            g = 90 - (p * 90)  # 90 to 0
            b = 0
        
        color = (int(r), int(g), int(b))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.radius))
