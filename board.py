"""

Filename:     board.py
Author:       Kyle Cookerly

Description:  The Board class for terminal-based snake clone

"""

from random import randint                     # For RNG fruit placement


class Board:
    """Represents the game board. Class handles the board and the fruit"""
    BOARD_WIDTH = 60       # X values
    BOARD_HEIGHT = 20      # Y values
    FRUIT_CHAR = "@"

    fruit_position = [randint(1, BOARD_WIDTH - 2), randint(1, BOARD_HEIGHT - 2)]

    def __init__(self, window):
        """
        :param window: the window object that the game creates
        """
        self.window = window

    def display_fruit(self):
        """Draws the fruit to the screen based on x and y coordinates"""
        self.window.addch(self.fruit_position[1], self.fruit_position[0], self.FRUIT_CHAR)

    def update_fruit_position(self):
        """
        Ensures that the new fruit coordinates are an empty coordinate and not part of the snake
        Generates a random fruit position after eating it and updates the position variables
        """
        fruit_drawn = False
        while not fruit_drawn:
            self.set_fruit_y(randint(1, self.BOARD_HEIGHT - 2))
            self.set_fruit_x(randint(1, self.BOARD_WIDTH - 2))

            if self.window.inch(self.get_fruit_y(), self.get_fruit_x()) == ord(" "):
                fruit_drawn = True

            else:
                self.set_fruit_y(randint(1, self.BOARD_HEIGHT - 2))
                self.set_fruit_x(randint(1, self.BOARD_WIDTH - 2))

    def get_fruit_x(self):
        return self.fruit_position[0]

    def get_fruit_y(self):
        return self.fruit_position[1]

    def set_fruit_x(self, x_val: int):
        self.fruit_position[0] = x_val

    def set_fruit_y(self, y_val: int):
        self.fruit_position[1] = y_val

    def get_board_width(self):
        return self.BOARD_WIDTH

    def get_board_height(self):
        return self.BOARD_HEIGHT
