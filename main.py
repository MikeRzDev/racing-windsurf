"""
2D Car Racing Game

A simple racing game where you control a car and avoid CPU-controlled cars.
Use arrow keys to move your car and try to survive as long as possible!
"""

from game.game_manager import GameManager

def main():
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main()
