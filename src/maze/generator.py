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
            win: Window|None=None
            ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__size = (num_rows, num_cols)
        self.__cell = (cell_width, cell_height)
        self.__win = win
        self.__cells: list[list[Cell]] = []
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
            self.__cells.append(row)

        if self.__win:
            self.__draw_cells()

    def __draw_cells(self):
        for row in self.__cells:
            for cell in row:
                cell.draw()
                self.__animate()

    def __animate(self):
        self.__win.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self):
        entrance = self.__cells[0][0]
        exit = self.__cells[-1][-1]

        entrance.has_left_wall = False
        exit.has_right_wall = False
        
