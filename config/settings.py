import pygame

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Game elements
ROAD_WIDTH = 300
CAR_WIDTH = 40
CAR_HEIGHT = 60
PLAYER_SPEED = 5
BASE_CPU_SPEED = 3
ROAD_SPEED = 5  # Speed of road movement
GAME_DURATION = 60000  # 60 seconds in milliseconds

# Timing
INITIAL_SPAWN_RATE = 2000  # milliseconds between spawns
DIFFICULTY_INCREASE_RATE = 5000  # Increase difficulty every 5 seconds

# File paths
HIGH_SCORE_FILE = "highscore.json"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
DARK_RED = (139, 0, 0)
WINDOW_BLUE = (100, 149, 237)

# Game states
GAME_RUNNING = 'running'
GAME_OVER = 'game_over'
GAME_WIN = 'win'
