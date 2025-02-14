# 2D Car Racing Game

A dynamic 2D car racing game built with Pygame featuring multiple levels, power-ups, and challenging obstacles.

## Game Features
- Progressive difficulty with multiple levels
- Power-up system (unlocks at Level 3)
- Shooting mechanics to destroy obstacles
- Meteor challenges (appears at Level 5)
- Dynamic speed scaling with each level
- High score system

## Game Rules
- Control your car using UP/DOWN arrow keys
- Press SPACE to shoot (when power-up is active)
- Avoid colliding with red CPU cars and meteors
- Survive each level's duration to progress
- Collect power-ups to enable shooting ability
- Score points by:
  - Shooting CPU cars (2 points)
  - Destroying meteors (100 points)
  - Catching meteors in explosions (30 points)
- Press R to restart when game is over

## Setup
1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

## Level Progression
- Each level increases game difficulty
- World speed and player speed scale up with levels
- Level 3: Unlocks power-ups and shooting mechanics
- Level 5: Introduces meteor challenges
- Background music changes with level progression
