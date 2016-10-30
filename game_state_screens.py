"""

Filename:     logo.py
Author:       Kyle Cookerly
Date:         10/29/2016

Description:  Function for the main menu logo and command to launch the game

"""

import curses


def draw_start_window():
    """"""
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


