from maze.maze import Maze
from graphics.window import (Window)
import logging
import argparse

HEIGHT = 150
WIDTH = 150

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

    win = Window(800, 600)

    maze = Maze(50, 50, 5, 7, 100, 100, win)

    win.wait_for_close()

main()
