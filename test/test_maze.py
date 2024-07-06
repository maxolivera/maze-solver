from src.maze.generator import Maze
import unittest

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        cell_size = 50
        maze = Maze(50, 50, num_rows, num_cols, cell_size, cell_size)

        self.assertTrue(
                f"({num_rows}, {num_cols}) size" in str(maze)
        )
