"""

Filename:     snake_game.py
Author:       Kyle Cookerly

Description:  The Game, Snake, and Board classes for terminal-based snake clone

"""

import curses                                  # For terminal control
from random import randint                     # For RNG fruit placement


curses.initscr()                               # Starts screen
curses.noecho()                                # Hides the keyboard input from the terminal
curses.curs_set(0)
window = curses.newwin(20, 60, 0, 10)          # Creates window
window.border(0)                               # Draws border by default


# TODO  Try to break into snake, board and game class files

class Game:
    MAX_GAME_SPEED = 75
    SCORE_INCREASE = 10

    pass_through_walls = None
    current_game_speed = 110
    fruit_eaten = 0
    score = 0
    game_over = False

    def __init__(self, mode):
        """
        @Param bool that corresponds to the game type the user selects, if True the snake can pass through the walls
        if False the game is over when the snake hits the wall
        """
        self.pass_through_walls = mode
        self.board = Board()
        self.snake = Snake()

    def run_game(self):
        """
        Run_game is the main gameplay function that calls the functions necessary to run the game loop.
        Functions are called in specific order to ensure correct gameplay
        """
        window.addstr(19, 49, "Score:" + str(self.score))
        window.addstr(0, 28, "SNAKE")

        self.board.display_fruit()
        self.snake.display_snake()
        self.snake.move_position()               # Gets user input for movement
        self.check_fruit_collision()
        self.snake.check_tail_collision()
        self.set_game_over()                     # Checks if the snake class signaled a game over
        if not self.pass_through_walls:
            self.game_over_if_wall_hit()
        else:
            self.pass_through_if_wall_hit()

        self.snake.jump_snake_position()         # Fixes the game crashing bug where you can get stuck in the wall

        window.border(0)                         # Redraws border, passing through the wall will break border without
        window.timeout(self.current_game_speed)  # Controls game speed

    def check_fruit_collision(self):
        """
        Function contains the collision logic for the fruit, also ensures
        that the fruit is not redrawn in an occupied coordinate
        """
        if self.snake.get_snake_head_x() == self.board.get_fruit_x() and \
                        self.snake.get_snake_head_y() == self.board.get_fruit_y():
            self.score += self.SCORE_INCREASE
            self.fruit_eaten += 1
            self.snake.grow_snake()
            self.increase_game_speed()
            self.board.update_fruit_position()

    def set_game_over(self):
        """
        If a game over is passed in from the snake class, the
        game over variable is set to true in the game class too,
        thus ending the game
        """
        if self.snake.is_game_over():
            self.game_over = True

    def is_game_over(self):
        """Returns boolean for main game loop to end or continue"""
        return self.game_over

    def increase_game_speed(self):
        """Will increase the game speed by 1 every 2nd fruit eaten, up to 70 eaten"""
        if self.fruit_eaten % 2 == 0:
            if self.current_game_speed > self.MAX_GAME_SPEED:
                self.current_game_speed -= 1

    def game_over_if_wall_hit(self):
        """
        Gameplay option: Game over when walls are hit by snake head.
        """
        if self.snake.get_snake_head_y() == self.board.get_board_height() - 1 or \
                        self.snake.get_snake_head_x() == self.board.get_board_width() - 1:
            self.game_over = True  # Y wall hit

        if self.snake.get_snake_head_x() == 0 or self.snake.get_snake_head_y() == 0:
            self.game_over = True  # X wall hit

    def pass_through_if_wall_hit(self):
        """
        Gameplay option: No game over when walls are hit, snake will pass through the wall to the other side
        """
        if self.snake.get_snake_head_x() == 0:
            self.snake.set_snake_head_x(self.board.get_board_width() - 1)

        elif self.snake.get_snake_head_y() == 0:
            self.snake.set_snake_head_y(self.board.get_board_height() - 1)

        elif self.snake.get_snake_head_x() == self.board.get_board_width() - 1:
            self.snake.set_snake_head_x(0)

        elif self.snake.get_snake_head_y() == self.board.get_board_height() - 1:
            self.snake.set_snake_head_y(0)

    def get_game_score(self):
        """returns the current score"""
        return self.score

    def end_window(self):
        """Ends the curses window"""
        curses.endwin()


