"""

Filename:     snake_main.py
Author:       Kyle Cookerly

Description:  Console-based Snake clone, written in Python 3.5.1
              using the curses module.

"""

from snake_game import Game
from game_state_screens import draw_start_window, draw_game_over_window, draw_option_select_window


def main():
    draw_start_window()
    game_mode = draw_option_select_window()     # Draws the option screen and assigns the value received to game_mode
    snake_game = Game(game_mode)

    while not snake_game.is_game_over():
        snake_game.run_game()

    snake_game.end_window()
    draw_game_over_window(snake_game.get_game_score())

if __name__ == "__main__":
    main()
