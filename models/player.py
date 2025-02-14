import pygame
from config.settings import WINDOW_HEIGHT, ROAD_WIDTH, CAR_WIDTH, CAR_HEIGHT, PLAYER_SPEED, BLACK, DARK_RED, WINDOW_BLUE
from models.bullet import Bullet

class Player:
    def __init__(self, window_width):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.x = (window_width - self.width) // 2
        self.y = WINDOW_HEIGHT - self.height - 20
        self.speed = PLAYER_SPEED
        self.has_power_up = False
        self.power_up_time = 0
        self.power_up_duration = 5000  # 5 seconds in milliseconds
    
    def move(self, keys, window_width):
        # Vertical movement
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < WINDOW_HEIGHT - self.height:
            self.y += self.speed
        
        # Horizontal movement
        road_left = (window_width - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH - self.width
        
        if keys[pygame.K_LEFT] and self.x > road_left:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < road_right:
            self.x += self.speed
    
    def shoot(self):
        if not self.has_power_up:
            return None
        # Create two bullets side by side
        bullet1 = Bullet(self.x + self.width * 0.25, self.y)
        bullet2 = Bullet(self.x + self.width * 0.75, self.y)
        return [bullet1, bullet2]
    
    def update_power_up(self, current_time):
        if self.has_power_up:
            if current_time - self.power_up_time >= self.power_up_duration:
                self.has_power_up = False
    
    def draw(self, screen):
        # Draw car body
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        
        # Draw windows
        window_width = self.width * 0.7
        window_height = self.height * 0.2
        window_x = self.x + (self.width - window_width) / 2
        window_y = self.y + self.height * 0.2
        pygame.draw.rect(screen, WINDOW_BLUE, (window_x, window_y, window_width, window_height))
        
        # Draw wheels
        wheel_radius = 5
        wheel_positions = [
            (self.x + wheel_radius + 2, self.y + wheel_radius + 2),
            (self.x + self.width - wheel_radius - 2, self.y + wheel_radius + 2),
            (self.x + wheel_radius + 2, self.y + self.height - wheel_radius - 2),
            (self.x + self.width - wheel_radius - 2, self.y + self.height - wheel_radius - 2)
        ]
        for pos in wheel_positions:
            pygame.draw.circle(screen, DARK_RED, pos, wheel_radius)
        
        # Draw power-up indicator if active
        if self.has_power_up:
            remaining_time = (self.power_up_duration - (pygame.time.get_ticks() - self.power_up_time)) / self.power_up_duration
            if remaining_time > 0:
                bar_width = 50
                bar_height = 5
                bar_x = self.x + (self.width - bar_width) / 2
                bar_y = self.y - 10
                pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * remaining_time, bar_height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
