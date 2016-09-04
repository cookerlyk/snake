"""

Filename:     Snake_game.py
Author:       Kyle Cookerly
Date:         07/01/2016

Description:  The Game, Snake, and Board classes for terminal-based snake clone

"""

import curses                                  # For terminal control
from random import randint                     # For RNG food placement


curses.initscr()                               # Starts screen
window = curses.newwin(20, 60, 0, 10)          # Creates window
curses.noecho()                                # Hides the keyboard input from the terminal
curses.curs_set(0)
window.border(0)                               # Draws border by default


class Game(object):
    """The Game class class handles the game as a whole"""
    def __init__(self):
        self.board = Board()
        self.snake = Snake()
        self.height = 0
        self.width = 0

    def run_game(self):
        """
        Run_game is the main gameplay function that calls the functions necessary to run the game loop.
        Functions are called in specific order to ensure correct gameplay
        """
        window.addstr(19, 49, "Score:" + str(self.snake.get_score()))
        window.addstr(0, 28, "SNAKE")
        self.board.display_fruit()             # Draws fruit
        self.snake.display_snake()             # Draws snake
        self.snake.move_position()             # Gets user input for movement
        self.snake.check_fruit_collision()     # Checks if fruit was hit
        self.snake.check_tail_collision()      # Checks if the snake hit its own tail
        # self.snake.game_over_if_wall_hit()     # Game ends if the walls are hit by the snake if not commented out
        self.snake.pass_through_walls()        # Allows the snake to pass through walls if not commented out
        self.snake.stop_wall_bug()             # Fixes the game crashing wall bug where you can get stuck in the wall
        window.border(0)                       # Redraws border, passing through the wall will break border without
        window.timeout(self.snake.game_speed)  # Controls game speed

    def end(self):
        """Ends the curses window"""
        curses.endwin()


class Board(object):
    """Represents the game board where the game will take place"""
    board_width = 60                       # X values
    board_height = 20                      # Y values
    fruit_position = [randint(1, board_width - 2), randint(1, board_height - 2)]

    def display_fruit(self):
        """Draws the fruit to the screen based on x and y coordinates"""
        window.addch(Board.fruit_position[1], Board.fruit_position[0], "@")


