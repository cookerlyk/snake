"""

Filename:     snake_main.py
Author:       Kyle Cookerly

Description:  Console-based Snake clone, written in Python 3.5.1
              using the curses module.

"""

from snake_game import Game
from game_state_screens import draw_start_window, draw_game_over_window


def main():
    draw_start_window()                                  # Draws the game logo on startup
    snake_game = Game()                                  # Creates the object for the game

    while not snake_game.is_game_over():
        snake_game.run_game()                            # Calls gameplay function until game_over is true

    snake_game.end_window()                              # Closes the game window

    draw_game_over_window(snake_game.get_game_score())   # Draws the game over screen


if __name__ == "__main__":
    main()
