import random
from src.maze.generator import Maze
from src.graphics.window import (Window)
import logging
import argparse

X_PADDING = 50
Y_PADDING = 50
WIN_HEIGHT = 720
WIN_WIDTH = 1280
HEIGHT = 25 
WIDTH = 25

def main():
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-log',
                        '--loglevel',
                        default='warning',
                        help='Provide logging level. Example -log=info')

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel.upper())
    logging.info("Logging now setup.")

    win = Window(WIN_WIDTH, WIN_HEIGHT)

    if args.loglevel == "debug":
        seed = 0
    else:
        seed = None
    
    maze = Maze(
        X_PADDING,
        Y_PADDING,
        (WIN_HEIGHT - (Y_PADDING*2))//HEIGHT,
        (WIN_WIDTH - (X_PADDING*2))//WIDTH,
        HEIGHT,
        WIDTH,
        win,
        seed
    )

    if maze.solve():
        print("Solved!")
    else:
        print("The maze was not solved! :(")

    win.wait_for_close()

main()
