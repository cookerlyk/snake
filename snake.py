"""

Filename:     snake.py
Author:       Kyle Cookerly

Description:  The Snake class for terminal-based snake clone

"""


class Snake:
    """Class represents the snake"""
    UP_KEY = ord("w")
    DOWN_KEY = ord("s")
    LEFT_KEY = ord("a")
    RIGHT_KEY = ord("d")
    QUIT_KEY = ord("q")
    PAUSE_KEY = ord(" ")
    SEGMENT_CHAR = "#"
    INITIAL_LENGTH = 3
    STARTING_X = 30
    STARTING_Y = 9

    current_direction = None

    snake_position = [STARTING_X, STARTING_Y]
    snake_body = [snake_position[:]] * INITIAL_LENGTH
    key = None
    game_over = False
    last_valid_key = None

    def __init__(self, window, width, height):
        """
        :param window: the window object that the game creates
        :param width: the width of the board
        :param height: the height of the board
        """
        self.window = window
        self.board_width = width
        self.board_height = height

    def move_position(self):
        """
        Takes input from the keyboard for the snake movement using 'W' 'A' 'S' 'D' keys
        If there is no input, movement continues in direction of the last key press
        Invalid input will continue the snake on the path of the last valid key press
        """
        #TODO find a better way to handle the nested ifs
        movement = self.window.getch()
        self.key = self.key if movement == -1 else movement
        if self.key == self.UP_KEY:
            if self.current_direction != self.DOWN_KEY:
                self.last_valid_key = self.UP_KEY
                self.current_direction = self.last_valid_key
                self.move_up()
            else:
                self.move_down()

        elif self.key == self.LEFT_KEY:
            if self.current_direction != self.RIGHT_KEY:
                self.last_valid_key = self.LEFT_KEY
                self.current_direction = self.last_valid_key
                self.move_left()
            else:
                self.move_right()

        elif self.key == self.DOWN_KEY:
            if self.current_direction != self.UP_KEY:
                self.last_valid_key = self.DOWN_KEY
                self.current_direction = self.last_valid_key
                self.move_down()
            else:
                self.move_up()

        elif self.key == self.RIGHT_KEY:
            if self.current_direction != self.LEFT_KEY:
                self.last_valid_key = self.RIGHT_KEY
                self.current_direction = self.last_valid_key
                self.move_right()
            else:
                self.move_left()

        elif self.key == self.QUIT_KEY:
            self.game_over = True

        elif self.key == self.PAUSE_KEY:
            pass

        else:
            # Any invalid key press makes the snake continue moving in last valid direction
            if self.last_valid_key == self.UP_KEY:
                self.move_up()
            elif self.last_valid_key == self.LEFT_KEY:
                self.move_left()
            elif self.last_valid_key == self.DOWN_KEY:
                self.move_down()
            elif self.last_valid_key == self.RIGHT_KEY:
                self.move_right()

    def display_snake(self):
        """Draws the snake to the console"""
        end_of_snake = self.snake_body[-1][:]
        for i in range(len(self.snake_body) - 1, 0, -1):
            self.snake_body[i] = self.snake_body[i - 1]

        if end_of_snake not in self.snake_body:
            self.window.addch(end_of_snake[1], end_of_snake[0], " ")            # Erases the end of the snake

        self.window.addch(self.snake_position[1], self.snake_position[0], self.SEGMENT_CHAR)  # Draws the snake head

        self.snake_body[0] = self.snake_position[:]

    def check_tail_collision(self):
        """Checks if the snake head collides with the tail, gameover if true"""
        if self.key == self.UP_KEY and not self.did_go_back_on_self():
            if self.window.inch(self.snake_position[1], self.snake_position[0]) == ord(self.SEGMENT_CHAR):
                self.game_over = True
        elif self.key == self.LEFT_KEY and not self.did_go_back_on_self():
            if self.window.inch(self.snake_position[1], self.snake_position[0]) == ord(self.SEGMENT_CHAR):
                self.game_over = True
        elif self.key == self.DOWN_KEY and not self.did_go_back_on_self():
            if self.window.inch(self.snake_position[1], self.snake_position[0]) == ord(self.SEGMENT_CHAR):
                self.game_over = True
        elif self.key == self.RIGHT_KEY and not self.did_go_back_on_self():
            if self.window.inch(self.snake_position[1], self.snake_position[0]) == ord(self.SEGMENT_CHAR):
                self.game_over = True

    def jump_snake_position(self):
        """
        Function stops the wall bug from crashing the game if you get stuck between the walls.
        Places the snake on the opposite side if you are in the range to get stuck in the wall.
        Thus, if the snake is moving on the boundary itself, parallel with the wall, it will be
        moved to the other side.
        """
        # top wall
        if self.snake_position[1] == self.board_height - 1 and self.key == self.LEFT_KEY:
            self.snake_position[1] = 1
        elif self.snake_position[1] == self.board_height - 1 and self.key == self.RIGHT_KEY:
            self.snake_position[1] = 1

        # bottom wall
        if self.snake_position[1] == 0 and self.key == self.LEFT_KEY:
            self.snake_position[1] = self.board_height - 2
        elif self.snake_position[1] == 0 and self.key == self.RIGHT_KEY:
            self.snake_position[1] = self.board_height - 2

        # left wall
        if self.snake_position[0] == 0 and self.key == self.UP_KEY:
            self.snake_position[0] = self.board_width - 2
        elif self.snake_position[0] == 0 and self.key == self.DOWN_KEY:
            self.snake_position[0] = self.board_width - 2

        # right wall
        if self.snake_position[0] == self.board_width - 1 and self.key == self.UP_KEY:
            self.snake_position[0] = 1
        elif self.snake_position[0] == self.board_width - 1 and self.key == self.DOWN_KEY:
            self.snake_position[0] = 1

    def is_game_over(self):
        """Returns boolean for main game loop to end or continue"""
        return self.game_over

    def grow_snake(self):
        """Appends the snake when called adding 1 segment to the end of its body"""
        self.snake_body.append(self.snake_body[-1])

    # TODO better name?
    def did_go_back_on_self(self):
        """
        Checks if the snake went back on its self
        eg. did the user press to go down if the snake was moving up
        thus running over the second snake segment
        """
        if self.current_direction == self.UP_KEY:
            if self.key == self.DOWN_KEY:
                return True
        elif self.current_direction == self.DOWN_KEY:
            if self.key == self.UP_KEY:
                return True
        elif self.current_direction == self.LEFT_KEY:
            if self.key == self.RIGHT_KEY:
                return True
        elif self.current_direction == self.RIGHT_KEY:
            if self.key == self.LEFT_KEY:
                return True

        return False

    def move_up(self):
        self.snake_position[1] -= 1

    def move_down(self):
        self.snake_position[1] += 1

    def move_left(self):
        self.snake_position[0] -= 1

    def move_right(self):
        self.snake_position[0] += 1

    def get_snake_head_x(self):
        return self.snake_position[0]

    def get_snake_head_y(self):
        return self.snake_position[1]

    def set_snake_head_x(self, x_val: int):
        self.snake_position[0] = x_val

    def set_snake_head_y(self, y_val: int):
        self.snake_position[1] = y_val
