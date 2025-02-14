import pygame
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BASE_CPU_SPEED,
    INITIAL_SPAWN_RATE, DIFFICULTY_INCREASE_RATE, GAME_DURATION,
    GAME_RUNNING, GAME_OVER, GAME_WIN, WHITE, ROAD_SPEED, LEVEL_SPEED_MULTIPLIER
)
from models.player import Player
from models.cpu_car import CPUCar
from models.explosion import Explosion
from models.power_up import PowerUp
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
        self.bullets = []
        self.power_ups = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.last_power_up_spawn = pygame.time.get_ticks()
        self.power_up_spawn_rate = 10000  # 10 seconds
        self.last_difficulty_increase = pygame.time.get_ticks()
        self.game_state = GAME_RUNNING
        self.start_time = pygame.time.get_ticks()
        self.high_score = load_high_score()
        self.current_score = 0
        self.road_offset = 0
        self.current_level = 1
        self.level_up_time = 0
        self.show_level_up = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_state != GAME_RUNNING:
                    self.reset_game()
                elif event.key == pygame.K_SPACE and self.game_state == GAME_RUNNING:
                    new_bullets = self.player.shoot()
                    if new_bullets:
                        self.bullets.extend(new_bullets)
        return True
    
    def update(self):
        if self.game_state != GAME_RUNNING:
            return
        
        current_time = pygame.time.get_ticks()
        
        # Update player and power-up status
        keys = pygame.key.get_pressed()
        self.player.move(keys, WINDOW_WIDTH)
        self.player.update_power_up(current_time)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
            else:
                # Check for collisions with CPU cars
                for car in self.cpu_cars[:]:
                    if bullet.get_rect().colliderect(car.get_rect()):
                        # Use car size for explosion
                        target_size = max(car.get_rect().width, car.get_rect().height)
                        self.explosions.append(Explosion(
                            car.get_rect().centerx,
                            car.get_rect().centery,
                            target_size
                        ))
                        self.cpu_cars.remove(car)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        self.current_score += 2  # More points for shooting a car
                        break
        
        # Only handle power-ups after level 3
        if self.current_level >= 3:
            # Spawn power-ups if none active
            if not self.player.has_power_up and current_time - self.last_power_up_spawn >= self.power_up_spawn_rate:
                self.power_ups.append(PowerUp())
                self.last_power_up_spawn = current_time
            
            # Update power-ups
            for power_up in self.power_ups[:]:
                power_up.move()
                if power_up.is_off_screen(WINDOW_HEIGHT):
                    self.power_ups.remove(power_up)
                elif power_up.get_rect().colliderect(self.player.get_rect()):
                    self.player.has_power_up = True
                    self.player.power_up_time = current_time
                    self.power_ups.remove(power_up)
        else:
            # Clear any existing power-ups if below level 3
            self.power_ups.clear()
            self.bullets.clear()
            self.player.has_power_up = False
        
        elapsed_time = current_time - self.start_time
        
        # Check for level completion
        if elapsed_time >= GAME_DURATION:
            self.current_level += 1
            self.start_time = current_time
            self.show_level_up = True
            self.level_up_time = current_time
            # Clear existing CPU cars for the next level
            self.cpu_cars.clear()
            return
        
        # Calculate level-based speeds
        level_multiplier = LEVEL_SPEED_MULTIPLIER ** (self.current_level - 1)
        current_road_speed = ROAD_SPEED * level_multiplier
        current_cpu_speed = BASE_CPU_SPEED * level_multiplier
        
        # Spawn new CPU cars
        if current_time - self.last_spawn_time >= INITIAL_SPAWN_RATE:
            speed = current_cpu_speed + (elapsed_time // DIFFICULTY_INCREASE_RATE) * 0.5
            self.cpu_cars.append(CPUCar(WINDOW_WIDTH, speed))
            self.last_spawn_time = current_time
        
        # Update CPU cars
        for car in self.cpu_cars[:]:
            car.move()
            if car.is_off_screen():
                self.cpu_cars.remove(car)
                self.current_score += 1
        
        # Check collisions between player and CPU cars
        player_rect = self.player.get_rect()
        for car in self.cpu_cars:
            if player_rect.colliderect(car.get_rect()):
                # Use car size for explosion
                target_size = max(car.get_rect().width, car.get_rect().height)
                self.explosions.append(Explosion(
                    player_rect.centerx,
                    player_rect.centery,
                    target_size
                ))
                self.game_state = GAME_OVER
                if self.current_score > self.high_score:
                    self.high_score = self.current_score
                    save_high_score(self.high_score)
                break
        
        # Update road offset with fixed speed
        current_road_speed = ROAD_SPEED * level_multiplier
        self.road_offset = (self.road_offset + current_road_speed) % 90  # Use 90 (total_pattern) as modulo
        
        # Update level up display
        if self.show_level_up and current_time - self.level_up_time >= 2000:  # Show for 2 seconds
            self.show_level_up = False
        
        # Check win condition
        if elapsed_time >= GAME_DURATION:
            self.game_state = GAME_WIN
            if self.current_score > self.high_score:
                self.high_score = self.current_score
                save_high_score(self.high_score)
    
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
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        
        # Draw HUD
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.current_score}', True, (0, 0, 0))
        high_score_text = font.render(f'High Score: {self.high_score}', True, (0, 0, 0))
        level_text = font.render(f'Level: {self.current_level}', True, (0, 0, 0))
        time_left = max(0, (GAME_DURATION - (pygame.time.get_ticks() - self.start_time)) // 1000)
        time_text = font.render(f'Time: {time_left}s', True, (0, 0, 0))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))
        self.screen.blit(level_text, (10, 70))
        self.screen.blit(time_text, (10, 100))
        
        # Draw level up message
        if self.show_level_up:
            level_up_font = pygame.font.Font(None, 72)
            level_up_text = level_up_font.render(f'LEVEL UP!', True, (255, 0, 0))
            level_num_text = level_up_font.render(f'Level {self.current_level}', True, (255, 0, 0))
            
            x = WINDOW_WIDTH // 2 - level_up_text.get_width() // 2
            y = WINDOW_HEIGHT // 2 - level_up_text.get_height()
            self.screen.blit(level_up_text, (x, y))
            
            x = WINDOW_WIDTH // 2 - level_num_text.get_width() // 2
            y = WINDOW_HEIGHT // 2 + 20
            self.screen.blit(level_num_text, (x, y))
        
        # Draw game over/win message
        if self.game_state != GAME_RUNNING:
            message = "YOU WIN!" if self.game_state == GAME_WIN else "GAME OVER!"
            message_text = font.render(message, True, (0, 0, 0))
            restart_text = font.render("Press R to restart", True, (0, 0, 0))
            final_level_text = font.render(f"Final Level: {self.current_level}", True, (0, 0, 0))
            
            msg_x = WINDOW_WIDTH // 2 - message_text.get_width() // 2
            msg_y = WINDOW_HEIGHT // 2 - message_text.get_height()
            restart_x = WINDOW_WIDTH // 2 - restart_text.get_width() // 2
            restart_y = WINDOW_HEIGHT // 2 + restart_text.get_height()
            level_x = WINDOW_WIDTH // 2 - final_level_text.get_width() // 2
            level_y = restart_y + restart_text.get_height() + 10
            
            self.screen.blit(message_text, (msg_x, msg_y))
            self.screen.blit(restart_text, (restart_x, restart_y))
            self.screen.blit(final_level_text, (level_x, level_y))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