class Snake(object):
    """Class represents the snake"""
    game_speed = 110                      # Variable to hold integer to update the game speed
    fruit_eaten = 0                       # Keeps track of how many times food was eaten, for increasing game speed
    score = 0
    game_over = False
    snake_position = [30, 9]              # [X, Y] = starting head position
    snake_body = [snake_position[:]] * 3  # snake body is 3 segments to start
    key = None                            # default key is none

    def move_position(self):
        """
        Takes input from the keyboard for the snake movement using 'W' 'A' 'S' 'D' keys
        If there is no input, movement continues in direction of the last key press
        """
        movement = window.getch()
        self.key = self.key if movement == -1 else movement
        if self.key == ord("w"):      # Up, "w" key
            self.snake_position[1] -= 1

        elif self.key == ord("a"):    # Left, "a" key
            self.snake_position[0] -= 1

        elif self.key == ord("s"):    # Down, "s" key
            self.snake_position[1] += 1

        elif self.key == ord("d"):    # Right, "d" key
            self.snake_position[0] += 1

        elif self.key == ord("q"):    # Quit, "q" key
            self.game_over = True

        elif self.key == ord(" "):    # TODO...Pause, "space bar"
            pass

        else:                         # TODO...make any invalid key press continue last valid direction
            pass

    def display_snake(self):
        """Draws the snake to the console"""
        end_of_snake = self.snake_body[-1][:]
        for i in range(len(self.snake_body)-1, 0, -1):
            self.snake_body[i] = self.snake_body[i-1]

        if end_of_snake not in self.snake_body:
            window.addch(end_of_snake[1], end_of_snake[0], " ")            # Erases the end of the snake

        window.addch(self.snake_position[1], self.snake_position[0], "#")  # Draws the snake head

        self.snake_body[0] = self.snake_position[:]

    def check_fruit_collision(self):
        """
        Function contains the collision logic for the fruit, also ensures
        that the fruit is not redrawn in an occupied coordinate
        """
        if self.snake_position[0] == Board.fruit_position[0] and \
                self.snake_position[1] == Board.fruit_position[1]:
            self.score += 10
            self.fruit_eaten += 1
            self.snake_body.append(self.snake_body[-1])

            # Will increase the game speed by 1 every 2nd fruit eaten, up to 70 eaten
            if self.fruit_eaten % 2 == 0:
                if self.game_speed > 75:
                    self.game_speed -= 1

            # Ensures that the new fruit coordinates are an empty coordinate and not part of the snake
            # Generates a random fruit position after eating it
            fruit_drawn = False
            while not fruit_drawn:
                Board.fruit_position[1] = randint(1, Board.board_height - 2)
                Board.fruit_position[0] = randint(1, Board.board_width - 2)

                if window.inch(Board.fruit_position[1], Board.fruit_position[0]) == ord(" "):
                    fruit_drawn = True

                else:
                    Board.fruit_position[1] = randint(1, Board.board_height - 2)
                    Board.fruit_position[0] = randint(1, Board.board_width - 2)

    def check_tail_collision(self):
        """Checks if the snake head collides with the tail, gameover if true"""
        if self.key == ord("w"):
            if window.inch(self.snake_position[1] - 1, self.snake_position[0]) == ord("#"):
                self.game_over = True
        elif self.key == ord("a"):
            if window.inch(self.snake_position[1], self.snake_position[0] - 1) == ord("#"):
                self.game_over = True
        elif self.key == ord("s"):
            if window.inch(self.snake_position[1] + 1, self.snake_position[0]) == ord("#"):
                self.game_over = True
        elif self.key == ord("d"):
            if window.inch(self.snake_position[1], self.snake_position[0] + 1) == ord("#"):
                self.game_over = True

    def game_over_if_wall_hit(self):
        """
        Gameplay option: Game over when walls are hit by snake head.

        Comment out in the run_game function, if you want to be able to pass through walls

        Precondition: pass_through_walls function must be commented out in run_game function
        """
        if self.snake_position[1] == Board.board_height - 1 or \
                self.snake_position[0] == Board.board_width - 1:
            curses.beep()
            self.game_over = True  # Y wall hit

        if self.snake_position[0] == 0 or self.snake_position[1] == 0:
            curses.beep()
            self.game_over = True  # X wall hit

    def pass_through_walls(self):
        """
        Gameplay option: No game over when walls are hit, snake will pass through the wall to the other side

        Comment out in the run_game function, if you want the game to end if you hit a wall

        Precondition: game_over_if_wall_hit function must be commented out in run_game function
        """
        if self.snake_position[0] == 0:
            self.snake_position[0] = Board.board_width - 1

        elif self.snake_position[1] == 0:
            self.snake_position[1] = Board.board_height - 1

        elif self.snake_position[0] == Board.board_width - 1:
            self.snake_position[0] = 0

        elif self.snake_position[1] == Board.board_height - 1:
            self.snake_position[1] = 0

    def stop_wall_bug(self):
        """
        Function stops the wall bug from crashing the game if you get stuck between the walls.
        Places the snake on the opposite side if you are in the range to get stuck in the wall.
        Thus, if the snake is moving on the boundary itself, parallel with the wall, it will be
        moved to the other side.
        """
        # top wall
        if self.snake_position[1] == Board.board_height - 1 and self.key == ord("a"):
            self.snake_position[1] = 1
        elif self.snake_position[1] == Board.board_height - 1 and self.key == ord("d"):
            self.snake_position[1] = 1

        # bottom wall
        if self.snake_position[1] == 0 and self.key == ord("a"):
            self.snake_position[1] = Board.board_height - 2
        elif self.snake_position[1] == 0 and self.key == ord("d"):
            self.snake_position[1] = Board.board_height - 2

        # left wall
        if self.snake_position[0] == 0 and self.key == ord("w"):
            self.snake_position[0] = Board.board_width - 2
        elif self.snake_position[0] == 0 and self.key == ord("s"):
            self.snake_position[0] = Board.board_width - 2

        # right wall
        if self.snake_position[0] == Board.board_width - 1 and self.key == ord("w"):
            self.snake_position[0] = 1
        elif self.snake_position[0] == Board.board_width - 1 and self.key == ord("s"):
            self.snake_position[0] = 1

    def get_score(self):
        """Returns the score variable for use on the console display"""
        return self.score

    def is_game_over(self):
        """Returns boolean for main game loop to end or continue"""
        return self.game_over
