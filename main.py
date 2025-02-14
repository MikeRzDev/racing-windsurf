import pygame
import sys
import random
import json
import os
from pygame import gfxdraw
from models.player import Player
from models.cpu_car import CPUCar
from models.explosion import Explosion
from game.renderer import draw_road
   
# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ROAD_WIDTH = 300
CAR_WIDTH = 40
CAR_HEIGHT = 60
FPS = 60
PLAYER_SPEED = 5
BASE_CPU_SPEED = 3
INITIAL_SPAWN_RATE = 2000  # milliseconds between spawns
ROAD_SPEED = 5  # Speed of road movement
DIFFICULTY_INCREASE_RATE = 5000  # Increase difficulty every 5 seconds
HIGH_SCORE_FILE = "highscore.json"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
DARK_RED = (139, 0, 0)

# Game states
GAME_RUNNING = 'running'
GAME_OVER = 'game_over'
GAME_WIN = 'win'

# Load or create high score
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return json.load(f)['high_score']
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump({'high_score': score}, f)

def main():
    # Create the game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2D Car Racing")
    clock = pygame.time.Clock()
    
    # Load high score
    high_score = load_high_score()
    current_score = 0
    
    # Game objects and state
    player = Player(WINDOW_WIDTH)
    cpu_cars = []
    explosions = []
    last_spawn_time = pygame.time.get_ticks()
    last_difficulty_increase = pygame.time.get_ticks()
    game_state = GAME_RUNNING
    start_time = pygame.time.get_ticks()
    game_duration = 60000  # 60 seconds in milliseconds
    road_offset = 0
    cpu_speed = BASE_CPU_SPEED
    spawn_rate = INITIAL_SPAWN_RATE
    cars_avoided = 0

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
                    player = Player(WINDOW_WIDTH)
                    cpu_cars = []
                    explosions = []
                    game_state = GAME_RUNNING
                    start_time = pygame.time.get_ticks()
                    last_spawn_time = start_time
                    last_difficulty_increase = start_time
                    road_offset = 0
                    cpu_speed = BASE_CPU_SPEED
                    spawn_rate = INITIAL_SPAWN_RATE
                    cars_avoided = 0
        
        if game_state == GAME_RUNNING:
            # Update road animation
            road_offset = (road_offset + ROAD_SPEED) % (60)
            
            # Handle player movement
            keys = pygame.key.get_pressed()
            player.move(keys, WINDOW_WIDTH)
            
            # Increase difficulty over time
            if current_time - last_difficulty_increase > DIFFICULTY_INCREASE_RATE:
                cpu_speed += 0.2
                spawn_rate = max(500, spawn_rate - 100)
                last_difficulty_increase = current_time
            
            # Spawn new CPU cars
            if current_time - last_spawn_time > spawn_rate:
                cpu_cars.append(CPUCar(WINDOW_WIDTH, cpu_speed))
                last_spawn_time = current_time
            
            # Update CPU cars
            for car in cpu_cars[:]:
                car.move()
                if car.get_rect().colliderect(player.get_rect()):
                    game_state = GAME_OVER
                    explosions.append(Explosion(player.x + player.width//2, player.y + player.height//2))
                    if cars_avoided > high_score:
                        high_score = cars_avoided
                        save_high_score(high_score)
                elif car.is_off_screen():
                    cpu_cars.remove(car)
                    cars_avoided += 1
            
            # Update explosions
            explosions = [exp for exp in explosions if exp.update()]
            
            # Check win condition
            if elapsed_time >= game_duration:
                game_state = GAME_WIN
                if cars_avoided > high_score:
                    high_score = cars_avoided
                    save_high_score(high_score)
        
        # Draw everything
        screen.fill(WHITE)
        draw_road(screen, road_offset)
        player.draw(screen)
        for car in cpu_cars:
            car.draw(screen)
        for explosion in explosions:
            explosion.draw(screen)
        
        # Draw HUD
        font = pygame.font.Font(None, 36)
        if game_state == GAME_RUNNING:
            time_left = max(0, (game_duration - elapsed_time) // 1000)
            timer_text = font.render(f'Time: {time_left}s', True, BLACK)
            screen.blit(timer_text, (10, 10))
            
            score_text = font.render(f'Cars Avoided: {cars_avoided}', True, BLACK)
            screen.blit(score_text, (10, 50))
            
            high_score_text = font.render(f'High Score: {high_score}', True, BLACK)
            screen.blit(high_score_text, (10, 90))
        
        # Draw game over or win message
        if game_state in [GAME_OVER, GAME_WIN]:
            font_large = pygame.font.Font(None, 74)
            message = 'YOU WIN!' if game_state == GAME_WIN else 'GAME OVER'
            text = font_large.render(message, True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50))
            screen.blit(text, text_rect)
            
            score_text = font.render(f'Cars Avoided: {cars_avoided}', True, BLACK)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 10))
            screen.blit(score_text, score_rect)
            
            high_score_text = font.render(f'High Score: {high_score}', True, BLACK)
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
            screen.blit(high_score_text, high_score_rect)
            
            restart_text = font.render('Press SPACE to restart', True, BLACK)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 90))
            screen.blit(restart_text, restart_text)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
