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
GAME_DURATION = 10000  # 60 seconds per level
WORLD_SPEED_MULTIPLIER = 1.3  # Speed increase for road and CPU cars per level
PLAYER_SPEED_MULTIPLIER = 1.1  # Speed increase for player per level

# Timing
INITIAL_SPAWN_RATE = 2000  # milliseconds between spawns
DIFFICULTY_INCREASE_RATE = 5000  # Increase difficulty every 5 seconds

# File paths
HIGH_SCORE_FILE = "highscore.json"
def get_background_music(level):
    # After level 20, use the level 20 music
    adjusted_level = min(level - 1, 20)
    return f"assets/sound/cat_speed_{adjusted_level}.mp3"

# Sound settings
SOUND_SPEED_MULTIPLIER = 1.25  # Speed increase for background music per level

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
DARK_RED = (139, 0, 0)
WINDOW_BLUE = (100, 149, 237)
BROWN = (139, 69, 19)
METEOR_BLUE = (30, 144, 255)

# Meteor settings
METEOR_MIN_SPEED = 4
METEOR_MAX_SPEED = 7
METEOR_SIZE = 30
METEOR_SPAWN_RATE = 3000  # milliseconds between meteor spawns

# Game states
GAME_RUNNING = 'running'
GAME_OVER = 'game_over'
GAME_WIN = 'win'
