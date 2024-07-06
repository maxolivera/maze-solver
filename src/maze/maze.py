import time
from graphics.window import (Cell, Window)

class Maze():
    def __init__(
            self,
            x1: float,
            y1: float,
            num_rows: float,
            num_cols: float,
            cell_width: float,
            cell_height: float,
            win: Window
            ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__size = (num_rows, num_cols)
        self.__cell = (cell_width, cell_height)
        self.__win = win
        self.__cells: list[list[Cell]] = []
        self.__create_cells()

    def __create_cells(self) -> None:
        height, width = self.__size
        for i in range(height):
            row = []
            for j in range(width):
                cell = Cell(self.__x1 + (j * self.__cell[0]),
                            self.__y1 + (i * self.__cell[1]),
                            self.__x1 + ((j + 1) * self.__cell[0]),
                            self.__y1 + ((i + 1) * self.__cell[1]),
                            self.__win,
                            True, True, True, True)
                row.append(cell)
            self.__cells.append(row)

        self.__draw_cells()

    def __draw_cells(self):
        for row in self.__cells:
            for cell in row:
                cell.draw()
                self.__animate()

    def __animate(self):
        self.__win.redraw()
        time.sleep(0.05)
