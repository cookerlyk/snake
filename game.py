"""

Filename:     game.py
Author:       Kyle Cookerly

Description:  The main Game class for terminal-based snake clone

"""

import curses                                  # For terminal control
from board import Board
from snake import Snake


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
        :param mode: bool that corresponds to the game type the user selects, if True the snake can pass through the
        walls if False the game is over when the snake hits the wall
        """
        self.window = curses.newwin(20, 60, 0, 10)  # Creates window
        self.window.border(0)                       # Draws border by default

        self.game_mode = mode  # Store the game mode as a string

        # Initialize game attributes based on the selected game mode
        if self.game_mode == "solid_walls_with_lives":
            self.lives = 3  # Starting number of lives for this mode
            self.pass_through_walls = False
        elif self.game_mode == "pass_through_walls":
            self.pass_through_walls = True
        else:  # Default to solid walls if an unknown mode is provided
            self.pass_through_walls = False

        self.board = Board(self.window)
        self.snake = Snake(self.window, self.board.get_board_width(), self.board.get_board_height())

    def run_game(self):
        """
        Run_game is the main gameplay function that calls the functions necessary to run the game loop.
        Functions are called in specific order to ensure correct gameplay
        """
        self.window.addstr(19, 49, "Score:" + str(self.score))
        self.window.addstr(0, 28, "SNAKE")
        ###
        if self.game_mode == "solid_walls_with_lives":
            self.window.addstr(0, 2, "Lives: " + str(self.lives))  # Display lives on the screen
        ###
        self.board.display_fruit()
        self.snake.display_snake()
        self.snake.move_position()               # Gets user input for movement
        self.check_fruit_collision()
        self.snake.check_tail_collision()
        
        # Handle the "pass_through_walls" mode
        if self.game_mode == "pass_through_walls":
            self.pass_through_if_wall_hit()

        # Handle "solid_walls_with_lives" mode
        if self.game_mode == "solid_walls_with_lives":
            # Check for wall hit or self-collision
            wall_hit = self.snake.get_snake_head_y() == 0 or \
                    self.snake.get_snake_head_y() == self.board.get_board_height() - 1 or \
                    self.snake.get_snake_head_x() == 0 or \
                    self.snake.get_snake_head_x() == self.board.get_board_width() - 1

            if self.snake.is_game_over() or wall_hit:
                if self.lives > 1:
                    self.lives -= 1
                    self.reset_game()       # Reset the game, not end it
                else:
                    self.game_over = True  # No more lives


        # For other modes or if 'pass_through_walls' is enabled
        if self.game_mode != "pass_through_walls":
            self.game_over_if_wall_hit()

        if self.game_mode != "solid_walls_with_lives":
            self.set_game_over()

        self.snake.jump_snake_position()         # Fixes the game crashing bug where you can get stuck in the wall

        self.window.border(0)                    # Redraws border, passing through the wall will break border without
        self.window.timeout(self.current_game_speed)

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

    def reset_game(self):
        """Resets the game state but keeps the score and reduces lives."""
        # Clear the part of the window where the snake was
        for segment in self.snake.snake_body:
            self.window.addch(segment[1], segment[0], ' ')  # Replace old segments with spaces

        # Clear the old fruit
        self.window.addch(self.board.fruit_position[1], self.board.fruit_position[0], ' ')

        self.snake.reset_snake()  # Reset the snake
        self.board.update_fruit_position()  # Place a new fruit
        self.board.display_fruit()  # Redisplay the fruit
        self.window.refresh()  # Refresh the window to update the display

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
