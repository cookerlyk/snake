#Snake
###Clone of the classic game snake

Written in Python 3.5.1 using the curses module for terminal display and control.

The code supports two different game options, the first will end the game when a wall is hit by the head of the snake,
the second game mode allows the snake to pass through the walls to the other side and the game will only end if the
snake runs into its tail.

By default, the game allows the snake to pass through the walls, to enable the other game mode where hitting a wall
results in a game over, simply comment out line 58 in the snake_game.py file and un-comment line 57 in that same file.

Written and tested on Mac OS El Capitan.

##Running the Game
To run the game, download files and place in directory of your choice. Navigate to that
directory in the terminal and type "python3 snake_main.py" into the window and press enter.

###Dependencies
You must have python 3.x.x installed on your computer to run.<br/>
Compatible with Mac OS and Linux


##Controls

Up.....................W<br/>
Down.................S<br/>
Left....................A<br/>
Right..................D<br/>
Quit....................Q<br/>
Pause.................Spacebar<br/>
Resume..............Any Direction Key
