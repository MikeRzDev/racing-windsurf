import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ROAD_WIDTH = 300
CAR_WIDTH = 40
CAR_HEIGHT = 60
FPS = 60
PLAYER_SPEED = 5
CPU_SPEED = 3
CPU_SPAWN_RATE = 2000  # milliseconds between spawns
ROAD_SPEED = 5  # Speed of road movement

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Game states
GAME_RUNNING = 'running'
GAME_OVER = 'game_over'
GAME_WIN = 'win'

class Player:
    def __init__(self):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.x = (WINDOW_WIDTH - self.width) // 2
        self.y = WINDOW_HEIGHT - self.height - 20
        self.speed = PLAYER_SPEED
    
    def move(self, keys):
        # Vertical movement
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < WINDOW_HEIGHT - self.height:
            self.y += self.speed
        
        # Horizontal movement
        road_left = (WINDOW_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH - self.width
        
        if keys[pygame.K_LEFT] and self.x > road_left:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < road_right:
            self.x += self.speed
    
    def draw(self, screen):
        # Draw car body (black rectangle)
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class CPUCar:
    def __init__(self):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        # Random x position within road boundaries
        road_left = (WINDOW_WIDTH - ROAD_WIDTH) // 2
        road_right = road_left + ROAD_WIDTH - self.width
        self.x = random.randint(road_left, road_right)
        self.y = -self.height  # Start above screen
        self.speed = CPU_SPEED
    
    def move(self):
        self.y += self.speed
    
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def draw_road(screen, offset):
    # Draw road background
    road_x = (WINDOW_WIDTH - ROAD_WIDTH) // 2
    pygame.draw.rect(screen, GRAY, (road_x, 0, ROAD_WIDTH, WINDOW_HEIGHT))
    
    # Draw dashed lines with movement
    dash_length = 30
    dash_width = 4
    dash_x = WINDOW_WIDTH // 2 - dash_width // 2
    
    # Use offset to create moving effect
    for y in range((-dash_length + offset) % (dash_length * 2), WINDOW_HEIGHT + dash_length, dash_length * 2):
        pygame.draw.rect(screen, YELLOW, (dash_x, y, dash_width, dash_length))

def main():
    player = Player()
    cpu_cars = []
    last_spawn_time = pygame.time.get_ticks()
    game_state = GAME_RUNNING
    start_time = pygame.time.get_ticks()
    game_duration = 60000  # 60 seconds in milliseconds
    road_offset = 0  # For road animation
    
    # Create the game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2D Car Racing")
    clock = pygame.time.Clock()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_state != GAME_RUNNING:
                if event.key == pygame.K_SPACE:
                    # Reset game
                    player = Player()
                    cpu_cars = []
                    game_state = GAME_RUNNING
                    start_time = pygame.time.get_ticks()
                    last_spawn_time = start_time
                    road_offset = 0
        
        if game_state == GAME_RUNNING:
            # Update road animation
            road_offset = (road_offset + ROAD_SPEED) % (60)  # 60 is dash_length * 2
            
            # Handle player movement
            keys = pygame.key.get_pressed()
            player.move(keys)
            
            # Spawn new CPU cars
            if current_time - last_spawn_time > CPU_SPAWN_RATE:
                cpu_cars.append(CPUCar())
                last_spawn_time = current_time
            
            # Update CPU cars
            for car in cpu_cars[:]:
                car.move()
                # Check collision with player
                if car.get_rect().colliderect(player.get_rect()):
                    game_state = GAME_OVER
                # Remove cars that are off screen
                if car.is_off_screen():
                    cpu_cars.remove(car)
            
            # Check win condition
            if elapsed_time >= game_duration:
                game_state = GAME_WIN
        
        # Draw everything
        screen.fill(WHITE)
        draw_road(screen, road_offset)
        player.draw(screen)
        for car in cpu_cars:
            car.draw(screen)
        
        # Draw timer
        if game_state == GAME_RUNNING:
            time_left = max(0, (game_duration - elapsed_time) // 1000)
            font = pygame.font.Font(None, 36)
            timer_text = font.render(f'Time: {time_left}s', True, BLACK)
            screen.blit(timer_text, (10, 10))
            
            # Draw score (number of cars avoided)
            score_text = font.render(f'Score: {len(cpu_cars)}', True, BLACK)
            screen.blit(score_text, (10, 50))
        
        # Draw game over or win message
        if game_state in [GAME_OVER, GAME_WIN]:
            font = pygame.font.Font(None, 74)
            message = 'YOU WIN!' if game_state == GAME_WIN else 'GAME OVER'
            text = font.render(message, True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            screen.blit(text, text_rect)
            
            font = pygame.font.Font(None, 36)
            restart_text = font.render('Press SPACE to restart', True, BLACK)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
