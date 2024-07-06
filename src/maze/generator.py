import logging
import random
import time
from typing import override

from src.graphics.window import (Cell, Window)

class Maze():
    def __init__(
            self,
            x1: float,
            y1: float,
            num_rows: int,
            num_cols: int,
            cell_width: float,
            cell_height: float,
            win: Window|None=None,
            maze_seed: int|None=None,
            ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__size = (num_rows, num_cols)
        self.__cell = (cell_width, cell_height)
        self.__win = win
        self._cells: list[list[Cell]] = []
        self.__seed:int = random.seed(a=maze_seed)
        self.__create_cells()

    @override
    def __repr__(self) -> str:
        return f"Maze starts at ({self.__x1}, {self.__y1}) with {self.__size} size."

    def __create_cells(self) -> None:
        height, width = self.__size
        for i in range(height):
            row = []
            for j in range(width):
                cell = Cell(self.__x1 + (j * self.__cell[0]),
                            self.__y1 + (i * self.__cell[1]),
                            self.__x1 + ((j + 1) * self.__cell[0]),
                            self.__y1 + ((i + 1) * self.__cell[1]),
                            self.__win)
                row.append(cell)
            self._cells.append(row)

        self.__draw_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __draw_cells(self):
        for row in self._cells:
            for cell in row:
                cell.draw()
                self.__animate()

    def __animate(self):
        if self.__win:
            self.__win.redraw()
            time.sleep(0.01)

    def __break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        exit = self._cells[-1][-1]

        entrance.has_left_wall = False
        exit.has_right_wall = False 
        if self.__win:
            entrance.draw()
            exit.draw()

    def __break_walls_r(self, i: int, j: int):
        self.__animate()
        height, width = self.__size
        height -= 1
        width -= 1
        self._cells[i][j].visited = True
        while True:
            neighbors: list[str] = []
            if i - 1 >= 0:
                if not self._cells[i-1][j].visited:
                    neighbors.append("top")
            if i + 1 <= height:
                if not self._cells[i+1][j].visited:
                    neighbors.append("bottom")
            if j - 1 >= 0:
                if not self._cells[i][j-1].visited:
                    neighbors.append("left")
            if j + 1 <= width:
                if not self._cells[i][j+1].visited:
                    neighbors.append("right")
            if not neighbors:
                self._cells[i][j].draw()
                return
            else:
                direction = neighbors[random.randrange(0, len(neighbors))]
                logging.debug(f"I am at ({i}, {j}). I can go to {neighbors} and I will go to {direction}")
                match direction:
                    case "top":
                        self._cells[i][j].has_bottom_wall = False
                        self._cells[i][j].draw()
                        self._cells[i-1][j].has_top_wall = False
                        self._cells[i-1][j].draw()
                        self.__break_walls_r(i-1, j)
                    case "bottom":
                        self._cells[i][j].has_top_wall = False
                        self._cells[i][j].draw()
                        self._cells[i+1][j].has_bottom_wall = False
                        self._cells[i+1][j].draw()
                        self.__break_walls_r(i+1, j)
                    case "left":
                        self._cells[i][j].has_left_wall = False
                        self._cells[i][j].draw()
                        self._cells[i][j-1].has_right_wall = False
                        self._cells[i][j-1].draw()
                        self.__break_walls_r(i, j-1)
                    case "right":
                        self._cells[i][j].has_right_wall = False
                        self._cells[i][j].draw()
                        self._cells[i][j+1].has_left_wall = False
                        self._cells[i][j+1].draw()
                        self.__break_walls_r(i, j+1)

    def __reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self.__solve_r()

    def __solve_r(self, i:int = 0, j:int = 0):
        height, width = self.__size
        height -= 1
        width -= 1

        self.__animate()
        self._cells[i][j].visited = True

        if i+1 == len(self._cells) and j+1 == len(self._cells[0]):
            return True

        # check right cell
        if 0 <= j + 1 <= width and (
                not self._cells[i][j].has_right_wall
                and not self._cells[i][j+1].has_left_wall
                and not self._cells[i][j+1].visited
                ):
            print(f"I am at ({i}, {j}) and I can go to ({i}, {j+1})")
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self.__solve_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(
                        self._cells[i][j+1],
                        True
                )
        # check left cell
        if 0 <= j - 1 <= width and (
                not self._cells[i][j].has_left_wall
                and not self._cells[i][j-1].has_right_wall
                and not self._cells[i][j-1].visited
                ):
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self.__solve_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(
                        self._cells[i][j-1],
                        True
                )
        # check top cell
        if 0 <= i+1 <= height and (
                not self._cells[i][j].has_top_wall
                and not self._cells[i+1][j].has_bottom_wall
                and not self._cells[i+1][j].visited
                ):
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self.__solve_r(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(
                        self._cells[i+1][j],
                        True
                )
        # check bottom cell
        if 0 <= i-1 <= height and (
                not self._cells[i][j].has_bottom_wall
                and not self._cells[i-1][j].has_top_wall
                and not self._cells[i-1][j].visited
                ):
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self.__solve_r(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(
                        self._cells[i-1][j],
                        True
                )
        return False
