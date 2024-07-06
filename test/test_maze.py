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

    def test_entrance_and_exit(self):
        maze = Maze(50, 50, 12, 10, 50, 50)
        self.assertEqual(
                False,
                maze._cells[0][0].has_left_wall
        )
        self.assertEqual(
                False,
                maze._cells[-1][-1].has_right_wall
        )

    def test_visited_maze(self):
        maze = Maze(50, 50, 12, 10, 50, 50)
        for row in maze._cells:
            for cell in row:
                self.assertTrue(not cell.visited)
