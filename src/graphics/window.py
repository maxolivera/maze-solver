from typing import Self, override
from tkinter import Tk, BOTH, Canvas
import logging

CELL_COLOR = "black"

class Point():
    def __init__(self, x: float=0, y: float=0):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1: Point, p2: Point):
        self.__start = p1
        self.__end = p2

    def draw(self, canvas: Canvas, fill_color: str):
        _ = canvas.create_line(
                self.__start.x, self.__start.y,
                self.__end.x, self.__end.y,
                fill=fill_color, width=2
        )

class Window():
    def __init__(self, width: int, height: int) -> None:
        self.__active = False
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(self.__root, height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__active = True
        while self.__active:
            self.redraw()
        logging.info("Closing window...")

    def close(self) -> None:
        self.__active = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)

class Cell():
    def __init__(self, x1: float, y1: float, x2: float, y2: float, win: Window|None=None,
                 left: bool=True, right: bool=True,
                 top: bool=True, bottom: bool=True):
        self.__win = win
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom

    @override
    def __repr__(self) -> str:
        return f"Cell at p1: ({self.__x1}, {self.__y1}), p2: ({self.__x2}, {self.__y2})"

    def draw(self):
        x1 = self.__x1
        x2 = self.__x2
        y1 = self.__y1
        y2 = self.__y2
        if self.has_left_wall:
            self.__win.draw_line(
                    Line(
                    Point(x1, y1),
                    Point(x1, y2)
                ),
                    CELL_COLOR
            )
        if self.has_right_wall:
            self.__win.draw_line(
                    Line(
                    Point(x2, y1),
                    Point(x2, y2)
                ),
                    CELL_COLOR
            )
        if self.has_top_wall:
            self.__win.draw_line(
                    Line(
                    Point(x1, y2),
                    Point(x2, y2)
                ),
                    CELL_COLOR
            )
        if self.has_bottom_wall:
            self.__win.draw_line(
                    Line(
                    Point(x1, y1),
                    Point(x2, y1)
                ),
                    CELL_COLOR
            )

    def draw_move(self, to_cell: Self, undo: bool=False):
        if not undo:
            color = "red"
        else:
            color = "gray"

        center_self = Point(
                (self.__x1 + self.__x2) / 2,
                (self.__y1 + self.__y2) / 2
        )

        center_other = Point(
                (to_cell.__x1 + to_cell.__x2) / 2,
                (to_cell.__y1 + to_cell.__y2) / 2
        )

        self.__win.draw_line(Line(center_self, center_other), color)


