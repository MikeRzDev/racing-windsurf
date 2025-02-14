import pygame
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BASE_CPU_SPEED,
    INITIAL_SPAWN_RATE, DIFFICULTY_INCREASE_RATE, GAME_DURATION,
    GAME_RUNNING, GAME_OVER, GAME_WIN, WHITE, ROAD_SPEED
)
from models.player import Player
from models.cpu_car import CPUCar
from models.explosion import Explosion
from utils.score_manager import load_high_score, save_high_score
from game.renderer import draw_road

class GameManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("2D Car Racing")
        self.clock = pygame.time.Clock()
        
        self.reset_game()
    
    def reset_game(self):
        self.player = Player(WINDOW_WIDTH)
        self.cpu_cars = []
        self.explosions = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.last_difficulty_increase = pygame.time.get_ticks()
        self.game_state = GAME_RUNNING
        self.start_time = pygame.time.get_ticks()
        self.high_score = load_high_score()
        self.current_score = 0
        self.road_offset = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_state != GAME_RUNNING:
                self.reset_game()
        return True
    
    def update(self):
        if self.game_state != GAME_RUNNING:
            return
        
        # Update player
        keys = pygame.key.get_pressed()
        self.player.move(keys, WINDOW_WIDTH)
        
        # Update CPU cars
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        
        # Spawn new CPU cars
        if current_time - self.last_spawn_time >= INITIAL_SPAWN_RATE:
            speed = BASE_CPU_SPEED + (elapsed_time // DIFFICULTY_INCREASE_RATE) * 0.5
            self.cpu_cars.append(CPUCar(WINDOW_WIDTH, speed))
            self.last_spawn_time = current_time
        
        # Update CPU cars
        for car in self.cpu_cars[:]:
            car.move()
            if car.is_off_screen():
                self.cpu_cars.remove(car)
                self.current_score += 1
        
        # Check collisions
        player_rect = self.player.get_rect()
        for car in self.cpu_cars:
            if player_rect.colliderect(car.get_rect()):
                self.explosions.append(Explosion(
                    player_rect.centerx,
                    player_rect.centery
                ))
                self.game_state = GAME_OVER
                if self.current_score > self.high_score:
                    self.high_score = self.current_score
                    save_high_score(self.high_score)
                break
        
        # Update explosions
        self.explosions = [exp for exp in self.explosions if exp.update()]
        
        # Check win condition
        if elapsed_time >= GAME_DURATION:
            self.game_state = GAME_WIN
            if self.current_score > self.high_score:
                self.high_score = self.current_score
                save_high_score(self.high_score)
        
        # Update road animation
        self.road_offset = (self.road_offset + ROAD_SPEED) % 60
    
    def render(self):
        self.screen.fill(WHITE)
        
        # Draw road
        draw_road(self.screen, self.road_offset)
        
        # Draw game objects
        self.player.draw(self.screen)
        for car in self.cpu_cars:
            car.draw(self.screen)
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        # Draw HUD
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.current_score}', True, (0, 0, 0))
        high_score_text = font.render(f'High Score: {self.high_score}', True, (0, 0, 0))
        time_left = max(0, (GAME_DURATION - (pygame.time.get_ticks() - self.start_time)) // 1000)
        time_text = font.render(f'Time: {time_left}s', True, (0, 0, 0))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))
        self.screen.blit(time_text, (10, 70))
        
        # Draw game over/win message
        if self.game_state != GAME_RUNNING:
            message = "YOU WIN!" if self.game_state == GAME_WIN else "GAME OVER!"
            message_text = font.render(message, True, (0, 0, 0))
            restart_text = font.render("Press R to restart", True, (0, 0, 0))
            
            msg_x = WINDOW_WIDTH // 2 - message_text.get_width() // 2
            msg_y = WINDOW_HEIGHT // 2 - message_text.get_height()
            restart_x = WINDOW_WIDTH // 2 - restart_text.get_width() // 2
            restart_y = WINDOW_HEIGHT // 2 + restart_text.get_height()
            
            self.screen.blit(message_text, (msg_x, msg_y))
            self.screen.blit(restart_text, (restart_x, restart_y))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
