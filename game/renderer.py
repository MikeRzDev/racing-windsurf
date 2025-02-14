import pygame
from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, GRAY, BLACK, YELLOW,
    GAME_RUNNING, GAME_OVER, GAME_WIN, ROAD_WIDTH
)

def draw_road(screen, offset):
    road_x = (WINDOW_WIDTH - ROAD_WIDTH) // 2
    
    # Draw road background
    pygame.draw.rect(screen, GRAY, (road_x, 0, ROAD_WIDTH, WINDOW_HEIGHT))
    
    # Draw road lines with fixed parameters
    line_width = 10
    line_height = 50
    line_gap = 40
    total_pattern = line_height + line_gap
    line_x = WINDOW_WIDTH // 2 - line_width // 2
    
    # Calculate number of lines needed to fill screen plus one extra to prevent gaps
    num_lines = WINDOW_HEIGHT // total_pattern + 2
    
    # Draw yellow center lines
    for i in range(num_lines):
        y = -line_height + (offset % total_pattern) + (i * total_pattern)
        if y < WINDOW_HEIGHT:  # Only draw if line is on screen
            pygame.draw.rect(screen, YELLOW, (line_x, y, line_width, line_height))
    
    # Draw road edges
    edge_width = 5
    pygame.draw.rect(screen, WHITE, (road_x, 0, edge_width, WINDOW_HEIGHT))
    pygame.draw.rect(screen, WHITE, (road_x + ROAD_WIDTH - edge_width, 0, edge_width, WINDOW_HEIGHT))
    
def draw_game(screen, game_manager):
    # Fill background
    screen.fill(BLACK)
    
    # Draw road with offset
    draw_road(screen, game_manager.road_offset)
    
    # Draw power-ups
    for power_up in game_manager.power_ups:
        power_up.draw(screen)
    
    # Draw bullets
    for bullet in game_manager.bullets:
        bullet.draw(screen)
    
    # Draw CPU cars
    for car in game_manager.cpu_cars:
        car.draw(screen)
    
    # Draw player
    game_manager.player.draw(screen)
    
    # Draw explosions
    for explosion in game_manager.explosions[:]:
        if explosion.is_finished():
            game_manager.explosions.remove(explosion)
        else:
            explosion.draw(screen)
    
    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {game_manager.current_score}", True, WHITE)
    high_score_text = font.render(f"High Score: {game_manager.high_score}", True, WHITE)
    level_text = font.render(f"Level: {game_manager.current_level}", True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))
    screen.blit(level_text, (WINDOW_WIDTH - 150, 10))
    
    # Draw game over or level up text
    if game_manager.game_state == GAME_OVER:
        game_over_text = font.render("Game Over! Press R to restart", True, WHITE)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        screen.blit(game_over_text, text_rect)
    elif game_manager.show_level_up:
        if pygame.time.get_ticks() - game_manager.level_up_time < 2000:  # Show for 2 seconds
            level_up_text = font.render(f"Level {game_manager.current_level}!", True, WHITE)
            text_rect = level_up_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            screen.blit(level_up_text, text_rect)
            
            # Show power-up unlock message at level 3
            if game_manager.current_level == 3:
                unlock_text = font.render("Power-ups Unlocked! Collect red circles to shoot!", True, WHITE)
                unlock_rect = unlock_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 40))
                screen.blit(unlock_text, unlock_rect)
        else:
            game_manager.show_level_up = False
    
    # Draw power-up timer bar
    if game_manager.power_up_active:
        power_up_bar_width = 200
        power_up_bar_height = 20
        power_up_bar_x = WINDOW_WIDTH - power_up_bar_width - 10
        power_up_bar_y = 10
        power_up_bar_fill = (game_manager.power_up_time - (pygame.time.get_ticks() - game_manager.power_up_start_time)) / game_manager.power_up_time
        
        pygame.draw.rect(screen, WHITE, (power_up_bar_x, power_up_bar_y, power_up_bar_width, power_up_bar_height), 2)
        pygame.draw.rect(screen, WHITE, (power_up_bar_x, power_up_bar_y, power_up_bar_width * power_up_bar_fill, power_up_bar_height))
    
    pygame.display.flip()
