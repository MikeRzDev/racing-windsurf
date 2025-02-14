import pygame
from config.settings import WINDOW_HEIGHT, ROAD_WIDTH, CAR_WIDTH, CAR_HEIGHT, PLAYER_SPEED, BLACK, DARK_RED, WINDOW_BLUE

class Player:
    def __init__(self, window_width):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.x = (window_width - self.width) // 2
        self.y = WINDOW_HEIGHT - self.height - 20
        self.speed = PLAYER_SPEED
    
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
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
