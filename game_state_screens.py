"""

Filename:     game_state_screens.py
Author:       Kyle Cookerly

Description:  Function for the main menu logo and command to launch the game
              the game option window and the game over window

"""

import curses


def draw_start_window():
    """
    Draws the main logo to the screen
    """
    start_screen = curses.newwin(20, 60, 0, 8)
    start_screen.addstr(7, 7,  "  ______   ___    _       _       _   __   ______  ")
    start_screen.addstr(8, 7,  " / _____\ |   \  | |     / \     | | / /  | _____| ")
    start_screen.addstr(9, 7,  " \ \___   | |\ \ | |    /___\    | |/ /   | |___   ")
    start_screen.addstr(10, 7, "  \__  \  | | \ \| |   / \_/ \   |  _ \   | ____|  ")
    start_screen.addstr(11, 7, " ____\  \ | |  \   |  /  ___  \  | | \ \  | |____  ")
    start_screen.addstr(12, 7, " \______/ |_|   \__| /__/   \__\ |_|  \_\ |______| ")

    start_screen.addstr(15, 7, "               Press any key to play               ")
    while True:
        if start_screen.getch() is not None:
            break
    curses.endwin()


def draw_option_select_window():
    """
    Draws the game type option and choices to the screen
    :return: bool based on the game type selection
    """
    option_screen = curses.newwin(20, 60, 0, 8)
    option_screen.addstr(7, 24,  "Select Game Mode")
    option_screen.addstr(12, 13, "(1) Solid Walls    (2) Pass Through Walls")
    key_pressed = None
    while True:
        key_pressed = option_screen.getch()
        if key_pressed == ord("1") or key_pressed == ord("2"):
            break
    curses.endwin()
    if key_pressed == ord("1"):
        return False
    else:
        return True



def draw_game_over_window(score):
    """
    Draws the game over message and the user's final score onto the screen
    :param score: Passed in score the user got in that round
    """
    game_over_screen = curses.newwin(20, 60, 0, 10)
    game_over_screen.addstr(7, 25, "Game Over")
    game_over_screen.addstr(10, 22, "Final Score: " + str(score))
    game_over_screen.addstr(15, 17, "Press any key to continue")
    while True:
        if game_over_screen.getch() is not None:
            break
    curses.endwin()
    

