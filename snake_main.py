"""

Filename:     Snake_main.py
Author:       Kyle Cookerly
Date:         07/01/2016

Description:  Console-based Snake clone, written in Python 3.5.1
              using the curses module.

"""

from snake_game import Game


def main():
    snake_game = Game()                           # Creates the object for the game

    while not snake_game.snake.is_game_over():
        snake_game.run_game()                     # Calls gameplay function until game_over is true

    snake_game.end()                              # Closes the window


if __name__ == "__main__":
    main()
