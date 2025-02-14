import pygame
import random
import math
from config.settings import (
    WINDOW_WIDTH, METEOR_SIZE, BROWN, METEOR_MIN_SPEED,
    METEOR_MAX_SPEED, ROAD_WIDTH, WINDOW_HEIGHT
)

class Meteor:
    def __init__(self):
        self.size = METEOR_SIZE
        road_left = (WINDOW_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        
        # Randomly choose left or right side of the road
        self.from_left = random.choice([True, False])
        
        if self.from_left:
            self.x = road_left - self.size
            self.dx = random.uniform(1, 2)  # Diagonal movement to the right
        else:
            self.x = road_right + self.size
            self.dx = random.uniform(-2, -1)  # Diagonal movement to the left
            
        self.y = -self.size
        self.speed = random.uniform(METEOR_MIN_SPEED, METEOR_MAX_SPEED)
        
        # Fire trail parameters
        self.trail_particles = []
        self.max_trail_particles = 25  # Increased from 15
        
        # Road contact explosion timing
        self.road_contact_time = None
        self.explosion_delay = random.uniform(1000, 2000)  # 1-2 seconds in milliseconds
        self.should_explode = False
        self.has_exploded = False  # New flag to track explosion state
        
    def move(self):
        self.x += self.dx
        self.y += self.speed
        
        # Update fire trail
        for _ in range(3):  # Create 3 particles per frame for even denser effect
            spread_x = random.uniform(-15, 15)  # Increased spread
            spread_y = random.uniform(0, 40)    # Increased trail length
            self.trail_particles.append({
                'x': self.x + spread_x,
                'y': self.y - spread_y,
                'size': random.uniform(15, 35),  # Increased particle size
                'life': 1.0
            })
        
        # Update and remove old particles
        updated_particles = []
        for particle in self.trail_particles:
            particle['life'] -= 0.05  # Even slower fade for longer trails
            if particle['life'] > 0:
                updated_particles.append(particle)
        
        self.trail_particles = updated_particles
        if len(self.trail_particles) > self.max_trail_particles:
            self.trail_particles = self.trail_particles[-self.max_trail_particles:]
            
        # Check for road contact
        road_left = (WINDOW_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH
        if road_left <= self.x <= road_right and self.y >= WINDOW_HEIGHT - 100:  # Increased detection area
            if not self.road_contact_time:
                self.road_contact_time = pygame.time.get_ticks()
    
    def should_create_explosion(self):
        if self.road_contact_time and not self.has_exploded:
            current_time = pygame.time.get_ticks()
            if current_time - self.road_contact_time >= self.explosion_delay:
                self.has_exploded = True
                return True
        return False
    
    def draw(self, screen):
        # Draw fire trail with more vibrant colors
        for particle in self.trail_particles:
            alpha = int(255 * particle['life'])
            # Create more vibrant fire colors with yellow core
            life_factor = particle['life']
            if life_factor > 0.7:  # Inner core (yellow-white)
                color = (
                    255,                                    # Red
                    255,                                    # Green
                    int(255 * (life_factor - 0.7) * 3.3),  # Blue (fade in)
                    alpha
                )
            else:  # Outer flame (orange-red)
                color = (
                    255,                                    # Red
                    int(200 * life_factor),                # Green
                    0,                                      # Blue
                    alpha
                )
            
            surf = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, 
                             (particle['size']//2, particle['size']//2), 
                             particle['size']//2)
            screen.blit(surf, (particle['x'] - particle['size']//2, 
                             particle['y'] - particle['size']//2))
            
        # Draw meteor
        pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y)), self.size)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                         self.size * 2, self.size * 2)
    
    def is_off_screen(self, height):
        return (self.y > height + self.size * 2 or 
                self.x < -self.size * 2 or 
                self.x > WINDOW_WIDTH + self.size * 2)