class Board:
    """Represents the game board. Class handles the board and the fruit"""
    BOARD_WIDTH = 60       # X values
    BOARD_HEIGHT = 20      # Y values
    FRUIT_CHAR = "@"

    fruit_position = [randint(1, BOARD_WIDTH - 2), randint(1, BOARD_HEIGHT - 2)]

    def display_fruit(self):
        """Draws the fruit to the screen based on x and y coordinates"""
        window.addch(self.fruit_position[1], self.fruit_position[0], self.FRUIT_CHAR)

    def update_fruit_position(self):
        """
        Ensures that the new fruit coordinates are an empty coordinate and not part of the snake
        Generates a random fruit position after eating it and updates the position variables
        """
        fruit_drawn = False
        while not fruit_drawn:
            self.set_fruit_y(randint(1, self.BOARD_HEIGHT - 2))
            self.set_fruit_x(randint(1, self.BOARD_WIDTH - 2))

            if window.inch(self.get_fruit_y(), self.get_fruit_x()) == ord(" "):
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

    def move_position(self):
        """
        Takes input from the keyboard for the snake movement using 'W' 'A' 'S' 'D' keys
        If there is no input, movement continues in direction of the last key press
        Invalid input will continue the snake on the path of the last valid key press
        """
        #TODO find a better way to handle the nested ifs
        movement = window.getch()
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
            window.addch(end_of_snake[1], end_of_snake[0], " ")            # Erases the end of the snake

        window.addch(self.snake_position[1], self.snake_position[0], self.SEGMENT_CHAR)  # Draws the snake head

        self.snake_body[0] = self.snake_position[:]

    def check_tail_collision(self):
        """Checks if the snake head collides with the tail, gameover if true"""
        if self.key == self.UP_KEY and not self.did_go_back_on_self():
            if window.inch(self.snake_position[1], self.snake_position[0]) == ord(self.SEGMENT_CHAR):
                self.game_over = True
        elif self.key == self.LEFT_KEY and not self.did_go_back_on_self():
            if window.inch(self.snake_position[1], self.snake_position[0]) == ord(self.SEGMENT_CHAR):
                self.game_over = True
        elif self.key == self.DOWN_KEY and not self.did_go_back_on_self():
            if window.inch(self.snake_position[1], self.snake_position[0]) == ord(self.SEGMENT_CHAR):
                self.game_over = True
        elif self.key == self.RIGHT_KEY and not self.did_go_back_on_self():
            if window.inch(self.snake_position[1], self.snake_position[0]) == ord(self.SEGMENT_CHAR):
                self.game_over = True

    def jump_snake_position(self):
        """
        Function stops the wall bug from crashing the game if you get stuck between the walls.
        Places the snake on the opposite side if you are in the range to get stuck in the wall.
        Thus, if the snake is moving on the boundary itself, parallel with the wall, it will be
        moved to the other side.
        """
        # top wall
        if self.snake_position[1] == Board.BOARD_HEIGHT - 1 and self.key == self.LEFT_KEY:
            self.snake_position[1] = 1
        elif self.snake_position[1] == Board.BOARD_HEIGHT - 1 and self.key == self.RIGHT_KEY:
            self.snake_position[1] = 1

        # bottom wall
        if self.snake_position[1] == 0 and self.key == self.LEFT_KEY:
            self.snake_position[1] = Board.BOARD_HEIGHT - 2
        elif self.snake_position[1] == 0 and self.key == self.RIGHT_KEY:
            self.snake_position[1] = Board.BOARD_HEIGHT - 2

        # left wall
        if self.snake_position[0] == 0 and self.key == self.UP_KEY:
            self.snake_position[0] = Board.BOARD_WIDTH - 2
        elif self.snake_position[0] == 0 and self.key == self.DOWN_KEY:
            self.snake_position[0] = Board.BOARD_WIDTH - 2

        # right wall
        if self.snake_position[0] == Board.BOARD_WIDTH - 1 and self.key == self.UP_KEY:
            self.snake_position[0] = 1
        elif self.snake_position[0] == Board.BOARD_WIDTH - 1 and self.key == self.DOWN_KEY:
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



